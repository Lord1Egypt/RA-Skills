#!/usr/bin/env python3
"""
Send image messages via Telegram Bot API.

Usage:
    TELEGRAM_BOT_TOKEN=<token> python3 telegram_send_image.py \
        --image /path/to/image.jpg \
        --to <chat_id> \
        [--caption "Here is your result"]

    # Or with a URL (auto-downloaded):
    TELEGRAM_BOT_TOKEN=<token> python3 telegram_send_image.py \
        --image https://example.com/result.jpg \
        --to <chat_id>

This is a wrapper around scripts.notifications.telegram for backward compatibility.
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

from notifications import TelegramNotifier
from notifications.base import MissingCredentialsError


def main():
    parser = argparse.ArgumentParser(
        description='通过 Telegram Bot API 发送图片。请使用 TELEGRAM_BOT_TOKEN 环境变量配置 Token。'
    )
    parser.add_argument("--image", required=True, help='本地图片文件路径或 URL')
    parser.add_argument("--to", required=True, help='Telegram 的 chat_id')
    parser.add_argument("--caption", default="", help='说明文字（可选）')
    args = parser.parse_args()

    try:
        notifier = TelegramNotifier()
        result = notifier.send_image(args.image, args.to, args.caption)
    except MissingCredentialsError as error:
        print(json.dumps(error.payload), file=sys.stderr)
        return 1
    if result.get("status") != "ok":
        payload = result.get("error_details") or {"error": result.get("error", "Telegram sendPhoto failed")}
        print(json.dumps(payload), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
