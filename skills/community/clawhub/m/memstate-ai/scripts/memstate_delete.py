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

def delete_memory(project_id, keypath, recursive=False):
    url = f"{BASE_URL}/memories/delete"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "memstate-skill/1.0"
    }
    
    data = {
        "project_id": project_id,
        "keypath": keypath,
        "recursive": recursive
    }

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
    parser = argparse.ArgumentParser(description="Soft-delete a memory by keypath")
    parser.add_argument("--project", required=True, help="Project ID")
    parser.add_argument("--keypath", required=True, help="Keypath to delete")
    parser.add_argument("--recursive", action="store_true", help="Delete the entire keypath subtree")
    
    args = parser.parse_args()
    sys.exit(delete_memory(args.project, args.keypath, args.recursive))
