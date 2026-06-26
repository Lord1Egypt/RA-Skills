#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KuaiDi100 Express Tracking Skill for OpenClaw
Uses KuaiDi100 API: https://www.kuaidi100.com/
"""

import sys
import json
import os
import hashlib
import requests

API_URL = "https://poll.kuaidi100.com/poll/query.do"
AUTO_URL = "https://poll.kuaidi100.com/poll/autonomous.do"

# 快递公司代码映射
COM_CODES = {
    "shunfeng": "顺丰速运",
    "yuantong": "圆通速递",
    "zhongtong": "中通快递",
    "yunda": "韵达快运",
    "shentong": "申通快递",
    "jtexpress": "极兔速递",
    "tiantian": "天天快递",
    "ems": "EMS",
    "youzhengguonei": "中国邮政",
    "debang": "德邦快递",
    "jd": "京东快递",
    "suning": "苏宁快递",
}

def query_express(key: str, customer: str, req: dict):
    """调用快递100查询接口"""
    number = req.get("number", "")
    com = req.get("com", "")
    phone = req.get("phone", "")

    param = {
        "com": com,
        "num": number,
        "phone": phone,
        "resultv2": "1",
        "show": "0",
        "order": "desc"
    }
    param_str = json.dumps(param)

    # 生成签名
    temp_sign = param_str + key + customer
    md = hashlib.md5()
    md.update(temp_sign.encode())
    sign = md.hexdigest().upper()

    request_data = {"customer": customer, "param": param_str, "sign": sign}

    try:
        resp = requests.post(API_URL, data=request_data, timeout=30)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

    if resp.status_code != 200:
        return {"error": "http_error", "status_code": resp.status_code, "body": resp.text}

    try:
        data = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}

    if data.get("message") != "ok":
        return {"error": "api_error", "message": data.get("message", "Unknown error")}

    return data

def auto_detect(key: str, customer: str, number: str):
    """自动识别快递公司"""
    param = {"num": number}
    try:
        resp = requests.post(AUTO_URL, data=param, timeout=10)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}
    
    if resp.status_code != 200:
        return {"error": "http_error", "status_code": resp.status_code, "body": resp.text}

    try:
        data = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}

    if data and len(data) > 0:
        return {"com": data[0].get("comCode", ""), "name": data[0].get("name", "")}
    return {"error": "detect_failed", "message": "Could not detect courier"}

def main():
    if len(sys.argv) < 2:
        print("Usage: kuaidi100.py '{\"number\":\"单号\",\"com\":\"jd\"}'", file=sys.stderr)
        sys.exit(1)

    key = os.getenv("KUAIDI100_KEY")
    customer = os.getenv("KUAIDI100_CUSTOMER")

    if not key or not customer:
        print("Error: KUAIDI100_KEY and KUAIDI100_CUSTOMER must be set.", file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]
    if arg.lower() == "companies":
        # 返回支持的快递公司列表
        ...

    req = json.loads(arg)
    number = req.get("number", "")
    com = req.get("com", "")

    if not com:
        detect_result = auto_detect(key, customer, number)
        com = detect_result.get("com", "")

    result = query_express(key, customer, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()