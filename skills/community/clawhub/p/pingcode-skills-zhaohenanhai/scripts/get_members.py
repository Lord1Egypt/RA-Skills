#!/usr/bin/env python3
"""
PingCode API Client - 获取企业成员列表
GET /v1/directory/users
"""

import requests
import json
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import BASE_URL, CLIENT_ID, CLIENT_SECRET


def get_access_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("错误：请设置 PINGCODE_CLIENT_ID 和 PINGCODE_CLIENT_SECRET", file=sys.stderr)
        sys.exit(1)
    url = f"{BASE_URL}/v1/auth/token"
    params = {"grant_type": "client_credentials", "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"获取令牌失败: {e}", file=sys.stderr)
        return None


def get_members(access_token, keyword=None, page_size=50, page_index=0):
    """获取企业成员列表"""
    url = f"{BASE_URL}/v1/directory/users"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    params = {"page_size": page_size, "page_index": page_index}
    if keyword:
        params["keyword"] = keyword
    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"获取成员列表失败: {e}", file=sys.stderr)
        return None


def format_members(data):
    if not data or "values" not in data:
        return "没有找到成员"
    members = data["values"]
    total = data.get("total", len(members))
    if not members:
        return "没有成员"
    lines = [f"👥 企业成员列表 (共 {total} 人，显示 {len(members)} 条)\n"]
    for m in members:
        uid = m.get("id", "?")
        name = m.get("name", "?")
        display = m.get("display_name", name)
        email = m.get("email", "")
        status = m.get("status", "?")
        status_icon = "🟢" if status == "enabled" else "🔴"
        lines.append(f"{status_icon} {display} (@{name})")
        lines.append(f"   ID: {uid}")
        if email:
            lines.append(f"   邮箱: {email}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="获取 PingCode 企业成员列表")
    parser.add_argument("--keyword", help="按名称关键词搜索")
    parser.add_argument("--limit", type=int, default=50, help="返回数量（默认50）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    token = get_access_token()
    if not token:
        sys.exit(1)

    data = get_members(token, keyword=args.keyword, page_size=args.limit)
    if not data:
        sys.exit(1)

    if getattr(args, "json"):
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(format_members(data))


if __name__ == "__main__":
    main()
