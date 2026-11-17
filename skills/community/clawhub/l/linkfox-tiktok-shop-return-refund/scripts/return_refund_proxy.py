#!/usr/bin/env python3
"""TikTok Shop ERP return_refund — generic path/method proxy."""

from __future__ import annotations

import json
import sys

from _return_refund_api_runner import run_return_refund_proxy


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: return_refund_proxy.py '<JSON>'\n"
            "Required: openId, path, method\n"
            "path whitelist: return_refund/, authorization/",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_return_refund_proxy(params, "return_refund_proxy.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
