#!/usr/bin/env python3
"""
Delete a Kibana Data View via the Kibana Data Views API.
Usage: python3 delete_data_view.py [kibana-url] [view-id]
"""

import json
import sys
import urllib.request
import urllib.error

DEFAULT_KIBANA = "http://192.168.99.43"

def delete_data_view(kibana_url, view_id):
    url = f"{kibana_url}/api/data_views/{view_id}"
    
    req = urllib.request.Request(
        url,
        headers={"kbn-xsrf": "true"},
        method="DELETE"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return {"success": True, "status_code": response.status}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        try:
            error_json = json.loads(error_body)
            return {"success": False, "error": error_json.get("message", error_body)}
        except:
            return {"success": False, "error": error_body}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 delete_data_view.py <kibana-url> <view-id>")
        print(f"Example: python3 delete_data_view.py {DEFAULT_KIBANA} 'my-view-id'")
        sys.exit(1)
    
    kibana_url = sys.argv[1]
    view_id = sys.argv[2]
    
    print(f"Deleting data view:")
    print(f"  URL: {kibana_url}")
    print(f"  View ID: {view_id}")
    print("-" * 50)
    
    result = delete_data_view(kibana_url, view_id)
    
    if result["success"]:
        print(f"✅ Data view deleted successfully (status: {result['status_code']})")
    else:
        print(f"❌ Failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()