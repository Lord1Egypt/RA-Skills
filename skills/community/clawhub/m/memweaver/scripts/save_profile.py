#!/usr/bin/env python3
"""
MemWeaver — Profile Save Script

Receives a YAML-formatted user profile from stdin or file,
saves it to the output directory with automatic backup of old profiles.

Usage:
    echo '<yaml>' | python3 save_profile.py
    python3 save_profile.py --file profile_draft.yaml
    python3 save_profile.py --output custom_path.yaml --stdin

Exit codes:
    0  Success
    1  Argument error or write failure
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="MemWeaver Profile Saver")
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: output/profile_YYYYMMDD.yaml)",
    )
    parser.add_argument(
        "--file",
        default=None,
        help="Read profile content from file (alternative to stdin)",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        default=False,
        help="Read profile content from stdin",
    )
    return parser.parse_args()


def find_workspace(script_dir):
    """Walk up from script directory to find workspace root"""
    current = Path(script_dir).resolve()
    for _ in range(5):
        if (current / ".codebuddy").is_dir():
            return current
        current = current.parent
    return None


def main():
    args = parse_args()

    # Read profile content
    content = None
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # Default: read from stdin
        if sys.stdin.isatty():
            print("Error: Please provide profile content via stdin or --file", file=sys.stderr)
            sys.exit(1)
        content = sys.stdin.read()

    if not content or not content.strip():
        print("Error: Profile content is empty", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = Path(script_dir).parent
        output_dir = skill_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        output_path = output_dir / f"profile_{today}.yaml"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Backup old file if exists
    if output_path.exists():
        backup_path = output_path.with_suffix(".yaml.bak")
        shutil.copy2(output_path, backup_path)
        print(f"📦 Backed up old profile: {backup_path.name}", file=sys.stderr)

    # Write
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Profile saved: {output_path}", file=sys.stderr)
    print(f"   Content: {len(content.splitlines())} lines", file=sys.stderr)

    # Output path to stdout for Agent reference
    print(str(output_path))


if __name__ == "__main__":
    main()
