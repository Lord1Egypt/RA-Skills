#!/usr/bin/env python3
"""Interactive helper to capture and persist the WellAPI API key."""
from __future__ import annotations

import getpass
import sys

from api_key import REGISTER_URL, save_api_key


def main() -> int:
    print("=" * 60)
    print("gpt-image-2-generation — API key setup")
    print("=" * 60)
    print(
        "If you do not have a WellAPI API key yet, register for a free one at:\n"
        f"  {REGISTER_URL}\n"
    )

    try:
        # getpass hides the key from the terminal; falls back to input() in
        # environments that do not support hidden input.
        try:
            api_key = getpass.getpass("Paste your WellAPI API key: ").strip()
        except (EOFError, getpass.GetPassWarning):
            api_key = input("Paste your WellAPI API key: ").strip()
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        return 130

    if not api_key:
        print("No key provided. Nothing was saved.", file=sys.stderr)
        return 1

    path = save_api_key(api_key)
    masked = api_key[:4] + "…" + api_key[-4:] if len(api_key) > 8 else "****"
    print(f"\nSaved API key ({masked}) to:\n  {path}")
    print("You can now run: python3 scripts/generate_image.py --prompt \"...\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
