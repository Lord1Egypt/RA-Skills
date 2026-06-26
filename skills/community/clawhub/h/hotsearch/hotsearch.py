#!/usr/bin/env python3
"""
Hot search (Weibo/Baidu/Douyin) skill for OpenClaw.
基于极速数据微博百度热搜榜单 API：
https://www.jisuapi.com/api/hotsearch/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/hotsearch"


def _call_hotsearch(path: str, appkey: str):
    url = f"{BASE_URL}/{path}"
    params = {"appkey": appkey}

    try:
        resp = requests.get(url, params=params, timeout=10)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}

    if data.get("status") != 0:
        return {
            "error": "api_error",
            "code": data.get("status"),
            "message": data.get("msg"),
        }

    return data.get("result", [])


def weibo_hot(appkey: str):
    """微博热搜 /hotsearch/weibo"""
    return _call_hotsearch("weibo", appkey)


def baidu_hot(appkey: str):
    """百度热搜 /hotsearch/baidu"""
    return _call_hotsearch("baidu", appkey)


def douyin_hot(appkey: str):
    """抖音热搜 /hotsearch/douyin"""
    return _call_hotsearch("douyin", appkey)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\\n"
            "  hotsearch.py weibo   # 微博热搜\\n"
            "  hotsearch.py baidu   # 百度热搜\\n"
            "  hotsearch.py douyin  # 抖音热搜",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "weibo":
        result = weibo_hot(appkey)
    elif cmd == "baidu":
        result = baidu_hot(appkey)
    elif cmd == "douyin":
        result = douyin_hot(appkey)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

