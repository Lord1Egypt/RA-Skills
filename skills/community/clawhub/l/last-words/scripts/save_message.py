#!/usr/bin/env python3
"""
Save or update the final message.
Usage: python3 save_message.py --message "content" [--audio-path /path/to/audio]
"""

import argparse
import sys
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database import save_message, init_db


def main():
    parser = argparse.ArgumentParser(description="Save final message")
    parser.add_argument("--message", "-m", required=True, help="Message content (text)")
    parser.add_argument("--audio-path", "-a", help="Path to audio file (optional)")

    args = parser.parse_args()

    try:
        init_db()
        save_message(args.message, args.audio_path)
        print(f"✓ Message saved successfully")
        print(f"  Content: {args.message[:50]}{'...' if len(args.message) > 50 else ''}")
        if args.audio_path:
            print(f"  Audio: {args.audio_path}")
    except Exception as e:
        print(f"✗ Error saving message: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
