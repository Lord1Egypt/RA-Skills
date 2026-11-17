#!/usr/bin/env python3
"""
Shopee Store — update_tier_variation

官方: https://open.shopee.com/documents/v2/v2.global_product.update_tier_variation?module=90&type=1

入参说明见 references/apis/update-tier-variation.md。
"""

from __future__ import annotations

import json
import sys

from _global_product_api_runner import run_global_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: update_tier_variation.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_global_product_api("update_tier_variation", params, "update_tier_variation.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
