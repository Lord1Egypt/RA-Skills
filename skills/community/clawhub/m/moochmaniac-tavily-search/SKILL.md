---
name: tavily-search
description: Real-time web search using Tavily API optimized for AI agents. Use when you need current information, recent news, factual research, competitive analysis, or any data not in your training cutoff. Searches return structured results with URLs, content snippets, relevance scores, and optional AI-generated answers.
---

# Tavily Search

Web search powered by Tavily API, optimized for AI agent consumption with structured, relevant results.

## When to Use

- User asks for current/recent information beyond training cutoff
- Research tasks requiring multiple sources
- Fact-checking or verification
- Competitor analysis, market research
- News and updates on specific topics
- Finding documentation or resources

## Quick Start

Basic search (5 results):
```bash
python3 scripts/search.py "your query here"
```

With options:
```bash
# Fewer results
python3 scripts/search.py "AI agents" --max-results 3

# AI-generated answer
python3 scripts/search.py "what is OpenClaw" --answer

# Advanced search (deeper crawling)
python3 scripts/search.py "casino bonuses" --depth advanced

# Include images
python3 scripts/search.py "WordPress themes" --images

# Raw JSON output
python3 scripts/search.py "n8n automation" --json
```

## Parameters

- **query** (required): Search query string
- `--max-results N`: Number of results (1-10, default 5)
- `--depth`: Search depth
  - `basic` (default): Fast, good for most queries
  - `advanced`: Deeper crawling, more comprehensive
- `--answer`: Include AI-generated answer summary
- `--images`: Include relevant image URLs
- `--json`: Output raw JSON instead of formatted text

## Output Structure

Formatted output includes:
- Query and response time
- AI-generated answer (if requested)
- Search results with:
  - Title and URL
  - Relevance score (0-1)
  - Content snippet (truncated to 300 chars)
- Images (if requested)

JSON output provides full Tavily API response for programmatic use.

## API Key Setup

The script looks for the Tavily API key in:
1. `workspace/secrets/tavily_api_key` (OpenClaw workspace)
2. `secrets/tavily_api_key` (relative to current directory)
3. `TAVILY_API_KEY` environment variable

Current key is stored at: `workspace/secrets/tavily_api_key`

## Examples

**Research task:**
```bash
python3 scripts/search.py "WordPress plugin security best practices 2026" --max-results 5 --answer
```

**Quick fact check:**
```bash
python3 scripts/search.py "OpenClaw GitHub repository" --max-results 3
```

**Competitive analysis:**
```bash
python3 scripts/search.py "top casino affiliate sites" --depth advanced --max-results 10
```

**News monitoring:**
```bash
python3 scripts/search.py "AI agent frameworks January 2026" --answer
```

## Tips

- Use specific queries for better results
- `--answer` is useful for summarization tasks
- `--depth advanced` for comprehensive research (uses more API credits)
- Relevance scores help identify best sources
- `--json` output is useful for parsing and processing results programmatically
