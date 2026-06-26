#!/usr/bin/env python3
"""
Meta Ads Creator - 配置管理模块
管理 Access Token、广告账户 ID 等配置
"""

import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".workbuddy" / "meta_ads_config.json"


def get_config():
    """读取配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_config(config):
    """保存配置"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def init_config(access_token, ad_account_id, app_id=None, app_secret=None):
    """初始化配置"""
    config = {
        "access_token": access_token,
        "ad_account_id": ad_account_id,
        "app_id": app_id,
        "app_secret": app_secret,
        "api_version": "v18.0"
    }
    save_config(config)
    print(f"✅ 配置已保存到: {CONFIG_FILE}")
    return config


def get_access_token():
    """获取 Access Token"""
    config = get_config()
    token = config.get("access_token")
    if not token:
        raise ValueError("Access Token 未配置，请先运行 init_config.py 进行配置")
    return token


def get_ad_account_id():
    """获取广告账户 ID"""
    config = get_config()
    account_id = config.get("ad_account_id")
    if not account_id:
        raise ValueError("广告账户 ID 未配置，请先运行 init_config.py 进行配置")
    return account_id


def get_api_version():
    """获取 API 版本"""
    config = get_config()
    return config.get("api_version", "v18.0")


if __name__ == "__main__":
    # 命令行交互式配置
    print("=== Meta Ads API 配置 ===")
    print("请提供以下信息（这些信息将保存在本地配置文件中）:\n")
    
    access_token = input("Access Token: ").strip()
    ad_account_id = input("广告账户 ID (如: act_123456789): ").strip()
    app_id = input("App ID (可选): ").strip() or None
    app_secret = input("App Secret (可选): ").strip() or None
    
    if not access_token or not ad_account_id:
        print("❌ Access Token 和广告账户 ID 是必填项")
        exit(1)
    
    init_config(access_token, ad_account_id, app_id, app_secret)
    print("\n配置完成！你现在可以使用其他脚本创建广告了。")
