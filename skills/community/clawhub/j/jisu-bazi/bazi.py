#!/usr/bin/env python3
"""
Bazi (Four Pillars) paipan skill for OpenClaw.
基于极速数据八字排盘 API：
https://www.jisuapi.com/api/bazi
"""

import sys
import json
import os
import requests


PAIPAN_URL = "https://api.jisuapi.com/bazi/paipan"


def paipan(appkey: str, req: dict):
    """
    八字排盘 /bazi/paipan

    请求 JSON 示例：
    {
        "name": "张三",
        "city": "杭州",
        "year": 2009,
        "month": 10,
        "day": 18,
        "hour": 2,
        "minute": 5,
        "sex": 1,
        "islunar": 0,
        "istaiyang": 0,
        "islunarmonth": 2
    }
    """
    name = req.get("name")
    city = req.get("city", "")
    year = req.get("year")
    month = req.get("month")
    day = req.get("day")
    hour = req.get("hour")
    minute = req.get("minute")
    sex = req.get("sex")

    missing = []
    if not name:
        missing.append("name")
    if year is None:
        missing.append("year")
    if month is None:
        missing.append("month")
    if day is None:
        missing.append("day")
    if hour is None:
        missing.append("hour")
    if minute is None:
        missing.append("minute")
    if sex is None:
        missing.append("sex")

    if missing:
        return {
            "error": "missing_param",
            "message": f"Missing required fields: {', '.join(missing)}",
        }

    data = {
        "appkey": appkey,
        "name": name,
        "city": city,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "sex": sex,
        "islunar": req.get("islunar", 0),
        "istaiyang": req.get("istaiyang", 0),
        "islunarmonth": req.get("islunarmonth", 2),
    }

    try:
        resp = requests.get(PAIPAN_URL, params=data, timeout=15)
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
            "  bazi.py '{\"name\":\"张三\",\"city\":\"杭州\",\"year\":2009,\"month\":10,\"day\":18,\"hour\":2,\"minute\":5,\"sex\":1,\"islunar\":0,\"istaiyang\":0}'",
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

    result = paipan(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

