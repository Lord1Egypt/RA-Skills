#!/usr/bin/env python3
"""Oxylabs Browser Agent: navigate and interact with websites like a human."""
import sys, os
from oxylabs_ai_studio.apps.browser_agent import BrowserAgent

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
prompt = sys.argv[2] if len(sys.argv) > 2 else "Extract main content"
api_key = os.getenv("OXYLABS_API_KEY", "")
if not api_key:
    print("ERROR: OXYLABS_API_KEY environment variable not set.")
    sys.exit(1)

agent = BrowserAgent(api_key=api_key)
result = agent.run(url=url, user_prompt=prompt, output_format="markdown")
print(result.data)
