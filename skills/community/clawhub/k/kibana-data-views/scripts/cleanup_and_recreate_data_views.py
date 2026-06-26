#!/usr/bin/env python3
"""
Clean up and recreate all Kibana Data Views for Omni-Monitor.
This fixes corrupted/orphaned data views that exist in list but return 404 on GET.

Usage: python3 cleanup_and_recreate_data_views.py [kibana-url] [--dry-run]
"""

import json
import sys
import urllib.request
import urllib.error

DEFAULT_KIBANA = "http://192.168.99.43"

# All required data views for Omni-Monitor
ALL_DATA_VIEWS = [
    {"title": "zbx-metrics-*", "name": "Zabbix Metrics"},
    {"title": "zbx-hosts-*", "name": "Zabbix Hosts"},
    {"title": "zbx-problems-*", "name": "Zabbix Problems"},
    {"title": "zbx-triggers-*", "name": "Zabbix Triggers"},
    {"title": "k8s-pod-logs-*", "name": "K8s Pod Logs"},
    {"title": "k8s-audit-logs-*", "name": "K8s Audit Logs"},
    {"title": "vm-system-logs-*", "name": "VM System Logs"},
    {"title": "ingress-nginx-logs-*", "name": "Ingress Nginx Logs"},
    {"title": "netbox-app-logs-*", "name": "NetBox App Logs"},
    {"title": "wiki-app-logs-*", "name": "Wiki.js App Logs"},
    {"title": "elastic-app-logs-*", "name": "Elasticsearch App Logs"},
    {"title": "logstash-app-logs-*", "name": "Logstash App Logs"},
    {"title": "kibana-app-logs-*", "name": "Kibana App Logs"},
    {"title": "*-logs-*", "name": "All Logs"},
]

def api_request(kibana_url, method, path, data=None):
    """Make an API request to Kibana."""
    url = f"{kibana_url}{path}"
    
    headers = {"kbn-xsrf": "true"}
    if data:
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=headers,
        method=method
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 204:
                return {"success": True, "status": 204}
            return {"success": True, "data": json.loads(response.read().decode())}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        try:
            error_json = json.loads(error_body)
            return {"success": False, "status": e.code, "error": error_json}
        except:
            return {"success": False, "status": e.code, "error": error_body}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_all_data_views(kibana_url):
    """Get all data views using the list API."""
    result = api_request(kibana_url, "GET", "/api/data_views")
    if result["success"]:
        return result["data"].get("data_view", [])
    return []

def get_data_view(kibana_url, view_id):
    """Get a specific data view by ID."""
    return api_request(kibana_url, "GET", f"/api/data_views/{view_id}")

def delete_data_view(kibana_url, view_id):
    """Delete a data view by ID."""
    return api_request(kibana_url, "DELETE", f"/api/data_views/{view_id}")

def create_data_view(kibana_url, title, name):
    """Create a new data view."""
    return api_request(
        kibana_url, "POST", "/api/data_views/data_view",
        data={
            "data_view": {
                "title": title,
                "name": name,
                "timeFieldName": "@timestamp",
                "allowNoIndex": True
            }
        }
    )

def cleanup_and_recreate(kibana_url, dry_run=False):
    """Main function to clean up and recreate data views."""
    print("=" * 60)
    print("Kibana Data Views - Cleanup & Recreate")
    print("=" * 60)
    print(f"Target: {kibana_url}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()
    
    # Step 1: Get all current data views
    print("[1/4] Fetching current data views...")
    all_dvs = get_all_data_views(kibana_url)
    print(f"      Found {len(all_dvs)} data view(s) in list")
    print()
    
    # Step 2: Filter out duplicates and check which are corrupt
    print("[2/4] Analyzing data views...")
    title_to_dvs = {}
    for dv in all_dvs:
        title = dv.get("title", "")
        if title not in title_to_dvs:
            title_to_dvs[title] = []
        title_to_dvs[title].append(dv)
    
    # Identify duplicates and corrupt entries
    duplicates = []
    corrupt = []
    valid = []
    
    for title, dvs in title_to_dvs.items():
        if len(dvs) > 1:
            duplicates.append((title, dvs))
        # Check if the data view is accessible
        if dvs:
            dv = dvs[0]  # Check first one
            dv_id = dv.get("id")
            if dv_id:
                check = get_data_view(kibana_url, dv_id)
                if check["success"]:
                    valid.append((title, dv))
                else:
                    corrupt.append((title, dv_id))
            else:
                corrupt.append((title, "NO_ID"))
    
    print(f"      Valid unique: {len(valid)}")
    print(f"      Duplicates: {len(duplicates)}")
    print(f"      Corrupt (404): {len(corrupt)}")
    print()
    
    if dry_run:
        print("[3/4] DRY RUN - Would delete these corrupt/duplicate IDs:")
        for title, dv_id in corrupt:
            print(f"      - {title}: {dv_id}")
        for title, dvs in duplicates:
            print(f"      - DUPLICATE: {title} ({len(dvs)} copies)")
        print()
        print("[4/4] DRY RUN - Would create:")
        for dv in ALL_DATA_VIEWS:
            print(f"      - {dv['title']} ({dv['name']})")
        return True
    
    # Step 3: Delete corrupt/duplicate data views
    print("[3/4] Cleaning up corrupt and duplicate data views...")
    
    # Delete corrupt ones
    for title, dv_id in corrupt:
        print(f"  Deleting corrupt: {title} ({dv_id})...")
        delete_data_view(kibana_url, dv_id)
    
    # Delete duplicates (keep first, delete rest)
    for title, dvs in duplicates:
        for dv in dvs[1:]:  # Skip first, delete rest
            dv_id = dv.get("id")
            print(f"  Deleting duplicate: {title} ({dv_id})...")
            delete_data_view(kibana_url, dv_id)
    
    print()
    
    # Step 4: Recreate all required data views
    print("[4/4] Recreating all required data views...")
    
    # First re-check what's left
    remaining = get_all_data_views(kibana_url)
    remaining_titles = {dv.get("title") for dv in remaining}
    
    created = []
    failed = []
    
    for dv_spec in ALL_DATA_VIEWS:
        title = dv_spec["title"]
        name = dv_spec["name"]
        
        if title in remaining_titles:
            print(f"  ✅ {title} - already exists, skipping")
            continue
        
        print(f"  Creating: {title}...")
        result = create_data_view(kibana_url, title, name)
        
        if result["success"]:
            new_dv = result["data"].get("data_view", {})
            print(f"     ✅ Created (ID: {new_dv.get('id', 'N/A')})")
            created.append(title)
        else:
            error_msg = result.get("error", {})
            if isinstance(error_msg, dict):
                error_msg = error_msg.get("message", str(error_msg))
            print(f"     ❌ Failed: {error_msg}")
            failed.append(title)
    
    print()
    print("=" * 60)
    print("Summary:")
    print(f"  Created: {len(created)}")
    print(f"  Failed: {len(failed)}")
    
    if failed:
        print(f"\n⚠️ Failed to create: {', '.join(failed)}")
        return False
    
    print("\n✅ All data views are now valid and accessible!")
    return True

def main():
    kibana_url = DEFAULT_KIBANA
    dry_run = False
    
    for arg in sys.argv[1:]:
        if arg.startswith("http"):
            kibana_url = arg
        elif arg in ["--dry-run", "-n"]:
            dry_run = True
    
    success = cleanup_and_recreate(kibana_url, dry_run=dry_run)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()