#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询当前用户个人花园限制与用量（调用服务端 API）
author: 灏天文库
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api_client import request, output_result


def main() -> None:
    result = request("GET", "/api/garden/limits-usage")
    output_result(result)


if __name__ == "__main__":
    main()
