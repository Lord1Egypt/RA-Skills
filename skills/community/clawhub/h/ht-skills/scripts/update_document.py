#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新文档（调用服务端 API）
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
    parser = argparse.ArgumentParser(description="更新文档")
    parser.add_argument("--id", required=True, type=int, dest="document_id", help="文档 ID（必填）")
    parser.add_argument("--name", help="更新文档标题")
    parser.add_argument("--content", help="更新文档正文")
    parser.add_argument("--content-file", help="从文件读取正文并更新")
    parser.add_argument("--sort", type=int, help="排序值")
    parser.add_argument("--parent", type=int, help="父文档 ID")
    args = parser.parse_args()
    updates = {}
    if args.name is not None:
        updates["name"] = args.name
    if args.content is not None:
        updates["content"] = args.content
    if args.content_file:
        path = Path(args.content_file)
        if not path.is_absolute():
            path = get_client_root() / path
        if path.exists():
            updates["content"] = path.read_text(encoding="utf-8")
        else:
            output_result({"success": False, "error": f"文件不存在: {args.content_file}"})
            sys.exit(1)
    if args.sort is not None:
        updates["sort"] = args.sort
    if args.parent is not None:
        updates["parent"] = args.parent
    if not updates:
        output_result({"success": False, "error": "请至少指定 --name、--content、--content-file、--sort 或 --parent 之一"})
        sys.exit(1)
    result = request("PATCH", f"/api/documents/{args.document_id}", json_body=updates)
    output_result(result)


if __name__ == "__main__":
    main()
