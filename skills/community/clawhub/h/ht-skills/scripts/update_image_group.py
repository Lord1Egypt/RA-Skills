#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改当前用户图片分组名称
author: 灏天文库
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="修改图片分组名称")
    parser.add_argument("--id", required=True, type=int, help="分组 ID")
    parser.add_argument("--name", required=True, help="新分组名称")
    args = parser.parse_args()

    result = request("PATCH", f"/api/image-groups/{args.id}", json_body={"group_name": args.name})
    output_result(result)


if __name__ == "__main__":
    main()
