#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档片段检索（调用服务端 API，转发 HT_RAG/retrieve，不调用大模型）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="检索相关文档片段及出处")
    parser.add_argument("--content", required=True, help="检索内容")
    parser.add_argument(
        "--collection-ids",
        required=True,
        nargs="+",
        help="文集 ID 列表，支持 21 或 collection_21 格式，可传多个（最多 5 个，超出仅使用前 5 个）",
    )
    args = parser.parse_args()

    if len(args.collection_ids) > 5:
        print(
            "警告：最多支持 5 个文集，超出部分将由服务端忽略，仅使用前 5 个",
            file=sys.stderr,
        )

    result = request(
        "POST",
        "/api/rag/retrieve",
        json_body={
            "content": args.content,
            "collection_ids": [str(cid) for cid in args.collection_ids],
        },
        timeout=120,
    )
    output_result(result)


if __name__ == "__main__":
    main()
