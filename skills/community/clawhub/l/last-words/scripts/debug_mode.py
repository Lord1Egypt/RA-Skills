#!/usr/bin/env python3
"""
Debug mode management for last-words skill.
When debug mode is enabled, messages can be sent immediately without waiting for 30 days.

Usage:
  python3 debug_mode.py on          # Enable debug mode
  python3 debug_mode.py off         # Disable debug mode
  python3 debug_mode.py status      # Check debug mode status
  python3 debug_mode.py send        # Immediate send in debug mode
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, get_config, get_message
import sqlite3


def get_db_path():
    return Path.home() / ".openclaw" / "last-words" / "data.db"


def set_debug_mode(enabled: bool):
    """Enable or disable debug mode."""
    init_db()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debug_config (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute(
        "INSERT OR REPLACE INTO debug_config (key, value) VALUES ('debug_mode', ?)",
        ("1" if enabled else "0",)
    )

    conn.commit()
    conn.close()

    status = "enabled" if enabled else "disabled"
    print(f"✓ Debug mode {status}")

    if enabled:
        print("  ⚠️  Warning: Messages can now be sent immediately without waiting 30 days")
        print("  💡 Use 'debug_mode.py send' to trigger immediate delivery")


def is_debug_mode():
    """Check if debug mode is enabled."""
    init_db()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT value FROM debug_config WHERE key = 'debug_mode'")
        row = cursor.fetchone()
        conn.close()
        return row is not None and row[0] == "1"
    except:
        conn.close()
        return False


def get_status():
    """Get debug mode status."""
    debug = is_debug_mode()

    print("=" * 50)
    print("Debug Mode Status")
    print("=" * 50)

    if debug:
        print("\n🐛 Debug Mode: ENABLED")
        print("  ⚠️  Messages can be sent immediately")
        print("  💡 Use 'python3 debug_mode.py send' to test delivery")
    else:
        print("\n✓ Debug Mode: DISABLED")
        print("  Normal operation: 30-day inactivity required")

    # Show current config
    config = get_config()
    message = get_message()

    print(f"\n📋 Current Setup:")
    if message:
        print(f"  Message: ✓ Set ({len(message['content'])} chars)")
        if message.get('audio_path'):
            print(f"  Audio: ✓ Attached")
    else:
        print(f"  Message: ✗ Not set")

    if config:
        print(f"  Delivery: {config['method']} → {config['contact']}")
    else:
        print(f"  Delivery: ✗ Not configured")

    print("\n" + "=" * 50)


def immediate_send():
    """Trigger immediate send in debug mode."""
    if not is_debug_mode():
        print("✗ Debug mode is not enabled!")
        print("  Run: python3 debug_mode.py on")
        return False

    config = get_config()
    message = get_message()

    if not message:
        print("✗ No message set!")
        print("  Run: python3 save_message.py --message \"your message\"")
        return False

    if not config:
        print("✗ No delivery configuration!")
        print("  Run: python3 configure_delivery.py --method email --contact \"email@example.com\"")
        return False

    print("🐛 Debug Mode: Triggering immediate send...")
    print("")

    # Import here to avoid circular imports
    from check_activity import deliver_via_email, log_check
    from datetime import datetime

    try:
        success = deliver_via_email(config, message)

        if success:
            # Log the delivery
            log_check(days_inactive=999, warning_sent=False, warning_level=0, delivered=True)
            print("")
            print("✓ Message delivered successfully in DEBUG mode!")
            print(f"  Sent to: {config['contact']}")
            print(f"  Method: {config['method']}")
            if message.get('audio_path'):
                print(f"  Audio: Included")
        else:
            print("✗ Delivery failed")

        return success

    except Exception as e:
        print(f"✗ Delivery failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Debug mode for last-words skill")
    parser.add_argument("command", choices=["on", "off", "status", "send"],
                        help="Command: on/off (toggle), status (check), send (immediate delivery)")

    args = parser.parse_args()

    try:
        if args.command == "on":
            set_debug_mode(True)
        elif args.command == "off":
            set_debug_mode(False)
        elif args.command == "status":
            get_status()
        elif args.command == "send":
            immediate_send()
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
