#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改文档归属：将文档移动到目标文集（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="修改文档归属：将文档移动到目标文集")
    parser.add_argument("--id", required=True, type=int, dest="document_id", help="文档 ID（必填）")
    parser.add_argument("--collection-id", required=True, type=int, help="目标文集 ID（必填）")
    parser.add_argument("--from-collection-id", type=int, help="原文集 ID（若文档属于多个文集则必填）")
    args = parser.parse_args()

    body = {"collection_id": args.collection_id}
    if args.from_collection_id is not None:
        body["from_collection_id"] = args.from_collection_id

    result = request(
        "PATCH",
        f"/api/documents/{args.document_id}/collection",
        json_body=body,
    )
    output_result(result)


if __name__ == "__main__":
    main()
