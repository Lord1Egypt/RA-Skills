#!/usr/bin/env python3
"""Sora/Veo/Grok/豆包/Vidu 任务查询：GET /v1/videos/{task_id}（兼容旧版 /content）"""

import argparse
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from _config import first_env, load_env_file, resolve_env_file_from_argv
from _logger import error_exit, print_json

DEFAULT_TIMEOUT = 60
DEFAULT_INTERVAL = 5
DEFAULT_MAX_WAIT = 600
DEFAULT_ENV_FILE = ".env"
TERMINAL_STATUSES = {"completed", "failed", "cancelled"}


def provider_priority(provider: str):
    provider = (provider or "").strip().lower()
    if provider == "vidu":
        return ["VIDU", "SORA", "DOUBAO", "VEO", "GROK"]
    if provider == "doubao":
        return ["DOUBAO", "SORA", "VIDU", "VEO", "GROK"]
    if provider == "veo":
        return ["VEO", "SORA", "VIDU", "DOUBAO", "GROK"]
    if provider == "grok":
        return ["GROK", "SORA", "VIDU", "DOUBAO", "VEO"]
    return ["SORA", "VEO", "VIDU", "DOUBAO", "GROK"]


def env_by_provider(provider: str, suffix: str, default: str = "", include_video: bool = False) -> str:
    names = [f"{prefix}_{suffix}" for prefix in provider_priority(provider)]
    if include_video:
        names.append(f"VIDEO_{suffix}")
    return first_env(*names, default=default)


def extract_video_url(payload: dict) -> str:
    def pick_from_map(obj: dict) -> str:
        for key in ("video_url", "videoUrl", "url", "output"):
            value = obj.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, dict):
                nested = pick_from_map(value)
                if nested:
                    return nested
        return ""

    if not isinstance(payload, dict):
        return ""

    direct = pick_from_map(payload)
    if direct:
        return direct

    data = payload.get("data")
    if isinstance(data, dict):
        return pick_from_map(data)

    return ""


def pick_task_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {}

    data = payload.get("data")
    if isinstance(data, dict) and ("id" in data or "task_id" in data or "status" in data):
        return data
    return payload


def fetch_task(url: str, api_key: str, timeout: int):
    req = urllib.request.Request(
        url,
        method="GET",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            if not raw.strip():
                return {}
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                error_exit(f"任务查询返回非 JSON：{raw[:500]}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        if e.code == 404:
            return {"_http_status": 404, "_http_body": err_body}
        error_exit(f"API 错误 {e.code}: {err_body}")
    except (TimeoutError, socket.timeout):
        return {"_request_timeout": True}
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            return {"_request_timeout": True}
        error_exit(f"网络错误: {e.reason}")


def normalize_status(value: str, has_video_url: bool) -> str:
    text = (value or "").strip().lower()
    if not text and has_video_url:
        return "completed"
    return text


def build_result(task_id: str, payload: dict) -> dict:
    task = pick_task_payload(payload)
    resolved_task_id = (
        task.get("id")
        or task.get("task_id")
        or payload.get("id")
        or payload.get("task_id")
        or task_id
    )
    video_url = extract_video_url(payload)
    status = normalize_status(task.get("status") or payload.get("status") or "", bool(video_url))

    result = {
        "id": resolved_task_id,
        "object": task.get("object", payload.get("object", "")),
        "model": task.get("model", payload.get("model", "")),
        "status": status,
        "progress": task.get("progress", payload.get("progress", 0)),
        "created_at": task.get("created_at", payload.get("created_at", None)),
        "size": task.get("size", payload.get("size", "")),
    }
    completed_at = task.get("completed_at", payload.get("completed_at", None))
    if completed_at is not None:
        result["completed_at"] = completed_at
    expires_at = task.get("expires_at", payload.get("expires_at", None))
    if expires_at is not None:
        result["expires_at"] = expires_at
    remixed_from = task.get("remixed_from_video_id", payload.get("remixed_from_video_id", None))
    if remixed_from:
        result["remixed_from_video_id"] = remixed_from
    if video_url:
        result["video_url"] = video_url
    error = task.get("error", payload.get("error", None))
    if isinstance(error, dict) and error:
        result["error"] = error
    return result


def main():
    env_file = resolve_env_file_from_argv(sys.argv[1:])
    load_env_file(env_file)
    provider_hint = (os.environ.get("VIDEO_PROVIDER_HINT") or "").strip().lower()

    parser = argparse.ArgumentParser(
        description="查询 Sora/Veo/Grok/豆包/Vidu 视频任务状态",
        epilog="""
环境变量:
    API_KEY       必填，Bearer 鉴权
    API_BASE_URL  必填，接口域名，如 https://xxxxx

示例:
  # 单次查询
  python3 sora_query_video.py video_xxx

  # 轮询直到完成
  python3 sora_query_video.py video_xxx --wait --interval 5 --max-wait 900
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--env-file",
        default=env_file,
        help="环境变量文件路径（默认 .env）",
    )
    parser.add_argument(
        "--provider",
        choices=["sora", "veo", "grok", "doubao", "vidu"],
        default="",
        help="可选：指定配置优先来源（默认按环境提示自动回退）",
    )
    parser.add_argument("task_id", help="任务 ID（由 sora_generate_video.py 返回）")
    parser.add_argument(
        "--base-url",
        default="",
        help="接口域名，不带 /v1/videos，例如 https://xxxxx",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Bearer Token（不需要填写 Bearer 前缀）",
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="单次请求超时秒数（默认 60）")
    parser.add_argument("--wait", action="store_true", help="持续轮询直到任务完成/失败/取消")
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        help="轮询间隔秒数（默认 5）",
    )
    parser.add_argument(
        "--max-wait",
        type=int,
        default=DEFAULT_MAX_WAIT,
        help="最大等待秒数（默认 600）",
    )
    parser.add_argument(
        "--use-deprecated-content-endpoint",
        action="store_true",
        help="[已弃用] 改用 /v1/videos/{task_id}/content（默认推荐 /v1/videos/{task_id}）",
    )
    parser.add_argument("--raw", action="store_true", help="输出原始响应")
    args = parser.parse_args()

    provider = (args.provider or provider_hint).strip().lower()
    args.base_url = args.base_url or os.environ.get("API_BASE_URL", "")
    args.api_key = args.api_key or os.environ.get("API_KEY", "")

    if not args.base_url:
        error_exit("请通过 --base-url 或 API_BASE_URL 提供接口域名")
    if not args.api_key:
        error_exit("请通过 --api-key 或 API_KEY 提供 API Key")
    if args.interval <= 0:
        error_exit("--interval 必须大于 0")
    if args.max_wait <= 0:
        error_exit("--max-wait 必须大于 0")

    task_id_quoted = urllib.parse.quote(args.task_id, safe="")
    if args.use_deprecated_content_endpoint:
        query_url = f"{args.base_url.rstrip('/')}/v1/videos/{task_id_quoted}/content"
    else:
        query_url = f"{args.base_url.rstrip('/')}/v1/videos/{task_id_quoted}"

    start_at = time.time()
    attempts = 0

    while True:
        attempts += 1
        payload = fetch_task(query_url, args.api_key, args.timeout)
        elapsed = int(time.time() - start_at)

        if payload.get("_request_timeout"):
            if args.wait and elapsed < args.max_wait:
                time.sleep(args.interval)
                continue

            output = {
                "id": args.task_id,
                "status": "network_timeout",
                "attempts": attempts,
                "elapsedSeconds": elapsed,
            }
            if args.raw:
                output["raw"] = payload
            print_json(output)
            sys.exit(1)

        if payload.get("_http_status") == 404:
            if args.wait and elapsed < args.max_wait:
                time.sleep(args.interval)
                continue

            output = {
                "id": args.task_id,
                "status": "not_found",
                "attempts": attempts,
                "elapsedSeconds": elapsed,
            }
            if args.raw:
                output["raw"] = payload
            print_json(output)
            sys.exit(1)

        result = build_result(args.task_id, payload)
        result["attempts"] = attempts
        result["elapsedSeconds"] = int(time.time() - start_at)
        if args.raw:
            result["raw"] = payload

        if not args.wait:
            print_json(result)
            return

        if result["status"] in TERMINAL_STATUSES:
            print_json(result)
            if result["status"] == "completed":
                return
            sys.exit(1)

        if result["elapsedSeconds"] >= args.max_wait:
            result["timedOut"] = True
            print_json(result)
            sys.exit(1)

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
