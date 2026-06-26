#!/usr/bin/env python3
"""Oxylabs AI-Map: discover and list all URLs on a domain."""
import sys, os
from oxylabs_ai_studio.apps.ai_map import AiMap

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
prompt = sys.argv[2] if len(sys.argv) > 2 else "Find all pages"
api_key = os.getenv("OXYLABS_API_KEY", "")
if not api_key:
    print("ERROR: OXYLABS_API_KEY environment variable not set.")
    sys.exit(1)

ai_map = AiMap(api_key=api_key)
result = ai_map.map(url=url, user_prompt=prompt)
print(result.data)
