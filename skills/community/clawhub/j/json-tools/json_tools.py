#!/usr/bin/env python3
"""
JSON Power Tools — a Swiss-army-knife CLI for JSON files.

Commands: validate, format, query, diff, filter, stats, flatten, merge
Zero dependencies (Python stdlib only).
"""

import json
import sys
import os
from collections import Counter


# ── helpers ──────────────────────────────────────────────────────────────

def load_json(path):
    """Load JSON from file or stdin ('-' denotes stdin)."""
    if path == "-":
        return json.load(sys.stdin)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ── commands ─────────────────────────────────────────────────────────────

def cmd_validate(args):
    """Validate JSON file(s). Exits 1 on invalid."""
    exit_code = 0
    for path in args.paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
            print(f"\u2705 {path}: valid JSON")
        except json.JSONDecodeError as e:
            print(f"\u274c {path}: invalid JSON \u2014 {e}", file=sys.stderr)
            exit_code = 1
        except FileNotFoundError:
            print(f"\u274c {path}: file not found", file=sys.stderr)
            exit_code = 1
    sys.exit(exit_code)


def cmd_format(args):
    """Pretty-print JSON with configurable indentation."""
    data = load_json(args.path)
    indent = args.indent or 2
    print(json.dumps(data, indent=indent, ensure_ascii=args.ascii))


def cmd_query(args):
    """Extract values using dot-notation paths."""
    data = load_json(args.file)
    keys = args.dot_path.split(".")
    current = data
    for key in keys:
        try:
            if key.lstrip("-").isdigit() and isinstance(current, list):
                current = current[int(key)]
            elif isinstance(current, dict):
                current = current[key]
            else:
                print(f"\u274c Key '{key}' not found in {type(current).__name__}", file=sys.stderr)
                sys.exit(1)
        except (IndexError, KeyError, TypeError):
            print(f"\u274c Cannot traverse '{key}' in {type(current).__name__}", file=sys.stderr)
            sys.exit(1)
    print(json.dumps(current, indent=2, ensure_ascii=False))


def cmd_diff(args):
    """Show structural differences between two JSON files."""
    data_a = load_json(args.file_a)
    data_b = load_json(args.file_b)
    diffs = deep_diff(data_a, data_b, path="")
    if not diffs:
        print("\u2705 Files are identical")
        sys.exit(0)
    for d in diffs:
        kind = d["kind"]
        p = d["path"]
        if kind == "removed":
            print(f"\033[91m- {p}: {json.dumps(d['value'])}\033[0m")
        elif kind == "added":
            print(f"\033[92m+ {p}: {json.dumps(d['value'])}\033[0m")
        elif kind == "changed":
            print(f"\033[93m~ {p}: {json.dumps(d['old'])} \u2192 {json.dumps(d['new'])}\033[0m")
    sys.exit(1)


def deep_diff(a, b, path=""):
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        all_keys = set(a.keys()) | set(b.keys())
        for k in sorted(all_keys):
            p = f"{path}.{k}" if path else k
            if k not in a:
                diffs.append({"kind": "added", "path": p, "value": b[k]})
            elif k not in b:
                diffs.append({"kind": "removed", "path": p, "value": a[k]})
            else:
                diffs.extend(deep_diff(a[k], b[k], p))
    elif isinstance(a, list) and isinstance(b, list):
        max_len = max(len(a), len(b))
        for i in range(max_len):
            p = f"{path}[{i}]"
            if i >= len(a):
                diffs.append({"kind": "added", "path": p, "value": b[i]})
            elif i >= len(b):
                diffs.append({"kind": "removed", "path": p, "value": a[i]})
            else:
                diffs.extend(deep_diff(a[i], b[i], p))
    elif a != b:
        diffs.append({"kind": "changed", "path": path or "(root)", "old": a, "new": b})
    return diffs


def cmd_filter(args):
    """Filter arrays by a key-value condition."""
    data = load_json(args.file)
    if not isinstance(data, list):
        print(f"\u274c filter expects a JSON array (got {type(data).__name__})", file=sys.stderr)
        sys.exit(1)
    key = args.key
    value = args.value
    try:
        value = json.loads(value)
    except (json.JSONDecodeError, TypeError):
        pass
    filtered = [item for item in data if isinstance(item, dict) and item.get(key) == value]
    print(json.dumps(filtered, indent=2, ensure_ascii=False))


def cmd_stats(args):
    """Compute statistics for a JSON file."""
    data = load_json(args.file)
    stats = compute_stats(data)
    print(json.dumps(stats, indent=2, ensure_ascii=False))


def compute_stats(data):
    result = {}
    if isinstance(data, dict):
        result["type"] = "object"
        result["key_count"] = len(data)
        type_counts = Counter(type(v).__name__ for v in data.values())
        result["value_types"] = dict(type_counts)
        max_depth = 1
        for v in data.values():
            child = compute_stats(v)
            if "max_depth" in child:
                max_depth = max(max_depth, 1 + child["max_depth"])
        result["max_depth"] = max_depth
    elif isinstance(data, list):
        result["type"] = "array"
        result["length"] = len(data)
        type_counts = Counter(type(v).__name__ for v in data)
        result["value_types"] = dict(type_counts)
        max_depth = 1
        for v in data:
            child = compute_stats(v)
            if "max_depth" in child:
                max_depth = max(max_depth, 1 + child["max_depth"])
        result["max_depth"] = max_depth
    else:
        result["type"] = type(data).__name__
        result["value"] = data
        result["max_depth"] = 0
    return result


def cmd_flatten(args):
    """Convert nested JSON to flat key-value pairs."""
    data = load_json(args.file)
    sep = args.separator or "."
    flat = {}
    do_flatten(data, "", flat, sep)
    print(json.dumps(flat, indent=2, ensure_ascii=False))


def do_flatten(data, prefix, flat, sep):
    if isinstance(data, dict):
        for k, v in data.items():
            p = f"{prefix}{sep}{k}" if prefix else str(k)
            if isinstance(v, (dict, list)):
                do_flatten(v, p, flat, sep)
            else:
                flat[p] = v
    elif isinstance(data, list):
        for i, v in enumerate(data):
            p = f"{prefix}[{i}]"
            if isinstance(v, (dict, list)):
                do_flatten(v, p, flat, sep)
            else:
                flat[p] = v
    else:
        flat[prefix] = data


def cmd_merge(args):
    """Deep-merge two or more JSON files."""
    if len(args.files) < 2:
        print("\u274c merge requires at least 2 files", file=sys.stderr)
        sys.exit(1)
    result = load_json(args.files[0])
    for path in args.files[1:]:
        data = load_json(path)
        result = deep_merge(result, data)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\u2705 Merged {len(args.files)} files \u2192 {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def deep_merge(a, b):
    """Recursively merge b into a."""
    if isinstance(a, dict) and isinstance(b, dict):
        result = dict(a)
        for k in b:
            if k in result:
                result[k] = deep_merge(result[k], b[k])
            else:
                result[k] = b[k]
        return result
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    return b


# ── argparse ─────────────────────────────────────────────────────────────

def build_parser():
    import argparse
    parser = argparse.ArgumentParser(
        description="JSON Power Tools \u2014 validate, format, query, diff, filter, stats, flatten, merge"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="Check if JSON file(s) are well-formed")
    p.add_argument("paths", nargs="+", metavar="FILE", help="JSON files to validate")

    p = sub.add_parser("format", help="Pretty-print JSON")
    p.add_argument("path", help="JSON file path (use - for stdin)")
    p.add_argument("--indent", type=int, default=2, help="Indentation spaces")
    p.add_argument("--ascii", action="store_true", help="Ensure ASCII output")

    p = sub.add_parser("query", help="Query JSON using dot-notation path")
    p.add_argument("file", help="JSON file path")
    p.add_argument("--path", "-p", dest="dot_path", required=True, help="Dot-notation path e.g. users.0.name")

    p = sub.add_parser("diff", help="Show differences between two JSON files")
    p.add_argument("file_a", metavar="FILE_A", help="First JSON file")
    p.add_argument("file_b", metavar="FILE_B", help="Second JSON file")

    p = sub.add_parser("filter", help="Filter array by key=value")
    p.add_argument("file", help="JSON file path (must contain an array)")
    p.add_argument("--key", required=True, help="Key to filter on")
    p.add_argument("--value", required=True, help="Value to match")

    p = sub.add_parser("stats", help="Compute JSON statistics")
    p.add_argument("file", help="JSON file path")

    p = sub.add_parser("flatten", help="Flatten nested JSON to key-value pairs")
    p.add_argument("file", help="JSON file path")
    p.add_argument("--separator", default=".", help="Key separator")

    p = sub.add_parser("merge", help="Deep-merge multiple JSON files")
    p.add_argument("files", nargs="+", metavar="FILE", help="Files to merge (first is base)")
    p.add_argument("--output", "-o", help="Output file (default: stdout)")

    sub.add_parser("self-test", help="Run built-in self tests")

    return parser


def _self_test():
    """Real test of deep_diff, deep_merge, and compute_stats. Returns 0/1."""
    import io
    import contextlib

    # 1. deep_diff: a changed + added field.
    diffs = deep_diff({"a": 1, "b": 2}, {"a": 1, "b": 3, "c": 4})
    kinds = {d["kind"] for d in diffs}
    if "changed" not in kinds or "added" not in kinds:
        print(f"self-test: FAIL (deep_diff kinds: {kinds})")
        return 1

    # 2. deep_merge: nested dicts merge, lists concatenate.
    merged = deep_merge({"x": {"y": 1}}, {"x": {"z": 2}, "w": [1]})
    if merged.get("x", {}).get("y") != 1 or merged.get("x", {}).get("z") != 2:
        print("self-test: FAIL (deep_merge dict merge)")
        return 1
    if merged.get("w") != [1]:
        print("self-test: FAIL (deep_merge base list)")
        return 1
    merged2 = deep_merge({"w": [1]}, {"w": [2]})
    if merged2["w"] != [1, 2]:
        print("self-test: FAIL (deep_merge list concat)")
        return 1

    # 3. compute_stats on nested structure.
    stats = compute_stats({"k": [1, {"n": 2}]})
    if stats.get("type") != "object" or stats.get("key_count") != 1:
        print("self-test: FAIL (compute_stats object)")
        return 1
    if stats.get("max_depth") < 2:
        print("self-test: FAIL (compute_stats depth)")
        return 1

    # 4. do_flatten produces dotted keys.
    flat = {}
    do_flatten({"a": {"b": 1}}, "", flat, ".")
    if flat.get("a.b") != 1:
        print(f"self-test: FAIL (do_flatten: {flat})")
        return 1

    print("self-test: PASS")
    return 0


def main():
    parser = build_parser()
    args = parser.parse_args()
    cmds = {
        "validate": cmd_validate,
        "format": cmd_format,
        "query": cmd_query,
        "diff": cmd_diff,
        "filter": cmd_filter,
        "stats": cmd_stats,
        "flatten": cmd_flatten,
        "merge": cmd_merge,
    }
    if args.command == "self-test":
        sys.exit(_self_test())
    cmds[args.command](args)


if __name__ == "__main__":
    main()
