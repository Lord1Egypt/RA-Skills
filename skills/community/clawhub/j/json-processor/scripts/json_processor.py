#!/usr/bin/env python3
"""JSON Processor — query, validate, diff, transform, and format JSON data.

Usage:
  python3 json_processor.py query data.json "$.store.book[*].title"
  python3 json_processor.py validate data.json --schema schema.json
  python3 json_processor.py diff file1.json file2.json
  python3 json_processor.py transform data.json --jq '{items: .[].name}'
  python3 json_processor.py format data.json --indent 2
  python3 json_processor.py flatten data.json
  python3 json_processor.py stats data.json
"""

import argparse
import json
import os
import sys
import re
from collections import Counter
from datetime import datetime


# ─── JSONPath-like Query Engine ──────────────────────────────────────────────

def jsonpath_query(data, path_expr):
    """Simple JSONPath-like query engine.
    Supports: $.key, $.key.subkey, $[0], $[*], $.key[*].sub
    """
    if not path_expr.startswith("$"):
        return None, f"Path must start with '$'"
    path_expr = path_expr[1:]  # strip $
    if not path_expr:
        return data, None

    # Normalize: .key → ['key'], [0] → [0], [*] → [*]
    tokens = []
    i = 0
    while i < len(path_expr):
        c = path_expr[i]
        if c == ".":
            # attribute access
            i += 1
            start = i
            while i < len(path_expr) and path_expr[i] not in ("[", "."):
                i += 1
            key = path_expr[start:i]
            if key:
                tokens.append(("key", key))
        elif c == "[":
            i += 1
            start = i
            while i < len(path_expr) and path_expr[i] != "]":
                i += 1
            val = path_expr[start:i].strip("'\"")
            if val == "*":
                tokens.append(("wildcard",))
            elif val.isdigit():
                tokens.append(("index", int(val)))
            else:
                tokens.append(("key", val))
            i += 1  # skip ]
        else:
            i += 1

    def _resolve(obj, tokens, depth=0):
        if depth >= len(tokens):
            return obj
        token = tokens[depth]
        if token[0] == "key":
            key = token[1]
            if isinstance(obj, dict) and key in obj:
                return _resolve(obj[key], tokens, depth + 1)
            return None
        elif token[0] == "index":
            idx = token[1]
            if isinstance(obj, (list, tuple)) and idx < len(obj):
                return _resolve(obj[idx], tokens, depth + 1)
            return None
        elif token[0] == "wildcard":
            if isinstance(obj, list):
                results = []
                for item in obj:
                    r = _resolve(item, tokens, depth + 1)
                    if r is not None:
                        results.append(r)
                return results
            elif isinstance(obj, dict):
                results = []
                for val in obj.values():
                    r = _resolve(val, tokens, depth + 1)
                    if r is not None:
                        results.append(r)
                return results
            return None
        return None

    result = _resolve(data, tokens)
    if result is None:
        return None, f"Path '{path_expr}' not found"
    return result, None


# ─── JSON Schema Validation (basic) ──────────────────────────────────────────

def validate_schema(data, schema):
    """Basic JSON Schema validation (subset of JSON Schema draft-07)."""
    errors = []

    def _validate(value, schema_node, path=""):
        if not isinstance(schema_node, dict):
            return

        # type check
        if "type" in schema_node:
            type_map = {
                "string": str, "number": (int, float),
                "integer": int, "boolean": bool,
                "array": list, "object": dict, "null": type(None),
            }
            expected = type_map.get(schema_node["type"])
            if expected and not isinstance(value, expected):
                expected_str = schema_node["type"]
                errors.append(f"{path}: expected {expected_str}, got {type(value).__name__}")

        # enum check
        if "enum" in schema_node:
            if value not in schema_node["enum"]:
                errors.append(f"{path}: value {value!r} not in enum {schema_node['enum']}")

        # pattern check (string)
        if "pattern" in schema_node and isinstance(value, str):
            if not re.search(schema_node["pattern"], value):
                errors.append(f"{path}: '{value}' does not match pattern {schema_node['pattern']}")

        # minLength / maxLength (string)
        if isinstance(value, str):
            if "minLength" in schema_node and len(value) < schema_node["minLength"]:
                errors.append(f"{path}: length {len(value)} < minLength {schema_node['minLength']}")
            if "maxLength" in schema_node and len(value) > schema_node["maxLength"]:
                errors.append(f"{path}: length {len(value)} > maxLength {schema_node['maxLength']}")

        # minimum / maximum (number)
        if isinstance(value, (int, float)):
            if "minimum" in schema_node and value < schema_node["minimum"]:
                errors.append(f"{path}: {value} < minimum {schema_node['minimum']}")
            if "maximum" in schema_node and value > schema_node["maximum"]:
                errors.append(f"{path}: {value} > maximum {schema_node['maximum']}")

        # required (object)
        if isinstance(value, dict) and "required" in schema_node:
            for req_key in schema_node["required"]:
                if req_key not in value:
                    errors.append(f"{path}: missing required key '{req_key}'")

        # properties (object)
        if isinstance(value, dict) and "properties" in schema_node:
            for key, prop_schema in schema_node["properties"].items():
                if key in value:
                    _validate(value[key], prop_schema, f"{path}.{key}")

        # items (array)
        if isinstance(value, list) and "items" in schema_node:
            for idx, item in enumerate(value):
                _validate(item, schema_node["items"] if isinstance(schema_node["items"], dict) else schema_node["items"][0] if isinstance(schema_node["items"], list) and schema_node["items"] else {}, f"{path}[{idx}]")

        # additionalProperties
        if isinstance(value, dict) and "properties" in schema_node and "additionalProperties" in schema_node:
            if schema_node["additionalProperties"] is False:
                allowed = set(schema_node["properties"].keys())
                for key in value:
                    if key not in allowed:
                        errors.append(f"{path}: unexpected key '{key}'")

    _validate(data, schema)
    return errors


# ─── JSON Diff ────────────────────────────────────────────────────────────────

def json_diff(a, b, path="$"):
    """Recursive diff between two JSON values."""
    diffs = []
    if type(a) != type(b):
        diffs.append(f"{path}: type mismatch ({type(a).__name__} vs {type(b).__name__})")
        diffs.append(f"  - {json.dumps(a, ensure_ascii=False)[:200]}")
        diffs.append(f"  + {json.dumps(b, ensure_ascii=False)[:200]}")
        return diffs

    if isinstance(a, dict):
        all_keys = set(a.keys()) | set(b.keys())
        for key in sorted(all_keys):
            child_path = f"{path}.{key}"
            if key not in a:
                diffs.append(f"{child_path}: added → {json.dumps(b[key], ensure_ascii=False)[:100]}")
            elif key not in b:
                diffs.append(f"{child_path}: removed ← {json.dumps(a[key], ensure_ascii=False)[:100]}")
            else:
                if a[key] != b[key]:
                    diffs.extend(json_diff(a[key], b[key], child_path))
    elif isinstance(a, list):
        max_len = max(len(a), len(b))
        for i in range(max_len):
            child_path = f"{path}[{i}]"
            if i >= len(a):
                diffs.append(f"{child_path}: added → {json.dumps(b[i], ensure_ascii=False)[:100]}")
            elif i >= len(b):
                diffs.append(f"{child_path}: removed ← {json.dumps(a[i], ensure_ascii=False)[:100]}")
            else:
                if a[i] != b[i]:
                    diffs.extend(json_diff(a[i], b[i], child_path))
    else:
        if a != b:
            diffs.append(f"{path}: {a!r} → {b!r}")

    return diffs


# ─── JSON Transform (jq-like) ────────────────────────────────────────────────

def jq_expression(data, expr):
    """Simple jq-like expression evaluator.
    Supports: .key, .[].key, .key.subkey, .[].{new: .old, ...}
    """
    expr = expr.strip()

    # { items: .[].name }
    if expr.startswith("{") and expr.endswith("}"):
        # Object construction
        inner = expr[1:-1].strip()
        parts = [p.strip() for p in inner.split(",")]
        result = {}
        for part in parts:
            if ":" not in part:
                continue
            k, v = part.split(":", 1)
            k = k.strip().strip("'\"")
            v = v.strip()
            values = _eval_jq_expr(data, v)
            result[k] = values
        return result

    return _eval_jq_expr(data, expr)


def _eval_jq_expr(data, expr):
    """Evaluate a simple jq expression against data."""
    expr = expr.strip()
    if expr == ".":
        return data
    if expr.startswith("."):
        expr = expr[1:]
    if not expr:
        return data

    # Handle .[].key  (array wildcard)
    array_match = re.match(r"^\[\*\]\.(.+)$", expr)
    if array_match:
        if isinstance(data, list):
            sub_key = array_match.group(1)
            r = [_eval_jq_expr(item, f".{sub_key}") for item in data]
            return [x for x in r if x is not None]
        return None

    # Handle .key[].sub
    parts = re.split(r"\.(?![^\[]*\])", expr)
    current = data
    for part in parts:
        if not part:
            continue
        # part might be key[idx] or key[*]
        bracket_match = re.match(r"^([^\[]*)\[(.*)\]$", part)
        if bracket_match:
            key = bracket_match.group(1)
            idx_str = bracket_match.group(2).strip().strip("'\"")
            if key:
                if isinstance(current, dict):
                    current = current.get(key)
                else:
                    return None
            if current is None:
                return None
            if idx_str == "*":
                if isinstance(current, list):
                    continue  # skip to next part
                return None
            elif idx_str.isdigit():
                idx = int(idx_str)
                if isinstance(current, list) and idx < len(current):
                    current = current[idx]
                else:
                    return None
            else:
                # string key in brackets
                if isinstance(current, dict):
                    current = current.get(idx_str)
                else:
                    return None
        else:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
    return current


# ─── Flatten ──────────────────────────────────────────────────────────────────

def flatten_json(data, prefix=""):
    """Flatten nested JSON to dot-notation key-value pairs."""
    items = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, (dict, list)):
                items.extend(flatten_json(value, new_key))
            else:
                items.append((new_key, value))
    elif isinstance(data, list):
        for i, value in enumerate(data):
            new_key = f"{prefix}[{i}]"
            if isinstance(value, (dict, list)):
                items.extend(flatten_json(value, new_key))
            else:
                items.append((new_key, value))
    else:
        items.append((prefix, data))
    return items


# ─── Stats ────────────────────────────────────────────────────────────────────

def json_stats(data, prefix="$"):
    """Calculate statistics about JSON structure."""
    stats = {"nodes": 0, "depth": 0, "types": Counter(), "keys": Counter()}

    def _walk(obj, depth=0):
        stats["nodes"] += 1
        stats["depth"] = max(stats["depth"], depth)
        stats["types"][type(obj).__name__] += 1
        if isinstance(obj, dict):
            for key, val in obj.items():
                stats["keys"][key] += 1
                _walk(val, depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item, depth + 1)

    _walk(data)
    return stats


# ─── Load JSON from file or stdin ────────────────────────────────────────────

def load_json(source):
    """Load JSON from file or string."""
    if source == "-":
        return json.load(sys.stdin)
    if os.path.exists(source):
        with open(source) as f:
            return json.load(f)
    return json.loads(source)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="JSON Processor — query, validate, diff, transform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  json_processor.py query data.json "$.store.book[*].title"
  json_processor.py validate data.json --schema schema.json
  json_processor.py diff old.json new.json
  json_processor.py transform data.json --jq '{names: .[].name}'
  json_processor.py format data.json --indent 2 --output pretty.json
  json_processor.py flatten data.json
  json_processor.py stats data.json
  cat data.json | json_processor.py format -""",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # query
    q = subparsers.add_parser("query", help="JSONPath-style query")
    q.add_argument("file", help="JSON file or '-' for stdin")
    q.add_argument("path", help="JSONPath expression (e.g. $.store.book[*].title)")

    # validate
    v = subparsers.add_parser("validate", help="Validate JSON against schema")
    v.add_argument("file", help="JSON file to validate")
    v.add_argument("--schema", "-s", required=True, help="JSON Schema file")

    # diff
    d = subparsers.add_parser("diff", help="Diff two JSON files")
    d.add_argument("file1", help="Original JSON file")
    d.add_argument("file2", help="New JSON file")

    # transform
    t = subparsers.add_parser("transform", help="jq-like transform")
    t.add_argument("file", help="JSON file or '-' for stdin")
    t.add_argument("--jq", help="jq expression")

    # format
    f = subparsers.add_parser("format", help="Pretty-print JSON")
    f.add_argument("file", help="JSON file or '-' for stdin")
    f.add_argument("--indent", type=int, default=2, help="Indent level (default: 2)")
    f.add_argument("--output", "-o", help="Output file")
    f.add_argument("--sort-keys", action="store_true", help="Sort keys alphabetically")
    f.add_argument("--compact", action="store_true", help="Compact output (no whitespace)")

    # flatten
    fl = subparsers.add_parser("flatten", help="Flatten nested JSON to dot-notation")
    fl.add_argument("file", help="JSON file or '-' for stdin")
    fl.add_argument("--output", "-o", help="Output file")

    # stats
    s = subparsers.add_parser("stats", help="JSON structure statistics")
    s.add_argument("file", help="JSON file or '-' for stdin")

    args = parser.parse_args()

    if args.command == "query":
        data = load_json(args.file)
        result, error = jsonpath_query(data, args.path)
        if error:
            print(f"❌ {error}", file=sys.stderr)
            sys.exit(1)
        if result is None:
            print("null")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "validate":
        data = load_json(args.file)
        schema = load_json(args.schema)
        errors = validate_schema(data, schema)
        if errors:
            print(f"❌ Validation failed ({len(errors)} errors):\n")
            for e in errors:
                print(f"  • {e}")
            sys.exit(1)
        else:
            print(f"✅ Valid — conforms to schema")

    elif args.command == "diff":
        a = load_json(args.file1)
        b = load_json(args.file2)
        diffs = json_diff(a, b)
        if diffs:
            print(f"📋 Differences ({len(diffs)}):\n")
            for d in diffs:
                print(f"  {d}")
        else:
            print("✅ Identical")

    elif args.command == "transform":
        data = load_json(args.file)
        if args.jq:
            result = jq_expression(data, args.jq)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("❌ No --jq expression provided", file=sys.stderr)
            sys.exit(1)

    elif args.command == "format":
        data = load_json(args.file)
        if args.compact:
            output = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        else:
            output = json.dumps(data, indent=args.indent, sort_keys=args.sort_keys, ensure_ascii=False)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output + "\n")
            print(f"📄 Saved: {args.output}")
        else:
            print(output)

    elif args.command == "flatten":
        data = load_json(args.file)
        flat = flatten_json(data)
        result = {k: v for k, v in flat}
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output + "\n")
            print(f"📄 Saved: {args.output}")
        else:
            print(output)

    elif args.command == "stats":
        data = load_json(args.file)
        s = json_stats(data)
        print(f"📊 JSON Statistics\n")
        print(f"  Total nodes:     {s['nodes']}")
        print(f"  Max depth:       {s['depth']}")
        print(f"  Types:")
        for tname, count in s["types"].most_common():
            print(f"    {tname}: {count}")
        if s["keys"]:
            print(f"  Top keys:")
            for key, count in s["keys"].most_common(10):
                print(f"    {key}: {count}")


if __name__ == "__main__":
    main()
