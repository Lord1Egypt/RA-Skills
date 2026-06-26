#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.request

API_KEY = os.environ.get("MEMSTATE_API_KEY")
if not API_KEY:
    print("Error: MEMSTATE_API_KEY environment variable is required", file=sys.stderr)
    sys.exit(1)
BASE_URL = "https://api.memstate.ai/api/v1"

def remember_content(project_id, content, source=None, context=None):
    url = f"{BASE_URL}/ingest"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "memstate-skill/1.0"
    }
    
    data = {
        "project_id": project_id,
        "content": content
    }
    
    if source:
        data["source"] = source
    if context:
        data["context"] = context

    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            job_id = result.get("job_id")
            if not job_id:
                print(json.dumps(result, indent=2))
                return 0
                
            print(f"Job started with ID: {job_id}. Polling for completion...")
            
            # Poll for completion
            while True:
                time.sleep(2)
                status_url = f"{BASE_URL}/jobs/{job_id}"
                status_req = urllib.request.Request(status_url, headers=headers)
                
                with urllib.request.urlopen(status_req) as status_resp:
                    status_result = json.loads(status_resp.read().decode("utf-8"))
                    status = status_result.get("status")
                    
                    if status in ["completed", "failed", "error"]:
                        print(json.dumps(status_result, indent=2))
                        return 0 if status == "completed" else 1
                        
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code} - {e.read().decode('utf-8')}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save markdown or text, extracting keypaths automatically")
    parser.add_argument("--project", required=True, help="Project ID")
    parser.add_argument("--content", required=True, help="Markdown or text to remember")
    parser.add_argument("--source", help="Source type (agent, readme, docs, etc.)")
    parser.add_argument("--context", help="Optional hint to guide extraction")
    
    args = parser.parse_args()
    sys.exit(remember_content(args.project, args.content, args.source, args.context))
