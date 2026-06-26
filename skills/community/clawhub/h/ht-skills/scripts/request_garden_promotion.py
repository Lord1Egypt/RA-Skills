#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提交个人花园文集晋升精品文集申请"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="申请将个人花园文集晋升为精品文集")
    parser.add_argument("--collection-id", type=int, required=True, help="个人花园文集 ID")
    parser.add_argument("--reason", default="", help="申请说明（可选，最多500字）")
    args = parser.parse_args()
    body = {"collection_id": args.collection_id, "reason": args.reason or ""}
    result = request("POST", "/api/collection-uploads/promotion-request", json_body=body)
    output_result(result)


if __name__ == "__main__":
    main()
