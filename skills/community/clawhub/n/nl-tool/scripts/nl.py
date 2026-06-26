#!/usr/bin/env python3
import sys
for i, line in enumerate(open(sys.argv[1] if len(sys.argv)>1 else sys.stdin.read()), 1):
    print(f"{i:6d}  {line.rstrip()}")
