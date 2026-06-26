#!/usr/bin/env python3
"""
Loki Log Query Script

Query logs from Grafana Loki via HTTP API.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus
import urllib.request
import urllib.error
import socket

# Set timeout
socket.setdefaulttimeout(30)


def parse_time(time_str):
    """Parse time string to ISO format."""
    if not time_str:
        return None
    
    time_str = time_str.strip()
    
    # Already ISO format
    if 'T' in time_str:
        return time_str
    
    # Relative time like "now-1h", "now-30m"
    if time_str.startswith('now-'):
        value = time_str[4:]
        if value.endswith('h'):
            delta = timedelta(hours=int(value[:-1]))
        elif value.endswith('m'):
            delta = timedelta(minutes=int(value[:-1]))
        elif value.endswith('s'):
            delta = timedelta(seconds=int(value[:-1]))
        elif value.endswith('d'):
            delta = timedelta(days=int(value[:-1]))
        else:
            delta = timedelta(minutes=int(value))
        
        return (datetime.now(timezone.utc) - delta).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Just "now"
    if time_str == 'now':
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Try parsing as datetime
    try:
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    except:
        pass
    
    return time_str


def query_loki(loki_url, query, start=None, end=None, limit=100, direction="backward"):
    """Query Loki API."""
    
    # Build query parameters
    params = {
        'query': query,
        'limit': limit,
        'direction': direction
    }
    
    if start:
        params['start'] = parse_time(start) or start
    if end:
        params['end'] = parse_time(end) or end
    
    # Build URL
    query_string = '&'.join(f'{k}={quote_plus(str(v))}' for k, v in params.items())
    url = f"{loki_url.rstrip('/')}/loki/api/v1/query_range?{query_string}"
    
    # Make request
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/json')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
    except urllib.error.URLError as e:
        print(f"Error connecting to Loki: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}", file=sys.stderr)
        sys.exit(1)
    
    return data


def format_results(data):
    """Format Loki response for display."""
    if not data.get('data', {}).get('result'):
        return "No results found."
    
    results = []
    for stream in data['data']['result']:
        labels = stream.get('stream', {})
        label_str = ", ".join(f"{k}={v}" for k, v in labels.items())
        
        results.append(f"# {label_str}")
        
        for value in stream.get('values', []):
            # value is [timestamp_ns, line]
            ts, line = value
            # Convert nanosecond timestamp to readable format
            try:
                ts_sec = int(ts) / 1e9
                dt = datetime.fromtimestamp(ts_sec, timezone.utc)
                ts_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                ts_str = ts[:10]  # fallback
            
            results.append(f"[{ts_str}] {line}")
    
    return "\n".join(results)


def main():
    parser = argparse.ArgumentParser(description='Query logs from Loki')
    parser.add_argument('--loki-url', default='http://localhost:3100',
                      help='Loki API URL (default: http://localhost:3100)')
    parser.add_argument('--query', required=True,
                      help='LogQL query string')
    parser.add_argument('--start', 
                      help='Start time (ISO 8601 or relative like now-1h)')
    parser.add_argument('--end',
                      help='End time (ISO 8601 or relative like now)')
    parser.add_argument('--limit', type=int, default=100,
                      help='Max results (default: 100)')
    parser.add_argument('--direction', choices=['forward', 'backward'], 
                      default='backward', help='Query direction')
    parser.add_argument('--json', action='store_true',
                      help='Output raw JSON')
    
    args = parser.parse_args()
    
    # Set default time range if not provided
    if not args.start:
        args.start = "now-1h"
    if not args.end:
        args.end = "now"
    
    data = query_loki(args.loki_url, args.query, args.start, args.end, 
                     args.limit, args.direction)
    
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_results(data))


if __name__ == '__main__':
    main()