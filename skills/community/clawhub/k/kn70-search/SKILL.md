---
name: search
description: Search the web using multiple engines (Tavily, multi-search-engine, or SearXNG)
---

Provides tools for web search using Tavily (AI-optimized), multi-search-engine (17 engines without API key), or SearXNG (self-hosted).

**Usage**:
```typescript
// Use Tavily (recommended)
search_web({ query: "AI news", engine: "tavily", max_results: 10 })

// Use multi-search-engine (no API key needed)
search_web({ query: "AI news", engine: "multi", max_results: 10 })

// Use SearXNG (Windows Docker Desktop required)
search_web({ query: "AI news", engine: "searxng", max_results: 10 })
```

**Engine Comparison**:
| Engine | Speed | Quality | Cost | Notes |
|--------|-------|---------|------|-------|
| tavily | ⚡ Fast | ⭐⭐⭐⭐⭐ | Free (dev) | AI-optimized, includes snippets |
| multi | ⚡ Fast | ⭐⭐⭐⭐ | Free | 17 engines (Baidu, Bing, Google, etc.) |
| searxng | 🐌 Medium | ⭐⭐⭐⭐⭐ | Free | Self-hosted, requires Docker Desktop |
