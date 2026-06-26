#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request

API_KEY = os.environ.get("MEMSTATE_API_KEY")
if not API_KEY:
    print("Error: MEMSTATE_API_KEY environment variable is required", file=sys.stderr)
    sys.exit(1)
BASE_URL = "https://api.memstate.ai/api/v1"

def set_memory(project_id, keypath, value, category=None, topics=None):
    url = f"{BASE_URL}/memories/remember"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "memstate-skill/1.0"
    }
    
    data = {
        "project_id": project_id,
        "keypath": keypath,
        "content": value
    }
    
    if category:
        data["category"] = category
    if topics:
        data["topics"] = topics.split(",")

    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(json.dumps(result, indent=2))
            return 0
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code} - {e.read().decode('utf-8')}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set a single fact at a specific keypath")
    parser.add_argument("--project", required=True, help="Project ID")
    parser.add_argument("--keypath", required=True, help="Hierarchical path (e.g., config.port)")
    parser.add_argument("--value", required=True, help="Value to store")
    parser.add_argument("--category", help="Category (decision, fact, config, etc.)")
    parser.add_argument("--topics", help="Comma-separated list of topics")
    
    args = parser.parse_args()
    sys.exit(set_memory(args.project, args.keypath, args.value, args.category, args.topics))
