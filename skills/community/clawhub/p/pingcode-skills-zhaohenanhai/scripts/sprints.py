#!/usr/bin/env python3
"""
PingCode API Client - 迭代管理
GET  /v1/project/projects/{project_id}/sprints         获取迭代列表
POST /v1/project/projects/{project_id}/sprints         创建迭代
GET  /v1/project/projects/{project_id}/sprints/{id}    获取单个迭代
PATCH /v1/project/projects/{project_id}/sprints/{id}   更新迭代
"""

import requests
import json
import sys
import os
import argparse
from datetime import datetime

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


def get_sprints(access_token, project_id, status=None, page_size=50):
    url = f"{BASE_URL}/v1/project/projects/{project_id}/sprints"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    params = {"page_size": page_size, "page_index": 0}
    if status:
        params["status"] = status
    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"获取迭代列表失败: {e}", file=sys.stderr)
        return None


def create_sprint(access_token, project_id, payload):
    url = f"{BASE_URL}/v1/project/projects/{project_id}/sprints"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"创建迭代失败: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(f"响应: {e.response.text}", file=sys.stderr)
        return None


def update_sprint(access_token, project_id, sprint_id, payload):
    url = f"{BASE_URL}/v1/project/projects/{project_id}/sprints/{sprint_id}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    try:
        r = requests.patch(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"更新迭代失败: {e}", file=sys.stderr)
        return None


def parse_ts(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())


def format_sprint(s):
    sid = s.get("id", "?")
    name = s.get("name", "?")
    status = s.get("status", "?")
    status_map = {"pending": "⏳ 未开始", "in_progress": "🔄 进行中", "completed": "✅ 已完成"}
    status_str = status_map.get(status, status)
    assignee = s.get("assignee") or {}
    assignee_name = assignee.get("display_name", "未分配") if isinstance(assignee, dict) else "未分配"
    start = s.get("start_at")
    end = s.get("end_at")
    start_str = datetime.fromtimestamp(start).strftime("%Y-%m-%d") if start else "?"
    end_str = datetime.fromtimestamp(end).strftime("%Y-%m-%d") if end else "?"
    return f"{status_str}  [{sid[:8]}] {name}\n   时间: {start_str} ~ {end_str} | 负责人: {assignee_name}"


def main():
    parser = argparse.ArgumentParser(description="PingCode 迭代管理")
    sub = parser.add_subparsers(dest="action", required=True)

    # list
    p_list = sub.add_parser("list", help="获取迭代列表")
    p_list.add_argument("--project_id", required=True, help="项目 ID")
    p_list.add_argument("--status", choices=["pending", "in_progress", "completed"], help="按状态过滤")
    p_list.add_argument("--json", action="store_true")

    # create
    p_create = sub.add_parser("create", help="创建迭代")
    p_create.add_argument("--project_id", required=True)
    p_create.add_argument("--name", required=True, help="迭代名称")
    p_create.add_argument("--start_at", required=True, help="开始日期 YYYY-MM-DD")
    p_create.add_argument("--end_at", required=True, help="结束日期 YYYY-MM-DD")
    p_create.add_argument("--assignee_id", required=True, help="负责人 ID")
    p_create.add_argument("--description", help="描述")
    p_create.add_argument("--status", choices=["pending", "in_progress", "completed"], default="pending")
    p_create.add_argument("--json", action="store_true")

    # update
    p_update = sub.add_parser("update", help="更新迭代")
    p_update.add_argument("--project_id", required=True)
    p_update.add_argument("--sprint_id", required=True, help="迭代 ID")
    p_update.add_argument("--name", help="新名称")
    p_update.add_argument("--start_at", help="开始日期 YYYY-MM-DD")
    p_update.add_argument("--end_at", help="结束日期 YYYY-MM-DD")
    p_update.add_argument("--status", choices=["pending", "in_progress", "completed"])
    p_update.add_argument("--assignee_id")
    p_update.add_argument("--json", action="store_true")

    args = parser.parse_args()

    token = get_access_token()
    if not token:
        sys.exit(1)

    if args.action == "list":
        data = get_sprints(token, args.project_id, status=args.status)
        if not data:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            sprints = data.get("values", [])
            total = data.get("total", len(sprints))
            print(f"🗓 迭代列表 (共 {total} 个)\n")
            for s in sprints:
                print(format_sprint(s))
                print()

    elif args.action == "create":
        payload = {
            "name": args.name,
            "start_at": parse_ts(args.start_at),
            "end_at": parse_ts(args.end_at),
            "assignee_id": args.assignee_id,
            "status": args.status,
        }
        if args.description:
            payload["description"] = args.description
        result = create_sprint(token, args.project_id, payload)
        if not result:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"✅ 迭代已创建: [{result.get('id', '?')[:8]}] {result.get('name', '?')}")

    elif args.action == "update":
        payload = {}
        if args.name:
            payload["name"] = args.name
        if args.start_at:
            payload["start_at"] = parse_ts(args.start_at)
        if args.end_at:
            payload["end_at"] = parse_ts(args.end_at)
        if args.status:
            payload["status"] = args.status
        if args.assignee_id:
            payload["assignee_id"] = args.assignee_id
        if not payload:
            print("没有要更新的字段", file=sys.stderr)
            sys.exit(1)
        result = update_sprint(token, args.project_id, args.sprint_id, payload)
        if not result:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"✅ 迭代已更新: [{result.get('id', '?')[:8]}] {result.get('name', '?')}")


if __name__ == "__main__":
    main()
