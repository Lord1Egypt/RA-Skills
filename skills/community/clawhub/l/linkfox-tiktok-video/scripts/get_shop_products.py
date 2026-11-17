#!/usr/bin/env python3
"""
TikTok Video — get_shop_products (Get Shop Products 202509)
官方: https://partner.tiktokshop.com/docv2/page/get-shop-products-202509
MRD: https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f

Usage:
  python get_shop_products.py '{"openId": "...", "page_size": 20}'
  python get_shop_products.py '{"openId": "...", "title_keyword": "apple", "sort_field": "PRICE", "sort_order": "DESC", "page_size": 20}'
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_shop_products.py '<JSON>'\n"
            "Required: openId (or ttsAccessToken), page_size (default 20)\n"
            "Optional: title_keyword, sort_field, sort_order, page_token",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    params.setdefault("page_size", 20)
    print(
        json.dumps(
            run_video_api("get_shop_products", params, "get_shop_products.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
