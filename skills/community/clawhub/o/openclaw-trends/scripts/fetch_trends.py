#!/usr/bin/env python3
"""
Fetch OpenClaw trends from multiple sources.

Sources:
- YouTube (Data API v3)
- X/Twitter (web search)
- GitHub (gh CLI / REST API)
- Reddit (web search)
- Hacker News (web search)
- General web (articles, tutorials, blogs)
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Optional
import urllib.request
import urllib.parse
import urllib.error

# YouTube API Key (set via environment or default)
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyC-4zq2k2ohAwtQM7lF8jPct_QhzpENG88")

# Search queries
SEARCH_TERMS = [
    "openclaw",
    "openclaw ai",
    "openclaw agent",
    "openclaw tutorial",
]

def get_date_filter(days: int) -> str:
    """Get date filter for web search (YYYY-MM-DD)."""
    date = datetime.now() - timedelta(days=days)
    return date.strftime("%Y-%m-%d")


def search_youtube(days: int = 3, max_results: int = 10) -> list[dict]:
    """Search YouTube for OpenClaw videos using Data API v3."""
    results = []
    
    if not YOUTUBE_API_KEY:
        print("Warning: No YouTube API key set", file=sys.stderr)
        return results
    
    published_after = (datetime.now() - timedelta(days=days)).isoformat() + "Z"
    
    for query in SEARCH_TERMS[:2]:  # Limit queries
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "order": "date",
                "publishedAfter": published_after,
                "maxResults": max_results,
                "key": YOUTUBE_API_KEY,
            }
            
            full_url = f"{url}?{urllib.parse.urlencode(params)}"
            
            req = urllib.request.Request(full_url)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            for item in data.get("items", []):
                video_id = item["id"]["videoId"]
                snippet = item["snippet"]
                results.append({
                    "source": "YouTube",
                    "title": snippet["title"],
                    "description": snippet.get("description", "")[:200],
                    "url": f"https://youtube.com/watch?v={video_id}",
                    "date": snippet["publishedAt"][:10],
                    "thumbnail": snippet["thumbnails"].get("default", {}).get("url", ""),
                })
        except Exception as e:
            print(f"YouTube search error: {e}", file=sys.stderr)
    
    return results


def search_github(days: int = 3) -> list[dict]:
    """Search GitHub for OpenClaw repos, discussions, releases."""
    results = []
    
    try:
        # Check if gh CLI is available
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
        
        # Search repos
        cmd = ["gh", "search", "repos", "openclaw", "--limit", "10", "--json", "name,description,url,updatedAt,stargazersCount"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if proc.returncode == 0:
            repos = json.loads(proc.stdout)
            cutoff = datetime.now() - timedelta(days=days)
            
            for repo in repos:
                updated = datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00"))
                if updated.replace(tzinfo=None) >= cutoff:
                    results.append({
                        "source": "GitHub Repo",
                        "title": repo["name"],
                        "description": (repo.get("description") or "")[:200],
                        "url": repo["url"],
                        "date": repo["updatedAt"][:10],
                        "stars": repo.get("stargazersCount", 0),
                    })
    except Exception as e:
        print(f"GitHub search error: {e}", file=sys.stderr)
    
    return results


def format_results(results: list[dict], output_format: str = "text") -> str:
    """Format results for output."""
    if not results:
        return "No recent OpenClaw content found."
    
    # Deduplicate by URL
    seen = set()
    unique = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)
    
    # Sort by date (newest first)
    unique.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    if output_format == "json":
        return json.dumps(unique, indent=2)
    
    # Text format
    lines = [f"# OpenClaw Trends ({len(unique)} results)\n"]
    
    # Group by source
    by_source = {}
    for r in unique:
        src = r["source"]
        by_source.setdefault(src, []).append(r)
    
    for source, items in sorted(by_source.items()):
        lines.append(f"\n## {source}\n")
        for item in items:
            lines.append(f"**{item['title']}**")
            if item.get("description"):
                lines.append(f"> {item['description'][:150]}...")
            lines.append(f"🔗 {item['url']}")
            if item.get("date"):
                lines.append(f"📅 {item['date']}")
            lines.append("")
    
    return "\n".join(lines)


def search_web(query: str, site: str = None, days: int = 3) -> list[dict]:
    """Search web using DuckDuckGo HTML (no API key needed)."""
    results = []
    
    try:
        # Build search query
        search_q = query
        if site:
            search_q = f"site:{site} {query}"
        
        # Use DuckDuckGo HTML version for parsing
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(search_q)}"
        
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw-Trends/1.0)"
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode("utf-8", errors="ignore")
        
        # Parse results from HTML
        import re
        
        # DuckDuckGo HTML results pattern
        pattern = r'<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for i, (href, title) in enumerate(matches[:10]):
            # DuckDuckGo uses redirect URLs, extract actual URL
            if "uddg=" in href:
                actual_url = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("uddg", [href])[0]
            else:
                actual_url = href
            
            results.append({
                "source": site or "Web",
                "title": title.strip(),
                "description": "",
                "url": actual_url,
                "date": datetime.now().strftime("%Y-%m-%d"),
            })
    except Exception as e:
        print(f"Web search error ({site or 'general'}): {e}", file=sys.stderr)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch OpenClaw trends")
    parser.add_argument("--days", type=int, default=3, help="Days to look back (default: 3)")
    parser.add_argument("--output", choices=["json", "text"], default="text", help="Output format")
    parser.add_argument("--notify", action="store_true", help="Send to notification channel")
    parser.add_argument("--no-web", action="store_true", help="Skip X/Reddit/HN web search")
    args = parser.parse_args()
    
    print(f"Fetching OpenClaw trends from last {args.days} days...", file=sys.stderr)
    
    all_results = []
    
    # YouTube
    print("Checking YouTube...", file=sys.stderr)
    all_results.extend(search_youtube(days=args.days))
    
    # GitHub
    print("Checking GitHub...", file=sys.stderr)
    all_results.extend(search_github(days=args.days))
    
    # Web search (X/Twitter, Reddit, HN)
    if not args.no_web:
        print("Checking X/Twitter...", file=sys.stderr)
        all_results.extend(search_web("openclaw", site="x.com", days=args.days))
        
        print("Checking Reddit...", file=sys.stderr)
        all_results.extend(search_web("openclaw", site="reddit.com", days=args.days))
        
        print("Checking Hacker News...", file=sys.stderr)
        all_results.extend(search_web("openclaw", site="news.ycombinator.com", days=args.days))
    
    # Format output
    output = format_results(all_results, args.output)
    
    if args.notify:
        # Send via OpenClaw message tool (would need integration)
        print(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
