#!/usr/bin/env python3
"""
TikTok Video — get_shoppable_video_status (Get Shoppable Video Status 202509)
官方: https://partner.tiktokshop.com/docv2/page/get-shoppable-video-status-202509
MRD: https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f

Usage:
  python get_shoppable_video_status.py '{"openId": "...", "video_id": "7548431509997292816"}'
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_shoppable_video_status.py '<JSON>'\n"
            "Required: openId (or ttsAccessToken), video_id\n"
            "  video_id — from post_shoppable_video (data.video.id)\n"
            "Returns: data.video.post_status (SUCCESS / FAIL / PROCESSING)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_video_api(
                "get_shoppable_video_status",
                params,
                "get_shoppable_video_status.py",
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
