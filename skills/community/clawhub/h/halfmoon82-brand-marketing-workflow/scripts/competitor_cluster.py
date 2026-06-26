#!/usr/bin/env python3
"""Cluster competitor signals into simple theme buckets."""
from __future__ import annotations
import json
import sys
from collections import defaultdict

THEME_KEYS = ["theme", "format", "tone", "frequency", "hook"]

def main() -> int:
    raw = sys.stdin.read().strip()
    items = json.loads(raw) if raw else []
    buckets = defaultdict(list)
    for item in items:
        theme = item.get("theme", "unknown")
        buckets[theme].append(item)
    print(json.dumps({"themes": dict(buckets), "theme_keys": THEME_KEYS}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
