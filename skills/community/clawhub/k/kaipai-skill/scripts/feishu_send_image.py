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

# Add parent to path
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from notifications import FeishuNotifier


def main():
    parser = argparse.ArgumentParser(description="Send image messages via Feishu")
    parser.add_argument("--image", required=True, help="Image file path or URL")
    parser.add_argument(
        "--to", required=True, help="Recipient open_id (ou_xxx) or group chat_id (oc_xxx)"
    )
    args = parser.parse_args()

    notifier = FeishuNotifier()
    result = notifier.send_image(args.image, args.to)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
