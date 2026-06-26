#!/usr/bin/env python3
"""Mkdir Tool - Create directories."""
import argparse, os, sys
parser = argparse.ArgumentParser()
parser.add_argument('dirs', nargs='+')
parser.add_argument('--parents', '-p', action='store_true')
args = parser.parse_args()
for d in args.dirs:
    try:
        os.makedirs(d, exist_ok=True) if args.parents else os.mkdir(d)
        print(f"Created: {d}")
    except Exception as e: print(f"Error: {e}", file=sys.stderr)
