#!/usr/bin/env python3
"""
JSON Query Tool - A simple jq-like CLI for querying JSON files.

Usage:
    jsonq <file> <query> [options]
    
Examples:
    jsonq data.json "users.name"
    jsonq data.json "users[0].email"
    jsonq data.json "users[*].name" --format table
"""

import json
import sys
import re
from typing import Any, List, Union


def parse_query(query: str) -> List[Union[str, int, slice]]:
    """
    Parse a query string into path components.
    
    Supports:
    - dot notation: users.name
    - array index: users[0]
    - array wildcard: users[*]
    - nested: company.departments[0].employees[*].name
    """
    parts = []
    i = 0
    
    while i < len(query):
        if query[i] == '.':
            i += 1
            continue
        
        # Array index or wildcard [n] or [*]
        if query[i] == '[':
            end = query.find(']', i)
            if end == -1:
                raise ValueError(f"Unmatched bracket at position {i}")
            content = query[i+1:end]
            if content == '*':
                parts.append(slice(None))  # All items
            else:
                try:
                    parts.append(int(content))
                except ValueError:
                    raise ValueError(f"Invalid array index: {content}")
            i = end + 1
        # Key name
        elif query[i] != '.':
            # Find end of key (next dot or bracket or end)
            j = i
            while j < len(query) and query[j] not in '.[]':
                j += 1
            key = query[i:j]
            if key == '*':
                parts.append('*')  # Wildcard
            else:
                parts.append(key)
            i = j
        else:
            i += 1
    
    return parts


def get_value(data: Any, parts: List[Union[str, int, slice]]) -> Any:
    """
    Traverse data following the parsed path parts.
    """
    if not parts:
        return data
    
    part = parts[0]
    remaining = parts[1:]
    
    # Handle wildcard
    if part == '*':
        if isinstance(data, dict):
            results = {}
            for key, value in data.items():
                result = get_value(value, remaining)
                if result is not None:
                    results[key] = result
            return results if results else None
        return None
    
    # Handle array slice (all items)
    if isinstance(part, slice):
        if isinstance(data, list):
            results = []
            for item in data:
                result = get_value(item, remaining)
                if result is not None:
                    results.append(result)
            return results
        return None
    
    # Handle array index
    if isinstance(part, int):
        if isinstance(data, list) and 0 <= part < len(data):
            return get_value(data[part], remaining)
        return None
    
    # Handle string key
    if isinstance(data, dict) and part in data:
        return get_value(data[part], remaining)
    
    return None


def format_output(data: Any, format_type: str) -> str:
    """Format output based on format type."""
    if format_type == 'raw':
        if isinstance(data, str):
            return data
        if isinstance(data, (list, dict)):
            return json.dumps(data, ensure_ascii=False, indent=2)
        return str(data)
    
    elif format_type == 'table':
        return format_table(data)
    
    else:  # json
        return json.dumps(data, ensure_ascii=False, indent=2)


def format_table(data: Any) -> str:
    """Format data as a simple table."""
    if not isinstance(data, list):
        if not isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False)
        data = [data]
    
    if not data:
        return "(empty)"
    
    # Get all unique keys from all items
    all_keys = set()
    for item in data:
        if isinstance(item, dict):
            all_keys.update(item.keys())
    
    if not all_keys:
        return json.dumps(data, ensure_ascii=False)
    
    keys = sorted(all_keys)
    
    # Calculate column widths
    widths = {k: len(k) for k in keys}
    for item in data:
        for k in keys:
            val = str(item.get(k, ''))
            widths[k] = max(widths[k], len(val))
    
    # Build table
    lines = []
    
    # Header
    header = '  '.join(k.ljust(widths[k]) for k in keys)
    lines.append(header)
    lines.append('-' * len(header))
    
    # Rows
    for item in data:
        row = '  '.join(str(item.get(k, '')).ljust(widths[k]) for k in keys)
        lines.append(row)
    
    return '\n'.join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='JSON Query Tool - Simple jq-like CLI for JSON files'
    )
    parser.add_argument('file', help='JSON file to query')
    parser.add_argument('query', help='Query path (e.g., "users.name")')
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'raw', 'table'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '-c', '--compact',
        action='store_true',
        help='Compact JSON output'
    )
    
    args = parser.parse_args()
    
    # Load JSON file
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Parse and execute query
    try:
        parts = parse_query(args.query)
    except ValueError as e:
        print(f"Error: Invalid query: {e}", file=sys.stderr)
        sys.exit(1)
    
    result = get_value(data, parts)
    
    if result is None:
        print("(null)", file=sys.stderr)
        sys.exit(1)
    
    # Output result
    if args.compact and args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))
    else:
        print(format_output(result, args.format))


if __name__ == '__main__':
    main()
