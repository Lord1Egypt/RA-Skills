#!/usr/bin/env python3
"""
notion-write-idea.py — 想法入库写入脚本（带用户确认）

用法:
  python3 notion-write-idea.py create < JSON   # 从 stdin 读取 JSON
  python3 notion-write-idea.py update <JSON>   # 更新页面

确认流程:
  1. 展示即将写入的字段内容
  2. 用户输入 y/Y 确认后才写入
  3. 写入后读取验证，返回页面 URL
"""

import sys
import json
import subprocess
import os

NOTION_KEY_FILE = os.path.expanduser("~/.config/notion/api_key")
DB_ID = "339d8e39-9e68-814b-8fc9-c06adfb3ae00"


def get_api_key():
    if not os.path.exists(NOTION_KEY_FILE):
        raise FileNotFoundError(f"API key not found: {NOTION_KEY_FILE}")
    return open(NOTION_KEY_FILE).read().strip()


def notion_req(method, endpoint, body=None, version="2022-06-28"):
    key = get_api_key()
    cmd = [
        "curl", "-s", "-X", method,
        f"https://api.notion.com/v1/{endpoint}",
        "-H", f"Authorization: Bearer {key}",
        "-H", f"Notion-Version: {version}",
        "-H", "Content-Type: application/json",
    ]
    if body:
        cmd += ["-d", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(r.stdout)


def confirm_write(properties: dict) -> bool:
    print("\n" + "=" * 50)
    print("📋 即将写入 Notion 的内容：")
    print("=" * 50)
    for key, val in properties.items():
        display = str(val)[:80]
        print(f"  {key}: {display}")
    print("=" * 50)
    print("确认写入？(y/n): ", end="", flush=True)
    resp = input().strip().lower()
    return resp == "y"


def create_page(properties: dict) -> dict:
    body = {
        "parent": {"database_id": DB_ID},
        "properties": properties
    }
    result = notion_req("POST", "pages", body, version="2022-06-28")
    if result.get("object") == "error":
        raise Exception(f"创建失败 [{result.get('code')}]: {result.get('message')}")
    return result


def update_page(page_id: str, properties: dict) -> dict:
    body = {"properties": properties}
    result = notion_req("PATCH", f"pages/{page_id}", body, version="2022-06-28")
    if result.get("object") == "error":
        raise Exception(f"更新失败 [{result.get('code')}]: {result.get('message')}")
    return result


def verify_page(page_id: str) -> dict:
    return notion_req("GET", f"pages/{page_id}", version="2025-09-03")


def main():
    if len(sys.argv) < 2:
        print("用法: notion-write-idea.py <create|update>")
        sys.exit(1)

    action = sys.argv[1]

    # 从 stdin 读取 JSON
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        sys.exit(1)

    if action == "create":
        properties = data.get("properties", data)
        if not confirm_write(properties):
            print("❌ 已取消写入")
            sys.exit(0)
        result = create_page(properties)
        page_id = result.get("id", "")
        print(f"✅ 创建成功: https://notion.so/{page_id.replace('-', '')}")

    elif action == "update":
        page_id = data.get("page_id")
        properties = data.get("properties", {})
        if not page_id:
            print("❌ 缺少 page_id")
            sys.exit(1)
        if not confirm_write(properties):
            print("❌ 已取消写入")
            sys.exit(0)
        result = update_page(page_id, properties)
        # 验证
        verified = verify_page(page_id)
        print(f"✅ 更新成功: https://notion.so/{page_id.replace('-', '')}")
    else:
        print(f"❌ 未知操作: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
