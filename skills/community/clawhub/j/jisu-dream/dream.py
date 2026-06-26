#!/usr/bin/env python3
"""
Dream (Zhougong) skill for OpenClaw.
基于极速数据周公解梦 API：
https://www.jisuapi.com/api/dream/
"""

import sys
import json
import os
import requests


DREAM_SEARCH_URL = "https://api.jisuapi.com/dream/search"


def _call_dream_api(appkey: str, params: dict = None):
    query = {"appkey": appkey}
    if params:
        for k, v in params.items():
            if v not in (None, ""):
                query[k] = v

    try:
        resp = requests.get(DREAM_SEARCH_URL, params=query, timeout=10)
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


def dream_search(appkey: str, req: dict):
    """
    周公解梦搜索 /dream/search

    请求 JSON 示例：
    {
        "keyword": "鞋",
        "pagenum": 1,
        "pagesize": 10
    }
    """
    keyword = req.get("keyword")
    if not keyword:
        return {"error": "missing_param", "message": "keyword is required"}

    pagenum = req.get("pagenum", 1)
    pagesize = req.get("pagesize", 10)

    params = {
        "keyword": keyword,
        "pagenum": pagenum,
        "pagesize": pagesize,
    }
    return _call_dream_api(appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\\n"
            "  dream.py search '{\"keyword\":\"鞋\",\"pagenum\":1,\"pagesize\":10}'  # 周公解梦搜索",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd != "search":
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Error: JSON body is required.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[2]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(req, dict):
        print("Error: JSON body must be an object.", file=sys.stderr)
        sys.exit(1)

    result = dream_search(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

