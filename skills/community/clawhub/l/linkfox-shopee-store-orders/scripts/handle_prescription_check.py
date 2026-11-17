#!/usr/bin/env python3
"""
Shopee Store — handle_prescription_check

官方: https://open.shopee.com/documents/v2/v2.order.handle_prescription_check?module=94&type=1

入参说明见 references/apis/handle-prescription-check.md。
"""

from __future__ import annotations

import json
import sys

from _order_api_runner import run_order_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: handle_prescription_check.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_order_api("handle_prescription_check", params, "handle_prescription_check.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
