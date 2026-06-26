#!/usr/bin/env python3
"""
快代理 - 查询账户余额

Usage:
    python check_balance.py
    python check_balance.py --secret-id YOUR_ID --signature YOUR_SIG
"""

import argparse
import os
import sys
import requests

# 账户余额API
BALANCE_API = "https://dev.kdlapi.com/api/getaccountbalance"


def check_balance(secret_id: str = None, signature: str = None):
    """
    查询账户余额

    Args:
        secret_id: API密钥ID (或从环境变量KUAIDAILI_SECRET_ID读取)
        signature: API签名 (或从环境变量KUAIDAILI_SIGNATURE读取)
    """
    # 从环境变量获取凭证
    secret_id = secret_id or os.environ.get("KUAIDAILI_SECRET_ID")
    signature = signature or os.environ.get("KUAIDAILI_SIGNATURE")

    if not secret_id or not signature:
        print("错误: 缺少API凭证", file=sys.stderr)
        print("请设置环境变量 KUAIDAILI_SECRET_ID 和 KUAIDAILI_SIGNATURE", file=sys.stderr)
        sys.exit(1)

    params = {"secret_id": secret_id, "signature": signature}

    try:
        resp = requests.get(BALANCE_API, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") == 0:
            balance = data.get("data", {})
            print(f"账户余额: ¥{balance.get('balance', 0)}")
            print(f"可用余额: ¥{balance.get('available_balance', 0)}")
            return balance
        else:
            print(f"API错误: {data.get('msg')}", file=sys.stderr)
            sys.exit(1)

    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询快代理账户余额")
    parser.add_argument("--secret-id", help="API密钥ID")
    parser.add_argument("--signature", help="API签名")

    args = parser.parse_args()
    check_balance(secret_id=args.secret_id, signature=args.signature)


if __name__ == "__main__":
    main()
