#!/usr/bin/env python3
"""
TikTok Video — get_showcase_products (Get Showcase Products 202405)
官方: https://partner.tiktokshop.com/docv2/page/get-showcase-products-202405

Usage:
  python get_showcase_products.py '{"openId": "...", "page_size": 20, "origin": "SHOWCASE"}'
  python get_showcase_products.py '{"openId": "...", "page_size": 20, "origin": "LIVE"}'
  python get_showcase_products.py '{"openId": "...", "page_size": 20, "origin": "SHOWCASE", "page_token": "..."}'
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_showcase_products.py '<JSON>'\n"
            "Required: openId (or ttsAccessToken), page_size (default 20), origin (default SHOWCASE)\n"
            "Optional: page_token\n"
            "origin: SHOWCASE | LIVE",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    params.setdefault("page_size", 20)
    params.setdefault("origin", "SHOWCASE")
    print(
        json.dumps(
            run_video_api("get_showcase_products", params, "get_showcase_products.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
