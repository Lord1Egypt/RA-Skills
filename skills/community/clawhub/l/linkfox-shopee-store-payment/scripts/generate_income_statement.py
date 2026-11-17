#!/usr/bin/env python3
"""
Shopee Store — generate_income_statement

官方: https://open.shopee.com/documents/v2/v2.payment.generate_income_statement?module=97&type=1

入参说明见 references/apis/generate-income-statement.md。
"""

from __future__ import annotations

import json
import sys

from _payment_api_runner import run_payment_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: generate_income_statement.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_payment_api("generate_income_statement", params, "generate_income_statement.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
