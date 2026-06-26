#!/usr/bin/env python3
"""
快递鸟运单查询脚本
支持通过快递鸟API实时查询运单轨迹信息
"""

import hashlib
import base64
import argparse
import json
import os
import sys

import requests


CHARSET = 'UTF-8'

# 默认正式环境API地址
DEFAULT_API_URL = 'https://api.kdniao.com/api/dist'

# 接口类型配置
INTERFACE_TYPE = {
    'R8002': {'code': '8002', 'desc': '快递查询'},
}


def md5(s, charset):
    """MD5加密"""
    return hashlib.md5(s.encode(charset)).hexdigest()


def base64_encode(s, charset):
    """Base64编码"""
    return base64.b64encode(s.encode(charset)).decode(charset)


def encrypt(content, key_value, charset):
    """数据加密：先拼接密钥，再MD5，最后Base64编码"""
    if key_value:
        content += key_value
    return base64_encode(md5(content, charset), charset)


def remote_request(api_url, interface_type, request_data, customer_code, app_key):
    """
    调用快递鸟API
    """
    params = {
        'EBusinessID': customer_code,
        'RequestType': interface_type,
        'RequestData': request_data,
        'DataSign': encrypt(request_data, app_key, CHARSET),
        'DataType': 2
    }

    try:
        response = requests.post(api_url, data=params, timeout=30)

        if response.status_code >= 400:
            print(json.dumps({
                "success": False,
                "error": f"HTTP请求失败: 状态码 {response.status_code}",
                "details": response.text
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        return response.text

    except requests.exceptions.RequestException as e:
        print(json.dumps({
            "success": False,
            "error": f"API调用失败: {str(e)}"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


def query_tracking(logistic_code, api_url=None):
    """
    查询运单轨迹
    """
    credential_env_var = "KUAIDI_BIRD_API_CREDENTIALS"
    credential = os.getenv(credential_env_var)

    if not credential:
        print(json.dumps({
            "success": False,
            "error": "缺少快递鸟API凭证配置",
            "required_env_var": credential_env_var,
            "expected_format": "CUSTOMER_CODE|APP_KEY",
            "example": f"export {credential_env_var}=\"1292092|993d0b97-07fa-478c-bfea-ca3597f2ce0f\""
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        parts = credential.split('|')
        if len(parts) != 2:
            raise ValueError("凭证格式错误")
        customer_code = parts[0].strip()
        app_key = parts[1].strip()

        if not customer_code or not app_key:
            raise ValueError("CUSTOMER_CODE和APP_KEY不能为空")

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": f"凭证解析失败: {str(e)}",
            "required_env_var": credential_env_var,
            "expected_format": "CUSTOMER_CODE|APP_KEY",
            "example": f"export {credential_env_var}=\"1292092|993d0b97-07fa-478c-bfea-ca3597f2ce0f\""
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if not api_url:
        api_url = DEFAULT_API_URL

    request_data = json.dumps({"LogisticCode": logistic_code}, ensure_ascii=False)

    interface_code = INTERFACE_TYPE['R8002']['code']
    result_text = remote_request(api_url, interface_code, request_data, customer_code, app_key)

    try:
        result = json.loads(result_text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    except json.JSONDecodeError as e:
        print(json.dumps({
            "success": False,
            "error": f"响应解析失败: {str(e)}",
            "raw_response": result_text
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='快递鸟运单查询工具')
    parser.add_argument('--logistic-code', required=True, help='运单号')
    parser.add_argument('--api-url', default=DEFAULT_API_URL, help='API地址（默认为正式环境）')

    args = parser.parse_args()
    query_tracking(args.logistic_code, args.api_url)


if __name__ == "__main__":
    main()
