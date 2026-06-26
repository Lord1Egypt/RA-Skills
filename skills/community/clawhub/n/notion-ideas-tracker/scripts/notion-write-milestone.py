#!/usr/bin/env python3
"""
notion-write-milestone.py — 里程碑写入脚本（带用户确认）

用法:
  python3 notion-write-milestone.py create < idea.json

确认流程:
  1. 展示即将写入的字段内容
  2. 用户输入 y/Y 确认后才写入
  3. 写入后返回页面 URL
"""

import sys
import json
import subprocess
import os

NOTION_KEY_FILE = os.path.expanduser("~/.config/notion/api_key")
MILESTONE_DB_ID = "339d8e39-9e68-8130-932c-ecf46af154b5"


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


def confirm_write(fields: dict) -> bool:
    print("\n" + "=" * 50)
    print("🏃 即将写入里程碑：")
    print("=" * 50)
    for key, val in fields.items():
        display = str(val)[:80]
        print(f"  {key}: {display}")
    print("=" * 50)
    print("确认写入？(y/n): ", end="", flush=True)
    return input().strip().lower() == "y"


def build_properties(data: dict) -> dict:
    """将扁平 JSON 转为 Notion properties 格式"""
    props = {}

    def rt(v):
        return {"rich_text": [{"text": {"content": v or ""}}]}

    def sel(v):
        return {"select": {"name": v}}

    def rel(page_id):
        return {"relation": [{"id": page_id}]}

    if "里程碑标题" in data:
        props["里程碑标题"] = {"title": [{"text": {"content": data["里程碑标题"]}}]}
    if "所属想法ID" in data:
        props["所属想法"] = rel(data["所属想法ID"])
    if "处理过程" in data:
        props["处理过程"] = rt(data["处理过程"])
    if "决策记录" in data:
        props["决策记录"] = rt(data["决策记录"])
    if "产物链接" in data:
        props["产物链接"] = {"url": data.get("产物链接") or None}
    if "状态" in data:
        props["状态"] = sel(data["状态"])
    if "创建时间" in data:
        props["创建时间"] = {"date": {"start": data["创建时间"]}}

    return props


def create_milestone(data: dict) -> dict:
    properties = build_properties(data)
    body = {
        "parent": {"database_id": MILESTONE_DB_ID},
        "properties": properties
    }
    result = notion_req("POST", "pages", body, version="2022-06-28")
    if result.get("object") == "error":
        raise Exception(f"创建失败 [{result.get('code')}]: {result.get('message')}")
    return result


def update_milestone(page_id: str, data: dict) -> dict:
    properties = build_properties(data)
    result = notion_req("PATCH", f"pages/{page_id}", {"properties": properties}, version="2022-06-28")
    if result.get("object") == "error":
        raise Exception(f"更新失败 [{result.get('code')}]: {result.get('message')}")
    return result


def main():
    if len(sys.argv) < 2:
        print("用法: notion-write-milestone.py <create|update>")
        sys.exit(1)

    action = sys.argv[1]

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        sys.exit(1)

    if action == "create":
        if not confirm_write(data):
            print("❌ 已取消写入")
            sys.exit(0)
        result = create_milestone(data)
        page_id = result.get("id", "")
        print(f"✅ 创建成功: https://notion.so/{page_id.replace('-', '')}")

    elif action == "update":
        page_id = data.pop("page_id", None)
        if not page_id:
            print("❌ 缺少 page_id")
            sys.exit(1)
        if not confirm_write(data):
            print("❌ 已取消写入")
            sys.exit(0)
        result = update_milestone(page_id, data)
        print(f"✅ 更新成功: https://notion.so/{page_id.replace('-', '')}")

    else:
        print(f"❌ 未知操作: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
