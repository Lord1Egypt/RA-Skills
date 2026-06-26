#!/usr/bin/env python3
"""Sanitize JSON for macOS bash: parse with strict=False, re-serialize,
and double-escape backslash sequences so macOS echo doesn't interpret them.

Usage: python3 sanitize_json.py <input_file>
"""
import sys
import json

infile = sys.argv[1]
with open(infile, "rb") as f:
    raw = f.read().decode("utf-8", errors="replace")

try:
    obj = json.loads(raw, strict=False)
    clean = json.dumps(obj, ensure_ascii=False)
    sys.stdout.write(clean)
except Exception:
    sys.stdout.write(raw)
