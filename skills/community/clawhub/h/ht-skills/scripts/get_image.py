#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询当前用户指定图片详情（含 file_url、file_path）
author: 灏天文库
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询图片详情")
    parser.add_argument("--id", required=True, type=int, help="图片 ID（image 表主键）")
    args = parser.parse_args()

    result = request("GET", f"/api/images/{args.id}")
    output_result(result)


if __name__ == "__main__":
    main()
