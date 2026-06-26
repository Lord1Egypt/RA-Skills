#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _common import json_dump, machine_meta
from _swift_helper import emit_failure, run_helper


def main() -> int:
    parser = argparse.ArgumentParser(description="Sample Apple Silicon power via IOReport")
    parser.add_argument("--interval-ms", type=int, default=1000, help="sampling window in milliseconds (default: 1000)")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    try:
        data = run_helper(root, "powerstat", args=[str(args.interval_ms)], timeout=max(30, args.interval_ms / 1000 + 10))
        json_dump({**machine_meta(), **data})
        return 0
    except Exception as e:
        return emit_failure(
            "powerstat",
            f"Swift IOReport helper failed to build or run: {e}",
            [
                "Verify Command Line Tools / swiftc availability.",
                "If the helper builds but returns no channels, re-check IOReport channel naming on this macOS build.",
            ],
        )


if __name__ == "__main__":
    raise SystemExit(main())
