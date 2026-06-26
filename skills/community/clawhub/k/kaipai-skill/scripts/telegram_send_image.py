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

# Add parent to path
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from notifications import TelegramNotifier


def main():
    parser = argparse.ArgumentParser(
        description="Send image via Telegram Bot API. "
                    "Bot token must be set via TELEGRAM_BOT_TOKEN env var."
    )
    parser.add_argument("--image", required=True, help="Local image file path or URL")
    parser.add_argument("--to", required=True, help="Telegram chat_id")
    parser.add_argument("--caption", default="", help="Caption text (optional)")
    args = parser.parse_args()

    notifier = TelegramNotifier()
    result = notifier.send_image(args.image, args.to, args.caption)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
