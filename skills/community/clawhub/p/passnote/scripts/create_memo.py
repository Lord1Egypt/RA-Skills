#!/usr/bin/env python3
import argparse
import os
import sys
import json
import urllib.request
import urllib.error

def main():
    parser = argparse.ArgumentParser(description="Create a PassNote memo")
    parser.add_argument("content", type=str, help="The content of the memo")
    parser.add_argument("--expire-hours", type=int, default=24, help="Hours until the memo expires (1-48)")
    
    args = parser.parse_args()
    
    api_url = os.environ.get("PASSNOTE_API_URL", "http://localhost:8000")
    api_token = os.environ.get("PASSNOTE_API_TOKEN")
    
    if not api_token:
        print("Error: PASSNOTE_API_TOKEN environment variable is not set.", file=sys.stderr)
        print("Please configure this skill in ~/.openclaw/openclaw.json", file=sys.stderr)
        sys.exit(1)
        
    api_url = api_url.rstrip("/")
    endpoint = f"{api_url}/api/v1/skill/memos/"
    
    payload = {
        "content": args.content,
        "expire_hours": args.expire_hours
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(endpoint, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {api_token}")
    
    try:
        response = urllib.request.urlopen(req)
        response_data = json.loads(response.read().decode("utf-8"))
        
        if response_data.get("code") == 0 and "data" in response_data:
            memo_data = response_data["data"]
            pass_key = memo_data.get("pass_key")
            
            frontend_url = api_url.replace("api.", "") # simplistic guess for frontend URL
            if "localhost" in frontend_url or "127.0.0.1" in frontend_url:
                frontend_url = "http://localhost:5173"
                
            view_link = f"{frontend_url}/note/{pass_key}"
            
            print(f"Memo created successfully!")
            print(f"Passcode: {pass_key}")
            print(f"View Link: {view_link}")
            print(f"Expires at: {memo_data.get('expired_at')}")
        else:
            print(f"Failed to create memo: {response_data.get('message', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
            
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_msg)
            print(f"API Error ({e.code}): {error_json.get('message', error_msg)}", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"HTTP Error {e.code}: {error_msg}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
