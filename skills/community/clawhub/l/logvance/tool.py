#!/usr/bin/env python3
"""
logvance - Format and convert log timestamps to local time
"""
import argparse
import sys
import re
from datetime import datetime, timezone
import time

def parse_iso_timestamp(ts_str):
    formats = [
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S'
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(ts_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None

def convert_line(line, local_tz=True):
    # Match common ISO-like timestamps
    timestamp_pattern = r'\b(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)\b'
    match = re.search(timestamp_pattern, line)
    if not match:
        return line

    ts_str = match.group(1)
    dt = parse_iso_timestamp(ts_str)
    if not dt:
        return line

    if local_tz:
        local_dt = dt.astimezone()
    else:
        local_dt = dt

    # Remove microsecond precision for logs
    local_dt = local_dt.replace(microsecond=0)

    new_ts = local_dt.strftime('%Y-%m-%d %H:%M:%S%z')
    # Replace with offset like +0200 -> +02:00
    if len(new_ts) == 25 and new_ts.endswith('00'):
        new_ts = new_ts[:-2] + ':' + new_ts[-2:]

    return line.replace(ts_str, new_ts)

def main():
    parser = argparse.ArgumentParser(description="Convert log timestamps to local time")
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help="Log file to process (default: stdin)")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
                        help="Output file (default: stdout)")

    args = parser.parse_args()

    try:
        for line in args.file:
            converted = convert_line(line.rstrip('\n'))
            print(converted, file=args.output)
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
