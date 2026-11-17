#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 HIFLEET_API_KEY 换取 Skills 控制台一次性登录链接并打开浏览器。

换票 API：HIFLEET_API_BASE（默认 https://api.hifleet.com）
  POST /openclaw/account/session/from-api-key
打开页面：接口返回的 consoleUrl（一般为 https://skills.hifleet.com/openclaw/console.html?...ticket=）

Security: api_key 仅用于换票请求；浏览器只打开含短时 ticket 的 consoleUrl，
不把 api_key 写入地址栏。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import webbrowser


def get_api_key() -> str:
    return (os.environ.get("HIFLEET_API_KEY") or "").strip()


def get_api_base() -> str:
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")


def create_console_session(api_base: str, api_key: str, redirect: str) -> dict:
    url = api_base + "/openclaw/account/session/from-api-key"
    body = json.dumps({"apiKey": api_key, "redirect": redirect}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if str(payload.get("status")) not in ("1", "1.0"):
        raise RuntimeError(payload.get("msg") or payload.get("message") or "换票失败")
    data = payload.get("data") or {}
    if not data.get("consoleUrl"):
        raise RuntimeError("响应缺少 consoleUrl")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="用 api_key 打开 HiFleet Skills 控制台")
    parser.add_argument(
        "--redirect",
        default="usage",
        help="落地页：usage / wallet / subscription / plans / api-keys / invoices",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="只打印 consoleUrl，不打开浏览器",
    )
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("请配置环境变量 HIFLEET_API_KEY", file=sys.stderr)
        return 1
    if not api_key.startswith("sk_"):
        print("HIFLEET_API_KEY 格式异常，应以 sk_ 开头", file=sys.stderr)
        return 1

    redirect = args.redirect.strip()
    if not redirect.startswith("/"):
        redirect = "/" + redirect

    try:
        data = create_console_session(get_api_base(), api_key, redirect)
    except urllib.error.HTTPError as ex:
        err = ex.read().decode("utf-8", errors="replace")
        print("换票 HTTP 错误: %s %s" % (ex.code, err), file=sys.stderr)
        return 1
    except Exception as ex:
        print("换票失败: %s" % ex, file=sys.stderr)
        return 1

    console_url = data["consoleUrl"]
    print("userId=%s" % data.get("userId"))
    print("consoleUrl=%s" % console_url)
    if args.print_only:
        return 0
    webbrowser.open(console_url)
    print("已尝试打开浏览器。若未弹出，请手动打开上方 consoleUrl。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
