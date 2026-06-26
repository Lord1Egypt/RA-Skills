#!/usr/bin/env python3
"""
JSON Formatter - Format, compress, validate, and convert JSON
"""

import argparse
import json
import sys

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def read_input(input_str: str, is_file: bool) -> str:
    """Read input from string or file"""
    if is_file:
        with open(input_str, 'r', encoding='utf-8') as f:
            return f.read()
    return input_str


def format_json(input_str: str, indent: int = 2) -> dict:
    """Format/beautify JSON"""
    try:
        data = json.loads(input_str)
        formatted = json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=False)
        return {"success": True, "result": formatted}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse error: {str(e)}"}


def compress_json(input_str: str) -> dict:
    """Compress/minify JSON"""
    try:
        data = json.loads(input_str)
        compressed = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        return {"success": True, "result": compressed}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse error: {str(e)}"}


def validate_json(input_str: str) -> dict:
    """Validate JSON syntax"""
    try:
        json.loads(input_str)
        return {"success": True, "valid": True, "message": "JSON is valid"}
    except json.JSONDecodeError as e:
        return {
            "success": True,
            "valid": False,
            "error": str(e),
            "line": e.lineno,
            "column": e.colno,
            "message": f"Invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
        }


def to_yaml(input_str: str, indent: int = 2) -> dict:
    """Convert JSON to YAML"""
    if not YAML_AVAILABLE:
        return {
            "success": False,
            "error": "PyYAML not installed. Install with: pip install pyyaml"
        }

    try:
        data = json.loads(input_str)
        yaml_str = yaml.dump(data, allow_unicode=True, default_flow_style=False, indent=indent)
        return {"success": True, "result": yaml_str}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse error: {str(e)}"}
    except yaml.YAMLError as e:
        return {"success": False, "error": f"YAML error: {str(e)}"}


def from_yaml(input_str: str, indent: int = 2) -> dict:
    """Convert YAML to JSON"""
    if not YAML_AVAILABLE:
        return {
            "success": False,
            "error": "PyYAML not installed. Install with: pip install pyyaml"
        }

    try:
        data = yaml.safe_load(input_str)
        json_str = json.dumps(data, indent=indent, ensure_ascii=False)
        return {"success": True, "result": json_str}
    except yaml.YAMLError as e:
        return {"success": False, "error": f"YAML parse error: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(
        description='JSON Formatter - Format, compress, validate, and convert JSON'
    )
    parser.add_argument(
        'action',
        choices=['format', 'compress', 'validate', 'to-yaml', 'from-yaml'],
        help='Action to perform'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input JSON/YAML string or file path'
    )
    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help='Indentation spaces (default: 2)'
    )
    parser.add_argument(
        '--file', '-f',
        action='store_true',
        help='Treat input as file path'
    )

    args = parser.parse_args()

    # Read input
    try:
        input_str = read_input(args.input, args.file)
    except FileNotFoundError as e:
        result = {"success": False, "error": f"File not found: {str(e)}"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        result = {"success": False, "error": str(e)}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    # Execute action
    if args.action == 'format':
        result = format_json(input_str, args.indent)
    elif args.action == 'compress':
        result = compress_json(input_str)
    elif args.action == 'validate':
        result = validate_json(input_str)
    elif args.action == 'to-yaml':
        result = to_yaml(input_str, args.indent)
    elif args.action == 'from-yaml':
        result = from_yaml(input_str, args.indent)
    else:
        result = {"success": False, "error": f"Unknown action: {args.action}"}

    # Output result
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
