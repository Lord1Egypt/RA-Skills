#!/usr/bin/env python3
"""
logflux - Real-time log file parser and colorizer
"""
import argparse
import re
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama for Windows compatibility
except ImportError:
    # If colorama not available, define dummy styles
    class Fore:
        RED = ''
        YELLOW = ''
        GREEN = ''
        CYAN = ''
        RESET = ''
    class Style:
        RESET_ALL = ''

def colorize_log_line(line):
    """Apply colors to different log levels and timestamps."""
    # Colorize timestamps (ISO or common formats)
    line = re.sub(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', f'{Fore.CYAN}\\1{Fore.RESET}', line)
    line = re.sub(r'(\d{2}:\d{2}:\d{2})', f'{Fore.CYAN}\\1{Fore.RESET}', line)

    # Colorize log levels
    line = re.sub(r'(ERROR)', f'{Style.RESET_ALL}{Fore.RED}[\\1]{Fore.RESET}{Style.RESET_ALL}', line, flags=re.IGNORECASE)
    line = re.sub(r'(WARN|WARNING)', f'{Style.RESET_ALL}{Fore.YELLOW}[\\1]{Fore.RESET}{Style.RESET_ALL}', line, flags=re.IGNORECASE)
    line = re.sub(r'(INFO)', f'{Style.RESET_ALL}{Fore.GREEN}[\\1]{Fore.RESET}{Style.RESET_ALL}', line, flags=re.IGNORECASE)
    line = re.sub(r'(DEBUG)', f'{Style.RESET_ALL}{Fore.CYAN}[\\1]{Fore.RESET}{Style.RESET_ALL}', line, flags=re.IGNORECASE)

    return line

def tail_file(filepath, follow=False, lines=10):
    """Read last N lines of file, optionally follow (like 'tail -f')."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)

    with path.open('r', encoding='utf-8', errors='replace') as f:
        if follow:
            # Read initial lines
            recent_lines = []
            for line in f:
                recent_lines.append(line)
                if len(recent_lines) > lines:
                    recent_lines.pop(0)
            for line in recent_lines:
                print(colorize_log_line(line.rstrip()))
            # Follow mode
            while True:
                where = f.tell()
                line = f.readline()
                if line:
                    print(colorize_log_line(line.rstrip()))
                else:
                    time.sleep(0.1)
                    f.seek(where)
        else:
            # Print last N lines
            all_lines = f.readlines()
            for line in all_lines[-lines:]:
                print(colorize_log_line(line.rstrip()))

def main():
    parser = argparse.ArgumentParser(
        description="Real-time log file colorizer with smart pattern highlighting"
    )
    parser.add_argument("file", help="Log file to read")
    parser.add_argument(
        "-f", "--follow",
        action="store_true",
        help="Follow the file as it grows (like tail -f)"
    )
    parser.add_argument(
        "-n", "--lines",
        type=int,
        default=10,
        help="Number of lines to show from end of file (default: 10)"
    )

    args = parser.parse_args()

    try:
        tail_file(args.file, follow=args.follow, lines=args.lines)
    except KeyboardInterrupt:
        print(f"\n{Style.RESET_ALL}Stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
