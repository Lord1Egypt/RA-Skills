#!/usr/bin/env python3
"""
Unified web search across multiple search engines.
Supports: Tavily API, Google, Bing, Baidu, DuckDuckGo (via agent-browser)
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.parse
from typing import Optional

# Search engine configurations
ENGINES = {
    "google": {
        "url_template": "https://www.google.com/search?q={query}",
        "name": "Google",
    },
    "bing": {
        "url_template": "https://www.bing.com/search?q={query}",
        "name": "Bing",
    },
    "baidu": {
        "url_template": "https://www.baidu.com/s?wd={query}",
        "name": "百度",
    },
    "duckduckgo": {
        "url_template": "https://duckduckgo.com/?q={query}",
        "name": "DuckDuckGo",
    },
}


def get_tavily_api_key() -> Optional[str]:
    """Get Tavily API key from environment or config file."""
    # Check environment first
    key = os.environ.get("TAVILY_API_KEY")
    if key:
        return key

    # Check config file
    config_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("TAVILY_API_KEY="):
                    return line.split("=", 1)[1].strip()

    return None


def search_tavily(query: str, max_results: int = 5, include_answer: bool = False, format: str = "json") -> dict:
    """Search using Tavily API."""
    api_key = get_tavily_api_key()
    if not api_key:
        return {
            "error": "TAVILY_API_KEY not found. Set environment variable or add to ~/.openclaw/.env",
            "query": query,
            "engine": "tavily",
            "results": [],
        }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    tavily_script = os.path.join(script_dir, "..", "..", "openclaw-tavily-search", "scripts", "tavily_search.py")

    if not os.path.exists(tavily_script):
        # Fallback to direct API call
        return search_tavily_direct(query, api_key, max_results, include_answer, format)

    cmd = [
        "python3",
        tavily_script,
        "--query", query,
        "--max-results", str(max_results),
        "--format", "brave" if format == "json" else format,
    ]

    if include_answer:
        cmd.append("--include-answer")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            data["engine"] = "tavily"
            return data
        else:
            return {
                "error": result.stderr or "Tavily search failed",
                "query": query,
                "engine": "tavily",
                "results": [],
            }
    except Exception as e:
        return {
            "error": str(e),
            "query": query,
            "engine": "tavily",
            "results": [],
        }


def search_tavily_direct(query: str, api_key: str, max_results: int = 5, include_answer: bool = False, format: str = "json") -> dict:
    """Direct Tavily API call (fallback)."""
    try:
        import requests

        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "max_results": max_results,
            "include_answer": include_answer,
        }

        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Normalize to standard format
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", item.get("snippet", "")),
            })

        output = {
            "query": query,
            "engine": "tavily",
            "results": results,
        }

        if include_answer and data.get("answer"):
            output["answer"] = data["answer"]

        return output

    except ImportError:
        return {
            "error": "requests module not installed. Run: pip install requests",
            "query": query,
            "engine": "tavily",
            "results": [],
        }
    except Exception as e:
        return {
            "error": str(e),
            "query": query,
            "engine": "tavily",
            "results": [],
        }


def search_browser(engine: str, query: str, max_results: int = 5) -> dict:
    """Search using agent-browser to access search engine."""
    if engine not in ENGINES:
        return {
            "error": f"Unknown engine: {engine}. Available: {', '.join(ENGINES.keys())}",
            "query": query,
            "engine": engine,
            "results": [],
        }

    engine_config = ENGINES[engine]
    encoded_query = urllib.parse.quote(query)
    url = engine_config["url_template"].format(query=encoded_query)

    try:
        # Use agent-browser to open and snapshot the search results
        # Open the search URL
        open_result = subprocess.run(
            ["agent-browser", "open", url],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if open_result.returncode != 0:
            return {
                "error": f"Failed to open {engine}: {open_result.stderr}",
                "query": query,
                "engine": engine,
                "results": [],
            }

        # Wait for page to load
        subprocess.run(
            ["agent-browser", "wait", "2000"],
            capture_output=True,
            timeout=10,
        )

        # Get snapshot with interactive elements
        snapshot_result = subprocess.run(
            ["agent-browser", "snapshot", "-i", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if snapshot_result.returncode != 0:
            return {
                "error": f"Failed to snapshot: {snapshot_result.stderr}",
                "query": query,
                "engine": engine,
                "results": [],
            }

        # Parse snapshot and extract results
        results = parse_search_results(engine, snapshot_result.stdout, max_results)

        # Close browser
        subprocess.run(["agent-browser", "close"], capture_output=True, timeout=10)

        return {
            "query": query,
            "engine": engine,
            "results": results,
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Search timed out",
            "query": query,
            "engine": engine,
            "results": [],
        }
    except FileNotFoundError:
        return {
            "error": "agent-browser not found. Install with: npm install -g agent-browser",
            "query": query,
            "engine": engine,
            "results": [],
        }
    except Exception as e:
        return {
            "error": str(e),
            "query": query,
            "engine": engine,
            "results": [],
        }


def parse_search_results(engine: str, snapshot_json: str, max_results: int) -> list:
    """Parse search results from browser snapshot."""
    results = []

    try:
        snapshot = json.loads(snapshot_json)
    except json.JSONDecodeError:
        return results

    # Different engines have different DOM structures
    # This is a simplified extraction - real implementation would need more robust parsing

    count = 0
    for element in snapshot if isinstance(snapshot, list) else [snapshot]:
        if count >= max_results:
            break

        if isinstance(element, dict):
            # Look for link elements
            tag = element.get("tag", "").lower()
            role = element.get("role", "").lower()

            if tag == "a" or role == "link":
                text = element.get("text", "").strip()
                href = element.get("href", "")

                # Filter out navigation links
                if text and href and not href.startswith("#"):
                    # Skip if text is too short (likely nav element)
                    if len(text) > 20:
                        results.append({
                            "title": text[:200],  # Truncate long titles
                            "url": href,
                            "snippet": "",
                        })
                        count += 1

            # Recursively check children
            if "children" in element:
                child_results = parse_search_results(engine, json.dumps(element["children"]), max_results - count)
                results.extend(child_results)
                count = len(results)

    return results[:max_results]


def search_all(query: str, max_results: int = 5, format: str = "json") -> dict:
    """Aggregate results from multiple search engines."""
    all_results = []
    errors = []

    # Search Tavily (fast)
    tavily_result = search_tavily(query, max_results=max_results, format=format)
    if "error" not in tavily_result:
        all_results.extend(tavily_result.get("results", []))
    else:
        errors.append(f"tavily: {tavily_result['error']}")

    # Search Google
    google_result = search_browser("google", query, max_results=max_results)
    if "error" not in google_result:
        all_results.extend(google_result.get("results", []))
    else:
        errors.append(f"google: {google_result['error']}")

    # Search Baidu
    baidu_result = search_browser("baidu", query, max_results=max_results)
    if "error" not in baidu_result:
        all_results.extend(baidu_result.get("results", []))
    else:
        errors.append(f"baidu: {baidu_result['error']}")

    # Deduplicate by URL
    seen_urls = set()
    unique_results = []
    for result in all_results:
        url = result.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)

    return {
        "query": query,
        "engine": "all",
        "results": unique_results[:max_results * 2],  # Return more results for aggregation
        "sources": ["tavily", "google", "baidu"],
        "errors": errors if errors else None,
    }


def format_markdown(data: dict) -> str:
    """Format results as Markdown."""
    lines = [f'## Search Results: "{data["query"]}"', ""]

    if data.get("error"):
        lines.append(f"**Error:** {data['error']}")
        return "\n".join(lines)

    results = data.get("results", [])
    if not results:
        lines.append("No results found.")
        return "\n".join(lines)

    for i, result in enumerate(results, 1):
        title = result.get("title", "Untitled")
        url = result.get("url", "")
        snippet = result.get("snippet", "")

        if url:
            lines.append(f'{i}. **[{title}]({url})**')
        else:
            lines.append(f'{i}. **{title}**')

        if snippet:
            lines.append(f"   {snippet}")
        lines.append("")

    if data.get("answer"):
        lines.append("### Answer")
        lines.append(data["answer"])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Unified web search across multiple engines")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--engine", "-e", default="tavily",
                        choices=["tavily", "google", "bing", "baidu", "duckduckgo", "all"],
                        help="Search engine to use (default: tavily)")
    parser.add_argument("--max-results", "-n", type=int, default=5, help="Maximum results (default: 5)")
    parser.add_argument("--format", "-f", choices=["json", "md"], default="json",
                        help="Output format (default: json)")
    parser.add_argument("--include-answer", action="store_true",
                        help="Include AI-generated answer summary (Tavily only)")

    args = parser.parse_args()

    # Execute search based on engine
    if args.engine == "tavily":
        result = search_tavily(args.query, args.max_results, args.include_answer, args.format)
    elif args.engine == "all":
        result = search_all(args.query, args.max_results, args.format)
    else:
        result = search_browser(args.engine, args.query, args.max_results)

    # Format output
    if args.format == "md":
        print(format_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
