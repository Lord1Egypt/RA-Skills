#!/usr/bin/env python3


from __future__ import annotations

import argparse
import base64
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

import certifi


BASE_URL = "https://open-test.magiclight.ai"


def _get_ssl_context() -> ssl.SSLContext:
    """创建使用 certifi 证书的 SSL 上下文"""
    ctx = ssl.create_default_context(cafile=certifi.where())
    return ctx


def _get_api_key(explicit: Optional[str] = None) -> str:
    api_key = explicit or os.environ.get("MAGIC_API_KEY")
    if not api_key:
        raise ValueError("MAGIC_API_KEY is required (env or --api-key).")
    return api_key


def _http_request_json(
    *,
    method: str,
    url: str,
    api_key: str,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Dict[str, Any]] = None,
    timeout_s: int = 60,
    user_agent: str = "Magic-Media-Gen/1.0",
) -> Dict[str, Any]:
    all_headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": user_agent,
    }
    if headers:
        all_headers.update(headers)

    data: Optional[bytes] = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        all_headers.setdefault("Content-Type", "application/json")
    elif method.upper() in {"POST", "PUT", "PATCH"}:
        data = b"{}"
        all_headers.setdefault("Content-Type", "application/json")

    req = urllib.request.Request(url, data=data, headers=all_headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout_s, context=_get_ssl_context()) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"success": False, "error": {"code": str(e.code), "message": raw}}
    except urllib.error.URLError as e:
        return {"success": False, "error": {"code": "NETWORK_ERROR", "message": str(getattr(e, "reason", e))}}


def video_create_task(
    *,
    api_key: str,
    text: str,
    image_url: str,
) -> Dict[str, Any]:
    url = f"{BASE_URL}/api/misc/openclaw_add_task"
    headers = {"X-DashScope-Async": "enable"}
    body: Dict[str, Any] = {
        "text": text,
        "image_url": image_url,
    }
    return _http_request_json(method="POST", url=url, api_key=api_key, headers=headers, body=body, timeout_s=90)


def video_task_status(*, api_key: str, task_id: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/api/misc/openclaw_check_task?task_id={task_id}"
    return _http_request_json(method="GET", url=url, api_key=api_key, timeout_s=60)


def _print_json(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def image_put_url(*, api_key: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/api/misc/openclaw_put_url"
    return _http_request_json(method="GET", url=url, api_key=api_key, timeout_s=60)

def image_get_url(*, api_key: str, key: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/api/misc/openclaw_get_url?key={key}"
    return _http_request_json(method="GET", url=url, api_key=api_key, timeout_s=60)

def cmd_video_create(args: argparse.Namespace) -> int:
    api_key = _get_api_key(args.api_key)
    image_url = None
    try:
        if args.image.startswith("http"):
            image_content = urllib.request.urlopen(args.image, context=_get_ssl_context()).read()
            image_url = args.image if image_content else None
        else:
            image_content = open(args.image, "rb").read()
            image_put_url_resp = image_put_url(api_key=api_key)
            # _print_json(image_put_url_resp)
            image_key = image_put_url_resp.get("data", {}).get("key")
            put_url = image_put_url_resp.get("data", {}).get("put_url")
            # put_url是临时上传地址，需要上传图片到put_url
            req = urllib.request.Request(put_url, data=image_content, method="PUT")
            with urllib.request.urlopen(req, context=_get_ssl_context()) as resp:
                status = resp.getcode()
                if status != 200:
                    raise Exception(f"Failed to upload image to put_url, status: {status}")
            image_get_url_resp = image_get_url(api_key=api_key, key=image_key)
            # _print_json(image_get_url_resp)
            temp_image_url = image_get_url_resp.get("data", {}).get("get_url")
            image_url = temp_image_url if temp_image_url else None
    except Exception as e:
        print(f"Error: {e}")
        return 1
    # 重试3次
    for _ in range(3):
        resp = video_create_task(
            api_key=api_key,
            text=args.text,
            image_url=image_url,
        )
        if resp.get("data", {}).get("task_id"):
            break
        time.sleep(3)
    _print_json(resp)
    return 0


def cmd_video_status(args: argparse.Namespace) -> int:
    api_key = _get_api_key(args.api_key)
    resp = video_task_status(api_key=api_key, task_id=args.task_id)
    _print_json(resp)
    return 0


def cmd_video_wait(args: argparse.Namespace) -> int:
    api_key = _get_api_key(args.api_key)
    start = time.time()
    while True:
        resp = video_task_status(api_key=api_key, task_id=args.task_id)
        task_status = resp.get("data", {}).get("task_status", 0)
        if task_status in {2, 3}:
            _print_json(resp)
            return 0 if task_status == 2 else 1

        if time.time() - start > args.timeout:
            _print_json({"success": False, "error": "timeout"})
            return 1

        time.sleep(args.poll)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OpenClaw Media Gen - image & video generation")
    p.add_argument("--api-key", help="Override MAGIC_API_KEY")

    sub = p.add_subparsers(dest="command")

    vc = sub.add_parser("video-create", help="Create Wan 2.6 video generation task")
    vc.add_argument("--text", required=True, help="Text")
    vc.add_argument("--image", required=True, help="Image URL")
    vc.set_defaults(func=cmd_video_create)

    vs = sub.add_parser("video-status", help="Query video task status")
    vs.add_argument("--task-id", required=True, help="Task id")
    vs.set_defaults(func=cmd_video_status)

    vw = sub.add_parser("video-wait", help="Wait until video task finishes")
    vw.add_argument("--task-id", required=True, help="Task id")
    vw.add_argument("--poll", type=int, default=10, help="Poll interval seconds")
    vw.add_argument("--timeout", type=int, default=600, help="Timeout seconds")
    vw.set_defaults(func=cmd_video_wait)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

