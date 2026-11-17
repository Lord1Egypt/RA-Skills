#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提交个人花园文集晋升精品文集申请"""

import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result

PROMOTION_REMINDER = (
    "【晋升前必读】审核通过后，该文集将变为精品文集，"
    "OpenClaw/ht-skills 将无法再修改文集名称、文档内容等。"
    "请确认内容已定稿；审核通过后请前往 https://aiknowledge.cn 网页维护。"
)


def main() -> None:
    parser = argparse.ArgumentParser(description="申请将个人花园文集晋升为精品文集")
    parser.add_argument("--collection-id", type=int, required=True, help="个人花园文集 ID")
    parser.add_argument("--reason", default="", help="申请说明（可选，最多500字）")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="确认已阅读晋升后果并向用户说明后再提交（必填）",
    )
    args = parser.parse_args()

    if not args.confirm:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": "提交晋升申请前须向用户说明后果并获确认",
                    "reminder": PROMOTION_REMINDER,
                    "hint": "确认后请加 --confirm 重新执行本脚本",
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    body = {"collection_id": args.collection_id, "reason": args.reason or ""}
    result = request("POST", "/api/collection-uploads/promotion-request", json_body=body)
    output_result(result)


if __name__ == "__main__":
    main()
