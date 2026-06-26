"""Shared logging helpers for CLI scripts."""

import json
import os
import sys


def error_exit(message: str):
    print(f"错误：{message}", file=sys.stderr)
    sys.exit(1)


def warn(message: str):
    print(f"警告：{message}", file=sys.stderr)


def debug(message: str):
    if os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}:
        print(f"[DEBUG] {message}", file=sys.stderr)


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))
