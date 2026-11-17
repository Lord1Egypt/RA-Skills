#!/usr/bin/env python3
"""
Shopee Store — get_payment_method_list

官方: https://open.shopee.com/documents/v2/v2.payment.get_payment_method_list?module=97&type=1

入参说明见 references/apis/get-payment-method-list.md。
"""

from __future__ import annotations

import json
import sys

from _payment_api_runner import run_payment_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_payment_method_list.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_payment_api("get_payment_method_list", params, "get_payment_method_list.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
