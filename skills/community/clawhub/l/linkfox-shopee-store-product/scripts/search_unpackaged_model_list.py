#!/usr/bin/env python3
"""
Shopee Store — search_unpackaged_model_list

官方: https://open.shopee.com/documents/v2/v2.product.search_unpackaged_model_list?module=89&type=1

入参说明见 references/apis/search-unpackaged-model-list.md。
"""

from __future__ import annotations

import json
import sys

from _product_api_runner import run_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: search_unpackaged_model_list.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_product_api("search_unpackaged_model_list", params, "search_unpackaged_model_list.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
