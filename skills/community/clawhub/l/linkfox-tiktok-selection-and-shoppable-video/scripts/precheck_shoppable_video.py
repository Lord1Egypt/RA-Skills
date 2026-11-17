#!/usr/bin/env python3
"""
TikTok Video — precheck_shoppable_video (Pre-check Shoppable Video 202511)
官方: https://partner.tiktokshop.com/docv2/page/precheck-shoppable-video-202511
MRD: https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f

Usage:
  python precheck_shoppable_video.py '<JSON>'

Example:
  python precheck_shoppable_video.py '{
    "openId": "...",
    "video_info": {"file_id": "v12d00gd0024d3nfqr7og65"},
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
            "Usage: precheck_shoppable_video.py '<JSON>'\n"
            "Required: openId (or ttsAccessToken), video_info, product_link_info\n"
            "  video_info.file_id — from upload or large file bind\n"
            "  product_link_info.product_id — from linkfox-tiktok-video-products "
            "(get_shop_products / get_showcase_products)\n"
            "  product_link_info.title — product anchor title (< 30 chars recommended)\n"
            "Returns: data.precheck.task_id — use with get_shoppable_video_precheck_result.py\n"
            "Or pass full body via requestBody",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_video_api(
                "precheck_shoppable_video",
                params,
                "precheck_shoppable_video.py",
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
