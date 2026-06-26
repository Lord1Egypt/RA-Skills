#!/usr/bin/env python3
"""
logvibe - Colorize HTTP status codes in log files for quick visual analysis.
"""
import argparse
import re
import sys
import os

# ANSI color codes
COLORS = {
    '2': '\033[92m',  # Green for 2xx (Success)
    '3': '\033[94m',  # Blue for 3xx (Redirect)
    '4': '\033[93m',  # Yellow for 4xx (Client Error)
    '5': '\033[91m',  # Red for 5xx (Server Error)
    'reset': '\033[0m'
}

def colorize_status(line):
    """Find 3-digit HTTP status code and colorize it."""
    # Match common log patterns: standalone 3-digit number after space or tab
    pattern = r'(?<=\s)([2-5]\d{2})(?=\s|$)'
    return re.sub(pattern, lambda m: f"{COLORS[m.group(1)[0]]}{m.group(1)}{COLORS['reset']}", line)

def process_file(filepath):
    """Process each line of the file and print colorized output."""
    try:
        with open(filepath, 'r') as f:
            for line in f:
                print(colorize_status(line.rstrip('\n')))
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{filepath}'.", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Colorize HTTP status codes in log files")
    parser.add_argument('file', nargs='?', help="Log file to process (read from stdin if not provided)")
    parser.add_argument('--dark-bg', action='store_true', help="Optimize colors for dark background (default)")
    parser.add_argument('--light-bg', action='store_true', help="Optimize colors for light background (not currently used)")

    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: Path '{args.file}' does not exist.", file=sys.stderr)
            sys.exit(1)
        process_file(args.file)
    else:
        # Read from stdin
        for line in sys.stdin:
            print(colorize_status(line.rstrip('\n')))

if __name__ == '__main__':
    main()
