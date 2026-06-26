#!/usr/bin/env python3
import sys
import json
import requests
import argparse
import os
import time
import logging

# --- Configuration ---
DEFAULT_API_URL = "http://127.0.0.1:8001/search"
API_URL = os.getenv("MEMORY_PRO_API_URL", DEFAULT_API_URL)
TIMEOUT = int(os.getenv("MEMORY_PRO_TIMEOUT", 10))
# Increase retry attempts for slower starts (e.g. index rebuild)
MAX_RETRIES = 10 
RETRY_DELAY = 2  # seconds

# --- Logging ---
# Configure basic logging to stderr
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')
logger = logging.getLogger("memory-pro-client")

def search_semantic(query, top_k=3, json_output=False, mode=None):
    """
    Query the semantic search API with retry logic.
    """
    url = API_URL  # Use global or overridden URL
    
    payload = {
        "query": query,
        "top_k": top_k
    }
    if mode:
        payload["mode"] = mode
    headers = {"Content-Type": "application/json"}
    
    for attempt in range(MAX_RETRIES):
        try:
            # Send POST request
            response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            # Service might be starting up
            if attempt < MAX_RETRIES - 1:
                if not json_output:
                    sys.stderr.write(f"Connection failed, retrying ({attempt+1}/{MAX_RETRIES})...\n")
                time.sleep(RETRY_DELAY)
            else:
                if not json_output:
                    logger.error(f"Could not connect to Memory Pro service at {url}. Is it running?")
                sys.exit(1)
        
        except requests.exceptions.Timeout:
            # Request took too long
            if attempt < MAX_RETRIES - 1:
                if not json_output:
                    sys.stderr.write(f"Request timed out, retrying ({attempt+1}/{MAX_RETRIES})...\n")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Request timed out.")
                sys.exit(1)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            sys.exit(1)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from server.")
            sys.exit(1)
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(1)

def main():
    global API_URL
    
    parser = argparse.ArgumentParser(description="Query Memory Pro semantic search.")
    parser.add_argument("query", help="The search query string.")
    parser.add_argument("--top_k", "-k", type=int, default=3, help="Number of results to return.")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON.")
    parser.add_argument("--url", help="Override API URL", default=None)
    parser.add_argument("--mode", choices=["vector", "hybrid"], default=None, help="Search mode override")
    
    args = parser.parse_args()
    
    if args.url:
        API_URL = args.url
    
    result = search_semantic(args.query, args.top_k, args.json, args.mode)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n🔍 Search results for: '{args.query}'\n")
        results = result.get("results", [])
        
        if not results:
            print("No relevant memories found.")
        else:
            for i, item in enumerate(results, 1):
                # Handle dictionary items (from result list)
                if isinstance(item, dict):
                    score = item.get("score", 0.0)
                    sentence = item.get("sentence", "").strip()
                else:
                    # Fallback if structure is unexpected
                    score = 0.0
                    sentence = str(item)
                    
                print(f"{i}. [Score: {score:.2f}]")
                print(f"   {sentence}")
                print("-" * 40)

if __name__ == "__main__":
    main()
