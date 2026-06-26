#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建图片分组
author: 灏天文库
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="创建图片分组")
    parser.add_argument("--name", required=True, help="分组名称")
    args = parser.parse_args()

    result = request("POST", "/api/image-groups", json_body={"group_name": args.name})
    output_result(result)


if __name__ == "__main__":
    main()
