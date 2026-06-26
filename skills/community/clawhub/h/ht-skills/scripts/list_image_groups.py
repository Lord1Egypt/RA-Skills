#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询当前用户图片分组列表
author: 灏天文库
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询图片分组列表")
    parser.add_argument("--limit", type=int, default=100, help="每页条数，默认 100，最大 200")
    parser.add_argument("--offset", type=int, default=0, help="偏移，默认 0")
    args = parser.parse_args()

    limit = min(max(args.limit, 1), 200)
    offset = max(args.offset, 0)
    result = request("GET", "/api/image-groups", params={"limit": limit, "offset": offset})
    output_result(result)


if __name__ == "__main__":
    main()
