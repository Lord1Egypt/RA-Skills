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

    # secret = MD5(AK + SK)
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

def verify_invoice(data, tax_no=None):
    """查验发票"""
    api_url = os.getenv("HSY_API_URL", "https://huisuiyun.com")
    ak = os.getenv("HSY_AK")
    sk = os.getenv("HSY_SK")
    type_value = os.getenv("HSY_TYPE", "2")

    if not ak or not sk:
        return {
            "error": "环境变量未配置",
            "message": "请先配置 HSY_AK 和 HSY_SK 环境变量",
            "configUrl": "https://huisuiyun.com/account/conf/secretkey",
            "docUrl": "https://cdk.huisuiyun.com/docs/%E8%BE%85%E5%8A%A9%E5%8A%9F%E8%83%BD%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96token-%E5%90%8C%E6%AD%A5",
            "help": "点击 configUrl 获取慧穗云 AK/SK 秘钥，或查看 docUrl 了解详细配置说明"
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
    headers = {
        "Content-Type": "application/json",
        "X-Access-Token": token
    }

    # ISV token 需要传入 X-Tax-Token
    if type_value == "1" and tax_no:
        headers["X-Tax-Token"] = tax_no

    # 调用查验接口
    check_url = f"{api_url}/api/v2/agent/cdk/invoice/check"

    try:
        response = requests.post(check_url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: invoice-verify-hsy.py verify '<JSON>' [tax_no]"}))
        sys.exit(1)

    command = sys.argv[1]

    if command == "verify":
        try:
            data = json.loads(sys.argv[2])
            tax_no = sys.argv[3] if len(sys.argv) > 3 else None
            result = verify_invoice(data, tax_no)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON"}))
            sys.exit(1)
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)
