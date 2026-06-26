#!/usr/bin/env python3
"""
LogClip - Extract and reformat timestamped log entries by date range.
"""
import argparse
import sys
import re
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract log entries within a specified date range and reformat timestamps."
    )
    parser.add_argument(
        'start',
        help='Start datetime in YYYY-MM-DD or YYYY-MM-DD HH:MM:SS format'
    )
    parser.add_argument(
        'end',
        help='End datetime in YYYY-MM-DD or YYYY-MM-DD HH:MM:SS format'
    )
    parser.add_argument(
        '-i', '--input',
        help='Input file (default: stdin)',
        type=argparse.FileType('r'),
        default=sys.stdin
    )
    parser.add_argument(
        '-f', '--format',
        help='Output timestamp format (default: YYYY-MM-DD HH:MM:SS)',
        default='%Y-%m-%d %H:%M:%S'
    )
    parser.add_argument(
        '-r', '--regex',
        help='Custom timestamp pattern (must include groups: year, month, day, [hour, minute, second])',
        default=r'(\d{4})-(\d{2})-(\d{2})(?:\s(\d{2}):(\d{2}):(\d{2}))?'
    )
    return parser.parse_args()

def parse_datetime_input(dt_str):
    """Parse partial or full datetime string."""
    formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']
    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unable to parse datetime: {dt_str}")

def parse_timestamp(line, regex_pattern):
    """Extract datetime from line using regex, return (timestamp, rest_of_line)."""
    match = re.search(regex_pattern, line)
    if not match:
        return None, line
    parts = list(map(lambda x: x if x is not None else '00', match.groups()))
    # Fill missing time parts with zeros
    year, month, day, hour, minute, second = parts[:6]
    try:
        dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    except ValueError:
        return None, line  # Invalid date
    return dt, line[match.end():].lstrip()

def main():
    args = parse_args()
    try:
        start_dt = parse_datetime_input(args.start)
        end_dt = parse_datetime_input(args.end)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        for line in args.input:
            line = line.rstrip('\n')
            timestamp, content = parse_timestamp(line, args.regex)
            if timestamp and start_dt <= timestamp <= end_dt:
                formatted_time = timestamp.strftime(args.format)
                print(f"{formatted_time} {content}")
    except Exception as e:
        print(f"Error processing input: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
