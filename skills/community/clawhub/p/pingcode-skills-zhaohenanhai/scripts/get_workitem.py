#!/usr/bin/env python3
"""
PingCode API Client - 获取/删除单个工作项
GET  /v1/project/work_items/{id}
DELETE /v1/project/work_items/{id}
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


def get_workitem(access_token, workitem_id):
    """获取单个工作项详情"""
    url = f"{BASE_URL}/v1/project/work_items/{workitem_id}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"获取工作项失败: {e}", file=sys.stderr)
        return None


def delete_workitem(access_token, workitem_id):
    """删除工作项"""
    url = f"{BASE_URL}/v1/project/work_items/{workitem_id}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    try:
        r = requests.delete(url, headers=headers, timeout=30)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"删除工作项失败: {e}", file=sys.stderr)
        return False


def format_workitem(item):
    """格式化单个工作项详情输出"""
    if not item:
        return "未获取到工作项数据"

    item_id = item.get("id", "?")[:8]
    identifier = item.get("identifier", "?")
    title = item.get("title", "无标题")

    type_val = item.get("type") or {}
    item_type = type_val.get("name", type_val) if isinstance(type_val, dict) else type_val

    state = item.get("state") or {}
    state_name = state.get("name", "未知") if isinstance(state, dict) else state

    priority = item.get("priority") or {}
    priority_name = priority.get("name", "普通") if isinstance(priority, dict) else priority

    assignee = item.get("assignee") or {}
    assignee_name = assignee.get("display_name", "未分配") if isinstance(assignee, dict) else "未分配"

    project = item.get("project") or {}
    project_name = project.get("name", "?") if isinstance(project, dict) else "?"

    sprint = item.get("sprint") or {}
    sprint_name = sprint.get("name", "无") if isinstance(sprint, dict) else "无"

    lines = [
        f"📌 [{identifier}] {title}",
        f"   ID: {item_id}",
        f"   项目: {project_name}",
        f"   类型: {item_type} | 状态: {state_name} | 优先级: {priority_name}",
        f"   负责人: {assignee_name} | 迭代: {sprint_name}",
    ]

    desc = item.get("description")
    if desc:
        lines.append(f"   描述: {desc[:100]}{'...' if len(desc) > 100 else ''}")

    tags = item.get("tags", [])
    if tags:
        tag_names = [t.get("name", t) if isinstance(t, dict) else t for t in tags]
        lines.append(f"   标签: {', '.join(tag_names)}")

    sp = item.get("story_points")
    if sp is not None:
        lines.append(f"   故事点: {sp}")

    ew = item.get("estimated_workload")
    if ew is not None:
        lines.append(f"   预估工时: {ew}h")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="获取或删除 PingCode 单个工作项")
    parser.add_argument("workitem_id", help="工作项 ID")
    parser.add_argument("--delete", action="store_true", help="删除该工作项")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    token = get_access_token()
    if not token:
        sys.exit(1)

    if args.delete:
        ok = delete_workitem(token, args.workitem_id)
        if ok:
            print(f"✅ 工作项 {args.workitem_id} 已删除")
        else:
            sys.exit(1)
    else:
        item = get_workitem(token, args.workitem_id)
        if not item:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(item, indent=2, ensure_ascii=False))
        else:
            print(format_workitem(item))


if __name__ == "__main__":
    main()
