#!/usr/bin/env python3
"""
payment_api.py - 调用收款码 API 获取 tradeCode

用法：
    python payment_api.py --amount 50 [--order_type tip] [--payee "主播小明"] [--description "打赏主播小明50元"]

输出（成功）：
    SUCCESS
    tradeCode=62254562871846512
    tradeLink=https://pay-h5.4199191.xyz/pyment/62254562871846512

输出（失败）：
    FAIL
    message=错误原因描述
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

API_URL = "https://pay.4199191.xyz/code"
TIMEOUT = 30


def main():
    parser = argparse.ArgumentParser(description="调用收款码 API")
    parser.add_argument("--amount", type=float, default=None)
    parser.add_argument("--order_type", type=str, default=None)
    parser.add_argument("--payee", type=str, default=None)
    parser.add_argument("--description", type=str, default=None)
    args = parser.parse_args()

    payload = {}
    if args.amount is not None:
        payload["amount"] = args.amount
    if args.order_type is not None:
        payload["order_type"] = args.order_type
    if args.payee is not None:
        payload["payee"] = args.payee
    if args.description is not None:
        payload["description"] = args.description

    try:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            API_URL,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        try:
            raw = e.read().decode("utf-8")
        except Exception:
            print("FAIL")
            print("message=支付服务请求失败，请稍后重试")
            sys.exit(1)
    except urllib.error.URLError as e:
        print("FAIL")
        print("message=网络连接失败，请检查网络后重试")
        sys.exit(1)
    except TimeoutError:
        print("FAIL")
        print("message=请求超时，请稍后重试")
        sys.exit(1)
    except Exception:
        print("FAIL")
        print("message=支付服务暂时不可用，请稍后重试")
        sys.exit(1)

    try:
        result = json.loads(raw)
    except Exception:
        print("FAIL")
        print("message=响应解析失败，请稍后重试")
        sys.exit(1)

    result_code = result.get("resultCode")
    if result_code == 1:
        data = result.get("data", {})
        trade_code = data.get("tradeCode", "")
        trade_link = data.get("tradeLink", "")
        print("SUCCESS")
        print(f"tradeCode={trade_code}")
        print(f"tradeLink={trade_link}")
        sys.exit(0)
    else:
        message = result.get("message", "未知错误")
        print("FAIL")
        print(f"message={message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
