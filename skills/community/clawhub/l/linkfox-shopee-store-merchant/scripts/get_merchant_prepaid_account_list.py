#!/usr/bin/env python3
"""
Shopee Store — get_merchant_prepaid_account_list

官方: https://open.shopee.com/documents/v2/v2.merchant.get_merchant_prepaid_account_list?module=93&type=1

入参说明见 references/apis/get-merchant-prepaid-account-list.md。
"""

from __future__ import annotations

import json
import sys

from _merchant_api_runner import run_merchant_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_merchant_prepaid_account_list.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_merchant_api("get_merchant_prepaid_account_list", params, "get_merchant_prepaid_account_list.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
