#!/usr/bin/env python3
"""
Export a dashboard and its dependencies via Saved Objects API.
Usage: python3 export_dashboard.py [kibana-url] [dashboard-id]
"""

import json
import sys
import urllib.request

DEFAULT_KIBANA = "http://192.168.99.43"

def export_objects(kibana_url, objects):
    """Export saved objects as NDJSON."""
    url = f"{kibana_url}/api/saved_objects/_export"
    
    data = json.dumps({"objects": objects}).encode("utf-8")
    
    req = urllib.request.Request(
        url, data=data,
        headers={"kbn-xsrf": "true", "Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            # Response is NDJSON stream
            result = []
            for line in response:
                line = line.decode().strip()
                if line:
                    result.append(json.loads(line))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 export_dashboard.py <kibana-url> <dashboard-id>")
        print(f"Example: python3 export_dashboard.py {DEFAULT_KIBANA} abc123")
        sys.exit(1)
    
    kibana_url = sys.argv[1]
    dashboard_id = sys.argv[2]
    
    print(f"Exporting dashboard: {dashboard_id}")
    print("-" * 50)
    
    # First, get the dashboard to find its references
    get_url = f"{kibana_url}/api/saved_objects/dashboard/{dashboard_id}"
    req = urllib.request.Request(get_url, headers={"kbn-xsrf": "true"})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            dash = json.loads(response.read().decode())
            attrs = dash.get("dashboard", {}).get("attributes", {})
            print(f"Title: {attrs.get('title', 'N/A')}")
            
            # Get all references
            references = dash.get("references", [])
            print(f"References: {len(references)}")
            
            for ref in references:
                print(f"  - {ref.get('type')}: {ref.get('id')}")
            
    except urllib.error.HTTPError as e:
        print(f"Dashboard not found: {e.code}")
        sys.exit(1)
    
    # Now export the dashboard and its references
    objects_to_export = [{"type": "dashboard", "id": dashboard_id}]
    for ref in references:
        objects_to_export.append({"type": ref.get("type"), "id": ref.get("id")})
    
    print("\nExporting objects...")
    results = export_objects(kibana_url, objects_to_export)
    
    if results is None:
        print("Export failed")
        sys.exit(1)
    
    print(f"\nExported {len(results)} object(s):")
    for obj in results:
        print(f"  - {obj.get('type')}: {obj.get('id')} ({obj.get('attributes', {}).get('title', 'N/A')})")
    
    # Save to file
    output_file = f"/tmp/dashboard_export_{dashboard_id}.ndjson"
    with open(output_file, "w") as f:
        for obj in results:
            f.write(json.dumps(obj) + "\n")
    
    print(f"\n✅ Saved to: {output_file}")

if __name__ == "__main__":
    main()