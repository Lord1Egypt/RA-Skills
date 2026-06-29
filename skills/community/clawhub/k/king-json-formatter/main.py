#!/usr/bin/env python3
"""JSON Formatter & Validator — beautify, minify, validate, batch."""
import json, sys, os

VERSION = "1.0.0"

def format_json(data, indent=2, sort_keys=False):
    return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

def minify_json(data):
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

if __name__ == '__main__':
    if "--version" in sys.argv: print(VERSION); sys.exit(0)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    
    if not args:
        print(f"""JSON Formatter v{VERSION}
Usage: json-formatter <file> [options]
Options: --minify  --validate  --indent N  --sort-keys  --batch  --to-yaml  --to-xml
Free: format, minify, validate, color output
Pro ($0.99): error pinpointing, batch, export, key sort, custom indent""")
        sys.exit(0)
    
    for path in args:
        try:
            with open(path) as f: data = json.load(f)
            if "--minify" in sys.argv: result = minify_json(data)
            else: result = format_json(data, sort_keys="--sort-keys" in sys.argv)
            print(result)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)
