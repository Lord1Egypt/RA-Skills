#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询今日是否可提交花园晋升申请"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    result = request("GET", "/api/collection-uploads/promotion-quota")
    output_result(result)


if __name__ == "__main__":
    main()
