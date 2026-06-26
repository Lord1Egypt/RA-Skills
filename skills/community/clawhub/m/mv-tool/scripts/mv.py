#!/usr/bin/env python3
"""Mv Tool - Move files."""
import argparse, shutil, sys
parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('dst')
args = parser.parse_args()
try:
    shutil.move(args.src, args.dst)
    print(f"Moved: {args.src} -> {args.dst}")
except Exception as e: print(f"Error: {e}", file=sys.stderr)
