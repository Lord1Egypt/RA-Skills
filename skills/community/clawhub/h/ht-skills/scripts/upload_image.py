#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传图片到服务端（COS），支持备注与分组
author: 灏天文库
"""

import argparse
import mimetypes
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import post_multipart, output_result


def get_client_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="上传图片（multipart/form-data）")
    parser.add_argument("--file", required=True, help="本地图片文件路径")
    parser.add_argument("--remark", default="", help="备注（可选）")
    parser.add_argument("--group-id", type=int, default=None, help="图片分组 ID（可选，须属于当前用户）")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_absolute():
        path = get_client_root() / path
    if not path.is_file():
        output_result({"success": False, "error": f"文件不存在: {args.file}"})
        sys.exit(1)

    mime, _ = mimetypes.guess_type(str(path))
    content_type = mime or "application/octet-stream"
    raw = path.read_bytes()
    files = {"file": (path.name, raw, content_type)}

    data = {}
    if args.remark:
        data["remark"] = args.remark
    if args.group_id is not None:
        data["group_id"] = args.group_id

    result = post_multipart("/api/images/upload", files=files, data=data or None, timeout=180)
    output_result(result)


if __name__ == "__main__":
    main()
