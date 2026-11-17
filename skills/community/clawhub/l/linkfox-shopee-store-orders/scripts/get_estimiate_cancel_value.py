#!/usr/bin/env python3
"""
Shopee Store — get_estimiate_cancel_value

官方: https://open.shopee.com/documents/v2/v2.order.get_estimiate_cancel_value?module=94&type=1

入参说明见 references/apis/get-estimiate-cancel-value.md。
"""

from __future__ import annotations

import json
import sys

from _order_api_runner import run_order_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_estimiate_cancel_value.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_order_api("get_estimiate_cancel_value", params, "get_estimiate_cancel_value.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
