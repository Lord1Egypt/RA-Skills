#!/usr/bin/env python3
"""
Shopee Store — upload_image

官方: https://open.shopee.com/documents/v2/v2.livestream.upload_image?module=125&type=1

入参说明见 references/apis/upload-image.md。
"""

from __future__ import annotations

import json
import sys

from _livestream_api_runner import run_livestream_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: upload_image.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_livestream_api("upload_image", params, "upload_image.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
