#!/usr/bin/env python3
"""
Backward-compatible entrypoint.
"""
import sys

from convert_image_to_svg import main


if __name__ == "__main__":
    print(
        "Warning: scripts/convert_svg.py has been renamed to scripts/convert_image_to_svg.py. "
        "Running image-to-svg mode.",
        file=sys.stderr,
    )
    sys.exit(main() or 0)
