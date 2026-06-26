#!/usr/bin/env python3
"""Oxylabs AI-Scraper: extract content from a single URL."""
import sys, os
from oxylabs_ai_studio.apps.ai_scraper import AiScraper

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
api_key = os.getenv("OXYLABS_API_KEY", "")
if not api_key:
    print("ERROR: OXYLABS_API_KEY environment variable not set.")
    sys.exit(1)

scraper = AiScraper(api_key=api_key)
result = scraper.scrape(url=url, output_format="markdown")
print(result.data)
