#!/usr/bin/env python3
"""
TikTok Video — get_creator_profile (Get Creator Profile 202508)
官方: https://partner.tiktokshop.com/docv2/page/get-creator-profile-202508

Usage:
  python get_creator_profile.py '{"openId": "..."}'
  python get_creator_profile.py '{"ttsAccessToken": "TTP_xxx"}'
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_creator_profile.py '<JSON>'\n"
            "Required: openId OR ttsAccessToken",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_video_api("get_creator_profile", params, "get_creator_profile.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
