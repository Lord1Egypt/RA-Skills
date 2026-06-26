#!/usr/bin/env python3
"""Ls Tool - List files."""
import argparse, os
parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default='.')
parser.add_argument('-l', action='store_true')
args = parser.parse_args()
for f in sorted(os.listdir(args.path)):
    if args.l:
        stat = os.stat(os.path.join(args.path, f))
        print(f"{stat.st_size:>10} {f}")
    else:
        print(f)
