#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询文集详情（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询文集详情")
    parser.add_argument("--id", required=True, type=int, dest="collection_id", help="文集 ID（必填）")
    parser.add_argument("--include-docs", action="store_true", dest="include_docs", help="是否包含文档列表")
    args = parser.parse_args()
    params = {"include_docs": args.include_docs} if args.include_docs else {}
    result = request("GET", f"/api/collections/{args.collection_id}", params=params)
    output_result(result)


if __name__ == "__main__":
    main()
