#!/usr/bin/env python3
"""
Poly-Tradebot: CNBC News Fetcher and Classifier

Fetches articles from CNBC World, classifies by topic (geopolitics vs macroeconomics),
and invokes appropriate skills for structured analysis.

Usage:
    python fetch_cnbc.py [--url <custom_url>] [--count <n>]
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# CNBC World URL
DEFAULT_CNBC_URL = "https://www.cnbc.com/world/?region=world"

# Tag keywords for filtering
GEOPOLITICS_KEYWORDS = [
    "iran", "war", "military", "conflict", "sanctions", "regime", "irgc",
    "drone", "missile", "hormuz", "uae", "middle east", "fujairah", "tanker", "airspace"
]

MACROECONOMICS_KEYWORDS = [
    "fed", "treasury", "yield", "interest rate", "inflation", "central bank",
    "cpi", "employment", "gdp", "monetary policy", "stagflation", "rba", "ecb"
]

def classify_article(headline: str, content: str) -> str:
    """
    Classify article as 'geopolitics' or 'macroeconomics' based on keyword presence.
    """
    text = (headline + " " + content).lower()
    
    geo_count = sum(1 for kw in GEOPOLITICS_KEYWORDS if kw in text)
    macro_count = sum(1 for kw in MACROECONOMICS_KEYWORDS if kw in text)
    
    if geo_count > macro_count:
        return "geopolitics"
    elif macro_count > geo_count:
        return "macroeconomics"
    elif geo_count > 0:
        return "geopolitics"  # Default to geopolitics if war-related
    elif macro_count > 0:
        return "macroeconomics"
    else:
        return "uncertain"

def generate_memory_filename(topic: str, headline_slug: str) -> str:
    """
    Generate memory file path following naming convention.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    prefix = "geopolitics" if topic == "geopolitics" else "macro"
    slug = headline_slug.lower().replace(" ", "-").replace(",", "")[:50]
    return f"memory/{prefix}-{date_str}-cnbc-{slug}.md"

def main():
    """
    Main entry point. Parses arguments and orchestrates fetch + classify workflow.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Poly-Tradebot CNBC fetcher")
    parser.add_argument("--url", default=DEFAULT_CNBC_URL, help="CNBC URL to fetch")
    parser.add_argument("--count", type=int, default=3, help="Minimum articles to fetch")
    args = parser.parse_args()
    
    print(f"Fetching from: {args.url}")
    print(f"Target article count: {args.count}")
    print(f"Geopolitics keywords: {', '.join(GEOPOLITICS_KEYWORDS[:5])}...")
    print(f"Macroeconomics keywords: {', '.join(MACROECONOMICS_KEYWORDS[:5])}...")
    print("\nWorkflow:")
    print("1. web_fetch <url> → extract article content")
    print("2. classify_article(headline, content) → geopolitics | macroeconomics")
    print("3. Invoke skill: geopolitics-expert OR the_fed_agent")
    print("4. Save output to memory/ following 5-section format")
    print("\nReady for OpenClaw tool orchestration.")

if __name__ == "__main__":
    main()
