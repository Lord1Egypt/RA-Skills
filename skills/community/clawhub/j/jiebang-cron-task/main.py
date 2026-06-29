#!/usr/bin/env python3
"""
捷帮定时任务管理工具 - AI Agent Cron Task Manager
API: https://www.jiebang.site/api/cron-task
"""

import os
import sys
import json
import argparse
from pathlib import Path

from coze_workload_identity import requests

BASE_URL = "https://www.jiebang.site"
KEY_FILE = Path(__file__).parent / ".jiebang_api_key"


def get_api_key():
    """获取保存的API Key，如果没有则返回None"""
    if KEY_FILE.exists():
        return KEY_FILE.read_text().strip()
    return None


def save_api_key(key):
    """保存API Key到本地文件"""
    KEY_FILE.write_text(key.strip())
    return key


def ensure_key():
    """确保API Key可用，如果没有则自动注册"""
    key = get_api_key()
    if key:
        # 验证key是否有效
        try:
            resp = requests.get(
                f"{BASE_URL}/api/auth/info",
                headers={"Authorization": f"Bearer {key}"},
                timeout=10
            )
            if resp.status_code == 200:
                return key
        except Exception:
            pass

    # 注册新key
    try:
        resp = requests.post(
            f"{BASE_URL}/api/auth/register",
            headers={"Content-Type": "application/json"},
            json={},
            timeout=10
        )
        data = resp.json()
        if "api_key" in data:
            save_api_key(data["api_key"])
            return data["api_key"]
        else:
            print(json.dumps({"error": f"注册失败: {data}", "status": "error"}, ensure_ascii=False))
            return None
    except Exception as e:
        print(json.dumps({"error": f"注册请求失败: {str(e)}", "status": "error"}, ensure_ascii=False))
        return None


def api_headers():
    """获取带认证的请求头"""
    key = get_api_key()
    if not key:
        return None
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }


def create_task(name, cron, retries=None, tags=None, template=None, description=None):
    """创建定时任务"""
    headers = api_headers()
    if not headers:
        print(json.dumps({"error": "API Key不可用，请先运行 ensure-key", "status": "error"}, ensure_ascii=False))
        return

    body = {"name": name, "schedule": cron}
    if retries:
        body["max_retries"] = retries
    if tags:
        body["tags"] = tags if isinstance(tags, list) else tags.split(",")
    if template:
        body["template"] = template
    if description:
        body["description"] = description

    try:
        resp = requests.post(
            f"{BASE_URL}/api/cron-task",
            headers=headers,
            json=body,
            timeout=15
        )
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "error"}, ensure_ascii=False))


def list_tasks(due_only=False, tag=None):
    """查询任务列表"""
    headers = api_headers()
    if not headers:
        print(json.dumps({"error": "API Key不可用，请先运行 ensure-key", "status": "error"}, ensure_ascii=False))
        return

    params = {}
    if due_only:
        params["due"] = "true"
    if tag:
        params["tag"] = tag

    try:
        resp = requests.get(
            f"{BASE_URL}/api/cron-task",
            headers=headers,
            params=params,
            timeout=15
        )
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "error"}, ensure_ascii=False))


def complete_task(task_id, status="success", message=None):
    """标记任务完成"""
    headers = api_headers()
    if not headers:
        print(json.dumps({"error": "API Key不可用，请先运行 ensure-key", "status": "error"}, ensure_ascii=False))
        return

    body = {"status": status}
    if message:
        body["message"] = message

    try:
        resp = requests.post(
            f"{BASE_URL}/api/cron-task/{task_id}/done",
            headers=headers,
            params=body,
            timeout=15
        )
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "error"}, ensure_ascii=False))


def get_logs(task_id=None, limit=20):
    """查看执行日志"""
    headers = api_headers()
    if not headers:
        print(json.dumps({"error": "API Key不可用，请先运行 ensure-key", "status": "error"}, ensure_ascii=False))
        return

    url = f"{BASE_URL}/api/cron-task/logs"
    if task_id:
        url = f"{BASE_URL}/api/cron-task/{task_id}/logs"

    try:
        resp = requests.get(
            url,
            headers=headers,
            params={"limit": limit},
            timeout=15
        )
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "error"}, ensure_ascii=False))


def get_templates():
    """获取预设模板"""
    headers = api_headers()
    if not headers:
        print(json.dumps({"error": "API Key不可用，请先运行 ensure-key", "status": "error"}, ensure_ascii=False))
        return

    try:
        resp = requests.get(
            f"{BASE_URL}/api/cron-task/templates",
            headers=headers,
            timeout=15
        )
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "error"}, ensure_ascii=False))


def delete_task(task_id):
    """删除任务"""
    headers = api_headers()
    if not headers:
        print(json.dumps({"error": "API Key不可用，请先运行 ensure-key", "status": "error"}, ensure_ascii=False))
        return

    try:
        resp = requests.delete(
            f"{BASE_URL}/api/cron-task/{task_id}",
            headers=headers,
            timeout=15
        )
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "error"}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="捷帮定时任务管理工具")
    subparsers = parser.add_subparsers(dest="command")

    # ensure-key
    subparsers.add_parser("ensure-key", help="注册/验证API Key")

    # create
    create_p = subparsers.add_parser("create", help="创建定时任务")
    create_p.add_argument("--name", required=True, help="任务名称")
    create_p.add_argument("--cron", required=True, help="Cron表达式 (分 时 日 月 周)")
    create_p.add_argument("--retries", type=int, help="最大重试次数")
    create_p.add_argument("--tags", help="标签 (逗号分隔)")
    create_p.add_argument("--template", help="预设模板ID")
    create_p.add_argument("--desc", help="任务描述")

    # list
    list_p = subparsers.add_parser("list", help="查询任务列表")
    list_p.add_argument("--due", action="store_true", help="仅查看到期任务")
    list_p.add_argument("--tag", help="按标签筛选")

    # done
    done_p = subparsers.add_parser("done", help="标记任务完成")
    done_p.add_argument("task_id", help="任务ID")
    done_p.add_argument("--status", default="success", choices=["success", "failed"], help="执行状态")
    done_p.add_argument("--msg", help="附加消息")

    # logs
    logs_p = subparsers.add_parser("logs", help="查看执行日志")
    logs_p.add_argument("--task-id", help="指定任务ID")
    logs_p.add_argument("--limit", type=int, default=20, help="返回条数")

    # templates
    subparsers.add_parser("templates", help="获取预设模板")

    # delete
    delete_p = subparsers.add_parser("delete", help="删除任务")
    delete_p.add_argument("task_id", help="任务ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "ensure-key":
        key = ensure_key()
        if key:
            print(json.dumps({"status": "ok", "message": "API Key已就绪", "key_preview": key[:8] + "..."}, ensure_ascii=False))
    elif args.command == "create":
        create_task(args.name, args.cron, args.retries, args.tags, args.template, args.desc)
    elif args.command == "list":
        list_tasks(args.due, args.tag)
    elif args.command == "done":
        complete_task(args.task_id, args.status, args.msg)
    elif args.command == "logs":
        get_logs(args.task_id, args.limit)
    elif args.command == "templates":
        get_templates()
    elif args.command == "delete":
        delete_task(args.task_id)


if __name__ == "__main__":
    main()
