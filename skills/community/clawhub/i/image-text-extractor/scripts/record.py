#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf-image-text-extractor/scripts/record.py

PDF和图片文字提取 — 使用权限请求脚本
用途：每次使用本 Skill 前必须先调用，向服务端请求使用权限并完成鉴权校验

权限接口：https://redfox.hk/story/api/skill/record/save
鉴权方式：从环境变量 REDFOX_API_KEY 读取，通过 X-API-Key 请求头传入
失败策略：无 API Key 或接口失败时以非零退出码终止，由调用方提示用户

用法：
  python3 scripts/record.py
"""

import sys
import os

try:
    import requests
except ImportError:
    print("❌ 缺少依赖：requests，请执行：pip install requests")
    sys.exit(1)

RECORD_URL = "https://redfox.hk/story/api/skill/record/save"
SKILL_NAME = "PDF和图片文字提取"
REGISTER_URL = "https://redfox.hk/settings/api-keys?source=clawhub"


def _get_api_key() -> str:
    """从环境变量 REDFOX_API_KEY 读取 API Key，缺失时报错退出。"""
    key = os.getenv("REDFOX_API_KEY", "").strip()
    if not key:
        print("⚠️ 本 Skill 需要红狐 API Key 获取使用权限（免费，不扣积分）")
        print(f"   领取地址：{REGISTER_URL}")
        print("   领取后设置环境变量 REDFOX_API_KEY 即可使用")
        sys.exit(1)
    return key


def save_record() -> None:
    """调用权限接口，请求本 Skill 的使用权限。失败时以非零退出码终止。"""
    api_key = _get_api_key()
    payload = {"skillName": SKILL_NAME, "source": "PDF和图片文字提取-ClawHub"}
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-API-Key": api_key,
    }

    try:
        resp = requests.post(RECORD_URL, json=payload, headers=headers, verify=True, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接鉴权服务器：{e}")
        print(f"请检查网络后重试，或前往 {REGISTER_URL} 确认 API Key 是否有效")
        sys.exit(1)

    if resp.status_code != 200:
        print(f"❌ 鉴权接口返回 HTTP {resp.status_code}：{resp.text}")
        sys.exit(1)

    data = resp.json()
    code = data.get("code")

    if code in (200, 2000):
        print("✅ 鉴权通过，已获得使用权限")
        return

    if code in (3106, 3107):
        print("⚠️ 当前 API Key 无效或已过期，需要重新领取")
        print(f"   领取地址：{REGISTER_URL}")
        sys.exit(1)

    print(f"❌ 鉴权接口返回异常：{data}")
    sys.exit(1)


if __name__ == "__main__":
    save_record()
