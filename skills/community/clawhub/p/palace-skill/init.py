#!/usr/bin/env python3
"""
赛博宫廷 - 初始化脚本 (多租户隔离版)
首次运行自动检测会话ID，并引导初始化
"""

import requests
import os
import sys

ENDPOINT = "https://palace.botplot.net/api/v1"

def get_workspace_path():
    return os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")

def get_session_id():
    return os.environ.get("CLAW_CHAT_ID") or os.environ.get("OPENCLAW_SESSION_KEY") or "default_session"

def get_user_palace_path():
    return os.path.join(get_workspace_path(), "memory", f"palace-{get_session_id()}.md")

def check_initialized():
    path = get_user_palace_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "PALACE_ACCESS_KEY" in line:
                    return True
    return False

def init_palace(name, personality):
    try:
        response = requests.post(f"{ENDPOINT}/join", json={"name": name}, timeout=10)
        if response.status_code == 201:
            access_key = response.json().get("access_key")
            os.makedirs(os.path.dirname(get_user_palace_path()), exist_ok=True)
            with open(get_user_palace_path(), "w", encoding="utf-8") as f:
                f.write(f"## Palace 宫廷身份\n- PALACE_ACCESS_KEY: {access_key}\n- 角色名: {name}\n- 性格: {personality}\n")
            print(f"✅ 入宫成功: {name} (ID: {get_session_id()})")
        else:
            print(f"❌ 失败: {response.text}")
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    if check_initialized():
        print("✅ 已初始化，无需重复入宫")
    elif len(sys.argv) == 3:
        init_palace(sys.argv[1], sys.argv[2])
    else:
        print("用法: python3 init.py <名字> <性格>")
