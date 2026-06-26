import sys
import json
import requests
import os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillbossai.com/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

def web_search(query, num_results=5):
    result = pilot({
        "type": "search",
        "inputs": {"query": query, "num": num_results},
        "prefer": "balanced"
    })
    return result["result"]["results"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <query> [num_results]")
        sys.exit(1)

    query = sys.argv[1]
    num_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    try:
        results = web_search(query, num_results)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
