#!/usr/bin/env python3
"""
LogSift: A simple CLI tool to filter log files by keyword or date range.
"""
import argparse
import sys
import re
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Filter log entries by keyword or date range.")
    parser.add_argument("file", nargs="?", default="-", help="Log file to read (default: stdin)")
    parser.add_argument("-k", "--keyword", action="append", help="Keyword to search for (can be used multiple times)")
    parser.add_argument("-s", "--since", help="ISO date string (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) to start from")
    parser.add_argument("-u", "--until", help="ISO date string to end before")
    parser.add_argument("--date-format", default="%Y-%m-%d %H:%M:%S", help="Date format in log (default: '%%Y-%%m-%%d %%H:%%M:%%S')")
    parser.add_argument("--timestamp-regex", default=r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", help="Regex to extract timestamp")
    return parser.parse_args()

def parse_log_timestamp(log_line, regex_pattern, date_format):
    match = re.search(regex_pattern, log_line)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(), date_format)
    except ValueError:
        return None

def main():
    args = parse_args()
    
    # Compile keywords for efficiency
    keywords = [k.lower() for k in args.keyword] if args.keyword else None

    # Parse date bounds
    since_dt = datetime.strptime(args.since, args.date_format) if args.since else None
    until_dt = datetime.strptime(args.until, args.date_format) if args.until else None

    # Open file or stdin
    if args.file == "-":
        f = sys.stdin
    else:
        f = open(args.file, "r", encoding="utf-8")

    try:
        for line in f:
            line = line.rstrip()
            if not line:
                continue

            # Date filtering
            if since_dt or until_dt:
                timestamp = parse_log_timestamp(line, args.timestamp_regex, args.date_format)
                if timestamp:
                    if since_dt and timestamp < since_dt:
                        continue
                    if until_dt and timestamp > until_dt:
                        continue

            # Keyword filtering
            if keywords:
                line_lower = line.lower()
                if not any(k in line_lower for k in keywords):
                    continue

            print(line)
    except KeyboardInterrupt:
        pass
    finally:
        if f != sys.stdin:
            f.close()

if __name__ == "__main__":
    main()
