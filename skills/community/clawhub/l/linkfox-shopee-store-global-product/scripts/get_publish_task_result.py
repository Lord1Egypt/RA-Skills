#!/usr/bin/env python3
"""
Shopee Store — get_publish_task_result

官方: https://open.shopee.com/documents/v2/v2.global_product.get_publish_task_result?module=90&type=1

入参说明见 references/apis/get-publish-task-result.md。
"""

from __future__ import annotations

import json
import sys

from _global_product_api_runner import run_global_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_publish_task_result.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_global_product_api("get_publish_task_result", params, "get_publish_task_result.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
