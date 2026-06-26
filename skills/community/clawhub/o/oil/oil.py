#!/usr/bin/env python3
"""
Oil price skill for OpenClaw.
基于极速数据今日油价 API：
https://www.jisuapi.com/api/oil/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/oil"


def _call_oil_api(path: str, appkey: str, params: dict = None):
    if params is None:
        params = {}
    all_params = {"appkey": appkey}
    all_params.update({k: v for k, v in params.items() if v not in (None, "")})
    url = f"{BASE_URL}/{path}"

    try:
        resp = requests.get(url, params=all_params, timeout=10)
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


def query(appkey: str, req: dict):
    """
    省市油价查询 /oil/query

    请求 JSON 示例：
    { "province": "河南" }
    """
    province = req.get("province")
    if not province:
        return {"error": "missing_param", "message": "province is required"}

    return _call_oil_api("query", appkey, {"province": province})


def province_list(appkey: str):
    """
    全部省市列表 /oil/province
    """
    return _call_oil_api("province", appkey, {})


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  oil.py query '{\"province\":\"河南\"}'   # 查询指定省份油价\n"
            "  oil.py province                        # 查询支持的全部省市列表",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "province":
        result = province_list(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if cmd != "query":
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2 + 1:
        print("Error: JSON body is required for 'query'.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[2]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    result = query(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

