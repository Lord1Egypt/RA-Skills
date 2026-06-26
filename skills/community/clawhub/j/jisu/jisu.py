#!/usr/bin/env python3
"""
极速数据统一入口 skill for OpenClaw.
一个 JISU_API_KEY 调用多类接口：黄金、股票、天气、菜谱、汇率、MBTI、快递等。
API 文档：https://www.jisuapi.com/
"""

import json
import os
import re
import sys
from typing import Any

import requests


BASE_URL = "https://api.jisuapi.com"


# 支持的接口清单（用于 list 命令），api 为请求路径，与官网一致
API_LIST = [
    {"api": "gold/shgold", "desc": "上海黄金交易所价格"},
    {"api": "gold/shfutures", "desc": "上海期货交易所价格"},
    {"api": "gold/hkgold", "desc": "香港金银业贸易场价格"},
    {"api": "gold/bank", "desc": "银行账户黄金价格"},
    {"api": "gold/london", "desc": "伦敦金、银价格"},
    {"api": "gold/storegold", "desc": "金店金价，params 可选 date"},
    {"api": "stock/query", "desc": "股票当日行情（分钟粒度），params: code"},
    {"api": "stock/list", "desc": "股票列表，params: classid(1沪深3港股4北证), pagenum, pagesize"},
    {"api": "stock/detail", "desc": "股票详情，params: code"},
    {"api": "stockhistory/query", "desc": "股票历史行情，params: code, startdate, enddate"},
    {"api": "stockhistory/list", "desc": "股票历史列表，params: classid, pagenum, pagesize"},
    {"api": "stockhistory/detail", "desc": "股票历史详情，params: code"},
    {"api": "stockindex/sh", "desc": "上证/深证/创业板等指数行情"},
    {"api": "weather/query", "desc": "天气预报，params: city 或 cityid/citycode/location/ip"},
    {"api": "weather/city", "desc": "天气支持城市列表"},
    {"api": "recipe/search", "desc": "菜谱搜索，params: keyword, num, start"},
    {"api": "recipe/class", "desc": "菜谱分类"},
    {"api": "recipe/byclass", "desc": "按分类检索菜谱，params: classid, start, num"},
    {"api": "recipe/detail", "desc": "菜谱详情，params: id"},
    {"api": "character/questions", "desc": "MBTI 题目，params 可选 version(full/simple)"},
    {"api": "character/answer", "desc": "MBTI 提交答案，params: answer, version 可选"},
    {"api": "exchange/convert", "desc": "汇率换算，params: from, to, amount"},
    {"api": "exchange/single", "desc": "单货币汇率，params: currency"},
    {"api": "exchange/currency", "desc": "支持的货币列表"},
    {"api": "exchange/bank", "desc": "银行汇率，params 可选 bank"},
    {"api": "ip/location", "desc": "IP 归属地，params: ip"},
    {"api": "shouji/query", "desc": "手机归属地，params: shouji"},
    {"api": "idcard/query", "desc": "身份证查询，params: idcard"},
    {"api": "bankcard/query", "desc": "银行卡归属地，params: bankcard"},
    {"api": "express/query", "desc": "快递查询，params: type, number"},
    {"api": "express/type", "desc": "快递公司类型列表"},
    {"api": "car/brand", "desc": "汽车品牌列表"},
    {"api": "car/type", "desc": "车型，params: parentid"},
    {"api": "car/car", "desc": "车款，params: parentid"},
    {"api": "car/detail", "desc": "车型详情，params: carid"},
    {"api": "car/search", "desc": "车型搜索，params: keyword"},
    {"api": "car/hot", "desc": "热门车型，params 可选 pricetype"},
    {"api": "car/rank", "desc": "销量排行，params: ranktype, month 等"},
    {"api": "vehiclelimit/city", "desc": "限行城市列表"},
    {"api": "vehiclelimit/query", "desc": "限行查询，params: city, date 等"},
    {"api": "vin/query", "desc": "VIN 车辆信息，params: vin"},
    {"api": "vinrecognition/recognize", "desc": "VIN 车架号图像识别，params: pic(base64)"},
    {"api": "oil/query", "desc": "省市油价查询，params 可选 province"},
    {"api": "oil/province", "desc": "油价支持省市列表"},
    {"api": "silver/shgold", "desc": "上海黄金交易所白银价格"},
    {"api": "silver/shfutures", "desc": "上海期货交易所白银价格"},
    {"api": "silver/london", "desc": "伦敦银价格"},
    {"api": "calendar/query", "desc": "万年历，params: date"},
    {"api": "calendar/holiday", "desc": "节假日，params: date"},
    {"api": "huangli/date", "desc": "黄历，params: date"},
    {"api": "news/get", "desc": "新闻，params: channel, start, num"},
    {"api": "news/channel", "desc": "新闻频道"},
    {"api": "geoconvert/coord2addr", "desc": "坐标转地址，params: lat, lng"},
    {"api": "geoconvert/addr2coord", "desc": "地址转坐标，params: address"},
    {"api": "dream/search", "desc": "周公解梦搜索，params: keyword, pagenum, pagesize"},
    {"api": "hotsearch/weibo", "desc": "微博热搜榜"},
    {"api": "hotsearch/baidu", "desc": "百度热搜榜"},
    {"api": "hotsearch/douyin", "desc": "抖音热搜榜"},
    {"api": "futures/shfutures", "desc": "上海期货交易所期货价格"},
    {"api": "futures/dlfutures", "desc": "大连商品交易所期货价格"},
    {"api": "futures/zzfutures", "desc": "郑州商品交易所期货价格"},
    {"api": "futures/zgjrfutures", "desc": "中国金融期货交易所期货价格"},
    {"api": "futures/gzfutures", "desc": "广州期货交易所期货价格"},
    {"api": "todayhistory/query", "desc": "历史上的今天，params: month, day"},
    {"api": "weather2/query", "desc": "历史天气查询，params: date 必填，city 或 cityid 可选"},
    {"api": "weather2/city", "desc": "历史天气支持城市列表"},
    {"api": "enterprisecontact/query", "desc": "企业联系方式查询，params: company/creditno/regno/orgno 任填其一"},
    {"api": "qrcode/generate", "desc": "二维码生成，params: text, bgcolor, fgcolor, oxlevel, width, margin, logo, tempid"},
    {"api": "qrcode/read", "desc": "二维码识别，params: qrcode(URL 或 base64)"},
    {"api": "qrcode/template", "desc": "二维码模板样例列表"},
    {"api": "barcode/generate", "desc": "条码生成，params: type, barcode, fontsize, dpi, scale, height"},
    {"api": "barcode/read", "desc": "条码识别，params: barcode(URL 或 base64)"},
    {"api": "barcode2/query", "desc": "商品条码查询，params: barcode"},
    {"api": "generalrecognition/recognize", "desc": "通用文字识别 OCR，params: pic(base64)、type(cnen/en/fr/pt/de/it/es/ru/jp)"},
    {"api": "idcardrecognition/type", "desc": "身份证识别支持的证件类型列表"},
    {"api": "idcardrecognition/recognize", "desc": "身份证等证件 OCR 识别，params: typeid, pic(base64)"},
    {"api": "bankcardcognition/recognize", "desc": "银行卡 OCR 识别，params: pic(base64)"},
]


ALLOWED_APIS = {item["api"] for item in API_LIST}


def _normalize_and_validate_api_path(api_path: str) -> str:
    """
    对 API 路径做严格校验并限制在白名单内，避免 URL 注入/越权调用：
    - 仅允许字母、数字、下划线、斜杠、点（点会被转换为斜杠）
    - 禁止出现 @、?、#、:、\\ 等可导致 URL 语义变化的字符
    - 禁止以 / 开头、禁止空段、禁止 . / .. 路径段
    - 仅允许调用 API_LIST 中声明的接口
    """
    s = (api_path or "").strip()
    if not s:
        raise ValueError("api is required")

    if re.search(r"[@?:#\\]", s):
        raise ValueError("api contains forbidden characters")

    if not re.fullmatch(r"[A-Za-z0-9_./]+", s):
        raise ValueError("api contains invalid characters")

    s = s.replace(".", "/")
    if s.startswith("/"):
        raise ValueError("api must be relative path")

    parts = s.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise ValueError("api path is invalid")

    if s not in ALLOWED_APIS:
        raise ValueError("api is not in allowed list")

    return s


def _call_jisu_api(api_path: str, appkey: str, params: dict = None) -> Any:
    """
    统一调用：https://api.jisuapi.com/{api_path}
    - 大部分接口使用 GET；
    - 部分识别类接口（vinrecognition/generalrecognition/idcardrecognition/bankcardcognition）
      官方文档推荐使用 POST，这里自动切换为 POST，并将参数放在表单中。
    """
    try:
        api_path = _normalize_and_validate_api_path(api_path)
    except ValueError as e:
        return {"error": "invalid_api", "message": str(e)}

    url = f"{BASE_URL}/{api_path}"
    all_params = {"appkey": appkey}
    if params:
        for k, v in params.items():
            if v not in (None, ""):
                all_params[k] = v

    # 需要用 POST 的识别类接口
    post_apis = {
        "vinrecognition/recognize",
        "generalrecognition/recognize",
        "idcardrecognition/recognize",
        "bankcardcognition/recognize",
    }

    try:
        if api_path in post_apis:
            # 识别类接口按文档使用 POST，参数放在表单中
            resp = requests.post(url, data=all_params, timeout=15)
        else:
            resp = requests.get(url, params=all_params, timeout=15)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}
    if resp.status_code != 200:
        return {"error": "http_error", "status_code": resp.status_code, "body": resp.text}
    try:
        data = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}
    if data.get("status") != 0:
        return {"error": "api_error", "code": data.get("status"), "message": data.get("msg")}
    return data.get("result")


def cmd_call(appkey: str, req: dict) -> Any:
    """统一调用：req.api 为接口路径，req.params 为请求参数。"""
    api = req.get("api")
    if not api:
        return {"error": "missing_param", "message": "api is required"}
    params = req.get("params")
    if params is not None and not isinstance(params, dict):
        return {"error": "invalid_param", "message": "params must be an object"}
    return _call_jisu_api(api, appkey, params or {})


def cmd_list(_appkey: str, _req: dict) -> Any:
    """返回支持的接口列表。"""
    return {"apis": API_LIST, "doc": "https://www.jisuapi.com/"}


def _read_json_arg() -> dict:
    if len(sys.argv) < 3 or not sys.argv[2].strip():
        return {}
    raw = sys.argv[2]
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(obj, dict):
        print("Error: JSON body must be an object.", file=sys.stderr)
        sys.exit(1)
    return obj


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  jisu.py list                              # 列出支持的接口\n"
            "  jisu.py call '{\"api\":\"gold/shgold\"}'              # 无参接口\n"
            "  jisu.py call '{\"api\":\"stock/query\",\"params\":{\"code\":\"300917\"}}'  # 带参接口",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()
    req = _read_json_arg()

    if cmd == "list":
        result = cmd_list(appkey, req)
    elif cmd == "call":
        result = cmd_call(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
