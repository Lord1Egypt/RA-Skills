#!/usr/bin/env python3
"""
TikTok Video — get_shoppable_video_precheck_result (Get Shoppable Video Pre-check Result 202511)
官方: https://partner.tiktokshop.com/docv2/page/get-shoppable-video-precheck-result-202511
MRD: https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f

Usage:
  python get_shoppable_video_precheck_result.py '{"openId": "...", "task_id": "1123123123"}'
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_shoppable_video_precheck_result.py '<JSON>'\n"
            "Required: openId (or ttsAccessToken), task_id\n"
            "  task_id — from precheck_shoppable_video (data.precheck.task_id)\n"
            "Returns: data.precheck_task.result (SUCCESS / FAIL / PROCESSING)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_video_api(
                "get_shoppable_video_precheck_result",
                params,
                "get_shoppable_video_precheck_result.py",
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
