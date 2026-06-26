#!/usr/bin/env python3
"""Decompress base64+zstd from JSON. Usage: python _decompress.py [file] or stdin"""
import sys, json, base64
try:
    import zstandard
except ImportError:
    sys.exit(1)
src = open(sys.argv[1], encoding='utf-8') if len(sys.argv) > 1 else sys.stdin
j = json.load(src)
if src is not sys.stdin:
    src.close()
b = base64.b64decode(j.get('data', ''))
print(zstandard.ZstdDecompressor().decompress(b, max_output_size=10485760).decode('utf-8'), end='')
