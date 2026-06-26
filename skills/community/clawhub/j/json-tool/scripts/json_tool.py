#!/usr/bin/env python3
"""
JSON Tool - Validate, format, and transform JSON data
"""

import argparse
import json
import sys
from pathlib import Path


def load_json(filepath):
    """Load JSON from file."""
    try:
        with open(filepath) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_json(data, filepath, indent=2):
    """Save JSON to file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def validate_json(filepath):
    """Validate JSON syntax."""
    try:
        with open(filepath) as f:
            json.load(f)
        print(f"Valid JSON: {filepath}")
        return 0
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return 1


def format_json(filepath, indent=2, output=None):
    """Pretty print JSON."""
    data = load_json(filepath)
    if data is None:
        return 1
    
    output_path = output or filepath
    save_json(data, output_path, indent)
    print(f"Formatted: {output_path}")
    return 0


def minify_json(filepath, output=None):
    """Minify JSON."""
    data = load_json(filepath)
    if data is None:
        return 1
    
    output_path = output or filepath
    with open(output_path, 'w') as f:
        json.dump(data, f, separators=(',', ':'))
    print(f"Minified: {output_path}")
    return 0


def query_json(filepath, query):
    """Extract data using simple path query."""
    data = load_json(filepath)
    if data is None:
        return 1
    
    # Simple query: items[0].name -> ['items', 0, 'name']
    parts = []
    current = ''
    for char in query:
        if char in '.[],':
            if current:
                if current.isdigit():
                    parts.append(int(current))
                else:
                    parts.append(current)
                current = ''
            if char == '[':
                parts.append('[')
            elif char == ']':
                if parts[-1] == '[':
                    parts = parts[:-1]  # Empty []
        else:
            current += char
    if current:
        if current.isdigit():
            parts.append(int(current))
        else:
            parts.append(current)
    
    # Navigate
    result = data
    for part in parts:
        if part == '[':
            continue
        try:
            result = result[part]
        except (KeyError, IndexError, TypeError):
            print(f"Path not found: {query}")
            return 1
    
    print(json.dumps(result, indent=2))
    return 0


def sort_keys(data):
    """Recursively sort object keys."""
    if isinstance(data, dict):
        return {k: sort_keys(v) for k, v in sorted(data.items())}
    elif isinstance(data, list):
        return [sort_keys(item) for item in data]
    return data


def convert_json(filepath, format_type, output=None):
    """Convert JSON to other formats."""
    data = load_json(filepath)
    if data is None:
        return 1
    
    output_path = output or filepath
    
    if format_type == 'yaml':
        try:
            import yaml
            with open(output_path.replace('.json', '.yaml'), 'w') as f:
                yaml.dump(data, f)
            print(f"Converted to YAML: {output_path}")
        except ImportError:
            print("PyYAML not installed. Run: pip install pyyaml")
            return 1
    
    elif format_type == 'csv':
        import csv
        if isinstance(data, list) and data:
            keys = data[0].keys() if isinstance(data[0], dict) else []
            if keys:
                with open(output_path.replace('.json', '.csv'), 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)
                print(f"Converted to CSV")
                return 0
        print("CSV conversion requires array of objects")
        return 1
    
    else:
        print(f"Unknown format: {format_type}")
        return 1
    
    return 0


def main():
    parser = argparse.ArgumentParser(description='JSON Tool')
    parser.add_argument('file', nargs='?', help='JSON file')
    parser.add_argument('--format', action='store_true', help='Pretty print')
    parser.add_argument('--minify', action='store_true', help='Minify')
    parser.add_argument('--validate', action='store_true', help='Validate')
    parser.add_argument('--query', help='JSONPath query')
    parser.add_argument('--convert', help='Convert to format (yaml, csv)')
    parser.add_argument('--sort-keys', action='store_true', help='Sort keys')
    parser.add_argument('--indent', type=int, default=2, help='Indent size')
    parser.add_argument('--output', help='Output file')
    
    args = parser.parse_args()
    
    if not args.file:
        parser.print_help()
        return 0
    
    # Validate
    if args.validate:
        return validate_json(args.file)
    
    # Format
    if args.format:
        return format_json(args.file, args.indent, args.output)
    
    # Minify
    if args.minify:
        return minify_json(args.file, args.output)
    
    # Query
    if args.query:
        return query_json(args.file, args.query)
    
    # Sort keys
    if args.sort_keys:
        data = load_json(args.file)
        if data is None:
            return 1
        sorted_data = sort_keys(data)
        output_path = args.output or args.file
        save_json(sorted_data, output_path, args.indent)
        print(f"Sorted keys: {output_path}")
        return 0
    
    # Convert
    if args.convert:
        return convert_json(args.file, args.convert, args.output)
    
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
