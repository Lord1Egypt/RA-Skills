#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import os
import requests

# 接口配置
API_URL = "http://apis.juhe.cn/ip/ipNewV3"

# 优先从环境变量读取 JUHE_API_KEY
API_KEY = os.getenv("JUHE_API_KEY", "").strip()

def check_key():
    if not API_KEY:
        print(json.dumps({"error": "JUHE_API_KEY 环境变量未配置"}, ensure_ascii=False))
        sys.exit(1)

def query_ip(ip):
    params = {
        "ip": ip,
        "key": API_KEY
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        resp = requests.get(API_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": f"请求异常: {str(e)}"}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python PythonApplication1.py 114.114.114.114"
        }, ensure_ascii=False))
        return

    ip = sys.argv[1]
    result = query_ip(ip)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    check_key()
    main()