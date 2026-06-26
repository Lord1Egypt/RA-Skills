#!/usr/bin/env python3
"""
News skill for OpenClaw.
基于极速数据新闻 API：
https://www.jisuapi.com/api/news/
"""

import sys
import json
import os
import requests


NEWS_GET_URL = "https://api.jisuapi.com/news/get"
NEWS_CHANNEL_URL = "https://api.jisuapi.com/news/channel"


def get_news(appkey: str, req: dict):
    """
    调用 /news/get 接口，获取指定频道的新闻列表。

    请求 JSON 示例：
    {
        "channel": "头条",
        "num": 10,
        "start": 0
    }
    """
    channel = req.get("channel")
    if not channel:
        return {"error": "missing_param", "message": "channel is required"}

    params = {
        "appkey": appkey,
        "channel": channel,
    }
    if "num" in req and req["num"] is not None:
        params["num"] = req["num"]
    if "start" in req and req["start"] is not None:
        params["start"] = req["start"]

    try:
        resp = requests.get(NEWS_GET_URL, params=params, timeout=10)
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

    return data.get("result", {})


def get_channels(appkey: str):
    """
    调用 /news/channel 接口，获取可用新闻频道列表。
    返回 result 数组，如 ["头条","新闻","财经",...]
    """
    params = {"appkey": appkey}

    try:
        resp = requests.get(NEWS_CHANNEL_URL, params=params, timeout=10)
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


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  news.py channels                                  # 获取新闻频道列表\n"
            "  news.py '{\"channel\":\"头条\",\"num\":10,\"start\":0}'  # 获取频道新闻",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    # 子命令：频道列表
    if sys.argv[1].lower() in ("channel", "channels"):
        result = get_channels(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 默认：获取新闻，参数为 JSON
    raw = sys.argv[1]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if "channel" not in req or not req["channel"]:
        print("Error: 'channel' is required in request JSON.", file=sys.stderr)
        sys.exit(1)

    result = get_news(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

