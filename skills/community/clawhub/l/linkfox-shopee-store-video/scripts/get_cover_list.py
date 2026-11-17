#!/usr/bin/env python3
"""
Shopee Store — get_cover_list

官方: https://open.shopee.com/documents/v2/v2.video.get_cover_list?module=129&type=1

入参说明见 references/apis/get-cover-list.md。
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_cover_list.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_video_api("get_cover_list", params, "get_cover_list.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
