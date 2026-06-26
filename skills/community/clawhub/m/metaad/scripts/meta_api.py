#!/usr/bin/env python3
"""
Meta Marketing API 基础模块
封装常用的 API 调用方法
"""

import requests
from config_manager import get_access_token, get_ad_account_id, get_api_version

BASE_URL = "https://graph.facebook.com"


def get_headers():
    """获取 API 请求头"""
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }


def api_get(endpoint, params=None):
    """GET 请求"""
    url = f"{BASE_URL}/{get_api_version()}/{endpoint}"
    response = requests.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json()


def api_post(endpoint, data=None):
    """POST 请求"""
    url = f"{BASE_URL}/{get_api_version()}/{endpoint}"
    response = requests.post(url, headers=get_headers(), json=data)
    response.raise_for_status()
    return response.json()


def get_ad_account():
    """获取广告账户信息"""
    account_id = get_ad_account_id()
    return api_get(f"{account_id}", {"fields": "name,account_status,currency,timezone_name"})


def get_campaigns():
    """获取广告系列列表"""
    account_id = get_ad_account_id()
    return api_get(f"{account_id}/campaigns", {"fields": "id,name,status,objective"})


def debug_token():
    """调试 Token 有效性"""
    try:
        result = api_get("me", {"fields": "id,name"})
        print(f"✅ Token 有效")
        print(f"   用户: {result.get('name')} (ID: {result.get('id')})")
        return True
    except Exception as e:
        print(f"❌ Token 验证失败: {e}")
        return False


if __name__ == "__main__":
    # 测试 API 连接
    print("=== 测试 Meta API 连接 ===\n")
    
    try:
        # 验证 Token
        if debug_token():
            # 获取账户信息
            print("\n--- 广告账户信息 ---")
            account = get_ad_account()
            print(f"账户名称: {account.get('name')}")
            print(f"账户状态: {'正常' if account.get('account_status') == 1 else '异常'}")
            print(f"货币: {account.get('currency')}")
            print(f"时区: {account.get('timezone_name')}")
            
            # 获取广告系列
            print("\n--- 现有广告系列 ---")
            campaigns = get_campaigns()
            if campaigns.get('data'):
                for campaign in campaigns['data']:
                    print(f"  - {campaign['name']} (ID: {campaign['id']}, 状态: {campaign['status']})")
            else:
                print("  暂无广告系列")
    except Exception as e:
        print(f"错误: {e}")
