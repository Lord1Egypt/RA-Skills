#!/usr/bin/env python3
"""
Anatomy Context Injector
Checks if .anatomy.md exists and is fresh; if stale (>24h), triggers rescan.
Outputs the anatomy content for session context injection.

Usage:
    python3 anatomy_inject.py <project-path> [--max-age-hours 24] [--format compact]
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

SCRIPT_DIR = Path(__file__).parent
SCANNER = SCRIPT_DIR / 'anatomy_scan.py'


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Inject anatomy context')
    parser.add_argument('project_path', help='Project directory')
    parser.add_argument('--max-age-hours', type=int, default=24,
                        help='Max age before rescan (default: 24h)')
    parser.add_argument('--format', '-f', default='compact',
                        choices=['table', 'compact', 'summary'])
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Only output the anatomy content')
    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()
    anatomy_path = project_path / '.anatomy.md'

    needs_scan = False
    if not anatomy_path.exists():
        needs_scan = True
        if not args.quiet:
            print("[anatomy] No index found, scanning...")
    else:
        mtime = datetime.fromtimestamp(anatomy_path.stat().st_mtime)
        age = datetime.now() - mtime
        if age > timedelta(hours=args.max_age_hours):
            needs_scan = True
            if not args.quiet:
                print(f"[anatomy] Index stale ({age.total_seconds()//3600:.0f}h old), rescanning...")

    if needs_scan:
        cmd = [
            sys.executable, str(SCANNER),
            str(project_path),
            '--format', args.format,
            '--incremental',
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if not args.quiet and result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.returncode != 0:
            print(f"[anatomy] Scan failed: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    # Output the anatomy content
    if anatomy_path.exists():
        print(anatomy_path.read_text())
    else:
        print("[anatomy] No index available", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
