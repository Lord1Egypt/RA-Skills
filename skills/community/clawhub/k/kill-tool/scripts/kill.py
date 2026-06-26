#!/usr/bin/env python3
"""Kill Tool - Kill processes."""
import argparse, os, signal, sys
parser = argparse.ArgumentParser()
parser.add_argument('pid', type=int)
parser.add_argument('-9', action='store_true')
args = parser.parse_args()
try:
    os.kill(args.pid, signal.SIGKILL if args.9 else signal.SIGTERM)
    print(f"Killed process {args.pid}")
except ProcessLookupError: print(f"Process not found: {args.pid}")
except PermissionError: print(f"Permission denied: {args.pid}")
