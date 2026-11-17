#!/usr/bin/env python3
"""
Shopee Store — edit_manual_product_ad_keywords

官方: https://open.shopee.com/documents/v2/v2.ads.edit_manual_product_ad_keywords?module=117&type=1

入参说明见 references/apis/edit-manual-product-ad-keywords.md。
"""

from __future__ import annotations

import json
import sys

from _ads_api_runner import run_ads_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: edit_manual_product_ad_keywords.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ads_api("edit_manual_product_ad_keywords", params, "edit_manual_product_ad_keywords.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
