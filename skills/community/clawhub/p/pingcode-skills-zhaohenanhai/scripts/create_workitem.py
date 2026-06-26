#!/usr/bin/env python3
"""
PingCode API Client - 创建工作项
POST /v1/project/work_items
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


def create_workitem(access_token, payload):
    """创建工作项"""
    url = f"{BASE_URL}/v1/project/work_items"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"创建工作项失败: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(f"响应内容: {e.response.text}", file=sys.stderr)
        return None


def parse_timestamp(date_str):
    """将 YYYY-MM-DD 转为 Unix 时间戳"""
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())


def main():
    parser = argparse.ArgumentParser(description="创建 PingCode 工作项")
    parser.add_argument("--project_id", required=True, help="项目 ID")
    parser.add_argument("--title", required=True, help="工作项标题")
    parser.add_argument(
        "--type_id",
        default="task",
        help="工作项类型 (epic/feature/story/task/bug/issue 或自定义类型id)，默认 task",
    )
    parser.add_argument("--description", help="工作项描述")
    parser.add_argument("--assignee_id", help="负责人 ID")
    parser.add_argument("--priority_id", help="优先级 ID")
    parser.add_argument("--state_id", help="状态 ID")
    parser.add_argument("--parent_id", help="父工作项 ID")
    parser.add_argument("--sprint_id", help="迭代 ID（仅 scrum 项目）")
    parser.add_argument("--start_at", help="开始日期 YYYY-MM-DD")
    parser.add_argument("--end_at", help="截止日期 YYYY-MM-DD")
    parser.add_argument("--story_points", type=float, help="故事点")
    parser.add_argument("--estimated_workload", type=float, help="预估工时（小时）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    token = get_access_token()
    if not token:
        sys.exit(1)

    payload = {
        "project_id": args.project_id,
        "title": args.title,
        "type_id": args.type_id,
    }
    if args.description:
        payload["description"] = args.description
    if args.assignee_id:
        payload["assignee_id"] = args.assignee_id
    if args.priority_id:
        payload["priority_id"] = args.priority_id
    if args.state_id:
        payload["state_id"] = args.state_id
    if args.parent_id:
        payload["parent_id"] = args.parent_id
    if args.sprint_id:
        payload["sprint_id"] = args.sprint_id
    if args.start_at:
        payload["start_at"] = parse_timestamp(args.start_at)
    if args.end_at:
        payload["end_at"] = parse_timestamp(args.end_at)
    if args.story_points is not None:
        payload["story_points"] = args.story_points
    if args.estimated_workload is not None:
        payload["estimated_workload"] = args.estimated_workload

    result = create_workitem(token, payload)
    if not result:
        sys.exit(1)

    if getattr(args, "json"):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        item_id = result.get("id", "?")
        title = result.get("title", "?")
        type_id = result.get("type_id") or result.get("type", "?")
        print(f"✅ 工作项已创建")
        print(f"   ID: {item_id}")
        print(f"   标题: {title}")
        print(f"   类型: {type_id}")


if __name__ == "__main__":
    main()
