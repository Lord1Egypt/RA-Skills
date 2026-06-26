#!/usr/bin/env python3
import argparse
import os
import sys
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-file", dest="pr_file", required=True)
    parser.add_argument("--status", choices=["open", "closed", "blocked", "in_progress", "completed"], required=True)
    args = parser.parse_args()

    pr_file = args.pr_file
    new_status = args.status

    if not os.path.exists(pr_file):
        print(f"[Pre-flight Failed] Cannot update status. PR file '{pr_file}' not found.")
        sys.exit(1)

    try:
        with open(pr_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    if not re.search(r'^status:\s*\S+', content, re.MULTILINE):
        print(f"[Pre-flight Failed] File '{pr_file}' does not contain a 'status: ...' field.")
        sys.exit(1)

    updated_content = re.sub(r'^status:\s*\S+', f'status: {new_status}', content, count=1, flags=re.MULTILINE)

    try:
        with open(pr_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

    print(f"[STATUS_UPDATED] {pr_file} is now {new_status}.")
    sys.exit(0)

if __name__ == "__main__":
    main()
