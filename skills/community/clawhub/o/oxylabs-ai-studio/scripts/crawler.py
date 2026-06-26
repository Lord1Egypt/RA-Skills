#!/usr/bin/env python3
"""Oxylabs AI-Crawler: crawl an entire domain and extract content."""
import sys, os
from oxylabs_ai_studio.apps.ai_crawler import AiCrawler

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
prompt = sys.argv[2] if len(sys.argv) > 2 else "Extract all content"
api_key = os.getenv("OXYLABS_API_KEY", "")
if not api_key:
    print("ERROR: OXYLABS_API_KEY environment variable not set.")
    sys.exit(1)

crawler = AiCrawler(api_key=api_key)
result = crawler.crawl(url=url, user_prompt=prompt, output_format="markdown")
print(result.data)
