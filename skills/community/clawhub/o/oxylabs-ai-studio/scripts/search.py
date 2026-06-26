#!/usr/bin/env python3
"""Oxylabs AI-Search: search the web with natural language queries."""
import sys, os
from oxylabs_ai_studio.apps.ai_search import AiSearch

query = sys.argv[1] if len(sys.argv) > 1 else "test"
api_key = os.getenv("OXYLABS_API_KEY", "")
if not api_key:
    print("ERROR: OXYLABS_API_KEY environment variable not set.")
    sys.exit(1)

search = AiSearch(api_key=api_key)
result = search.search(query=query)
print(result.data)
