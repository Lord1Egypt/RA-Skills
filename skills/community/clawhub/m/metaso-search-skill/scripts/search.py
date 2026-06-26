import sys
import json
import requests
import os


def metaso_search(api_key: str, request_body: dict):
    """Search using Metaso AI API"""
    url = "https://metaso.cn/api/v1/search"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=request_body, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <JSON>")
        sys.exit(1)

    query_str = sys.argv[1]
    parse_data = {}

    try:
        parse_data = json.loads(query_str)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)

    if "q" not in parse_data:
        print("Error: 'q' (query) is required.")
        sys.exit(1)

    # Get API key from environment
    api_key = os.getenv("METASO_API_KEY")
    if not api_key:
        print("Error: METASO_API_KEY not set in environment.")
        sys.exit(1)

    # Build request body
    request_body = {
        "q": parse_data["q"],
        "scope": parse_data.get("scope", "webpage"),
        "size": parse_data.get("size", 10),
        "page": parse_data.get("page", 1),
        "conciseSnippet": parse_data.get("conciseSnippet", False),
        "includeSummary": parse_data.get("includeSummary", False),
        "includeRawContent": parse_data.get("includeRawContent", False)
    }

    try:
        results = metaso_search(api_key, request_body)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
