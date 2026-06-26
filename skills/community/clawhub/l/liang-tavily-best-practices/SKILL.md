---
name: tavily-best-practices
description: Build production-ready Tavily integrations with best practices baked in. Reference documentation for implementing web search, content extraction, crawling, and research in agentic workflows, RAG systems, or autonomous agents.
homepage: https://tavily.com
metadata: {"openclaw":{"emoji":"📘","requires":{}}}
---

# Tavily Best Practices

Tavily is a search API designed for LLMs, enabling AI applications to access real-time web data.

## Installation

**Python:**
```bash
pip install tavily-python
```

**JavaScript:**
```bash
npm install @tavily/core
```

## Client Initialization

```python
from tavily import TavilyClient

# Option 1: Uses TAVILY_API_KEY env var (recommended)
client = TavilyClient()

# Option 2: Explicit API key
client = TavilyClient(api_key="tvly-YOUR_API_KEY")

# Async client for parallel queries
from tavily import AsyncTavilyClient
async_client = AsyncTavilyClient()
```

## Choosing the Right Method

**For custom agents/workflows:**

| Need | Method |
|------|--------|
| Web search results | `search()` |
| Content from specific URLs | `extract()` |
| Content from entire site | `crawl()` |
| URL discovery from site | `map()` |

**For out-of-the-box research:**

| Need | Method |
|------|--------|
| End-to-end research with AI synthesis | `research()` |

## Quick Reference

### search() - Web Search

```python
response = client.search(
    query="quantum computing breakthroughs",  # Keep under 400 chars
    max_results=10,
    search_depth="advanced",  # highest relevance
    topic="general"  # or "news"
)

for result in response["results"]:
    print(f"{result['title']}: {result['score']}")
```

**Key parameters:**
- `query` - Keep under 400 characters
- `max_results` - 1-20
- `search_depth` - `ultra-fast`, `fast`, `basic`, `advanced`
- `topic` - `general` or `news`
- `include_domains`, `exclude_domains` - Filter sources
- `time_range` - `day`, `week`, `month`, `year`

### extract() - URL Content Extraction

```python
# Two-step pattern (recommended for control)
search_results = client.search(query="Python async best practices")
urls = [r["url"] for r in search_results["results"] if r["score"] > 0.5]
extracted = client.extract(
    urls=urls[:20],
    query="async patterns",  # Reranks chunks by relevance
    chunks_per_source=3  # Prevents context explosion
)
```

**Key parameters:**
- `urls` - Max 20 URLs
- `extract_depth` - `basic` or `advanced`
- `query` - Reranks chunks by relevance
- `chunks_per_source` - 1-5 (prevents context explosion)

### crawl() - Site-Wide Extraction

```python
response = client.crawl(
    url="https://docs.example.com",
    max_depth=2,
    instructions="Find API documentation pages",  # Semantic focus
    chunks_per_source=3,  # Token optimization
    select_paths=["/docs/.*", "/api/.*"]
)
```

**Key parameters:**
- `url` - Root URL to crawl
- `max_depth` - 1-5 (start with 1)
- `max_breadth` - Links per page
- `limit` - Total pages cap
- `instructions` - Natural language guidance
- `chunks_per_source` - 1-5 (for agentic use)
- `select_paths`, `exclude_paths` - Regex patterns

### map() - URL Discovery

```python
response = client.map(
    url="https://docs.example.com",
    max_depth=2,
    instructions="Find all API and guide pages"
)
api_docs = [url for url in response["results"] if "/api/" in url]
```

Use `map()` when you only need URLs, not content (faster than crawl).

### research() - AI-Powered Research

```python
import time

# For comprehensive multi-topic research
result = client.research(
    input="Analyze competitive landscape for X in SMB market",
    model="pro"  # or "mini" for focused queries, "auto" when unsure
)
request_id = result["request_id"]

# Poll until completed
response = client.get_research(request_id)
while response["status"] not in ["completed", "failed"]:
    time.sleep(10)
    response = client.get_research(request_id)

print(response["content"])  # The research report
```

**Key parameters:**
- `input` - Research topic or question
- `model` - `mini` (quick), `pro` (comprehensive), `auto`
- `stream` - Stream results as they arrive
- `output_schema` - Structured JSON output
- `citation_format` - Citation style

## Search Depth Selection

| Depth | Latency | Relevance | Use Case |
|-------|---------|-----------|----------|
| `ultra-fast` | Lowest | Lower | Real-time chat, autocomplete |
| `fast` | Low | Good | Need chunks but latency matters |
| `basic` | Medium | High | General-purpose, balanced |
| `advanced` | Higher | Highest | Precision matters, research |

**Rule of thumb:** Start with `basic`, escalate to `advanced` for complex topics.

## Model Selection for Research

**Rule of thumb:** "what does X do?" → `mini`. "X vs Y vs Z" or "best way to..." → `pro`.

| Model | Use Case | Speed |
|-------|----------|-------|
| `mini` | Single topic, targeted research | ~30s |
| `pro` | Comprehensive multi-angle analysis | ~60-120s |
| `auto` | API chooses based on complexity | Varies |

## Crawl for Context vs Data Collection

**For agentic use (feeding results into context):**
Always use `instructions` + `chunks_per_source`. This returns only relevant chunks instead of full pages, preventing context window explosion.

**For data collection (saving to files):**
Omit `chunks_per_source` to get full page content.

## Common Patterns

### Pattern 1: Search + Extract

```python
# Find relevant URLs first
search_results = client.search(query="React hooks documentation")
high_quality_urls = [r["url"] for r in search_results["results"] if r["score"] > 0.7]

# Extract content from best results
extracted = client.extract(
    urls=high_quality_urls[:10],
    query="useState and useEffect",
    chunks_per_source=3
)
```

### Pattern 2: Map + Crawl

```python
# Discover structure first
map_results = client.map(
    url="https://docs.example.com",
    max_depth=2,
    instructions="Find API documentation pages"
)

# Crawl only relevant sections
api_urls = [url for url in map_results["results"] if "/api/" in url]
crawl_results = client.crawl(
    url="https://docs.example.com/api",
    max_depth=1,
    limit=len(api_urls)
)
```

### Pattern 3: Research with Citations

```python
result = client.research(
    input="Compare LangGraph vs CrewAI for multi-agent systems",
    model="pro"
)

# The response includes citations
print(result["content"])  # AI-synthesized report
print(result["citations"])  # Source references
```

## Performance Tips

- **Keep queries under 400 characters** - Think search query, not prompt
- **Break complex queries into sub-queries** - Better results than one massive query
- **Use `include_domains`** to focus on trusted sources
- **Use `time_range`** for recent information
- **Start conservative with crawl** (`max_depth=1`, `limit=20`)
- **Always set a `limit`** to prevent runaway crawls
- **Use `chunks_per_source` for agentic workflows** - prevents context explosion

## Cost Optimization

- Use `basic` depth as default (cheaper than `advanced`)
- Limit `max_results` to what you'll actually use
- Disable `include_raw_content` unless needed
- Use `chunks_per_source` instead of full content for context
- Cache results locally for repeated queries

## Error Handling

```python
from tavily import TavilyClient
from tavily.errors import TavilyError

client = TavilyClient()

try:
    result = client.search(query="example")
except TavilyError as e:
    print(f"Tavily API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Framework Integrations

Tavily integrates with popular frameworks:

- **LangChain** - `TavilySearch` tool
- **LlamaIndex** - `TavilySearch` tool
- **CrewAI** - Built-in Tavily tools
- **Vercel AI SDK** - Direct API calls

See the official documentation for integration examples.