#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询文集列表（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询文集列表")
    parser.add_argument("--name", help="按名称模糊搜索")
    args = parser.parse_args()
    params = {}
    if args.name:
        params["name"] = args.name
    result = request("GET", "/api/collections", params=params)
    output_result(result)


if __name__ == "__main__":
    main()
