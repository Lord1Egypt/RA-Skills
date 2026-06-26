#!/usr/bin/env python3
"""
Get current status of last-words configuration.
Usage: python3 get_status.py
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from database import get_message, get_config, get_last_chat, get_last_delivery_status, init_db


def main():
    try:
        init_db()

        print("=" * 50)
        print("Last Words - 最后留言 状态")
        print("=" * 50)

        # Message status
        message = get_message()
        if message:
            print(f"\n📝 Message: ✓ Saved")
            print(f"   Content: {message['content'][:60]}{'...' if len(message['content']) > 60 else ''}")
            print(f"   Saved at: {message['created_at']}")
            if message['audio_path']:
                print(f"   Audio: {message['audio_path']}")
        else:
            print("\n📝 Message: ✗ Not set")

        # Config status
        config = get_config()
        if config:
            print(f"\n📬 Delivery: ✓ Configured")
            print(f"   Method: {config['method']}")
            print(f"   Contact: {config['contact']}")
            if config['smtp_host']:
                print(f"   SMTP: {config['smtp_host']}:{config['smtp_port']}")
        else:
            print("\n📬 Delivery: ✗ Not configured")

        # Activity status
        last_chat = get_last_chat()
        days_inactive = (datetime.now() - last_chat).days

        print(f"\n⏰ Activity:")
        print(f"   Last chat: {last_chat.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Days inactive: {days_inactive}")

        # Warning levels
        status = get_last_delivery_status()
        if status:
            print(f"\n📊 Last Check:")
            print(f"   Warning sent: {'Yes' if status['warning_sent'] else 'No'}")
            if status['warning_level'] > 0:
                print(f"   Warning level: Day {status['warning_level'] * 10}")
            print(f"   Delivered: {'Yes' if status['delivered'] else 'No'}")
            if status['delivered']:
                print(f"   Delivered at: {status['checked_at']}")

        # Thresholds
        print(f"\n⚠️  Warning Thresholds:")
        print(f"   10 days: First warning")
        print(f"   20 days: Second warning")
        print(f"   30 days: Auto-delivery")

        print("\n" + "=" * 50)

    except Exception as e:
        print(f"✗ Error getting status: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
