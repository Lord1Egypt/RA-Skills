#!/usr/bin/env python3
"""
memstate_get.py — Browse and retrieve memories from Memstate AI.

Usage:
  python3 memstate_get.py                                    # List all projects
  python3 memstate_get.py --project myapp                   # Full project tree (domains)
  python3 memstate_get.py --project myapp --keypath db      # Subtree at keypath
  python3 memstate_get.py --project myapp --keypath db --include-content
  python3 memstate_get.py --memory-id <uuid>                # Single memory by ID
  python3 memstate_get.py --project myapp --keypath db --at-revision 3
"""
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

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "memstate-skill/1.0"
}


def get_memories(project_id=None, keypath=None, memory_id=None, include_content=False, at_revision=None):
    try:
        if memory_id:
            # GET /memories/{id} — single memory by UUID
            url = f"{BASE_URL}/memories/{memory_id}"
            req = urllib.request.Request(url, headers=HEADERS)

        elif project_id and keypath:
            # POST /keypaths — subtree at a specific keypath
            url = f"{BASE_URL}/keypaths"
            data = {
                "project_id": project_id,
                "keypath": keypath,
                "recursive": True,
                "include_content": include_content,
            }
            if at_revision:
                data["at_revision"] = at_revision
            req = urllib.request.Request(
                url, data=json.dumps(data).encode("utf-8"), headers=HEADERS, method="POST"
            )

        elif project_id:
            # GET /tree — full project domain tree
            url = f"{BASE_URL}/tree?project_id={project_id}"
            req = urllib.request.Request(url, headers=HEADERS)

        else:
            # GET /projects — list all projects
            print("Listing all projects...", file=sys.stderr)
            url = f"{BASE_URL}/projects"
            req = urllib.request.Request(url, headers=HEADERS)

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
    parser = argparse.ArgumentParser(
        description="Browse and retrieve memories from Memstate AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--project", help="Project ID")
    parser.add_argument("--keypath", help="Subkeypath within project (e.g. 'database' or 'config.port')")
    parser.add_argument("--memory-id", help="Get a single memory by its UUID")
    parser.add_argument("--include-content", action="store_true", help="Include full memory content in response")
    parser.add_argument("--at-revision", type=int, help="Optional revision number for time-travel queries")

    args = parser.parse_args()
    sys.exit(get_memories(args.project, args.keypath, args.memory_id, args.include_content, args.at_revision))
