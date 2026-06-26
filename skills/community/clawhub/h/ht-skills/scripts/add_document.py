#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新建文档到指定文集（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def get_client_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="新建文档并关联到指定文集")
    parser.add_argument("--collection-id", required=True, type=int, help="文集 ID（必填）")
    parser.add_argument("--name", required=True, help="文档名称（必填）")
    parser.add_argument("--content", default="", help="文档正文")
    parser.add_argument("--content-file", help="从文件读取正文")
    parser.add_argument("--parent", default=0, type=int, help="父文档 ID")
    args = parser.parse_args()
    content = args.content
    if args.content_file:
        path = Path(args.content_file)
        if not path.is_absolute():
            path = get_client_root() / path
        if path.exists():
            content = path.read_text(encoding="utf-8")
        else:
            output_result({"success": False, "error": f"文件不存在: {args.content_file}"})
            sys.exit(1)
    body = {
        "collection_id": args.collection_id,
        "name": args.name,
        "content": content or "",
        "parent": args.parent,
    }
    result = request("POST", "/api/documents", json_body=body)
    output_result(result)


if __name__ == "__main__":
    main()
