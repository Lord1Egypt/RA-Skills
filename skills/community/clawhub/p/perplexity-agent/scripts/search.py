import os
import sys
import json
import requests

def search_perplexity(query):
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print(json.dumps({"success": False, "error": "PERPLEXITY_API_KEY environment variable not set"}))
        return

    url = "https://api.perplexity.ai/v1/agent"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "preset": "pro-search",
        "input": query
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extract output_text according to the documentation
        output_text = ""
        for entry in data.get("output", []):
            if entry.get("type") == "message":
                for content in entry.get("content", []):
                    if content.get("type") == "output_text":
                        output_text += content.get("text", "")

        print(json.dumps({"success": True, "answer": output_text, "model": data.get("model")}))

    except requests.exceptions.RequestException as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Usage: python3 search.py <query>"}))
    else:
        search_perplexity(sys.argv[1])
