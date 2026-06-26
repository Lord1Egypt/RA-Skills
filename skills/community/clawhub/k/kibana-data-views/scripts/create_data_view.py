#!/usr/bin/env python3
"""
Create a Kibana Data View via the Kibana Data Views API.
Usage: python3 create_data_view.py [kibana-url] [title] [name] [time-field]
"""

import json
import sys
import urllib.request
import urllib.error

DEFAULT_KIBANA = "http://192.168.99.43"

def create_data_view(kibana_url, title, name, time_field="@timestamp", allow_no_index=True):
    url = f"{kibana_url}/api/data_views/data_view"
    
    payload = {
        "data_view": {
            "title": title,
            "name": name,
            "timeFieldName": time_field,
            "allowNoIndex": allow_no_index
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "kbn-xsrf": "true",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            return {"success": True, "data_view": result.get("data_view", {})}
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
    args = sys.argv[1:]
    
    if len(args) < 3:
        print("Usage: python3 create_data_view.py <kibana-url> <title> <name> [time-field]")
        print(f"Example: python3 create_data_view.py {DEFAULT_KIBANA} 'zbx-metrics-*' 'Zabbix Metrics' '@timestamp'")
        sys.exit(1)
    
    kibana_url = args[0]
    title = args[1]
    name = args[2]
    time_field = args[3] if len(args) > 3 else "@timestamp"
    
    print(f"Creating data view:")
    print(f"  URL: {kibana_url}")
    print(f"  Title: {title}")
    print(f"  Name: {name}")
    print(f"  Time Field: {time_field}")
    print("-" * 50)
    
    result = create_data_view(kibana_url, title, name, time_field)
    
    if result["success"]:
        dv = result["data_view"]
        print(f"✅ Data view created successfully!")
        print(f"   ID: {dv.get('id', 'N/A')}")
        print(f"   Title: {dv.get('title', 'N/A')}")
        print(f"   Name: {dv.get('name', 'N/A')}")
    else:
        print(f"❌ Failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()