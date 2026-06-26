#!/usr/bin/env python3
"""
Check and fix Kibana Data Views for Omni-Monitor project.
This script diagnoses the "Cannot read properties of undefined (reading 'indexpattern')" error.

Usage: python3 check_and_fix_data_views.py [kibana-url]
"""

import json
import sys
import urllib.request
import urllib.error

DEFAULT_KIBANA = "http://192.168.99.43"

# Omni-Monitor required data views
REQUIRED_DATA_VIEWS = [
    {"title": "zbx-metrics-*", "name": "Zabbix Metrics", "timeFieldName": "@timestamp"},
    {"title": "zbx-hosts-*", "name": "Zabbix Hosts", "timeFieldName": "@timestamp"},
    {"title": "zbx-problems-*", "name": "Zabbix Problems", "timeFieldName": "@timestamp"},
    {"title": "zbx-triggers-*", "name": "Zabbix Triggers", "timeFieldName": "@timestamp"},
    {"title": "k8s-pod-logs-*", "name": "K8s Pod Logs", "timeFieldName": "@timestamp"},
    {"title": "k8s-audit-logs-*", "name": "K8s Audit Logs", "timeFieldName": "@timestamp"},
    {"title": "vm-system-logs-*", "name": "VM System Logs", "timeFieldName": "@timestamp"},
    {"title": "ingress-nginx-logs-*", "name": "Ingress Nginx Logs", "timeFieldName": "@timestamp"},
    {"title": "netbox-app-logs-*", "name": "NetBox App Logs", "timeFieldName": "@timestamp"},
    {"title": "wiki-app-logs-*", "name": "Wiki.js App Logs", "timeFieldName": "@timestamp"},
    {"title": "elastic-app-logs-*", "name": "Elasticsearch App Logs", "timeFieldName": "@timestamp"},
    {"title": "logstash-app-logs-*", "name": "Logstash App Logs", "timeFieldName": "@timestamp"},
    {"title": "kibana-app-logs-*", "name": "Kibana App Logs", "timeFieldName": "@timestamp"},
    {"title": "*-logs-*", "name": "All Logs", "timeFieldName": "@timestamp"},
]

def list_data_views(kibana_url):
    """List all existing data views."""
    url = f"{kibana_url}/api/data_views"
    req = urllib.request.Request(url, headers={"kbn-xsrf": "true"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("data_views", [])
    except Exception as e:
        print(f"Error listing data views: {e}", file=sys.stderr)
        return []

def create_data_view(kibana_url, title, name, time_field="@timestamp"):
    """Create a data view."""
    url = f"{kibana_url}/api/data_views/data_view"
    
    payload = {
        "data_view": {
            "title": title,
            "name": name,
            "timeFieldName": time_field,
            "allowNoIndex": True
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"kbn-xsrf": "true", "Content-Type": "application/json"},
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

def check_and_fix(kibana_url, dry_run=False):
    """Check existing data views and create missing ones."""
    print("=" * 60)
    print("Kibana Data Views Diagnostic Tool")
    print("=" * 60)
    print(f"Target: {kibana_url}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()
    
    # List existing
    existing = list_data_views(kibana_url)
    existing_titles = {dv.get("title", ""): dv for dv in existing}
    
    print(f"Found {len(existing)} existing data view(s)")
    print()
    
    # Check each required
    missing = []
    present = []
    
    for required in REQUIRED_DATA_VIEWS:
        title = required["title"]
        if title in existing_titles:
            present.append(title)
            print(f"✅ {title}")
        else:
            missing.append(required)
            print(f"❌ {title} - MISSING")
    
    print()
    print("-" * 60)
    print(f"Summary: {len(present)} present, {len(missing)} missing")
    
    if not missing:
        print("\n✅ All required data views exist!")
        return True
    
    if dry_run:
        print("\n🔍 DRY RUN - Would create these data views:")
        for m in missing:
            print(f"   - {m['title']} ({m['name']})")
        return False
    
    # Create missing
    print("\n🔧 Creating missing data views...")
    created = []
    failed = []
    
    for required in missing:
        print(f"\n  Creating: {required['title']}...")
        result = create_data_view(
            kibana_url,
            required["title"],
            required["name"],
            required["timeFieldName"]
        )
        
        if result["success"]:
            dv = result["data_view"]
            print(f"     ✅ Created (ID: {dv.get('id', 'N/A')})")
            created.append(required["title"])
        else:
            print(f"     ❌ Failed: {result['error']}")
            failed.append(required["title"])
    
    print()
    print("-" * 60)
    print(f"Created: {len(created)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print(f"\n⚠️ Failed to create: {', '.join(failed)}")
    
    return len(failed) == 0

def main():
    kibana_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_KIBANA
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    success = check_and_fix(kibana_url, dry_run=dry_run)
    
    if not dry_run and success:
        print("\n✅ All data views are ready for Kibana dashboards!")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()