#!/usr/bin/env python3
"""
SearXNG CLI Utility
-------------------
A zero-dependency search tool for querying SearXNG instances.
Designed for clean text output, AI readability, and easy integration.
"""

import argparse
import os
import sys
import json
import ssl
import configparser
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Default SearXNG instance URL, configurable via config file
def get_searxng_url():
    """
    Reads SearXNG URL from config file.
    If config file doesn't exist or URL is not set, creates config file and prompts user to modify it.
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), "searxng.ini")
    
    # Check if config file exists
    if not os.path.exists(config_path):
        print("Error: Configuration file not found: searxng.ini", file=sys.stderr)
        print("Creating default configuration file...", file=sys.stderr)
        config["searxng"] = {"url": "http://localhost:8080"}
        with open(config_path, "w") as f:
            config.write(f)
        print("Please modify the URL in searxng.ini to point to your SearXNG instance.", file=sys.stderr)
        sys.exit(1)
    
    # Read config file
    config.read(config_path)
    
    # Check if [searxng] section exists
    if "searxng" not in config:
        print("Error: [searxng] section not found in searxng.ini", file=sys.stderr)
        print("Adding [searxng] section to configuration file...", file=sys.stderr)
        config["searxng"] = {"url": "http://localhost:8080"}
        with open(config_path, "w") as f:
            config.write(f)
        print("Please modify the URL in searxng.ini to point to your SearXNG instance.", file=sys.stderr)
        sys.exit(1)
    
    # Check if url key exists
    if "url" not in config["searxng"]:
        print("Error: url key not found in [searxng] section of searxng.ini", file=sys.stderr)
        print("Adding url key to configuration file...", file=sys.stderr)
        config["searxng"]["url"] = "http://localhost:8080"
        with open(config_path, "w") as f:
            config.write(f)
        print("Please modify the URL in searxng.ini to point to your SearXNG instance.", file=sys.stderr)
        sys.exit(1)
    
    return config["searxng"]["url"]

SEARXNG_URL = get_searxng_url()


def search_searxng(query, limit=10, category="general", language="auto", time_range=None):
    """
    Executes a GET request to the SearXNG JSON API.
    
    Args:
        query (str): The search terms.
        limit (int): Max number of results to slice from the response.
        category (str): Search category (general, news, it, science, etc.).
        language (str): UI/Search language (e.g., 'zh-CN', 'en').
        time_range (str): Filter results by 'day', 'week', 'month', or 'year'.
        
    Returns:
        dict: Parsed JSON response containing 'results', 'infoboxes', etc.
    """
    # Construct API parameters
    params = {
        "q": query,
        "format": "json",
        "categories": category,
    }
    if language != "auto":
        params["language"] = language
    if time_range:
        params["time_range"] = time_range

    # Build final URL with encoded query string
    full_url = f"{SEARXNG_URL}/search?{urlencode(params)}"
    
    # Configure SSL context to ignore certificate verification.
    # Essential for local instances using self-signed certificates.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        # Perform the HTTP GET request
        req = Request(full_url)
        with urlopen(req, context=ctx, timeout=30) as response:
            # Decode response body and convert to Python dictionary
            data = json.loads(response.read().decode("utf-8"))
            
            # Apply result limit manually
            if "results" in data:
                data["results"] = data["results"][:limit]
            return data
    except Exception as e:
        # Standard error reporting to stderr
        print(f"Error fetching results: {e}", file=sys.stderr)
        return {"error": str(e), "results": []}

def display_results_table(data, query):
    """
    Outputs search results to the console in a structured, plain-text format.
    Includes a summary table and detailed snippets for top results.
    """
    results = data.get("results", [])
    if not results:
        print(f"No results found for: {query}")
        return

    # Header Section
    print(f"\nSEARCH RESULTS: {query}")
    print("-" * 85)
    print(f"{'ID':<4} {'Title':<55} {'URL'}")
    print("-" * 85)

    # Main Results Table (truncated titles for layout stability)
    for i, result in enumerate(results, 1):
        title = result.get("title", "No Title")
        display_title = (title[:52] + "...") if len(title) > 52 else title
        url = result.get("url", "")
        print(f"{i:<4} {display_title:<55} {url}")

    # Detailed Snippets for Top 3 results
    print("\n--- TOP RESULT DETAILS ---")
    for i, result in enumerate(results[:3], 1):
        print(f"\n[{i}] {result.get('title')}")
        print(f"    URL: {result.get('url')}")
        # Clean up snippet content: remove newlines and extra spaces
        content = result.get('content', '').strip().replace('\n', ' ')
        if content:
            print(f"    Snippet: {content[:300]}...")

def main():
    """
    Entry point: Handles command-line argument parsing and orchestration.
    """
    parser = argparse.ArgumentParser(description="SearXNG CLI - Zero Dependency Search")
    
    # Subcommand pattern (e.g., 'script.py search "keyword"')
    subparsers = parser.add_subparsers(dest="command")
    search_parser = subparsers.add_parser("search", help="Execute a search query")
    
    # Argument Definitions
    search_parser.add_argument("query", nargs="+", help="Search terms")
    search_parser.add_argument("-n", "--limit", type=int, default=10, help="Number of results")
    search_parser.add_argument("-c", "--category", default="general", help="SearXNG category")
    search_parser.add_argument("-l", "--language", default="auto", help="Language code")
    search_parser.add_argument("-t", "--time-range", choices=["day", "week", "month", "year"], help="Time filter")
    search_parser.add_argument("-f", "--format", choices=["table", "json"], default="table", help="Output style")
    
    args = parser.parse_args()
    
    # Default to help if no command provided
    if not args.command:
        parser.print_help()
        return

    # Process search query and handle results
    query_string = " ".join(args.query)
    search_data = search_searxng(
        query=query_string, 
        limit=args.limit, 
        category=args.category, 
        language=args.language, 
        time_range=args.time_range
    )

    # Output selection
    if args.format == "json":
        # ensure_ascii=False preserves non-Latin characters (e.g., Chinese)
        print(json.dumps(search_data, indent=2, ensure_ascii=False))
    else:
        display_results_table(search_data, query_string)

if __name__ == "__main__":
    main()
