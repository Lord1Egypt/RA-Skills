#!/usr/bin/env python3
"""
Shopee Store — delete_discount_item

官方: https://open.shopee.com/documents/v2/v2.discount.delete_discount_item?module=99&type=1

入参说明见 references/apis/delete-discount-item.md。
"""

from __future__ import annotations

import json
import sys

from _discount_api_runner import run_discount_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: delete_discount_item.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_discount_api("delete_discount_item", params, "delete_discount_item.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
