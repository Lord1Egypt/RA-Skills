#!/usr/bin/env python3
"""
sync_capabilities.py — Sync platform capability manifest and version check

Usage:
    python sync_capabilities.py [--force]
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.capabilities import sync_capabilities
from lib.version_checker import check_version
from lib.schemas import NetworkError


def main():
    parser = argparse.ArgumentParser(description="Sync platform capabilities manifest")
    parser.add_argument("--force", action="store_true", help="Force refresh cache")
    parser.add_argument("--base-url", default=None, help="L2 API base URL")
    args = parser.parse_args()

    try:
        manifest = sync_capabilities(force=args.force, base_url=args.base_url)

        # Version check
        client_policy = manifest.get("client_policy", {})
        version_info = check_version(client_policy)

        # Build output
        output = {
            "ttl_seconds": manifest.get("ttl_seconds", 3600),
            "offline": manifest.get("offline", False),
            "client_policy": client_policy,
            "data_products": manifest.get("data_products", []),
            "remote_capabilities": manifest.get("remote_capabilities", []),
            "tool_hints": manifest.get("tool_hints", []),
            "routing_message": manifest.get("routing_message", ""),
            "upgrade": manifest.get("upgrade", {}),
            "version_check": version_info,
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))

    except NetworkError as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Unexpected error: {e}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
