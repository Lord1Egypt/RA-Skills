#!/usr/bin/env python3
"""OpenClaw-friendly launcher for last30days research.

Defaults to `--no-native-web` so the OpenClaw agent can use its own web_search
tool for grounded citations and routing policy.
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
ENGINE = SCRIPT_DIR / "last30days.py"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run last30days with OpenClaw defaults")
    parser.add_argument("topic", nargs="+", help="Topic to research")
    parser.add_argument("--emit", default="compact", choices=["compact", "json", "md", "context", "path"])
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--store", action="store_true")
    parser.add_argument("--search", default=None, help="Comma-separated source filter")
    parser.add_argument("--native-web", action="store_true", help="Enable native web API backends")

    args = parser.parse_args()
    topic = " ".join(args.topic)

    cmd = [sys.executable, str(ENGINE), topic, f"--emit={args.emit}"]
    if args.quick:
        cmd.append("--quick")
    if args.deep:
        cmd.append("--deep")
    if args.store:
        cmd.append("--store")
    if args.search:
        cmd.extend(["--search", args.search])
    if not args.native_web:
        cmd.append("--no-native-web")

    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
