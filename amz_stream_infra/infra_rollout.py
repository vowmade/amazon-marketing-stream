# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import aws_cdk as cdk

from .stack_definitions import AmzStreamConsumerStack
from .stack_definitions_firehose import AmzStreamConsumerStackFirehose

SUPPORTED_DELIVERY_METHODS = ["sqs", "firehose"]


def validate_delivery_method(delivery_method: str):
    if delivery_method not in SUPPORTED_DELIVERY_METHODS:
        raise ValueError(
            f"Unsupported delivery method: {delivery_method}. Supported delivery methods are: {
                ', '.join(SUPPORTED_DELIVERY_METHODS)}"
        )


def rollout_stacks(app: cdk.App, config: dict, delivery_method: str):
    validate_delivery_method(delivery_method)
    ambassadors_config = config["ambassadors"]
    datasets_config = config["datasets"]
    installation_region_config = config["consumerStackInstallationAwsRegion"]
    for advertising_region in datasets_config:
        for dataset_config in datasets_config[advertising_region]:
            if delivery_method == "sqs":
                AmzStreamConsumerStack(
                    app,
                    advertising_region,
                    installation_region_config[advertising_region],
                    dataset_config,
                    ambassadors_config,
                )
            elif delivery_method == "firehose":
                AmzStreamConsumerStackFirehose(
                    app,
                    advertising_region,
                    installation_region_config[advertising_region],
                    dataset_config,
                    ambassadors_config,
                )