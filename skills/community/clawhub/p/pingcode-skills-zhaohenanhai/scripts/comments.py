#!/usr/bin/env python3
"""
PingCode API Client - 评论管理
POST   /v1/comments              创建评论
GET    /v1/comments              获取评论列表
GET    /v1/comments/{id}         获取单条评论
DELETE /v1/comments/{id}         删除评论

principal_type 允许值: work_item, test_run, test_case, ticket, idea, page
"""

import requests
import json
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import BASE_URL, CLIENT_ID, CLIENT_SECRET

PRINCIPAL_TYPES = ["work_item", "test_run", "test_case", "ticket", "idea", "page"]


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


def create_comment(access_token, principal_type, principal_id, content):
    url = f"{BASE_URL}/v1/comments"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {"principal_type": principal_type, "principal_id": principal_id, "content": content}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"创建评论失败: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(f"响应: {e.response.text}", file=sys.stderr)
        return None


def get_comments(access_token, principal_type, principal_id):
    url = f"{BASE_URL}/v1/comments"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    params = {"principal_type": principal_type, "principal_id": principal_id}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"获取评论列表失败: {e}", file=sys.stderr)
        return None


def delete_comment(access_token, comment_id):
    url = f"{BASE_URL}/v1/comments/{comment_id}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    try:
        r = requests.delete(url, headers=headers, timeout=30)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"删除评论失败: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="PingCode 评论管理")
    sub = parser.add_subparsers(dest="action", required=True)

    # create
    p_c = sub.add_parser("create", help="创建评论")
    p_c.add_argument("--type", dest="principal_type", required=True, choices=PRINCIPAL_TYPES, help="主体类型")
    p_c.add_argument("--id", dest="principal_id", required=True, help="主体 ID（如工作项 ID）")
    p_c.add_argument("--content", required=True, help="评论内容")
    p_c.add_argument("--json", action="store_true")

    # list
    p_l = sub.add_parser("list", help="获取评论列表")
    p_l.add_argument("--type", dest="principal_type", required=True, choices=PRINCIPAL_TYPES)
    p_l.add_argument("--id", dest="principal_id", required=True)
    p_l.add_argument("--json", action="store_true")

    # delete
    p_d = sub.add_parser("delete", help="删除评论")
    p_d.add_argument("comment_id", help="评论 ID")

    args = parser.parse_args()

    token = get_access_token()
    if not token:
        sys.exit(1)

    if args.action == "create":
        result = create_comment(token, args.principal_type, args.principal_id, args.content)
        if result is None:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"✅ 评论已发布")

    elif args.action == "list":
        data = get_comments(token, args.principal_type, args.principal_id)
        if data is None:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            comments = data.get("values", []) if isinstance(data, dict) else []
            total = data.get("total", len(comments)) if isinstance(data, dict) else len(comments)
            print(f"💬 评论列表 (共 {total} 条)\n")
            for c in comments:
                cid = c.get("id", "?")[:8]
                content = c.get("content", "")
                author = c.get("created_by") or {}
                author_name = author.get("display_name", "?") if isinstance(author, dict) else "?"
                print(f"[{cid}] {author_name}: {content}")
                print()

    elif args.action == "delete":
        ok = delete_comment(token, args.comment_id)
        if ok:
            print(f"✅ 评论 {args.comment_id} 已删除")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
