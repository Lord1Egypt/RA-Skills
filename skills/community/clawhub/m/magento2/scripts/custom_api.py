#!/usr/bin/env python3
"""Generic API client for calling custom or discovered endpoints."""

import sys
import argparse
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, MagentoAPIError, print_error_and_exit

def main():
    parser = argparse.ArgumentParser(description="Call generic Magento REST API endpoints")
    parser.add_argument("method", choices=["GET", "POST", "PUT", "DELETE"], help="HTTP method")
    parser.add_argument("path", help="API path (e.g. 'blog/posts' or full '/rest/V1/blog/posts')")
    parser.add_argument("--data", help="JSON string for POST/PUT body")
    parser.add_argument("--params", help="JSON string for GET query parameters")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")

    args = parser.parse_args()
    client = get_client(args.site)

    data = None
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError:
            sys.exit("Error: --data must be a valid JSON string.")

    params = None
    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError:
            sys.exit("Error: --params must be a valid JSON string.")

    try:
        method = args.method.upper()
        if method == "GET":
            result = client.get(args.path, params=params)
        elif method == "POST":
            result = client.post(args.path, data or {})
        elif method == "PUT":
            result = client.put(args.path, data or {})
        elif method == "DELETE":
            result = client.delete(args.path)
        
        print(json.dumps(result, indent=2))
    except MagentoAPIError as e:
        print_error_and_exit(e)

if __name__ == "__main__":
    main()