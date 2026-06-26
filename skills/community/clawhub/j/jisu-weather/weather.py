#!/usr/bin/env python3
"""
Jisu Weather skill for OpenClaw.
基于极速数据全国天气预报 API：
https://www.jisuapi.com/api/weather/
"""

import sys
import json
import os
import requests


WEATHER_QUERY_URL = "https://api.jisuapi.com/weather/query"
WEATHER_CITY_URL = "https://api.jisuapi.com/weather/city"


def query_weather(appkey: str, req: dict):
    """
    调用 /weather/query 接口查询天气。

    请求 JSON 示例：
    {
        "city": "杭州",
        "cityid": 111,
        "citycode": "101260301",
        "location": "39.983424,116.322987",
        "ip": "8.8.8.8"
    }

    以上参数均为可选，但至少需要提供 city / cityid / citycode / location / ip 中的一个。
    """
    params = {
        "appkey": appkey,
    }

    # 这些字段官方都标记为可选
    for key in ("city", "cityid", "citycode", "location", "ip"):
        if key in req and req[key]:
            params[key] = req[key]

    try:
        resp = requests.get(WEATHER_QUERY_URL, params=params, timeout=10)
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

    # 直接返回 result，包含当前天气、指数、AQI、future daily / hourly 等
    return data.get("result", {})


def query_weather_cities(appkey: str):
    """
    调用 /weather/city 接口查询支持的城市列表。
    返回 result 数组，每项包含:
    { "cityid": "1", "parentid": "0", "citycode": "101010100", "city": "北京" }
    """
    params = {"appkey": appkey}

    try:
        resp = requests.get(WEATHER_CITY_URL, params=params, timeout=10)
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

    return data.get("result", [])


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  weather.py '{\"city\":\"杭州\"}'        # 查询指定城市天气\n"
            "  weather.py '{\"location\":\"39.9,116.3\"}'  # 按经纬度查询\n"
            "  weather.py cities                    # 获取支持的城市列表",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    # 子命令: 获取城市列表
    if sys.argv[1].lower() in ("city", "cities", "citylist"):
        result = query_weather_cities(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    raw = sys.argv[1]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    # 至少一个定位参数
    if not any(req.get(k) for k in ("city", "cityid", "citycode", "location", "ip")):
        print(
            "Error: at least one of city/cityid/citycode/location/ip "
            "must be provided in request JSON.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = query_weather(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

