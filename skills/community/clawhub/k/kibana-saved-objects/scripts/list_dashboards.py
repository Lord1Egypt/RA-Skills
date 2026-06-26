#!/usr/bin/env python3
"""
List all Kibana dashboards via Saved Objects API.
Usage: python3 list_dashboards.py [kibana-url]
"""

import json
import sys
import urllib.request

DEFAULT_KIBANA = "http://192.168.99.43"

def list_dashboards(kibana_url):
    """List all dashboard saved objects."""
    url = f"{kibana_url}/api/saved_objects/_find"
    
    data = json.dumps({
        "type": "dashboard",
        "page": 1,
        "perPage": 100
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url, data=data,
        headers={"kbn-xsrf": "true", "Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def main():
    kibana_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_KIBANA
    
    print(f"Connecting to: {kibana_url}")
    print("-" * 50)
    
    result = list_dashboards(kibana_url)
    
    if result is None:
        print("Failed to retrieve dashboards")
        sys.exit(1)
    
    dashboards = result.get("saved_objects", [])
    total = result.get("total", 0)
    
    print(f"Found {total} dashboard(s):\n")
    
    for dash in dashboards:
        attrs = dash.get("attributes", {})
        print(f"  ID: {dash.get('id')}")
        print(f"  Title: {attrs.get('title', 'N/A')}")
        print(f"  Description: {attrs.get('description', 'N/A')}")
        print()

if __name__ == "__main__":
    main()