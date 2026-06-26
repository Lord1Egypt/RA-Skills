#!/usr/bin/env python3
"""
Mobile empty-number detection skill for OpenClaw.
基于极速数据手机空号检测 API：
https://www.jisuapi.com/api/mobileempty/
"""

import sys
import json
import os
import requests


API_URL = "https://api.jisuapi.com/mobileempty/query"


def query_mobileempty(appkey: str, req: dict):
    """
    手机空号检测 /mobileempty/query

    请求 JSON 示例：
    {
        "mobiles": "18156080000,18156080001,18156080002"
    }
    """
    mobiles = req.get("mobiles")
    if not mobiles:
        return {"error": "missing_param", "message": "mobiles is required"}

    data = {
        "appkey": appkey,
        "mobiles": mobiles,
    }

    try:
        resp = requests.post(API_URL, data=data, timeout=15)
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


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  mobileempty.py '{\"mobiles\":\"18156080000,18156080001\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[1]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    result = query_mobileempty(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

