#!/usr/bin/env python3
"""
query parts refer pirce skill for OpenClaw.
积智数据 配件编码参考价格查询
"""

import sys
import json
import os
import requests
import re


PARTS_PRICE_REFER_URL = "https://erp.qipeidao.com/jzOpenClaw/getPriceRefer"

def query_price_refer(appkey: str, partsCodes: list, quality:str=None):
    """
    调用 /getPriceRefer 接口，按 配件编码 列表 查询 参考价格 信息。

    请求  示例：  '["1ZD807221GRU", "5LD807835BU34"]'  原厂
    """
    if not partsCodes:
        return {
            "error": "invalid_partsCodes",
            "msg": "partsCodes must be a list.",
        }
    params = {"apiKey": appkey,"partsOeList": partsCodes,"partsQuality": quality}
    try:
        resp = requests.post(PARTS_PRICE_REFER_URL, json=params, timeout=100)
    except Exception as e:
        return {
            "error": "request_failed",
            "msg": str(e),
        }

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "state": resp.status_code,
            "msg": resp.text,
        }

    data = json.loads(resp.text)
#     try:
#         data = resp.text.json()
#     except Exception:
#         return {
#             "error": "invalid_json",
#             "body": resp.text,
#         }
    return data;

def main():
    if len(sys.argv) < 1:
        print(
            "Usage: \n "
            "  get_parts_price4r.py  \"['1ZD807221GRU','5LD807835BU34']\"  原厂\n",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JZ_API_KEY")

    if not appkey:
        print("Error: JZ_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)


    # 默认：VIN 查询，参数为 JSON
    partsCodes = json.loads(sys.argv[1])
    quality = sys.argv[2]


    result = query_price_refer(appkey,partsCodes,quality)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

