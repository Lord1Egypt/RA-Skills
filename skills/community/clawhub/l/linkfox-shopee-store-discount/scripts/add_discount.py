#!/usr/bin/env python3
"""
Shopee Store — add_discount

官方: https://open.shopee.com/documents/v2/v2.discount.add_discount?module=99&type=1

入参说明见 references/apis/add-discount.md。
"""

from __future__ import annotations

import json
import sys

from _discount_api_runner import run_discount_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: add_discount.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_discount_api("add_discount", params, "add_discount.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
