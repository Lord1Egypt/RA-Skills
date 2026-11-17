#!/usr/bin/env python3
"""TikTok Shop ERP Fulfillment — generic path/method proxy."""

from __future__ import annotations

import json
import sys

from _fulfillment_api_runner import run_fulfillment_proxy


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: fulfillment_proxy.py '<JSON>'\n"
            "Required: openId, path, method\n"
            "path whitelist: fulfillment/, authorization/",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_fulfillment_proxy(params, "fulfillment_proxy.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
