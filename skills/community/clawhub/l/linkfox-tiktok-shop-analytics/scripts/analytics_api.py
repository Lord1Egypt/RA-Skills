#!/usr/bin/env python3
"""TikTok Shop ERP analytics — generic registered API caller."""

from __future__ import annotations

import json
import sys

from _analytics_api_runner import run_analytics_api
from _analytics_endpoints import list_api_names


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: analytics_api.py '<JSON with api field>'\n"
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
            run_analytics_api(str(params["api"]), params, "analytics_api.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
