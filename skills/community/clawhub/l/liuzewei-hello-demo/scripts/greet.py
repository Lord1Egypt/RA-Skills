#!/usr/bin/env python3
"""
Hello Demo - A simple greeting skill for OpenClaw
Author: wwwzhouhui
Version: 1.0.0
"""

import argparse
import sys
from datetime import datetime


def get_greeting(hour=None):
    """Get time-appropriate greeting"""
    if hour is None:
        hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    elif 18 <= hour < 22:
        return "Good evening"
    else:
        return "Hello"


def main():
    parser = argparse.ArgumentParser(
        description="A friendly greeting skill for OpenClaw"
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name to greet (default: World)"
    )
    parser.add_argument(
        "--time", "-t",
        action="store_true",
        help="Include time-appropriate greeting"
    )
    parser.add_argument(
        "--emoji", "-e",
        action="store_true",
        help="Add friendly emoji"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Build greeting
    if args.time:
        greeting = get_greeting()
    else:
        greeting = "Hello"
    
    # Construct message
    message = f"{greeting}, {args.name}!"
    
    if args.emoji:
        message += " 👋"
    
    print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
