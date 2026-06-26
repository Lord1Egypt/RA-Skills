#!/usr/bin/env python3
"""
Stock query skill for OpenClaw.
基于极速数据股票查询 API：
https://www.jisuapi.com/api/stock/
"""

import sys
import json
import os
from typing import Any, Dict
import requests


BASE_URL = "https://api.jisuapi.com/stock"


def _call_stock_api(path: str, appkey: str, params: Dict[str, Any]):
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

    return data.get("result")


def query(appkey: str, req: dict):
    """
    股票查询 /stock/query
    根据股票代码查询当日行情，数据粒度为分钟。返回 name、code、price、lastclosingprice、trendnum、updatetime、trend 等。
    请求 JSON：{ "code": "300917" }
    """
    code = req.get("code")
    if not code:
        return {"error": "missing_param", "message": "code is required"}
    return _call_stock_api("query", appkey, {"code": str(code).strip()})


def list_stock(appkey: str, req: dict):
    """
    股票列表查询 /stock/list
    classid: 1 沪深股市 3 港股 4 北证A股；可选 pagenum、pagesize。
    请求 JSON：{ "classid": 1, "pagenum": 1, "pagesize": 10 }
    """
    classid = req.get("classid")
    if classid is None:
        return {"error": "missing_param", "message": "classid is required"}
    params = {"classid": classid}
    if "pagenum" in req and req["pagenum"] is not None:
        params["pagenum"] = req["pagenum"]
    if "pagesize" in req and req["pagesize"] is not None:
        params["pagesize"] = req["pagesize"]
    return _call_stock_api("list", appkey, params)


def detail(appkey: str, req: dict):
    """
    股票详情查询 /stock/detail
    根据股票代码获取详情：最新价、最高/最低、成交量、成交额、换手率、涨跌幅、市盈率、市净率等。
    请求 JSON：{ "code": "300917" }
    """
    code = req.get("code")
    if not code:
        return {"error": "missing_param", "message": "code is required"}
    return _call_stock_api("detail", appkey, {"code": str(code).strip()})


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  stock.py query '{\"code\":\"300917\"}'              # 当日行情（含分钟趋势）\n"
            "  stock.py list '{\"classid\":1,\"pagenum\":1,\"pagesize\":10}'  # 股票列表\n"
            "  stock.py detail '{\"code\":\"300917\"}'              # 股票详情",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()
    req = {}
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        try:
            req = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(req, dict):
            req = {}

    if cmd == "query":
        result = query(appkey, req)
    elif cmd == "list":
        result = list_stock(appkey, req)
    elif cmd == "detail":
        result = detail(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
