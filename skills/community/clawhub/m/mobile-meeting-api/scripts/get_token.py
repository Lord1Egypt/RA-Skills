#!/usr/bin/env python3
"""
获取Access Token脚本
基于references/app_auth.html和CreateAppIdToken.md

用途：获取API访问令牌，用于后续API调用。
"""

import requests
import hmac
import hashlib
import base64
import time
import uuid
import sys

# 用户配置（请修改为实际值）
BASE_URL = "https://apigw.125339.com.cn"
APP_ID = input("请输入APP_ID: ").strip()
APP_KEY = input("请输入APP_KEY: ").strip()
USER_ID = input("请输入USER_ID（可留空）: ").strip()


def generate_auth_header(app_id, app_key, user_id, expire_time, nonce):
    """生成Authorization头（HMAC-SHA256签名）"""
    # 文档示例中签名字符串始终为 appId:userId:expireTime:nonce
    sign_content = f"{app_id}:{user_id}:{expire_time}:{nonce}"
    signature = hmac.new(
        app_key.encode('utf-8'),
        sign_content.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    access = base64.b64encode(app_id.encode('utf-8')).decode('utf-8')

    return {
        "Authorization": f"HMAC-SHA256 signature={signature},access={access}",
        "X-Token-Type": "LongTicket",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Language": "zh-CN",
        "X-Request-ID": str(uuid.uuid4())
    }


def get_token():
    """获取Access Token"""
    url = f"{BASE_URL}/v2/usg/acs/auth/appauth"
    expire_time = int(time.time()) + 3600
    nonce = str(uuid.uuid4()).replace('-', '')[:40]
    headers = generate_auth_header(APP_ID, APP_KEY, USER_ID, expire_time, nonce)

    payload = {
        "appId": APP_ID,
        "clientType": 72,
        "expireTime": expire_time,
        "nonce": nonce,
        "userId": USER_ID
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("Token获取成功:")
        print(f"Access Token: {data.get('accessToken')}")
        print(f"Refresh Token: {data.get('refreshToken')}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    get_token()