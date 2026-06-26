#!/usr/bin/env python3
"""
Import NDJSON file to Kibana via Saved Objects API.
Usage: python3 import_ndjson.py [kibana-url] [ndjson-file] [--overwrite]
"""

import json
import sys
import urllib.request
import os

DEFAULT_KIBANA = "http://192.168.99.43"

def import_ndjson(kibana_url, file_path, overwrite=True):
    """Import NDJSON file to Kibana."""
    url = f"{kibana_url}/api/saved_objects/_import?overwrite={str(overwrite).lower()}"
    
    # Read the NDJSON file
    with open(file_path, "rb") as f:
        ndjson_data = f.read()
    
    # Create multipart form data
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    body = f"--{boundary}\r\n"
    body += 'Content-Disposition: form-data; name="file"; filename="import.ndjson"\r\n'
    body += "Content-Type: application/x-ndjson\r\n\r\n"
    body = body.encode("utf-8") + ndjson_data + b"\r\n"
    body += f"--{boundary}--\r\n"
    
    req = urllib.request.Request(
        url, data=body,
        headers={
            "kbn-xsrf": "true",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        try:
            return json.loads(error_body)
        except:
            return {"success": False, "error": error_body}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 import_ndjson.py <kibana-url> <ndjson-file> [--overwrite]")
        print(f"Example: python3 import_ndjson.py {DEFAULT_KIBANA} /tmp/dashboard.ndjson --overwrite")
        sys.exit(1)
    
    kibana_url = sys.argv[1]
    file_path = sys.argv[2]
    overwrite = "--overwrite" in sys.argv
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    print(f"Importing: {file_path}")
    print(f"Overwrite: {overwrite}")
    print("-" * 50)
    
    result = import_ndjson(kibana_url, file_path, overwrite)
    
    if result.get("success"):
        print("✅ Import successful!")
        
        # Report results
        if "results" in result:
            created = result["results"].get("created", [])
            updated = result["results"].get("updated", [])
            conflict = result["results"].get("conflict", [])
            
            print(f"  Created: {len(created)}")
            print(f"  Updated: {len(updated)}")
            print(f"  Conflicts: {len(conflict)}")
    else:
        print(f"❌ Import failed: {result.get('error', result.get('message', 'Unknown error'))}")
        sys.exit(1)

if __name__ == "__main__":
    main()