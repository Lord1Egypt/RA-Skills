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

def get_history(project_id=None, keypath=None, memory_id=None):
    url = f"{BASE_URL}/memories/history"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "memstate-skill/1.0"
    }
    
    data = {}
    if memory_id:
        data["memory_id"] = memory_id
    elif project_id and keypath:
        data["project_id"] = project_id
        data["keypath"] = keypath
    else:
        print("Error: Must provide either --memory-id OR both --project and --keypath", file=sys.stderr)
        return 1

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
    parser = argparse.ArgumentParser(description="View version history for a keypath or memory chain")
    parser.add_argument("--project", help="Project ID (required with --keypath)")
    parser.add_argument("--keypath", help="Keypath to get history for")
    parser.add_argument("--memory-id", help="Memory ID to get history for")
    
    args = parser.parse_args()
    sys.exit(get_history(args.project, args.keypath, args.memory_id))
