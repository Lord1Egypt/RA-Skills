---
name: web-summarizer
version: 1.0.0
description: Fetch and summarize web pages for AI agents. Extract key information from URLs and return structured markdown summaries. No API key required.
---

# Web Content Summarizer

Fetch and summarize web pages for AI agents. Extract key information from URLs and return structured summaries.

## Usage

```bash
# Summarize a URL
bash scripts/summarize.sh https://example.com

# Summarize with specific focus
bash scripts/summarize.sh https://example.com "key findings"

# List output format
bash scripts/summarize.sh --help
```

## Features

- Fetches web page content
- Extracts title, main content, key points
- Returns structured markdown summary
- Handles errors gracefully
- Respects robots.txt

## How It Works

Uses `web_fetch` tool or curl to get page content, then extracts key information using text processing.

## Use Cases

- Research: quickly get summary of article before deep dive
- Agent memory: store summarized facts instead of full pages  
- Fact checking: verify claims by checking source content
