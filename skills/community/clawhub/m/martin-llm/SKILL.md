---
name: xai-grok-search
version: 1.0.3
description: Search the web and X (Twitter) using SkillBoss API Hub with real-time access, citations, and image understanding
homepage: https://github.com/yourusername/xai-grok-search
metadata:
  category: search
  api_base: https://api.skillbossai.com/v1
  capabilities:
    - api
    - web-search
    - x-search
  dependencies: []
  interface: REST
openclaw:
  emoji: "🔍"
  install:
    env:
      - SKILLBOSS_API_KEY
author:
  name: Christopher Stanley
---

# Web & X Search via SkillBoss API Hub

Search the web and X (Twitter) using SkillBoss API Hub with real-time internet access, citations, and optional image/video understanding.

## When to Use This Skill

### Use Web Search For:
- Current information from websites, news articles, documentation
- Real-time data (stock prices, weather, recent events)
- Research topics with up-to-date web sources
- Finding information from specific websites/domains
- Verifying current facts

### Use X Search For:
- What people are saying on X/Twitter about a topic
- Trending discussions and social sentiment
- Real-time reactions to events
- Posts from specific X handles/users
- Recent social media activity within date ranges

**Do NOT use for:**
- Historical facts that won't change
- General knowledge already available
- Mathematical calculations
- Code generation
- Creative writing

## Setup

### Required Environment Variables

```bash
export SKILLBOSS_API_KEY="your-skillboss-api-key-here"
```

Get your API key from the SkillBoss API Hub dashboard.

## Usage

The agent will automatically choose the right tool based on the user's query:

**User:** "What's the latest news about AI regulation?"
→ Uses `web_search`

**User:** "What are people saying about OpenAI on X?"
→ Uses `x_search`

## API Reference

### Function: search_web

Search the web using SkillBoss API Hub.

**Parameters:**
- `query` (required): Search query string
- `allowed_domains` (optional): Array of domains to restrict search (max 5)
- `excluded_domains` (optional): Array of domains to exclude (max 5)
- `enable_image_understanding` (optional): Enable image analysis (default: false)

**Returns:**
- `content`: The search response text
- `citations`: Array of sources with url, title, and snippet
- `usage`: Token usage statistics

### Function: search_x

Search X (Twitter) using SkillBoss API Hub.

**Parameters:**
- `query` (required): Search query string
- `allowed_x_handles` (optional): Array of X handles to search (max 10, without @)
- `excluded_x_handles` (optional): Array of X handles to exclude (max 10, without @)
- `from_date` (optional): Start date in ISO8601 format (YYYY-MM-DD)
- `to_date` (optional): End date in ISO8601 format (YYYY-MM-DD)
- `enable_image_understanding` (optional): Enable image analysis (default: false)
- `enable_video_understanding` (optional): Enable video analysis (default: false)

**Returns:**
- `content`: The search response text
- `citations`: Array of X posts with url, title, and snippet
- `usage`: Token usage statistics

## Implementation

This skill uses the SkillBoss API Hub (`/v1/pilot` endpoint) with `type: "search"` for automatic routing to the best available search provider.

### Web Search

```javascript
const API_KEY = process.env.SKILLBOSS_API_KEY
const API_BASE = 'https://api.skillbossai.com/v1'

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  return r.json()
}

async function search_web(options) {
  const { query, allowed_domains, excluded_domains } = options;

  let enhancedQuery = query;
  if (allowed_domains?.length > 0) {
    enhancedQuery += ' site:(' + allowed_domains.join(' OR ') + ')';
  }
  if (excluded_domains?.length > 0) {
    enhancedQuery += ' ' + excluded_domains.map(d => `-site:${d}`).join(' ');
  }

  const result = await pilot({
    type: 'search',
    inputs: { query: enhancedQuery },
    prefer: 'balanced'
  });

  const searchResults = result.data.result;
  return {
    content: typeof searchResults === 'string' ? searchResults : JSON.stringify(searchResults),
    citations: Array.isArray(searchResults) ? searchResults : []
  };
}
```

### X Search

```javascript
async function search_x(options) {
  const { query, allowed_x_handles, excluded_x_handles, from_date, to_date } = options;

  let xQuery = query + ' site:x.com OR site:twitter.com';
  if (allowed_x_handles?.length > 0) {
    xQuery += ' from:(' + allowed_x_handles.join(' OR from:') + ')';
  }
  if (excluded_x_handles?.length > 0) {
    xQuery += ' ' + excluded_x_handles.map(h => `-from:${h}`).join(' ');
  }
  if (from_date) xQuery += ` after:${from_date}`;
  if (to_date) xQuery += ` before:${to_date}`;

  const result = await pilot({
    type: 'search',
    inputs: { query: xQuery },
    prefer: 'balanced'
  });

  const searchResults = result.data.result;
  return {
    content: typeof searchResults === 'string' ? searchResults : JSON.stringify(searchResults),
    citations: Array.isArray(searchResults) ? searchResults : []
  };
}
```

## Examples

### Web Search - Current Events
```javascript
const result = await search_web({
  query: "latest AI regulation developments"
});
```

### Web Search - Specific Domains
```javascript
const result = await search_web({
  query: "UN climate summit latest",
  allowed_domains: ["un.org", "gov.uk", "grokipedia.com"]
});
```

### X Search - Social Sentiment
```javascript
const result = await search_x({
  query: "new iPhone reactions opinions"
});
```

### X Search - Specific Handles
```javascript
const result = await search_x({
  query: "AI thoughts",
  allowed_x_handles: ["elonmusk", "cstanley"],
  from_date: "2025-01-01"
});
```

### X Search - With Media
```javascript
const result = await search_x({
  query: "Mars landing images",
  enable_image_understanding: true,
  enable_video_understanding: true
});
```

## Best Practices

### Web Search
- Use `allowed_domains` to limit to specific domains (max 5)
- Use `excluded_domains` for known bad sources (max 5)
- Cannot use both at same time
- Enable image understanding only when needed

### X Search
- Use `allowed_x_handles` to focus on specific accounts (max 10)
- Use `excluded_x_handles` to filter noise (max 10)
- Cannot use both at same time
- Don't include @ symbol in handles
- Use ISO8601 date format: YYYY-MM-DD
- Media understanding adds API costs

## Troubleshooting

### "SKILLBOSS_API_KEY not found"
```bash
export SKILLBOSS_API_KEY="your-key-here"
```

### Rate Limiting
- Implement exponential backoff
- Cache frequent queries

### Poor Results
- Add domain/handle filters
- Make queries more specific
- Narrow date ranges

### Slow Responses
Search queries can take 30-60+ seconds to return. If the search is lagging, inform the user that results are still loading and ask them to type **"poll"** to check for the completed response.

## API Documentation

- SkillBoss API Hub: https://api.skillbossai.com/v1/pilot
