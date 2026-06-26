#!/usr/bin/env python3
"""
logfmt - Syntax-highlighted log file viewer with timestamp awareness.
"""
import argparse
import re
import sys
import os
from datetime import datetime
from typing import Optional, TextIO

# ANSI color codes
COLORS = {
    'RESET': '\033[0m',
    'ERROR': '\033[91m',      # Red
    'WARN': '\033[93m',       # Yellow
    'INFO': '\033[94m',       # Blue
    'DEBUG': '\033[90m',      # Gray
    'TIMESTAMP': '\033[95m',  # Magenta
    'LEVEL': '\033[1m',       # Bold
}

# Match common timestamp formats
TIMESTAMP_PATTERNS = [
    re.compile(r'\b(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)\b'),
    re.compile(r'\b(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},?\d*)\b'),
    re.compile(r'\b(\w{3} \d{1,2} \d{2}:\d{2}:\d{2})\b'),
]

# Match log levels
LEVEL_PATTERN = re.compile(r'\b(ERROR|WARN|INFO|DEBUG|CRITICAL|FATAL)\b', re.IGNORECASE)

def colorize_timestamp(match: re.Match) -> str:
    return f"{COLORS['TIMESTAMP']}{match.group(1)}{COLORS['RESET']}"

def colorize_level(match: re.Match) -> str:
    level = match.group(1).upper()
    color = COLORS.get(level, COLORS['LEVEL'])
    return f"{color}{level}{COLORS['RESET']}"

def format_line(line: str) -> str:
    # Colorize timestamps
    for pattern in TIMESTAMP_PATTERNS:
        line = pattern.sub(colorize_timestamp, line)
    
    # Colorize log levels
    line = LEVEL_PATTERN.sub(colorize_level, line)
    
    return line

def parse_args():
    parser = argparse.ArgumentParser(
        description="Syntax-highlight log files with timestamp support."
    )
    parser.add_argument(
        'file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="Log file to read (default: stdin)"
    )
    parser.add_argument(
        '-t', '--tail',
        action='store_true',
        help="Act like `tail -f`, follow input"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    file: TextIO = args.file
    
    try:
        if args.tail and file.isatty():
            print("Error: -t/--tail can only be used with piped input or files.", file=sys.stderr)
            sys.exit(1)
            
        while True:
            line = file.readline()
            if not line:
                if args.tail:
                    import time
                    time.sleep(0.1)
                    continue
                else:
                    break
            formatted = format_line(line.rstrip('\n'))
            print(formatted)
            if file == sys.stdin:
                sys.stdout.flush()
                
    except KeyboardInterrupt:
        sys.exit(0)
    except BrokenPipeError:
        # Handle piping to `head` or similar
        sys.stdout.close()
        sys.stderr.close()
        sys.exit(0)
    finally:
        if file != sys.stdin:
            file.close()

if __name__ == '__main__':
    main()
