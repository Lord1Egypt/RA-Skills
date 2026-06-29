#!/usr/bin/env python3
"""
Validate an image's exact pixel size.

Usage:
  python3 validate_image_size.py <image_path_or_url> <width> <height>
"""
import os
import sys
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...", file=sys.stderr)
    os.system(f"{sys.executable} -m pip install Pillow -q")
    from PIL import Image


def load_image(path_or_url):
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        try:
            import requests
        except ImportError:
            print("Installing requests...", file=sys.stderr)
            os.system(f"{sys.executable} -m pip install requests -q")
            import requests
        response = requests.get(path_or_url, timeout=30)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    return Image.open(path_or_url)


if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <image_path_or_url> <width> <height>", file=sys.stderr)
    sys.exit(1)

image_path = sys.argv[1]
expected_width = int(sys.argv[2])
expected_height = int(sys.argv[3])

img = load_image(image_path)
actual_width, actual_height = img.size

if (actual_width, actual_height) != (expected_width, expected_height):
    print(
        f"image size mismatch: expected {expected_width}x{expected_height}, "
        f"actual {actual_width}x{actual_height}",
        file=sys.stderr,
    )
    sys.exit(2)

print(f"ok: {actual_width}x{actual_height}")
