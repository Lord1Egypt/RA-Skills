#!/usr/bin/env python3
"""check_env.py — Verify Ladybug Python bindings (real_ladybug) are available.

Usage:
  python check_env.py
"""
import sys


def main() -> int:
    try:
        import real_ladybug as lb
    except ImportError as e:
        print("FAIL: cannot import real_ladybug:", e, file=sys.stderr)
        print("Install Ladybug client libraries and set PYTHONPATH if needed.", file=sys.stderr)
        return 1

    mod = getattr(lb, "__file__", "(built-in)")
    print("OK: real_ladybug importable")
    print(f"   module: {mod}")

    for name in ("Database", "Connection", "AsyncConnection"):
        if hasattr(lb, name):
            print(f"   {name}: yes")
        else:
            print(f"   {name}: missing", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
