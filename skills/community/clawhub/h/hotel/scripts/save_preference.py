#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_preferences, save_preferences

def main():
    parser = argparse.ArgumentParser(description="Save hotel preference")
    parser.add_argument("--key", required=True)
    parser.add_argument("--value", required=True)
    args = parser.parse_args()

    data = load_preferences()
    data["preferences"][args.key] = args.value
    save_preferences(data)

    print(f"✓ Preference saved")
    print(f"  {args.key} = {args.value}")

if __name__ == "__main__":
    main()
