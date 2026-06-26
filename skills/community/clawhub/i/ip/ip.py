#!/usr/bin/env python3
"""
IP location skill for OpenClaw.
基于极速数据 IP 查询 API：
https://www.jisuapi.com/api/ip/
"""

import sys
import json
import os
import requests


IP_LOCATION_URL = "https://api.jisuapi.com/ip/location"


def query_ip_location(appkey: str, req: dict):
    """
    调用 /ip/location 接口，根据 IP 查询归属地与运营商类型。

    请求 JSON 示例：
    {
        "ip": "122.224.186.100"
    }
    """
    params = {"appkey": appkey}

    ip = req.get("ip")
    if not ip:
        return {
            "error": "missing_param",
            "message": "ip is required",
        }
    params["ip"] = ip

    try:
        resp = requests.get(IP_LOCATION_URL, params=params, timeout=10)
    except Exception as e:
        return {
            "error": "request_failed",
            "message": str(e),
        }

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {
            "error": "invalid_json",
            "body": resp.text,
        }

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
            "  ip.py '{\"ip\":\"122.224.186.100\"}'  # 查询 IP 归属地与运营商",
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

    if "ip" not in req or not req["ip"]:
        print("Error: 'ip' is required in request JSON.", file=sys.stderr)
        sys.exit(1)

    result = query_ip_location(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

