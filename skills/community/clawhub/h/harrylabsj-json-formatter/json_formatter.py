#!/usr/bin/env python3
"""
JSON Formatter - Format and validate JSON files.

Usage:
    python json_formatter.py format <file> [-o output] [-i indent] [--sort-keys]
    python json_formatter.py validate <file>
"""

import argparse
import json
import sys
from pathlib import Path


def format_json(data, indent=2, sort_keys=False):
    """Format JSON data with specified indentation."""
    return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)


def validate_json(content):
    """Validate JSON content and return (is_valid, error_message)."""
    try:
        json.loads(content)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def read_input(source):
    """Read input from file or stdin."""
    if source == '-':
        return sys.stdin.read()
    else:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")
        return path.read_text(encoding='utf-8')


def write_output(content, destination=None):
    """Write output to file or stdout."""
    if destination:
        Path(destination).write_text(content, encoding='utf-8')
        print(f"Output written to: {destination}")
    else:
        print(content)


def cmd_format(args):
    """Handle format command."""
    try:
        content = read_input(args.input)
        data = json.loads(content)
        formatted = format_json(data, indent=args.indent, sort_keys=args.sort_keys)
        write_output(formatted, args.output)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3


def cmd_validate(args):
    """Handle validate command."""
    try:
        content = read_input(args.input)
        is_valid, error = validate_json(content)
        if is_valid:
            print("Valid JSON")
            return 0
        else:
            print(f"Error: {error}", file=sys.stderr)
            return 1
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3


def main():
    parser = argparse.ArgumentParser(
        description="Format and validate JSON files",
        prog="json_formatter.py"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Format command
    format_parser = subparsers.add_parser("format", help="Pretty-print JSON")
    format_parser.add_argument("input", help="Input file (use '-' for stdin)")
    format_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    format_parser.add_argument("-i", "--indent", type=int, default=2,
                               help="Indentation spaces (default: 2)")
    format_parser.add_argument("--sort-keys", action="store_true",
                               help="Sort keys alphabetically")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate JSON syntax")
    validate_parser.add_argument("input", help="Input file (use '-' for stdin)")

    args = parser.parse_args()

    if args.command == "format":
        return cmd_format(args)
    elif args.command == "validate":
        return cmd_validate(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
