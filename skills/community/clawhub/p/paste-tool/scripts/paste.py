#!/usr/bin/env python3
import sys
files = [open(f).readlines() for f in sys.argv[1:]] if sys.argv[1:] else [sys.stdin.readlines()]
maxlen = max(len(f) for f in files)
for i in range(maxlen):
    row = [files[j][i].rstrip('\n') if i < len(files[j]) else '' for j in range(len(files))]
    print('\t'.join(row))
