#!/usr/bin/env python3
"""Verify that gitcode-api is installed and usable."""

import os
import sys


def main() -> int:
    print(f"python: {sys.executable}")
    print(f"version: {sys.version.split()[0]}")

    try:
        import gitcode_api
    except ImportError as exc:
        print("gitcode-api import: FAILED")
        print("install with: pip install -U gitcode-api")
        print(f"details: {exc}")
        return 1

    print("gitcode-api import: OK")
    print(f"gitcode-api version: {getattr(gitcode_api, '__version__', 'unknown')}")

    token = os.getenv("GITCODE_ACCESS_TOKEN")
    if token:
        print("GITCODE_ACCESS_TOKEN: set")
    else:
        print("GITCODE_ACCESS_TOKEN: missing")
        print("set it with: export GITCODE_ACCESS_TOKEN='your-token', or use .env files")

    print("top-level clients: GitCode, AsyncGitCode")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
