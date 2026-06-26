#!/usr/bin/env python3
import sys
data = open(sys.argv[1], 'rb').read() if sys.argv[1:] else sys.stdin.buffer.read()
print(data.hex())
