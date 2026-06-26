#!/usr/bin/env python3
"""
parts EPC skill for OpenClaw.
积智数据-根据VIN+PARTSNAME或VIN+PARTSCODE 获取EPC 图组
"""

import sys
import json
import os
import requests
import re


PARTS_EPC_URL = "https://erp.qipeidao.com/jzOpenClaw/getPartsEpcGroup"

def getPartsEpcGroup(appkey: str, vin: str,partsName: str, partsCode:str):
    """
    调用 /getPartsEpcGroup 接口，按 17 位 VIN 车架号的车型 与 待查询的配件名称或配件编码 查询这些配件所在的 EPC 图组。

    请求 JSON 示例： "LSVAL41Z882104202"   "前保险杠皮"  "1ZD807221GRU"

    """
    if not is_valid_vin(vin):
        return {
            "error": "invalid_vin",
            "msg": "VIN must be 17 characters long and contain only letters and numbers.",
        }
    if not partsName and not partsCode:
        return {
            "error": "invalid_partsNameOrCode",
            "msg": "partsName or partsCode must be a string.",
        }
    params = {"apiKey": appkey, "vinCode": vin, "partsNameForEpc": partsName, "partsOeForEpc": partsCode}
    try:
        resp = requests.post(PARTS_EPC_URL, json=params, timeout=100)
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
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  get_parts_epc.py 'LSVAL41Z882104202' '前保险杠皮' '1ZD807221GRU'    # 按 VIN+配件编码 或配件名称 查询这些配件所在的 EPC 图组\n",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JZ_API_KEY")

    if not appkey:
        print("Error: JZ_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)


    # 默认：VIN 查询，参数为 JSON
    vin = sys.argv[1]
    if not vin:
        print("Error: 'vin' is required.", file=sys.stderr)
        sys.exit(1)
    partsName = sys.argv[2]
    partsCode = sys.argv[3]
    result = getPartsEpcGroup(appkey,vin,partsName,partsCode)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

