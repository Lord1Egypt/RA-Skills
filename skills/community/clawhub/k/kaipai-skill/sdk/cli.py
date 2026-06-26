#!/usr/bin/env python3
"""Kaipai AI SDK CLI - 简化版命令行接口"""

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from sdk import SkillClient
from sdk.core.config import INVOKE
from sdk.core.client import ConsumeDeniedError


def _print(data: dict) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _task_succeeded(result: dict) -> bool:
    """Align CLI exit code with SkillClient.execute/query payloads (no skill_status on raw API success)."""
    if not isinstance(result, dict):
        return False
    if result.get("skill_status") == "failed" or result.get("error"):
        return False
    if result.get("skill_status") == "completed":
        return True
    if result.get("output_urls"):
        return True
    data = result.get("data")
    if isinstance(data, dict) and data.get("status") in (10, 2, 20):
        return True
    return False


def _handle(func):
    """统一错误处理装饰器"""
    try:
        return func()
    except ConsumeDeniedError as e:
        _print({"error": "quota_error", "code": e.code, "message": e.msg})
        return 1
    except Exception as e:
        _print({"error": str(e)})
        return 1


def run_task(ak: str, sk: str, task: str, source: str, params: str = None) -> int:
    """运行任务（自动完成：上传+消费+提交+轮询）"""
    def _do():
        client = SkillClient(ak=ak, sk=sk)
        p = json.loads(params) if params else {}
        result = client.execute(task_name=task, source=source or "", params=p)
        _print(result)
        return 0 if _task_succeeded(result) else 1
    return _handle(_do)


def query_task(ak: str, sk: str, task_id: str) -> int:
    """查询任务状态"""
    def _do():
        client = SkillClient(ak=ak, sk=sk)
        result = client.query(task_id)
        _print(result)
        return 0 if _task_succeeded(result) else 1
    return _handle(_do)


def list_tasks(ak: str, sk: str) -> int:
    """列出可用任务"""
    def _do():
        SkillClient(ak=ak, sk=sk)
        tasks = [{"name": n, **c} for n, c in INVOKE.items()]
        _print({"tasks": tasks, "count": len(tasks)})
        return 0
    return _handle(_do)


def main() -> int:
    parser = argparse.ArgumentParser(description="Kaipai AI SDK CLI")
    parser.add_argument("--ak", default=os.environ.get("MT_AK"), help="Access Key")
    parser.add_argument("--sk", default=os.environ.get("MT_SK"), help="Secret Key")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # run-task: 上传+消费+提交+轮询（一站式）
    p = sub.add_parser("run-task", help="Run AI task (upload+consume+submit+poll)")
    p.add_argument("--task", required=True, help="Task name")
    p.add_argument("--input", default="", help="Input file or URL")
    p.add_argument("--params", help="Params (JSON)")

    # query-task: 查询任务状态
    p = sub.add_parser("query-task", help="Query task status")
    p.add_argument("--task-id", required=True, help="Task ID")

    # list-tasks: 列出任务
    sub.add_parser("list-tasks", help="List available tasks")

    args = parser.parse_args()

    if not args.ak or not args.sk:
        parser.error("--ak and --sk required (or MT_AK/MT_SK env vars)")

    # 路由到对应函数
    if args.cmd == "run-task":
        return run_task(args.ak, args.sk, args.task, args.input, args.params)
    elif args.cmd == "query-task":
        return query_task(args.ak, args.sk, args.task_id)
    elif args.cmd == "list-tasks":
        return list_tasks(args.ak, args.sk)

    return 0


if __name__ == "__main__":
    sys.exit(main())
