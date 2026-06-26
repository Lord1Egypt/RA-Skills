#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询文档详情（调用服务端 API）
author: 灏天文库
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询文档详情")
    parser.add_argument("--id", required=True, type=int, dest="document_id", help="文档 ID（必填）")
    args = parser.parse_args()
    result = request("GET", f"/api/documents/{args.document_id}")
    output_result(result)


if __name__ == "__main__":
    main()
