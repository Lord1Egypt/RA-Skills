#!/usr/bin/env python3
"""
Backward-compatible entrypoint for legacy script name.
"""
import sys

from guide_image_to_video import main


if __name__ == "__main__":
    print(
        "Warning: this skill is now image-to-video guidance. "
        "Use scripts/guide_image_to_video.py for the primary entrypoint.",
        file=sys.stderr,
    )
    sys.exit(main())
