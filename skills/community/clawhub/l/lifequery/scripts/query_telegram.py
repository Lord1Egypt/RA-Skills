#!/usr/bin/env python3
"""
Query Telegram history via LifeQuery API.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import argparse

def main():
    parser = argparse.ArgumentParser(description="Query a local LifeQuery instance.")
    parser.add_argument("query", help="The search query or question to ask about the user's Telegram history.")
    args = parser.parse_args()

    # Read configuration from environment variables defined in SKILL.md
    base_url = os.environ.get("LIFEQUERY_BASE_URL", "http://localhost:3134/v1").rstrip("/")
    api_key = os.environ.get("LIFEQUERY_API_KEY", "")

    url = f"{base_url}/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }
    
    # Support optional API key authentication
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # LifeQuery uses an OpenAI-compatible API endpoint structure
    data = {
        "model": "lifequery", 
        "messages": [
            {"role": "user", "content": args.query}
        ],
        "temperature": 0.0,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode("utf-8"), 
            headers=headers, 
            method="POST"
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        # Print the text answer (which LifeQuery automatically grounds with citations)
        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["message"]["content"]
            print(answer)
        else:
            print("Error: Unexpected response format from LifeQuery API.")
            print(json.dumps(result, indent=2))
        
    except urllib.error.URLError as e:
        print(f"Error communicating with LifeQuery API at {url}: {e}")
        if hasattr(e, 'read'):
            try:
                error_response = e.read().decode('utf-8')
                print(f"Server response: {error_response}")
            except Exception:
                pass
        sys.exit(1)

if __name__ == "__main__":
    main()
