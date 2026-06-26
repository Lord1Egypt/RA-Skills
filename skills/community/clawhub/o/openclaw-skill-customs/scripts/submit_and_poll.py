#!/usr/bin/env python3
"""
Leap 报关技能统一任务脚本（优化版）
- 指数退避轮询 + 减少上下文输出
- 支持 --quiet 模式，适合 OpenClaw Agent 调用
- 结构化错误处理 + 连续错误保护
"""

import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.error
import random
from typing import Optional, Dict

DEFAULT_BASE_URL = "https://platform.daofeiai.com"


class ApiError(Exception):
    """结构化 API 错误，保留 HTTP 状态码"""
    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"HTTP {status_code}: {body}")


def _request(method: str, url: str, api_key: str, json_body=None, timeout: int = 30) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    data = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise ApiError(e.code, body)
    except urllib.error.URLError as e:
        raise RuntimeError(f"连接失败: {e}") from e


def _emit_progress(attempt: int, elapsed: int, status: str, progress: int, quiet: bool = False):
    """减少输出频率，避免上下文膨胀"""
    if quiet:
        return
    # processing 状态每 3 次才输出一次，或状态发生变化时输出
    if status == "processing" and attempt % 3 != 0:
        return
    print(json.dumps({
        "poll_attempt": attempt,
        "elapsed_seconds": elapsed,
        "status": status,
        "progress": progress,
    }, ensure_ascii=False), file=sys.stderr)


def _poll_until_done(base_url: str, api_key: str, result_id: str,
                     interval: int = 8, max_wait: int = 300,
                     initial_delay: int = 3, quiet: bool = False,
                     save_to: Optional[str] = None):
    """优化版轮询：指数退避 + 结构化错误 + 减少输出 + 可选结果持久化"""
    poll_url = f"{base_url}/api/v1/process/tasks/{result_id}"
    start_time = time.time()

    time.sleep(initial_delay)  # 首次缓冲，可配置

    attempt = 0
    consecutive_errors = 0
    last_status: Optional[str] = None

    MAX_CONSECUTIVE_ERRORS = 4
    BASE_INTERVAL = max(2, interval // 2)   # 基础间隔
    MAX_INTERVAL = 30

    while True:
        attempt += 1
        elapsed = int(time.time() - start_time)

        if elapsed > max_wait:
            print(json.dumps({
                "status": "timeout",
                "result_id": result_id,
                "elapsed_seconds": elapsed,
                "message": f"等待超过 {max_wait} 秒，请稍后手动查询。",
                "manual_check": f'curl -H "Authorization: Bearer $LEAP_API_KEY" "{poll_url}"'
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        try:
            data = _request("GET", poll_url, api_key)
            consecutive_errors = 0

            status = data.get("status", "unknown")
            progress = data.get("progress", 0)

            # 状态变化或每3次输出一次进度
            if status != last_status or attempt % 3 == 0:
                _emit_progress(attempt, elapsed, status, progress, quiet)
                last_status = status

            if status == "completed":
                if save_to:
                    try:
                        with open(save_to, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        print(f"[结果已保存至 {os.path.abspath(save_to)}]", file=sys.stderr)
                    except OSError as write_err:
                        print(f"[警告] 保存结果文件失败: {write_err}", file=sys.stderr)
                print(json.dumps(data, ensure_ascii=False, indent=2))
                sys.exit(0)

            if status == "failed":
                print(json.dumps({
                    "status": "failed",
                    "error_message": data.get("error_message", "未知错误"),
                    "result_id": result_id,
                    "elapsed_seconds": elapsed,
                }, ensure_ascii=False, indent=2))
                sys.exit(1)

        except ApiError as e:
            if e.status_code == 404:
                print(json.dumps({
                    "status": "error",
                    "error_message": f"任务不存在: {result_id}，请检查 result_id 是否正确"
                }, ensure_ascii=False, indent=2))
                sys.exit(1)

            consecutive_errors += 1
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                print(json.dumps({
                    "status": "error",
                    "error_message": str(e)
                }, ensure_ascii=False, indent=2), file=sys.stderr)
                sys.exit(1)
            # 其他 HTTP 错误短暂继续轮询

        except Exception as e:
            consecutive_errors += 1
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                print(json.dumps({
                    "status": "error",
                    "error_message": str(e)
                }, ensure_ascii=False, indent=2), file=sys.stderr)
                sys.exit(1)
            _emit_progress(attempt, elapsed, "error", 0, quiet)

        # 指数退避 + 小抖动
        delay = min(BASE_INTERVAL * (1.6 ** (attempt - 1)), MAX_INTERVAL)
        delay += random.uniform(0, delay * 0.08)
        time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(description="Leap 异步任务提交与同步等待脚本（优化版）")
    parser.add_argument("--mode", required=True,
                        choices=["classify", "customs", "poll", "list-tasks", "cancel", "retry"],
                        help="任务模式")
    parser.add_argument("--file-id", action="append", default=[], help="文件ID (classify 模式可多次指定)")
    parser.add_argument("--json-data", help="报关模式所需的 JSON 参数（字符串形式）")
    parser.add_argument("--json-file", help="报关模式所需的 JSON 参数（文件路径，由 build_payload.py 生成）")
    parser.add_argument("--result-id", help="poll/cancel/retry 模式必填")
    parser.add_argument("--limit", type=int, default=10, help="list-tasks 返回数量")
    parser.add_argument("--interval", type=int, default=8, help="基础轮询间隔（秒）")
    parser.add_argument("--max-wait", type=int, default=300, help="最长等待秒数")
    parser.add_argument("--initial-delay", type=int, default=3, help="首次轮询前等待秒数")
    parser.add_argument("--quiet", action="store_true", help="安静模式，减少进度输出")
    parser.add_argument("--save-to", metavar="FILE",
                        help="任务完成后将完整结果 JSON 保存到指定文件（classify 推荐 classify_result.json，customs 推荐 customs_result.json）")

    args = parser.parse_args()

    api_key = os.environ.get("LEAP_API_KEY", "")
    base_url = DEFAULT_BASE_URL

    if not api_key:
        print(json.dumps({
            "status": "error",
            "error_message": "LEAP_API_KEY 未配置。请在 OpenClaw skill 设置中配置环境变量。"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # poll 模式
    if args.mode == "poll":
        if not args.result_id:
            print("错误: poll 模式必须提供 --result-id", file=sys.stderr)
            sys.exit(1)
        _poll_until_done(base_url, api_key, args.result_id,
                         args.interval, args.max_wait, args.initial_delay, args.quiet,
                         save_to=args.save_to)
        return

    # list-tasks 模式
    if args.mode == "list-tasks":
        url = f"{base_url}/api/v1/process/tasks?limit={args.limit}"
        try:
            data = _request("GET", url, api_key)
            print(json.dumps(data, ensure_ascii=False, indent=2))
            sys.exit(0)
        except Exception as e:
            print(json.dumps({"status": "error", "error_message": str(e)}, ensure_ascii=False, indent=2))
            sys.exit(1)

    # cancel 模式
    if args.mode == "cancel":
        if not args.result_id:
            print("错误: cancel 模式必须提供 --result-id", file=sys.stderr)
            sys.exit(1)
        url = f"{base_url}/api/v1/process/tasks/{args.result_id}"
        try:
            data = _request("DELETE", url, api_key)
            print(json.dumps(data, ensure_ascii=False, indent=2))
            sys.exit(0)
        except Exception as e:
            print(json.dumps({"status": "error", "error_message": str(e)}, ensure_ascii=False, indent=2))
            sys.exit(1)

    # retry 模式
    if args.mode == "retry":
        if not args.result_id:
            print("错误: retry 模式必须提供 --result-id", file=sys.stderr)
            sys.exit(1)
        url = f"{base_url}/api/v1/process/tasks/{args.result_id}/retry"
        try:
            data = _request("POST", url, api_key)
            print(json.dumps(data, ensure_ascii=False, indent=2))
            sys.exit(0)
        except Exception as e:
            print(json.dumps({"status": "error", "error_message": str(e)}, ensure_ascii=False, indent=2))
            sys.exit(1)

    # classify / customs 模式：提交任务
    payload: Dict = {}
    if args.mode == "classify":
        if not args.file_id:
            print("错误: classify 模式必须提供至少一个 --file-id", file=sys.stderr)
            sys.exit(1)
        payload["output"] = "classify_fast"
        payload["params"] = {"files": [{"file_id": fid} for fid in args.file_id]}
        payload["force_reprocess"] = True

    elif args.mode == "customs":
        if not args.json_data and not args.json_file:
            print("错误: customs 模式必须提供 --json-data 或 --json-file", file=sys.stderr)
            sys.exit(1)
        if args.json_file:
            if not os.path.isfile(args.json_file):
                print(json.dumps({
                    "status": "error",
                    "error_message": f"--json-file 指定的文件不存在: {args.json_file}。请先运行 build_payload.py 生成。"
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
            try:
                with open(args.json_file, "r", encoding="utf-8") as f:
                    params_data = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(json.dumps({
                    "status": "error",
                    "error_message": f"读取 --json-file 失败: {e}"
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
        else:
            try:
                params_data = json.loads(args.json_data)
            except json.JSONDecodeError as e:
                print(f"错误: --json-data 格式不合法 - {e}", file=sys.stderr)
                sys.exit(1)

        payload["output"] = "customs"
        payload["params"] = params_data if "files" in params_data else {"files": params_data}
        payload["force_reprocess"] = True

    # 提交任务
    submit_url = f"{base_url}/api/v1/process"
    try:
        submit_resp = _request("POST", submit_url, api_key, json_body=payload)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "stage": "submit",
            "error_message": str(e)
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    result_id = submit_resp.get("result_id")
    if not result_id:
        print(json.dumps({
            "status": "error",
            "stage": "submit",
            "error_message": "提交接口未返回 result_id"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(json.dumps({"stage": "submitted", "result_id": result_id}, ensure_ascii=False), file=sys.stderr)

    # 开始轮询
    _poll_until_done(base_url, api_key, result_id,
                     args.interval, args.max_wait, args.initial_delay, args.quiet,
                     save_to=args.save_to)


if __name__ == "__main__":
    main()