#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新文集信息（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="更新文集信息（名称、描述、简介）")
    parser.add_argument("--id", required=True, type=int, dest="collection_id", help="文集 ID（必填）")
    parser.add_argument("--name", help="更新文集名称")
    parser.add_argument("--description", help="更新文集简短介绍（50字以内）")
    parser.add_argument("--brief", help="更新文集详细介绍")
    args = parser.parse_args()

    body = {}
    if args.name is not None:
        body["name"] = args.name
    if args.description is not None:
        body["description"] = args.description
    if args.brief is not None:
        body["brief"] = args.brief

    if not body:
        output_result({"success": False, "error": "请至少指定 --name、--description 或 --brief 之一"})
        sys.exit(1)

    result = request("PATCH", f"/api/collections/{args.collection_id}", json_body=body)
    output_result(result)


if __name__ == "__main__":
    main()
