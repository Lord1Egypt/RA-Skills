#!/usr/bin/env python3
"""
Reset all last-words data.
Usage: python3 reset.py [--force]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import reset_all, init_db


def main():
    parser = argparse.ArgumentParser(description="Reset all last-words data")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Skip confirmation prompt")

    args = parser.parse_args()

    if not args.force:
        response = input("⚠️  This will delete all messages and configuration. Continue? [y/N]: ")
        if response.lower() not in ["y", "yes"]:
            print("Cancelled.")
            sys.exit(0)

    try:
        init_db()
        reset_all()
        print("✓ All data reset successfully")
    except Exception as e:
        print(f"✗ Error resetting data: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
