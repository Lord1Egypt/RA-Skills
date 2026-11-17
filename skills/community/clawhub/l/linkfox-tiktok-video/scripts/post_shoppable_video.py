#!/usr/bin/env python3
"""
TikTok Video — post_shoppable_video (Post Shoppable Video 202607)
官方: https://partner.tiktokshop.com/docv2/page/post-shoppable-video-202607
MRD: https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f

Usage:
  python post_shoppable_video.py '<JSON>'

Example:
  python post_shoppable_video.py '{
    "openId": "...",
    "video_info": {
      "file_id": "v12d00gd0024d3nfqr7og65",
      "title": "Sample video title",
      "is_ai_generated": false
    },
    "product_link_info": {
      "product_id": "17294069642063424",
      "title": "Sample product anchor title"
    }
  }'
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: post_shoppable_video.py '<JSON>'\n"
            "Required: openId (or ttsAccessToken), video_info, product_link_info\n"
            "  video_info.file_id — from upload_shoppable_video_file or large file bind\n"
            "  video_info.title — video caption (max 4000 UTF-16 runes)\n"
            "  product_link_info.product_id — from get_shop_products / get_showcase_products\n"
            "  product_link_info.title — product anchor title (< 30 chars recommended)\n"
            "Optional in video_info: cover_uri, cover_timestamp_ms, music_id, is_ai_generated\n"
            "  is_ai_generated — bool; true marks the post as AI-generated\n"
            "Response may include data.quota (e.g. \"3/day\") for posting quota\n"
            "Or pass full body via requestBody",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_video_api("post_shoppable_video", params, "post_shoppable_video.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
