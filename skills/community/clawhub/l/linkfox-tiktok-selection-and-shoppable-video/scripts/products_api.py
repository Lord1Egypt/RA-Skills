#!/usr/bin/env python3
"""
TikTok Video Products — generic API caller (registered endpoints)

Usage:
  python products_api.py '{"api": "<api_name>", "openId": "..."}'
"""

from __future__ import annotations

import json
import sys

from _products_api_runner import run_products_api
from _products_endpoints import list_api_names


def main() -> None:
    if len(sys.argv) < 2:
        names = list_api_names()
        hint = ", ".join(names) if names else "(none)"
        print(f"Usage: products_api.py '<JSON with api field>'\nAvailable: {hint}", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    if not params.get("api"):
        print("Missing required field: api", file=sys.stderr)
        sys.exit(1)
    print(
        json.dumps(
            run_products_api(str(params["api"]), params, "products_api.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
