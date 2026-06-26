#!/usr/bin/env python3
"""JSONPath Query Tool — Query JSON data using JSONPath expressions."""

import argparse
import json
import re
import sys

VERSION = "1.0.0"


class JSONPathError(Exception):
    pass


def tokenize(expr):
    """Tokenize a JSONPath expression into segments."""
    if not expr or expr == "$":
        return []

    # Remove leading $
    if expr.startswith("$"):
        expr = expr[1:]

    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]

        if c == '.':
            i += 1
            if i < len(expr) and expr[i] == '.':
                # Recursive descent
                tokens.append(("recurse", None))
                i += 1
            # Read key name
            start = i
            while i < len(expr) and expr[i] not in '.[]':
                i += 1
            key = expr[start:i]
            if key == '*':
                tokens.append(("wildcard", None))
            elif key:
                tokens.append(("key", key))

        elif c == '[':
            i += 1
            # Read until ]
            depth = 1
            start = i
            while i < len(expr) and depth > 0:
                if expr[i] == '[':
                    depth += 1
                elif expr[i] == ']':
                    depth -= 1
                i += 1
            content = expr[start:i - 1].strip()

            if content == '*':
                tokens.append(("wildcard", None))
            elif content.startswith("?"):
                tokens.append(("filter", content[1:].strip()))
            elif ':' in content:
                # Slice [start:end:step]
                parts = content.split(':')
                s = int(parts[0]) if parts[0].strip() else None
                e = int(parts[1]) if len(parts) > 1 and parts[1].strip() else None
                step = int(parts[2]) if len(parts) > 2 and parts[2].strip() else None
                tokens.append(("slice", (s, e, step)))
            elif ',' in content:
                # Union [key1,key2] or [0,1,2]
                items = [x.strip().strip("'\"") for x in content.split(',')]
                tokens.append(("union", items))
            elif (content.startswith("'") and content.endswith("'")) or \
                 (content.startswith('"') and content.endswith('"')):
                tokens.append(("key", content[1:-1]))
            else:
                try:
                    tokens.append(("index", int(content)))
                except ValueError:
                    tokens.append(("key", content))
        else:
            # Bare key at start
            start = i
            while i < len(expr) and expr[i] not in '.[]':
                i += 1
            key = expr[start:i]
            if key == '*':
                tokens.append(("wildcard", None))
            elif key:
                tokens.append(("key", key))

    return tokens


def eval_filter(node, expr):
    """Evaluate a filter expression like (@.price < 10)."""
    expr = expr.strip()
    if expr.startswith("(") and expr.endswith(")"):
        expr = expr[1:-1].strip()

    # Simple comparison: @.field op value
    m = re.match(r'@\.(\w+(?:\.\w+)*)\s*(==|!=|<=|>=|<|>)\s*(.+)', expr)
    if m:
        field_path = m.group(1).split('.')
        op = m.group(2)
        raw_val = m.group(3).strip().strip("'\"")

        # Navigate to field
        current = node
        for f in field_path:
            if isinstance(current, dict) and f in current:
                current = current[f]
            else:
                return False

        # Try numeric comparison
        try:
            left = float(current) if not isinstance(current, bool) else current
            right = float(raw_val)
        except (ValueError, TypeError):
            left = str(current)
            right = raw_val

        ops = {
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<': lambda a, b: a < b,
            '>': lambda a, b: a > b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
        }
        return ops[op](left, right)

    # Existence check: @.field
    m = re.match(r'@\.(\w+)', expr)
    if m:
        field = m.group(1)
        return isinstance(node, dict) and field in node

    return False


def query(data, tokens, idx=0):
    """Execute tokenized JSONPath query recursively."""
    if idx >= len(tokens):
        return [data]

    token_type, token_val = tokens[idx]

    results = []

    if token_type == "key":
        if isinstance(data, dict) and token_val in data:
            results.extend(query(data[token_val], tokens, idx + 1))

    elif token_type == "index":
        if isinstance(data, (list, tuple)):
            try:
                results.extend(query(data[token_val], tokens, idx + 1))
            except IndexError:
                pass

    elif token_type == "wildcard":
        if isinstance(data, dict):
            for v in data.values():
                results.extend(query(v, tokens, idx + 1))
        elif isinstance(data, (list, tuple)):
            for item in data:
                results.extend(query(item, tokens, idx + 1))

    elif token_type == "recurse":
        # Apply remaining tokens at this level and all nested levels
        results.extend(query(data, tokens, idx + 1))
        if isinstance(data, dict):
            for v in data.values():
                results.extend(query(v, tokens, idx))
        elif isinstance(data, (list, tuple)):
            for item in data:
                results.extend(query(item, tokens, idx))

    elif token_type == "slice":
        if isinstance(data, (list, tuple)):
            s, e, step = token_val
            sliced = data[s:e:step]
            for item in sliced:
                results.extend(query(item, tokens, idx + 1))

    elif token_type == "union":
        for item_key in token_val:
            if isinstance(data, dict) and item_key in data:
                results.extend(query(data[item_key], tokens, idx + 1))
            elif isinstance(data, (list, tuple)):
                try:
                    i = int(item_key)
                    results.extend(query(data[i], tokens, idx + 1))
                except (ValueError, IndexError):
                    pass

    elif token_type == "filter":
        if isinstance(data, (list, tuple)):
            for item in data:
                if eval_filter(item, token_val):
                    results.extend(query(item, tokens, idx + 1))
        elif isinstance(data, dict):
            if eval_filter(data, token_val):
                results.extend(query(data, tokens, idx + 1))

    return results


def jsonpath(data, expression):
    """Execute a JSONPath expression against JSON data."""
    tokens = tokenize(expression)
    return query(data, tokens)


def cmd_query(args):
    """Query JSON data with a JSONPath expression."""
    # Read JSON input
    if args.file:
        try:
            with open(args.file) as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
            sys.exit(1)

    results = jsonpath(data, args.expression)

    if args.first:
        results = results[:1]

    if args.count:
        print(len(results))
        return

    if args.format == "json":
        if len(results) == 1 and not args.always_array:
            print(json.dumps(results[0], indent=2, ensure_ascii=False))
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.format == "lines":
        for r in results:
            if isinstance(r, (dict, list)):
                print(json.dumps(r, ensure_ascii=False))
            else:
                print(r)
    elif args.format == "csv":
        if results and isinstance(results[0], dict):
            keys = list(results[0].keys())
            print(",".join(keys))
            for r in results:
                if isinstance(r, dict):
                    print(",".join(str(r.get(k, "")) for k in keys))
        else:
            for r in results:
                print(r)
    else:
        # text
        for r in results:
            if isinstance(r, (dict, list)):
                print(json.dumps(r, indent=2, ensure_ascii=False))
            else:
                print(r)

    if args.exit_empty and not results:
        sys.exit(1)


def cmd_paths(args):
    """List all possible JSONPath paths in the data."""
    if args.file:
        try:
            with open(args.file) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        data = json.load(sys.stdin)

    paths = []
    _collect_paths(data, "$", paths, max_depth=args.depth)

    for p in paths:
        print(p)


def _collect_paths(data, prefix, paths, max_depth=10, depth=0):
    """Recursively collect all paths."""
    if depth > max_depth:
        return

    paths.append(prefix)

    if isinstance(data, dict):
        for k, v in data.items():
            safe_key = k if re.match(r'^[a-zA-Z_]\w*$', k) else f"['{k}']"
            new_prefix = f"{prefix}.{safe_key}" if safe_key == k else f"{prefix}{safe_key}"
            _collect_paths(v, new_prefix, paths, max_depth, depth + 1)
    elif isinstance(data, list):
        for i, item in enumerate(data[:5]):  # Limit array exploration
            _collect_paths(item, f"{prefix}[{i}]", paths, max_depth, depth + 1)
        if len(data) > 5:
            paths.append(f"{prefix}[...]  ({len(data)} items total)")


def cmd_validate(args):
    """Validate a JSONPath expression."""
    try:
        tokens = tokenize(args.expression)
        if args.format == "json":
            print(json.dumps({
                "expression": args.expression,
                "valid": True,
                "tokens": [{"type": t, "value": v} for t, v in tokens],
            }, indent=2))
        else:
            print(f"Valid: {args.expression}")
            for t, v in tokens:
                print(f"  {t}: {v}")
    except Exception as e:
        if args.format == "json":
            print(json.dumps({"expression": args.expression, "valid": False, "error": str(e)}, indent=2))
        else:
            print(f"Invalid: {args.expression} — {e}")
        sys.exit(1)


def cmd_extract(args):
    """Extract and flatten values from JSON using multiple expressions."""
    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    extracted = {}
    for spec in args.specs:
        if '=' in spec:
            name, expr = spec.split('=', 1)
        else:
            name = spec.split('.')[-1].strip('[]').strip("'\"")
            expr = spec
        results = jsonpath(data, expr)
        extracted[name] = results[0] if len(results) == 1 else results

    if args.format == "json":
        print(json.dumps(extracted, indent=2, ensure_ascii=False))
    else:
        for k, v in extracted.items():
            if isinstance(v, (dict, list)):
                print(f"{k}: {json.dumps(v, ensure_ascii=False)}")
            else:
                print(f"{k}: {v}")


def main():
    parser = argparse.ArgumentParser(
        prog="jsonpath",
        description="Query JSON data using JSONPath expressions.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    sub = parser.add_subparsers(dest="command", required=True)

    # query
    p_query = sub.add_parser("query", help="Query JSON with a JSONPath expression")
    p_query.add_argument("expression", help="JSONPath expression (e.g., $.store.book[0].title)")
    p_query.add_argument("-f", "--file", help="JSON file (default: stdin)")
    p_query.add_argument("--format", choices=["json", "text", "lines", "csv"], default="json")
    p_query.add_argument("--first", action="store_true", help="Return only first match")
    p_query.add_argument("--count", action="store_true", help="Return match count only")
    p_query.add_argument("--always-array", action="store_true", help="Always output as array")
    p_query.add_argument("--exit-empty", action="store_true", help="Exit 1 if no matches")

    # paths
    p_paths = sub.add_parser("paths", help="List all JSONPath paths in data")
    p_paths.add_argument("-f", "--file", help="JSON file (default: stdin)")
    p_paths.add_argument("-d", "--depth", type=int, default=10, help="Max depth (default: 10)")

    # validate
    p_validate = sub.add_parser("validate", help="Validate a JSONPath expression")
    p_validate.add_argument("expression", help="JSONPath expression to validate")
    p_validate.add_argument("--format", choices=["text", "json"], default="text")

    # extract
    p_extract = sub.add_parser("extract", help="Extract multiple values using named expressions")
    p_extract.add_argument("specs", nargs="+", help="Extraction specs: name=$.path or $.path")
    p_extract.add_argument("-f", "--file", help="JSON file (default: stdin)")
    p_extract.add_argument("--format", choices=["json", "text"], default="json")

    args = parser.parse_args()

    commands = {
        "query": cmd_query,
        "paths": cmd_paths,
        "validate": cmd_validate,
        "extract": cmd_extract,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
