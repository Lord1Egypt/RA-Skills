#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新建文集（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

# 将 client 根目录加入 path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="新建文集（支持有则用、无则建）")
    parser.add_argument("--name", required=True, help="文集名称（必填）")
    parser.add_argument("--description", default="", help="文集简短介绍（50字以内）")
    parser.add_argument("--brief", default="", help="文集详细介绍")
    parser.add_argument("--get-if-exists", action="store_true", dest="get_if_exists",
                        help="若同名文集已存在则直接返回其 ID")
    args = parser.parse_args()
    description = args.description or f"关于{args.name}的文集"
    if len(description) > 50:
        description = description[:50]
    body = {
        "name": args.name,
        "description": description,
        "brief": args.brief,
        "get_if_exists": args.get_if_exists,
    }
    result = request("POST", "/api/collections", json_body=body)
    output_result(result)


if __name__ == "__main__":
    main()
