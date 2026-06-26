#!/usr/bin/env python3
"""
Invoice verify skill for OpenClaw.
基于极速数据发票查验 API：
https://www.jisuapi.com/api/invoiceverify/
"""

import sys
import json
import os
import requests


INVOICE_VERIFY_URL = "https://api.jisuapi.com/invoiceverify/verify"
INVOICE_TYPE_URL = "https://api.jisuapi.com/invoiceverify/type"


def verify_invoice(appkey: str, req: dict):
    """
    查询发票信息 /invoiceverify/verify

    请求 JSON 示例：
    {
        "code": "033001800311",
        "number": "61124608",
        "date": "2019-06-15",
        "extaxtotalfee": "2388.46",
        "totalfee": "",
        "checkcode": "62057237940487749830",
        "sellercreditno": ""
    }

    参数说明：
    - code: 发票代码（可选）
    - number: 发票号码（必填）
    - date: 开票日期（必填，格式：YYYY-MM-DD）
    - extaxtotalfee/totalfee: 合计金额或价税合计，二选一
    - checkcode: 校验码（部分场景必填）
    - sellercreditno: 销方税号（区块链发票必填）
    """
    params = {"appkey": appkey}

    number = req.get("number")
    date = req.get("date")
    if not number:
        return {"error": "missing_param", "message": "number is required"}
    if not date:
        return {"error": "missing_param", "message": "date is required"}

    # 基本必填
    params["number"] = number
    params["date"] = date

    # 可选参数
    for key in ("code", "extaxtotalfee", "totalfee", "checkcode", "sellercreditno"):
        value = req.get(key)
        if value not in (None, ""):
            params[key] = value

    try:
        resp = requests.get(INVOICE_VERIFY_URL, params=params, timeout=10)
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


def get_invoice_types(appkey: str):
    """
    获取发票类型列表 /invoiceverify/type
    返回数组，每项包含:
    { "type": "01", "name": "增值税专用发票" }
    """
    params = {"appkey": appkey}

    try:
        resp = requests.get(INVOICE_TYPE_URL, params=params, timeout=10)
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

    return data.get("result", [])


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  invoiceverify.py verify '{\"number\":\"61124608\",\"date\":\"2019-06-15\"}'  # 发票查验\n"
            "  invoiceverify.py type                                                      # 获取发票类型列表",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "type":
        result = get_invoice_types(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if cmd == "verify":
        if len(sys.argv) < 3:
            print("Error: JSON body is required for 'verify'.", file=sys.stderr)
            sys.exit(1)
        raw = sys.argv[2]
        try:
            req = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)

        if "number" not in req or not req["number"]:
            print("Error: 'number' is required in request JSON.", file=sys.stderr)
            sys.exit(1)
        if "date" not in req or not req["date"]:
            print("Error: 'date' is required in request JSON.", file=sys.stderr)
            sys.exit(1)

        result = verify_invoice(appkey, req)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"Error: unknown command '{cmd}'", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()

