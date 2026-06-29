#!/usr/bin/env python3
"""
Center-crop and resize an image to a target size from the current template.

Usage:
  python3 resize_cover.py <pic_url_or_path> <out_path> <width> <height>
"""
import os
import sys
from io import BytesIO
from urllib.parse import urlparse

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...", file=sys.stderr)
    os.system(f"{sys.executable} -m pip install Pillow requests -q")
    from PIL import Image

try:
    import requests
except ImportError:
    print("Installing requests...", file=sys.stderr)
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests


if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} <pic_url_or_path> <out_path> <width> <height>", file=sys.stderr)
    sys.exit(1)

pic_source = sys.argv[1]
out_path = sys.argv[2]
target_w = int(sys.argv[3])
target_h = int(sys.argv[4])

if urlparse(pic_source).scheme in {"http", "https"}:
    response = requests.get(pic_source, timeout=30)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGB")
else:
    img = Image.open(pic_source).convert("RGB")

source_w, source_h = img.width, img.height
if source_w < target_w or source_h < target_h:
    print(
        "source image is smaller than target; refuse to upscale: "
        f"source={source_w}x{source_h}, target={target_w}x{target_h}",
        file=sys.stderr,
    )
    sys.exit(2)

ratio = max(target_w / img.width, target_h / img.height)
new_w = int(img.width * ratio)
new_h = int(img.height * ratio)
img = img.resize((new_w, new_h), Image.LANCZOS)

left = (new_w - target_w) // 2
top = (new_h - target_h) // 2
img = img.crop((left, top, left + target_w, top + target_h))
img.save(out_path, "JPEG")

print(f"{out_path} {target_w}x{target_h} from {source_w}x{source_h}")
