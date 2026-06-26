#!/usr/bin/env python3
"""
Update the last chat timestamp to now.
This should be called whenever the user interacts with the agent.
Usage: python3 update_activity.py
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from database import update_last_chat, init_db


def main():
    try:
        init_db()
        update_last_chat()
        print(f"✓ Activity timestamp updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"✗ Error updating activity: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
