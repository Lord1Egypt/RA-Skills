#!/usr/bin/env python3
"""
Jisu QR code generate & read skill for OpenClaw.
基于极速数据二维码生成识别 API：
https://www.jisuapi.com/api/qrcode/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/qrcode"


def _call_api(path: str, appkey: str, params: dict = None):
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

    return data.get("result")


def cmd_generate(appkey: str, req: dict):
    """
    二维码生成 /qrcode/generate

    请求 JSON 示例：
    {
        "text": "https://www.jisuapi.com/api/sms",
        "width": 300,
        "tempid": 1,
        "margin": 10,
        "bgcolor": "FFFFFF",
        "fgcolor": "000000",
        "oxlevel": "L",
        "logo": "https://www.jisuapi.com/static/images/icon/qrcode.png"
    }
    """
    text = req.get("text")
    if not text:
        return {"error": "missing_param", "message": "text is required"}

    params = {
        "text": text,
        "bgcolor": req.get("bgcolor"),
        "fgcolor": req.get("fgcolor"),
        "oxlevel": req.get("oxlevel"),
        "width": req.get("width"),
        "margin": req.get("margin"),
        "logo": req.get("logo"),
        "tempid": req.get("tempid"),
    }
    return _call_api("generate", appkey, params)


def cmd_read(appkey: str, req: dict):
    """
    二维码识别 /qrcode/read

    请求 JSON 示例：
    {
        "qrcode": "https://api.jisuapi.com/qrcode/static/images/sample/1.png"
    }
    或 qrcode 为 base64 图片内容。
    """
    qrcode_val = req.get("qrcode")
    if not qrcode_val:
        return {"error": "missing_param", "message": "qrcode is required (URL or base64 string)"}

    params = {"qrcode": qrcode_val}
    return _call_api("read", appkey, params)


def cmd_template(appkey: str, _req: dict):
    """
    获取二维码模板样例 /qrcode/template
    """
    return _call_api("template", appkey, {})


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  qrcode.py generate '{\"text\":\"https://www.jisuapi.com/api/sms\",\"width\":300}'  # 生成二维码\n"
            "  qrcode.py read '{\"qrcode\":\"https://api.jisuapi.com/qrcode/static/images/sample/1.png\"}'  # 识别二维码\n"
            "  qrcode.py template '{}'  # 获取模板样例列表",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()

    req: dict = {}
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        raw = sys.argv[2]
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(obj, dict):
            print("Error: JSON body must be an object.", file=sys.stderr)
            sys.exit(1)
        req = obj

    if cmd == "generate":
        result = cmd_generate(appkey, req)
    elif cmd == "read":
        result = cmd_read(appkey, req)
    elif cmd == "template":
        result = cmd_template(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

