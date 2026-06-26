#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询文档列表（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询文档列表")
    parser.add_argument("--name", help="按文档名称模糊搜索")
    parser.add_argument("--collection-id", type=int, help="按文集 ID 筛选（强烈建议带上，否则无法查询）")
    args = parser.parse_args()
    if not args.collection_id:
        output_result({
            "success": False,
            "error": "查询文档列表请提供 --collection-id（文集ID）。若不知道文集ID，请先用 list_collections.py --name \"文集名称\" 查询，或向用户询问目标文集名称。",
        })
        sys.exit(1)
    params = {}
    if args.name:
        params["name"] = args.name
    params["collection_id"] = args.collection_id
    result = request("GET", "/api/documents", params=params)
    output_result(result)


if __name__ == "__main__":
    main()
