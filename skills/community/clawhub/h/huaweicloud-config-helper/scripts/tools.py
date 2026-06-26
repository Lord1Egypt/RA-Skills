import os

from huaweicloudsdkconfig.v1.region.config_region import ConfigRegion
from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkcore.exceptions import exceptions

from huaweicloudsdkconfig.v1 import ConfigClient
from huaweicloudsdkconfig.v1 import (
    ListBuiltInPolicyDefinitionsRequest,
    ListSchemasRequest,
    RunQueryRequest,
    QueryRunRequestBody
)


def generate_config_client():
    global_credentials = GlobalCredentials(
        os.getenv("HUAWEICLOUD_AK", ""),
        os.getenv("HUAWEICLOUD_SK", "")
    )

    return ConfigClient.new_builder() \
        .with_credentials(global_credentials) \
        .with_region(ConfigRegion.value_of("cn-north-4")) \
        .build()


def list_built_in_policy_definitions():
    config_client = generate_config_client()
    try:
        request = ListBuiltInPolicyDefinitionsRequest()
        request.x_language = "zh-cn"
        response = config_client.list_built_in_policy_definitions(request).to_dict()
        return response
    except exceptions.ClientRequestException as e:
        print("list_built_in_policy_definitions failed")
        print(f"Error code: {e.error_code}")
        print(f"Error message: {e.error_msg}")
        return None


def list_schema(marker=None):
    config_client = generate_config_client()
    try:
        request = ListSchemasRequest()
        request.limit = 200
        if marker:
            request.marker = marker
        response = config_client.list_schemas(request).to_dict()
        return response
    except exceptions.ClientRequestException as e:
        print("list_schema failed")
        print(f"Error code: {e.error_code}")
        print(f"Error message: {e.error_msg}")
        return None


def query_Config_resource_by_sql(sql):
    config_client = generate_config_client()
    try:
        request = RunQueryRequest()
        request.body = QueryRunRequestBody(
            expression=sql
        )
        response = config_client.run_query(request).to_dict()
        return response
    except exceptions.ClientRequestException as e:
        print("RunQuery failed")
        print(f"Error code: {e.error_code}")
        print(f"Error message: {e.error_msg}")
        return None
