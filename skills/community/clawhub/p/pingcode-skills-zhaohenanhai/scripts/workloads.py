#!/usr/bin/env python3
"""
PingCode API Client - 工时管理
POST   /v1/workloads              创建工时
GET    /v1/workloads              获取工时列表
PATCH  /v1/workloads/{id}         更新工时
GET    /v1/workloads/{id}         获取单条工时
DELETE /v1/workloads/{id}         删除工时
GET    /v1/workload_types         获取工时类型列表
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


def api_request(access_token, method, path, params=None, payload=None):
    url = f"{BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    try:
        r = requests.request(method, url, headers=headers, params=params, json=payload, timeout=30)
        r.raise_for_status()
        if r.status_code == 204 or not r.content:
            return {}
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败 [{method} {path}]: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(f"响应: {e.response.text}", file=sys.stderr)
        return None


def parse_ts(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())


def format_workload(w):
    wid = w.get("id", "?")[:8]
    duration = w.get("duration", 0)
    desc = w.get("description", "")
    report_at = w.get("report_at")
    date_str = datetime.fromtimestamp(report_at).strftime("%Y-%m-%d") if report_at else "?"
    wtype = w.get("type") or {}
    type_name = wtype.get("name", "默认") if isinstance(wtype, dict) else "默认"
    reporter = w.get("report_by") or {}
    reporter_name = reporter.get("display_name", "?") if isinstance(reporter, dict) else "?"
    return f"⏱ [{wid}] {duration}h  日期: {date_str}  类型: {type_name}  登记人: {reporter_name}" + (
        f"\n   说明: {desc}" if desc else ""
    )


def main():
    parser = argparse.ArgumentParser(description="PingCode 工时管理")
    sub = parser.add_subparsers(dest="action", required=True)

    # types
    p_types = sub.add_parser("types", help="获取工时类型列表")
    p_types.add_argument("--json", action="store_true")

    # create
    p_c = sub.add_parser("create", help="创建工时")
    p_c.add_argument("--principal_id", required=True, help="工作项 ID")
    p_c.add_argument("--type_id", required=True, help="工时类型 ID（从 types 子命令获取）")
    p_c.add_argument("--duration", type=float, required=True, help="工时时长（小时，0-24）")
    p_c.add_argument("--report_at", required=True, help="登记日期 YYYY-MM-DD")
    p_c.add_argument("--report_by_id", help="登记人 ID（企业鉴权必填）")
    p_c.add_argument("--description", help="说明")
    p_c.add_argument("--json", action="store_true")

    # list
    p_l = sub.add_parser("list", help="获取工时列表")
    p_l.add_argument("--principal_id", help="工作项 ID")
    p_l.add_argument("--report_by_id", help="登记人 ID")
    p_l.add_argument("--start_at", help="开始日期 YYYY-MM-DD")
    p_l.add_argument("--end_at", help="结束日期 YYYY-MM-DD")
    p_l.add_argument("--json", action="store_true")

    # update
    p_u = sub.add_parser("update", help="更新工时")
    p_u.add_argument("workload_id", help="工时 ID")
    p_u.add_argument("--type_id", help="工时类型 ID")
    p_u.add_argument("--duration", type=float, help="工时时长（小时）")
    p_u.add_argument("--report_at", help="登记日期 YYYY-MM-DD")
    p_u.add_argument("--report_by_id", help="登记人 ID")
    p_u.add_argument("--description", help="说明")
    p_u.add_argument("--json", action="store_true")

    # delete
    p_d = sub.add_parser("delete", help="删除工时")
    p_d.add_argument("workload_id", help="工时 ID")

    args = parser.parse_args()
    token = get_access_token()
    if not token:
        sys.exit(1)

    if args.action == "types":
        data = api_request(token, "GET", "/v1/workload_types")
        if data is None:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            types = data.get("values", []) if isinstance(data, dict) else []
            print(f"🏷 工时类型列表 (共 {len(types)} 种)\n")
            for t in types:
                print(f"  [{t.get('id', '?')}] {t.get('name', '?')}")

    elif args.action == "create":
        payload = {
            "principal_id": args.principal_id,
            "principal_type": "work_item",
            "type_id": args.type_id,
            "duration": args.duration,
            "report_at": parse_ts(args.report_at),
        }
        if args.report_by_id:
            payload["report_by_id"] = args.report_by_id
        if args.description:
            payload["description"] = args.description
        data = api_request(token, "POST", "/v1/workloads", payload=payload)
        if data is None:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"✅ 工时已登记  {args.duration}h on {args.report_at}")

    elif args.action == "list":
        params = {"principal_type": "work_item"}
        if args.principal_id:
            params["principal_id"] = args.principal_id
        if args.report_by_id:
            params["report_by_id"] = args.report_by_id
        if args.start_at:
            params["start_at"] = parse_ts(args.start_at)
        if args.end_at:
            params["end_at"] = parse_ts(args.end_at)
        data = api_request(token, "GET", "/v1/workloads", params=params)
        if data is None:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            workloads = data.get("values", []) if isinstance(data, dict) else []
            total = data.get("total", len(workloads)) if isinstance(data, dict) else len(workloads)
            print(f"⏱ 工时列表 (共 {total} 条)\n")
            for w in workloads:
                print(format_workload(w))
                print()

    elif args.action == "update":
        payload = {}
        if args.type_id:
            payload["type_id"] = args.type_id
        if args.duration is not None:
            payload["duration"] = args.duration
        if args.report_at:
            payload["report_at"] = parse_ts(args.report_at)
        if args.report_by_id:
            payload["report_by_id"] = args.report_by_id
        if args.description:
            payload["description"] = args.description
        if not payload:
            print("没有要更新的字段", file=sys.stderr)
            sys.exit(1)
        data = api_request(token, "PATCH", f"/v1/workloads/{args.workload_id}", payload=payload)
        if data is None:
            sys.exit(1)
        if getattr(args, "json"):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"✅ 工时 {args.workload_id} 已更新")

    elif args.action == "delete":
        data = api_request(token, "DELETE", f"/v1/workloads/{args.workload_id}")
        if data is None:
            sys.exit(1)
        print(f"✅ 工时 {args.workload_id} 已删除")


if __name__ == "__main__":
    main()
