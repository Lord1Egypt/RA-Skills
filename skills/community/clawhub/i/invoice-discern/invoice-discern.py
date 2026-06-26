#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import requests

def get_md5(text):
    """计算MD5（32位小写）"""
    return hashlib.md5(text.encode()).hexdigest().lower()

def get_token(api_url, ak, sk, type_value):
    """获取访问令牌"""
    token_url = f"{api_url}/api/v2/agent/common/cdk/getToken"
    secret_string = get_md5(ak + sk)

    payload = {
        "akString": ak,
        "secretString": secret_string,
        "type": int(type_value),
        "forceUpdate": 0
    }

    try:
        response = requests.post(token_url, json=payload)
        result = response.json()
        if result.get("code") == "200":
            return result["data"]
        else:
            return None, result.get("message", "获取Token失败")
    except Exception as e:
        return None, str(e)

def discern_invoice(file_path, tax_no=None):
    """识别发票"""
    api_url = os.getenv("HSY_API_URL", "https://huisuiyun.com")
    ak = os.getenv("HSY_AK")
    sk = os.getenv("HSY_SK")
    type_value = os.getenv("HSY_TYPE", "2")

    if not ak or not sk:
        return {
            "error": "环境变量未配置",
            "message": "请先配置 HSY_AK 和 HSY_SK 环境变量",
            "configUrl": "https://huisuiyun.com/account/conf/secretkey",
            "help": "点击 configUrl 获取慧穗云 AK/SK 秘钥"
        }

    # 获取 Token
    token_result = get_token(api_url, ak, sk, type_value)
    if isinstance(token_result, tuple):
        token, error = token_result
        if not token:
            return {"error": f"Token获取失败: {error}"}
    else:
        token = token_result

    # 准备请求头
    headers = {"X-Access-Token": token}
    if type_value == "1" and tax_no:
        headers["X-Tax-Token"] = tax_no

    # 调用识别接口
    discern_url = f"{api_url}/api/v2/agent/cdk/invoice/discern"

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(discern_url, files=files, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: invoice-discern.py discern <file_path> [tax_no]"}))
        sys.exit(1)

    command = sys.argv[1]

    if command == "discern":
        file_path = sys.argv[2]
        tax_no = sys.argv[3] if len(sys.argv) > 3 else None
        result = discern_invoice(file_path, tax_no)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)
