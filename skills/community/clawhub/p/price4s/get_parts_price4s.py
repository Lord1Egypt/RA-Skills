#!/usr/bin/env python3
"""
query parts 4S pirce skill for OpenClaw.
积智数据 配件 4S价查询
"""

import sys
import json
import os
import requests
import re


PARTS_PRICE4S_URL = "https://erp.qipeidao.com/jzOpenClaw/getPrice4s"

def query_price_4s(appkey: str, vin: str, partsCodes: list):
    """
    调用 /getPrice4s 接口，按 配件编码 列表 查询 4S价 信息。

    请求  示例： "LSVAL41Z882104202"  '["1ZD807221GRU", "5LD807835BU34"]'
    """
    if not partsCodes:
        return {
            "error": "invalid_partsCodes",
            "msg": "partsCodes must be a list.",
        }
    params = {"apiKey": appkey,"vinCode": vin, "partsOeList": partsCodes}
    try:
        resp = requests.post(PARTS_PRICE4S_URL, json=params, timeout=100)
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
def is_valid_vin(vin):
    return len(vin) == 17 and re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin)

def main():
    if len(sys.argv) < 1:
        print(
            "Usage: \n "
            "  get_parts_price4s.py  LSVAL41Z882104202  \"['1ZD807221GRU','5LD807835BU34']\"  \n",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JZ_API_KEY")

    if not appkey:
        print("Error: JZ_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)


    # 默认：VIN 查询，参数为 JSON
    vin = sys.argv[1]
    partsCodes = json.loads(sys.argv[2])


    result = query_price_4s(appkey,vin,partsCodes)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

