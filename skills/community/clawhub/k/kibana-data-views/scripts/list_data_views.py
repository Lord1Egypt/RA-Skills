#!/usr/bin/env python3
"""
List all Kibana Data Views via the Kibana Data Views API.
Usage: python3 list_data_views.py [kibana-url]
"""

import json
import sys
import urllib.request

DEFAULT_KIBANA = "http://192.168.99.43"

def list_data_views(kibana_url):
    url = f"{kibana_url}/api/data_views"
    
    req = urllib.request.Request(url, headers={"kbn-xsrf": "true"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            # API returns "data_view" (singular) as the array key
            return data.get("data_view", [])
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
    
    data_views = list_data_views(kibana_url)
    
    if data_views is None:
        print("Failed to retrieve data views")
        sys.exit(1)
    
    if not data_views:
        print("No data views found.")
        return
    
    print(f"Found {len(data_views)} data view(s):\n")
    
    for dv in data_views:
        print(f"  ID: {dv.get('id', 'N/A')}")
        print(f"  Title: {dv.get('title', 'N/A')}")
        print(f"  Name: {dv.get('name', 'N/A')}")
        print(f"  Time Field: {dv.get('timeFieldName', 'N/A')}")
        print()

if __name__ == "__main__":
    main()