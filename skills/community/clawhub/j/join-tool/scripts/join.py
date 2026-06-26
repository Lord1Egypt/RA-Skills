#!/usr/bin/env python3
import sys
if len(sys.argv)<3: print("Usage: join.py f1 f2"); sys.exit(1)
l1=open(sys.argv[1]).readlines()
l2=open(sys.argv[2]).readlines()
for a,b in zip(l1,l2): print(a.rstrip()+b.rstrip())
