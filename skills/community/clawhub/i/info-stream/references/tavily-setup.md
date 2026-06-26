# Tavily API Setup

## What is Tavily

Tavily is an AI-optimized search API that returns structured results with relevance scores. It's faster than web_fetch for broad discovery and returns results in a consistent format.

## Setup

1. Sign up at https://tavily.com
2. Get API key from dashboard
3. Set environment variable: `TAVILY_API_KEY=tvly-dev-xxxxx`

## Usage

```bash
node scripts/tavily-search.js "query" [max_results] [topic] [search_depth]
```

- `query`: Search query (required)
- `max_results`: Number of results (default: 5)
- `topic`: `general` or `news` (default: general)
- `search_depth`: `basic` or `advanced` (default: basic)

## Output

Returns JSON array with: title, url, content, score, published_date

## Best Practices

- Use `topic: news` for time-sensitive daily collection
- Use `search_depth: basic` for speed (reserve `advanced` for deep research)
- Group 3-5 keyword queries to cover different aspects of your domain
- Typical response time: 1-3 seconds per query

## Integration Pattern

Run multiple queries in sequence, then deduplicate by URL:

```bash
node scripts/tavily-search.js "browser news 2026" 5 news
node scripts/tavily-search.js "AI technology news" 5 news
node scripts/tavily-search.js "Web standards new features" 3 news
```

## Fallback

If Tavily is unavailable, fall back to `web_fetch` on core blogs. Always maintain a list of authoritative blogs as backup.
