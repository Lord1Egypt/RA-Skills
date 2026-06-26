#!/usr/bin/env python3
"""
Car catalog skill for OpenClaw.
基于极速数据车型大全 API：
https://www.jisuapi.com/api/car/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/car"


def _call_car_api(path: str, appkey: str, params: dict = None):
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


def brand(appkey: str):
    """
    获取所有品牌 /car/brand
    """
    return _call_car_api("brand", appkey, {})


def type_list(appkey: str, req: dict):
    """
    根据品牌获取车型 /car/type

    请求 JSON 示例：
    { "parentid": "1" }
    """
    parentid = req.get("parentid")
    if not parentid:
        return {"error": "missing_param", "message": "parentid is required"}
    return _call_car_api("type", appkey, {"parentid": parentid})


def car_series(appkey: str, req: dict):
    """
    根据车型获取车 /car/car

    请求 JSON 示例：
    {
        "parentid": "220",
        "sort": "",
        "isnev": ""
    }
    """
    parentid = req.get("parentid")
    if not parentid:
        return {"error": "missing_param", "message": "parentid is required"}

    params = {
        "parentid": parentid,
        "sort": req.get("sort"),
        "isnev": req.get("isnev"),
    }
    return _call_car_api("car", appkey, params)


def detail(appkey: str, req: dict):
    """
    根据 ID 获取车型详情 /car/detail

    请求 JSON 示例：
    { "carid": 2571 }
    """
    carid = req.get("carid")
    if carid in (None, ""):
        return {"error": "missing_param", "message": "carid is required"}

    return _call_car_api("detail", appkey, {"carid": carid})


def search(appkey: str, req: dict):
    """
    车型搜索 /car/search

    请求 JSON 示例：
    { "keyword": "奔驰E级2017款E200运动版" }
    """
    keyword = req.get("keyword")
    if not keyword:
        return {"error": "missing_param", "message": "keyword is required"}

    return _call_car_api("search", appkey, {"keyword": keyword})


def hot(appkey: str, req: dict):
    """
    获取热门车型 /car/hot

    请求 JSON 示例：
    { "pricetype": "2" }
    pricetype 可选：
      1: 5-8 万
      2: 8-15 万
      3: 15-20 万
      4: 20-30 万
      5: 30-50 万
    不传则返回 5-50 万的热门车型。
    """
    params = {}
    if "pricetype" in req and req["pricetype"] not in (None, ""):
        params["pricetype"] = req["pricetype"]
    return _call_car_api("hot", appkey, params)


def rank(appkey: str, req: dict):
    """
    获取销量排行榜 /car/rank

    请求 JSON 示例：
    {
        "ranktype": "1",
        "month": "2025-01",
        "week": ""
    }
    """
    ranktype = req.get("ranktype")
    if not ranktype:
        return {"error": "missing_param", "message": "ranktype is required"}

    params = {
        "ranktype": ranktype,
        "month": req.get("month"),
        "week": req.get("week"),
    }
    return _call_car_api("rank", appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  car.py brand                                      # 获取所有品牌\n"
            "  car.py type '{\"parentid\":\"1\"}'                 # 根据品牌获取车型\n"
            "  car.py car '{\"parentid\":\"220\"}'                 # 根据车型获取车款\n"
            "  car.py detail '{\"carid\":2571}'                   # 根据 ID 获取车型详情\n"
            "  car.py search '{\"keyword\":\"奔驰E级2017款E200运动版\"}'  # 车型搜索\n"
            "  car.py hot '{\"pricetype\":\"2\"}'                 # 热门车型\n"
            "  car.py rank '{\"ranktype\":\"1\",\"month\":\"2025-01\"}'  # 销量排行榜",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    # 无参数命令
    if cmd == "brand":
        result = brand(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if cmd not in ("type", "car", "detail", "search", "hot", "rank"):
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    # 其余命令需要 JSON
    if len(sys.argv) < 3:
        # hot / rank 等也统一要求 JSON，避免歧义
        print(f"Error: JSON body is required for '{cmd}'.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[2]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if cmd == "type":
        result = type_list(appkey, req)
    elif cmd == "car":
        result = car_series(appkey, req)
    elif cmd == "detail":
        result = detail(appkey, req)
    elif cmd == "search":
        result = search(appkey, req)
    elif cmd == "hot":
        result = hot(appkey, req)
    elif cmd == "rank":
        result = rank(appkey, req)
    else:
        print(f"Error: unhandled command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

