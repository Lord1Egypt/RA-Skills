#!/usr/bin/env python3
"""jsonpretty — JSON formatter, validator, query, and stats. Zero dependencies."""
import json, sys, argparse, os
from collections import Counter

def flatten(obj, prefix="", sep="."):
    """Flatten nested JSON into dot-notation key-value pairs."""
    items = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{prefix}{sep}{k}" if prefix else k
            items.update(flatten(v, new_key, sep))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{prefix}[{i}]"
            items.update(flatten(v, new_key, sep))
    else:
        items[prefix] = obj
    return items

def query_path(obj, path):
    """Simple dot-notation query: 'key.subkey[0].name'"""
    import re
    parts = re.split(r'\.(?![^\[]*\])', path)
    current = obj
    for part in parts:
        m = re.match(r'(.+?)\[(\d+)\]$', part)
        if m:
            key, idx = m.group(1), int(m.group(2))
            current = current[key][idx]
        elif isinstance(current, dict):
            current = current[part]
        elif isinstance(current, list) and part.isdigit():
            current = current[int(part)]
        else:
            return None
    return current

def stats(obj):
    """Compute stats about a JSON structure."""
    flat = flatten(obj)
    types = Counter(type(v).__name__ for v in flat.values())
    return {
        "keys": len(flat),
        "depth": max((k.count(".") + k.count("[") for k in flat), default=0),
        "types": dict(types),
        "size_bytes": len(json.dumps(obj)),
    }

def main():
    p = argparse.ArgumentParser(prog="jsonpretty", description="JSON formatter, validator, query, stats")
    p.add_argument("file", nargs="?", help="JSON file (reads stdin if omitted)")
    p.add_argument("-q", "--query", help="Dot-notation query path")
    p.add_argument("--flat", action="store_true", help="Flatten to dot-notation")
    p.add_argument("--stats", action="store_true", help="Show structure stats")
    p.add_argument("--compact", action="store_true", help="Compact output (no indent)")
    p.add_argument("--sort", action="store_true", help="Sort keys")
    p.add_argument("--validate", action="store_true", help="Validate only (exit code)")
    args = p.parse_args()

    try:
        raw = open(args.file).read() if args.file else sys.stdin.read()
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        if args.validate:
            print(f"❌ Invalid JSON: {e}")
            sys.exit(1)
        print(f"Error: Invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    if args.validate:
        print(f"✅ Valid JSON ({len(raw)} bytes)")
        sys.exit(0)

    if args.query:
        result = query_path(obj, args.query)
        print(json.dumps(result, indent=None if args.compact else 2, sort_keys=args.sort))
        return

    if args.stats:
        s = stats(obj)
        print(f"📊 Keys: {s['keys']}  Depth: {s['depth']}  Size: {s['size_bytes']} bytes")
        print(f"   Types: {s['types']}")
        return

    if args.flat:
        flat = flatten(obj)
        for k, v in flat.items():
            print(f"{k} = {json.dumps(v)}")
        return

    indent = None if args.compact else 2
    print(json.dumps(obj, indent=indent, sort_keys=args.sort, ensure_ascii=False))

if __name__ == "__main__":
    main()
