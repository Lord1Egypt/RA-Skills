#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询我的花园晋升申请记录"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    parser = argparse.ArgumentParser(description="查询我的花园晋升申请记录")
    parser.add_argument("--limit", type=int, default=50, help="返回条数，默认50")
    parser.add_argument("--offset", type=int, default=0, help="偏移量，默认0")
    args = parser.parse_args()
    result = request(
        "GET",
        "/api/collection-uploads/promotion-mine",
        params={"limit": args.limit, "offset": args.offset},
    )
    output_result(result)


if __name__ == "__main__":
    main()
