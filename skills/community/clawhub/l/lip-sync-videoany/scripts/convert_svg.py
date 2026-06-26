#!/usr/bin/env python3
"""
Backward-compatible entrypoint for legacy script name.
"""
import sys

from guide_lip_sync import main


if __name__ == "__main__":
    print(
        "Warning: this skill is now lip-sync guidance. "
        "Use scripts/guide_lip_sync.py for the primary entrypoint.",
        file=sys.stderr,
    )
    sys.exit(main())
