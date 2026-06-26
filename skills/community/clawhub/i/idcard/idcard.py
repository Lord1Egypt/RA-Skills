#!/usr/bin/env python3
"""
ID card attribution skill for OpenClaw.
基于极速数据身份证号码归属地查询 API：
https://www.jisuapi.com/api/idcard
"""

import sys
import json
import os
import requests


IDCARD_QUERY_URL = "https://api.jisuapi.com/idcard/query"
CITY2CODE_URL = "https://api.jisuapi.com/idcard/city2code"


def query_idcard(appkey: str, req: dict):
    """
    身份证查询 /idcard/query

    请求 JSON 示例：
    {
        "idcard": "41272519800102067x"
    }
    """
    idcard = req.get("idcard")
    if not idcard:
        return {"error": "missing_param", "message": "idcard is required"}

    params = {
        "appkey": appkey,
        "idcard": idcard,
    }

    try:
        resp = requests.get(IDCARD_QUERY_URL, params=params, timeout=10)
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


def city2code(appkey: str, req: dict):
    """
    城市查身份证前6位 /idcard/city2code

    请求 JSON 示例：
    {
        "city": "鹿邑"
    }
    """
    city = req.get("city")
    if not city:
        return {"error": "missing_param", "message": "city is required"}

    params = {
        "appkey": appkey,
        "city": city,
    }

    try:
        resp = requests.get(CITY2CODE_URL, params=params, timeout=10)
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
            "  idcard.py query    '{\"idcard\":\"41272519800102067x\"}'\n"
            "  idcard.py city2code '{\"city\":\"鹿邑\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd not in ("query", "city2code"):
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 3:
        print(f"Error: JSON body is required for '{cmd}'.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[2]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if cmd == "query":
        result = query_idcard(appkey, req)
    else:
        result = city2code(appkey, req)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

