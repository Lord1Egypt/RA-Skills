#!/usr/bin/env python3
"""
Gold price skill for OpenClaw.
基于极速数据黄金价格 API：
https://www.jisuapi.com/api/gold/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/gold"


def _call_gold_api(path: str, appkey: str, params: dict = None):
    if params is None:
        params = {}
    all_params = {"appkey": appkey}
    all_params.update(params)

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


def shgold(appkey: str):
    """上海黄金交易所价格 /gold/shgold"""
    return _call_gold_api("shgold", appkey)


def shfutures(appkey: str):
    """上海期货交易所价格 /gold/shfutures"""
    return _call_gold_api("shfutures", appkey)


def hkgold(appkey: str):
    """香港金银业贸易场价格 /gold/hkgold"""
    return _call_gold_api("hkgold", appkey)


def bank_gold(appkey: str):
    """银行账户黄金价格 /gold/bank"""
    return _call_gold_api("bank", appkey)


def london_gold(appkey: str):
    """伦敦金、银价格 /gold/london"""
    return _call_gold_api("london", appkey)


def store_gold(appkey: str, req: dict):
    """
    金店金价 /gold/storegold

    请求 JSON 示例：
    {
        "date": "2023-09-20"   # 可选，仅支持最近 7 天，不填则默认当天
    }
    """
    params: dict = {}
    date = req.get("date")
    if date:
        params["date"] = date
    return _call_gold_api("storegold", appkey, params)


def gold_history(appkey: str, req: dict):
    """
    黄金历史行情 /gold/history

    请求 JSON 示例：
    {
        "market": "london",
        "startdate": "2026-06-01",
        "enddate": "2026-06-10",
        "type": "xau"
    }

    market: london（伦敦）| ny（纽约）| td（TD）| futures（期货）
    type: 品种代码，如 xau、xag、gc 等
    """
    for field in ("market", "startdate", "enddate", "type"):
        if not req.get(field):
            return {"error": "missing_param", "message": f"{field} is required"}
    params = {
        "market": req["market"],
        "startdate": req["startdate"],
        "enddate": req["enddate"],
        "type": req["type"],
    }
    return _call_gold_api("history", appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  gold.py shgold                        # 上海黄金交易所价格\n"
            "  gold.py shfutures                     # 上海期货交易所价格\n"
            "  gold.py hkgold                        # 香港金银业贸易场价格\n"
            "  gold.py bank                          # 银行账户黄金价格\n"
            "  gold.py london                        # 伦敦金、银价格\n"
            "  gold.py storegold '{\"date\":\"2023-09-20\"}'  # 金店金价（可选 date）\n"
            "  gold.py history '{\"market\":\"london\",\"startdate\":\"2026-06-01\",\"enddate\":\"2026-06-10\",\"type\":\"xau\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "shgold":
        result = shgold(appkey)
    elif cmd == "shfutures":
        result = shfutures(appkey)
    elif cmd == "hkgold":
        result = hkgold(appkey)
    elif cmd == "bank":
        result = bank_gold(appkey)
    elif cmd == "london":
        result = london_gold(appkey)
    elif cmd == "storegold":
        if len(sys.argv) >= 3:
            raw = sys.argv[2]
            try:
                req = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            req = {}
        result = store_gold(appkey, req)
    elif cmd == "history":
        if len(sys.argv) < 3:
            print("Error: JSON request body is required for 'history'.", file=sys.stderr)
            sys.exit(1)
        try:
            req = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        result = gold_history(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

