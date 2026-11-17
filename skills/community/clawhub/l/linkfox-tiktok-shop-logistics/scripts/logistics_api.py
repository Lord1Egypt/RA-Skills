#!/usr/bin/env python3
"""TikTok Shop ERP Logistics — generic registered API caller."""

from __future__ import annotations

import json
import sys

from _logistics_api_runner import run_logistics_api
from _logistics_endpoints import list_api_names


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: logistics_api.py '<JSON with api field>'\n"
            f"Available: {', '.join(list_api_names())}",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    if not params.get("api"):
        print("Missing required field: api", file=sys.stderr)
        sys.exit(1)
    print(
        json.dumps(
            run_logistics_api(str(params["api"]), params, "logistics_api.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
