#!/usr/bin/env python3
"""
Send image messages via Feishu (Lark)

Usage:
    python3 feishu_send_image.py \
        --image /path/to/image.jpg \
        --to ou_xxx

    # Or with a URL (auto-downloaded):
    python3 feishu_send_image.py \
        --image https://example.com/result.jpg \
        --to oc_xxx

This is a wrapper around scripts.notifications.feishu for backward compatibility.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print(json.dumps({
        "error": "requests package not installed",
        "install_command": "pip install requests",
    }), file=sys.stderr)
    raise SystemExit(1)

# Add parent to path
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from notifications import FeishuNotifier
from notifications.base import MissingCredentialsError


def main():
    parser = argparse.ArgumentParser(description='通过飞书发送图片')
    parser.add_argument("--image", required=True, help='图片文件路径或 URL')
    parser.add_argument(
        "--to", required=True, help='接收方 open_id（ou_xxx）或群 chat_id（oc_xxx）'
    )
    args = parser.parse_args()

    try:
        notifier = FeishuNotifier()
        result = notifier.send_image(args.image, args.to)
    except MissingCredentialsError as error:
        print(json.dumps(error.payload), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
