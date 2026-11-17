#!/usr/bin/env python3
"""
TikTok Video — upload_shoppable_video_file (Upload Shoppable Video File 202505)
官方: https://partner.tiktokshop.com/docv2/page/upload-shoppable-video-file-202505
MRD: https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f

⚠️ 本接口为 multipart/form-data 二进制上传，当前 /tiktokVideo/developerProxy 不支持。
本脚本仅作规范入口；实际上传需等待网关 multipart 链路或使用大文件分片方案。

Usage:
  python upload_shoppable_video_file.py
  python upload_shoppable_video_file.py --help
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "Upload Shoppable Video File\n"
            "  Path: affiliate_creator/202505/videos/video_files\n"
            "  Method: POST multipart/form-data, field: data=<video file>\n"
            "\n"
            "Current limitation:\n"
            "  /tiktokVideo/developerProxy accepts JSON/string body only.\n"
            "  Binary video upload is NOT supported through video_proxy.py yet.\n"
            "\n"
            "When supported, expected params: openId + local video file path.\n"
            "See references/api.md for file format/size constraints.\n"
            "Videos > 10MB may require the Large File Upload Solution.",
            file=sys.stderr,
        )
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    result = run_video_api(
        "upload_shoppable_video_file",
        json.loads(sys.argv[1]),
        "upload_shoppable_video_file.py",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
