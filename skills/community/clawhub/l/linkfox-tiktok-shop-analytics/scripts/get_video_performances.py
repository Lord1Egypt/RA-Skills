#!/usr/bin/env python3
"""TikTok Shop ERP analytics — get_video_performances

Usage:
  python get_video_performances.py '<JSON>'
"""

from __future__ import annotations

import json
import sys

from _analytics_api_runner import run_analytics_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_video_performances.py '<JSON>'\n"
            "Hint: openId, start_date, end_date (YYYYMMDD); optional page_size/page_token\n"
            "Auth: openId (linkfox-tiktok-shop-auth; token backendized)\n"
            "Needs shop_cipher (auto if only 1 shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_analytics_api("get_video_performances", params, "get_video_performances.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
