#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置文集内文档的父级（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="设置文集内文档的父级（parent）及同级排序（sort）")
    parser.add_argument("--collection-id", required=True, type=int, help="文集 ID（必填）")
    parser.add_argument("--document-id", required=True, type=int, help="文档 ID（必填）")
    parser.add_argument("--parent", required=True, type=int, help="父文档 ID，0 表示根文档")
    parser.add_argument("--sort", type=int, help="同级排序（如第一节=1、第二节=2、第三节=3），sort 越小越靠前")
    args = parser.parse_args()

    body = {"parent": args.parent}
    if args.sort is not None:
        body["sort"] = args.sort
    result = request(
        "PATCH",
        f"/api/collections/{args.collection_id}/documents/{args.document_id}/parent",
        json_body=body,
    )
    output_result(result)


if __name__ == "__main__":
    main()
