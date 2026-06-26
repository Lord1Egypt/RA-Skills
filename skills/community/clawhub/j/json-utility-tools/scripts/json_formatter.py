#!/usr/bin/env python3
"""JSON Formatter Pro - Format, validate, minify, query, diff, sort JSON"""
import json, sys, re, argparse

def format_json(data, indent=2, sort=False):
    obj = json.loads(data)
    if sort:
        obj = sort_keys(obj)
    return json.dumps(obj, indent=indent, ensure_ascii=False)

def minify(data):
    obj = json.loads(data)
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=False)

def validate(data):
    try:
        json.loads(data)
        return "✓ Valid JSON"
    except json.JSONDecodeError as e:
        return f"✗ Invalid JSON: {e.msg} at line {e.lineno}, col {e.colno}"

def query(data, path):
    obj = json.loads(data)
    # Simple JSONPath-like query: $.users[*].name -> extract nested keys
    parts = path.strip('$').split('.')
    result = obj
    for p in parts:
        p = p.strip('[]*')
        if p.isdigit():
            result = result[int(p)]
        elif isinstance(result, list):
            result = [item.get(p, None) for item in result if isinstance(item, dict)]
        elif isinstance(result, dict):
            result = result.get(p, None)
        else:
            return "[]"
    return json.dumps(result, ensure_ascii=False)

def diff(a, b):
    obj_a = json.loads(a)
    obj_b = json.loads(b)
    changes = []
    all_keys = set(json.dumps(obj_a, sort_keys=True)) | set(json.dumps(obj_b, sort_keys=True))
    a_str = json.dumps(obj_a, sort_keys=True)
    b_str = json.dumps(obj_b, sort_keys=True)
    if a_str == b_str:
        return "✓ No differences"
    # Simple comparison
    if obj_a != obj_b:
        return f"✗ Objects differ:\n  A: {json.dumps(obj_a, ensure_ascii=False)[:100]}\n  B: {json.dumps(obj_b, ensure_ascii=False)[:100]}"
    return "✓ No differences"

def sort_keys(obj):
    if isinstance(obj, dict):
        return {k: sort_keys(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        return [sort_keys(i) for i in obj]
    return obj

def main():
    if len(sys.argv) < 3:
        print("Usage: json_formatter.py <action> <data> [extra]", file=sys.stderr)
        print("Actions: format | minify | validate | query | diff | sort")
        sys.exit(1)
    action = sys.argv[1].lower()
    data = sys.argv[2]
    extra = sys.argv[3] if len(sys.argv) > 3 else None
    try:
        if action == "format":
            indent = int(extra) if extra else 2
            print(format_json(data, indent))
        elif action == "minify":
            print(minify(data))
        elif action == "validate":
            print(validate(data))
        elif action == "query":
            if not extra:
                print("Query requires a path", file=sys.stderr)
                sys.exit(1)
            print(query(data, extra))
        elif action == "diff":
            if not extra:
                print("Diff requires two JSON strings", file=sys.stderr)
                sys.exit(1)
            print(diff(data, extra))
        elif action == "sort":
            print(format_json(data, sort=True))
        else:
            print(f"Unknown action: {action}", file=sys.stderr)
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e.msg} at line {e.lineno}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
