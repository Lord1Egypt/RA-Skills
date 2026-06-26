#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询当前用户图片列表
author: 灏天文库
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询当前用户图片列表")
    parser.add_argument("--group-id", type=int, default=None, help="按分组 ID 筛选")
    parser.add_argument("--name", default=None, help="按文件名模糊搜索（对应服务端 file_name）")
    parser.add_argument("--limit", type=int, default=50, help="每页条数，默认 50，最大 100")
    parser.add_argument("--offset", type=int, default=0, help="偏移，默认 0")
    args = parser.parse_args()

    limit = min(max(args.limit, 1), 100)
    offset = max(args.offset, 0)
    params = {"limit": limit, "offset": offset}
    if args.group_id is not None:
        params["group_id"] = args.group_id
    if args.name:
        params["file_name"] = args.name

    result = request("GET", "/api/images", params=params)
    output_result(result)


if __name__ == "__main__":
    main()
