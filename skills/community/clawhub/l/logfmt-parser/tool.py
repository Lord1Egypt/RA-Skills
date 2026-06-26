#!/usr/bin/env python3
"""
logfmt_parser - Convert log lines to JSON format
"""
import argparse
import sys
import re
import json
from datetime import datetime
from typing import Dict, Any, Optional

def parse_key_value_log(line: str) -> Dict[str, Any]:
    """Parse key=value style log entries."""
    data = {}
    # Basic key=value pattern with quoted values support
    pattern = r'(\w+)=("?)([^"\s]+|\[.*?\]|\{.*?\}|".*?")\2'
    matches = re.findall(pattern, line)
    
    for key, quote, value in matches:
        # Remove surrounding quotes if present
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        # Try to convert to int/float
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                pass
        data[key] = value
    
    return data

def detect_timestamp_format(ts: str) -> Optional[str]:
    """Detect common timestamp formats."""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%b %d %H:%M:%S",
        "%d/%b/%Y:%H:%M:%S",
    ]
    
    for fmt in formats:
        try:
            datetime.strptime(ts, fmt)
            return fmt
        except ValueError:
            continue
    return None

def add_timestamp_field(data: Dict[str, Any], line: str):
    """Attempt to find and parse timestamp from line."""
    # Common timestamp patterns
    timestamp_patterns = [
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
        r'\w{3} \s?\d{1,2} \d{2}:\d{2}:\d{2}',
        r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}',
    ]
    
    for pattern in timestamp_patterns:
        match = re.search(pattern, line)
        if match:
            ts_str = match.group()
            fmt = detect_timestamp_format(ts_str)
            if fmt:
                try:
                    dt = datetime.strptime(ts_str, fmt)
                    data['@timestamp'] = dt.isoformat()
                    return
                except:
                    pass

def process_line(line: str, parse_timestamp: bool) -> Dict[str, Any]:
    """Process a single log line."""
    line = line.strip()
    if not line:
        return {}
    
    data = parse_key_value_log(line)
    
    # Add timestamp if requested and not already present
    if parse_timestamp and '@timestamp' not in data:
        add_timestamp_field(data, line)
    
    # Add raw log if not present
    if 'log' not in data:
        data['log'] = line
    
    return data

def main():
    parser = argparse.ArgumentParser(
        description="Convert log files to JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  logfmt_parser -i access.log -o parsed.json
  cat app.log | logfmt_parser --timestamp > output.json
  logfmt_parser -i system.log --no-log-field
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='Input log file (default: stdin)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output JSON file (default: stdout)'
    )
    
    parser.add_argument(
        '--timestamp',
        action='store_true',
        help='Try to detect and parse timestamps'
    )
    
    parser.add_argument(
        '--no-log-field',
        action='store_true',
        help='Don\'t include original log line in output'
    )
    
    args = parser.parse_args()
    
    try:
        for line_num, line in enumerate(args.input, 1):
            try:
                result = process_line(line, args.timestamp)
                
                # Handle --no-log-field
                if args.no_log_field and 'log' in result:
                    del result['log']
                
                if result:  # Only output non-empty results
                    json.dump(result, args.output)
                    args.output.write('\n')
                    
            except Exception as e:
                print(f"Warning: Error processing line {line_num}: {e}", file=sys.stderr)
                
    except KeyboardInterrupt:
        print("\nProcessing interrupted.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
