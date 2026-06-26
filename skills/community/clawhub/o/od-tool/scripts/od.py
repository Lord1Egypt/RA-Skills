#!/usr/bin/env python3
import sys
data=open(sys.argv[1] if len(sys.argv)>1 else sys.stdin.read(),'rb').read()
for i in range(0,len(data),16):
    print(f'{i:07o} ', end='')
    for b in data[i:i+16]: print(f'{b:03o}', end=' ')
    print()
