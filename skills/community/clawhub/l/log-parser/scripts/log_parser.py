#!/usr/bin/env python3
"""
Log Parser - Parse and analyze various log formats
"""

import argparse
import json
import sys
import re
from datetime import datetime
from collections import Counter
from typing import Dict, List, Optional, Tuple

# Log format patterns
LOG_PATTERNS = {
    'nginx': re.compile(
        r'(?P<ip>[\d.]+)\s+-\s+-\s+\[(?P<datetime>[^\]]+)\]\s+'
        r'"(?P<method>\w+)\s+(?P<path>[^\s]+)\s+(?P<protocol>[^"]+)"\s+'
        r'(?P<status>\d+)\s+(?P<size>\d+)'
    ),
    'apache': re.compile(
        r'(?P<ip>[\d.]+)\s+-\s+-\s+\[(?P<datetime>[^\]]+)\]\s+'
        r'"(?P<method>\w+)\s+(?P<path>[^\s]+)\s+(?P<protocol>[^"]+)"\s+'
        r'(?P<status>\d+)\s+(?P<size>[\d-]+)'
    ),
    'syslog': re.compile(
        r'(?P<month>\w+)\s+(?P<day>\d+)\s+(?P<time>[\d:]+)\s+'
        r'(?P<host>\S+)\s+(?P<process>[^\[]+)\[(?P<pid>\d+)\]:\s+'
        r'(?P<message>.+)'
    ),
    'json': None,  # Will be parsed with json.loads
}

def detect_format(line: str) -> str:
    """Detect log format from a sample line"""
    # Try JSON first
    try:
        json.loads(line)
        return 'json'
    except:
        pass
    
    # Try other patterns
    for format_name, pattern in LOG_PATTERNS.items():
        if pattern and pattern.match(line):
            return format_name
    
    return 'unknown'

def parse_nginx_datetime(dt_str: str) -> str:
    """Convert nginx datetime format"""
    try:
        dt = datetime.strptime(dt_str, "%d/%b/%Y:%H:%M:%S %z")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return dt_str

def parse_line(line: str, log_format: str) -> Optional[Dict]:
    """Parse a single log line"""
    line = line.strip()
    if not line:
        return None
    
    if log_format == 'json':
        try:
            return json.loads(line)
        except:
            return None
    
    pattern = LOG_PATTERNS.get(log_format)
    if not pattern:
        return {'raw': line}
    
    match = pattern.match(line)
    if not match:
        return {'raw': line}
    
    data = match.groupdict()
    
    # Normalize datetime
    if 'datetime' in data:
        data['datetime'] = parse_nginx_datetime(data['datetime'])
    
    # Convert numeric fields
    if 'status' in data:
        data['status'] = int(data['status'])
    if 'size' in data:
        data['size'] = int(data['size']) if data['size'] != '-' else 0
    if 'pid' in data:
        data['pid'] = int(data['pid'])
    
    return data

def parse_file(file_path: str, log_format: str = 'auto') -> Tuple[List[Dict], str]:
    """Parse entire log file"""
    entries = []
    detected_format = log_format
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [], ''
    
    if not lines:
        return [], ''
    
    # Auto-detect format
    if log_format == 'auto':
        # Try first few non-empty lines
        for line in lines[:10]:
            if line.strip():
                detected_format = detect_format(line)
                break
    
    for line in lines:
        entry = parse_line(line, detected_format)
        if entry:
            entries.append(entry)
    
    return entries, detected_format

def get_stats(entries: List[Dict]) -> Dict:
    """Generate statistics from log entries"""
    stats = {
        'total_entries': len(entries),
        'format': '',
        'fields': {},
    }
    
    if not entries:
        return stats
    
    # Count field occurrences
    field_counter = Counter()
    for entry in entries:
        field_counter.update(entry.keys())
    
    stats['fields'] = dict(field_counter.most_common(20))
    
    # Extract common fields
    ips = []
    status_codes = []
    paths = []
    
    for entry in entries:
        if 'ip' in entry:
            ips.append(entry['ip'])
        if 'status' in entry:
            status_codes.append(str(entry['status']))
        if 'path' in entry:
            paths.append(entry['path'])
    
    if ips:
        stats['top_ips'] = dict(Counter(ips).most_common(10))
    if status_codes:
        stats['status_distribution'] = dict(Counter(status_codes).most_common(10))
    if paths:
        stats['top_paths'] = dict(Counter(paths).most_common(10))
    
    return stats

def filter_entries(entries: List[Dict], filters: Dict) -> List[Dict]:
    """Filter log entries"""
    filtered = entries
    
    for key, value in filters.items():
        if key == 'status':
            # Handle status code comparison
            filtered = [e for e in filtered if str(e.get('status', '')) == str(value)]
        elif key == 'ip':
            filtered = [e for e in filtered if value in str(e.get('ip', ''))]
        elif key == 'path':
            filtered = [e for e in filtered if value in str(e.get('path', ''))]
        else:
            filtered = [e for e in filtered if value in str(e.get(key, ''))]
    
    return filtered

def get_errors(entries: List[Dict]) -> List[Dict]:
    """Extract error entries"""
    errors = []
    for entry in entries:
        status = entry.get('status', 0)
        level = str(entry.get('level', '')).upper()
        
        # HTTP 4xx/5xx
        if isinstance(status, int) and status >= 400:
            errors.append(entry)
        # Log level ERROR/WARN
        elif level in ['ERROR', 'ERR', 'WARN', 'WARNING', 'FATAL', 'CRITICAL']:
            errors.append(entry)
    
    return errors

def get_top(entries: List[Dict], field: str, limit: int = 10) -> Dict:
    """Get top N values for a field"""
    values = []
    for entry in entries:
        if field in entry:
            values.append(str(entry[field]))
    
    return {
        'field': field,
        'top': dict(Counter(values).most_common(limit)),
        'unique_count': len(set(values))
    }

def main():
    parser = argparse.ArgumentParser(
        description='Log Parser - Parse and analyze log files'
    )
    parser.add_argument(
        'action',
        choices=['parse', 'stats', 'filter', 'errors', 'top'],
        help='Action to perform'
    )
    parser.add_argument(
        '--file', '-f',
        required=True,
        help='Log file path'
    )
    parser.add_argument(
        '--format',
        default='auto',
        choices=['auto', 'nginx', 'apache', 'syslog', 'json'],
        help='Log format (default: auto-detect)'
    )
    parser.add_argument(
        '--ip',
        help='Filter by IP address'
    )
    parser.add_argument(
        '--status',
        help='Filter by HTTP status code'
    )
    parser.add_argument(
        '--path',
        help='Filter by request path'
    )
    parser.add_argument(
        '--field',
        help='Field name for top action'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Limit for top results (default: 10)'
    )
    parser.add_argument(
        '--sample',
        type=int,
        default=5,
        help='Number of sample entries to show (default: 5)'
    )

    args = parser.parse_args()

    # Parse file
    entries, detected_format = parse_file(args.file, args.format)
    
    if not entries:
        result = {"success": False, "error": "No entries found or file not found"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    # Execute action
    if args.action == 'parse':
        result = {
            "success": True,
            "format": detected_format,
            "total_entries": len(entries),
            "sample": entries[:args.sample]
        }
    elif args.action == 'stats':
        stats = get_stats(entries)
        stats['format'] = detected_format
        result = {"success": True, **stats}
    elif args.action == 'filter':
        filters = {}
        if args.ip:
            filters['ip'] = args.ip
        if args.status:
            filters['status'] = args.status
        if args.path:
            filters['path'] = args.path
        
        filtered = filter_entries(entries, filters)
        result = {
            "success": True,
            "total_entries": len(entries),
            "filtered_entries": len(filtered),
            "filters": filters,
            "sample": filtered[:args.sample]
        }
    elif args.action == 'errors':
        errors = get_errors(entries)
        result = {
            "success": True,
            "total_entries": len(entries),
            "error_entries": len(errors),
            "errors": errors[:args.sample]
        }
    elif args.action == 'top':
        if not args.field:
            result = {"success": False, "error": "Missing --field parameter"}
        else:
            result = {
                "success": True,
                **get_top(entries, args.field, args.limit)
            }
    else:
        result = {"success": False, "error": f"Unknown action: {args.action}"}

    # Output result
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get('success') else 1)

if __name__ == '__main__':
    main()
