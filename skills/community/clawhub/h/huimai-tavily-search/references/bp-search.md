> ## Documentation Index
> Fetch the complete documentation index at: https://docs.tavily.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Best Practices for Search

> Learn how to optimize your queries, refine search filters, and leverage advanced parameters for better performance.

## Query Optimization

### Keep your query under 400 characters

Keep queries concise—under **400 characters**. Think of it as a query for an agent performing web search, not long-form prompts.

### Break complex queries into sub-queries

For complex or multi-topic queries, send separate focused requests:

```json  theme={null}
// Instead of one massive query, break it down:
{ "query": "Competitors of company ABC." }
{ "query": "Financial performance of company ABC." }
{ "query": "Recent developments of company ABC." }
```

## Search Depth

The `search_depth` parameter controls the tradeoff between latency and relevance:

<Expandable title="Latency vs relevance chart">
  <img src="https://mintcdn.com/tavilyai/-85Rr9EfVqo8fXvO/images/search-depth.png?fit=max&auto=format&n=-85Rr9EfVqo8fXvO&q=85&s=c57f2074dda171a1e3e9f96afbec8f10" alt="Latency vs Relevance by Search Depth" data-og-width="874" width="874" data-og-height="874" height="874" data-path="images/search-depth.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/tavilyai/-85Rr9EfVqo8fXvO/images/search-depth.png?w=280&fit=max&auto=format&n=-85Rr9EfVqo8fXvO&q=85&s=71a5fd07a8656ee310a89130f37d45f1 280w, https://mintcdn.com/tavilyai/-85Rr9EfVqo8fXvO/images/search-depth.png?w=560&fit=max&auto=format&n=-85Rr9EfVqo8fXvO&q=85&s=4022debcc3a7e036173f27e42e1fc938 560w, https://mintcdn.com/tavilyai/-85Rr9EfVqo8fXvO/images/search-depth.png?w=840&fit=max&auto=format&n=-85Rr9EfVqo8fXvO&q=85&s=138868083b0737aaa5b00f3064e7d5a8 840w, https://mintcdn.com/tavilyai/-85Rr9EfVqo8fXvO/images/search-depth.png?w=1100&fit=max&auto=format&n=-85Rr9EfVqo8fXvO&q=85&s=71a45f7709dc6e075026659bd24d1280 1100w, https://mintcdn.com/tavilyai/-85Rr9EfVqo8fXvO/images/search-depth.png?w=1650&fit=max&auto=format&n=-85Rr9EfVqo8fXvO&q=85&s=809950b3644e9382d935fb2fdf43a1a5 1650w, https://mintcdn.com/tavilyai/-85Rr9EfVqo8fXvO/images/search-depth.png?w=2500&fit=max&auto=format&n=-85Rr9EfVqo8fXvO&q=85&s=53662412a87ba84df069cf180d228418 2500w" />

  *This chart is a heuristic and is not to scale.*
</Expandable>

| Depth        | Latency | Relevance | Content Type |
| ------------ | ------- | --------- | ------------ |
| `ultra-fast` | Lowest  | Lower     | Content      |
| `fast`       | Low     | Good      | Chunks       |
| `basic`      | Medium  | High      | Content      |
| `advanced`   | Higher  | Highest   | Chunks       |

### Content types

| Type        | Description                                               |
| ----------- | --------------------------------------------------------- |
| **Content** | NLP-based summary of the page, providing general context  |
| **Chunks**  | Short snippets reranked by relevance to your search query |

Use **chunks** when you need highly targeted information aligned with your query. Use **content** when a general page summary is sufficient.

### Fast + Ultra-Fast

| Depth        | When to use                                                                                                                                                             |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ultra-fast` | When latency is absolutely crucial. Delivers near-instant results, prioritizing speed over relevance. Ideal for real-time applications where response time is critical. |
| `fast`       | When latency is more important than relevance, but you want results in reranked chunks format. Good for applications that need quick, targeted snippets.                |
| `basic`      | A solid balance between relevance and latency. Best for general-purpose searches where you need quality results without the overhead of advanced processing.            |
| `advanced`   | When you need the highest relevance and are willing to trade off latency. Best for queries seeking specific, detailed information.                                      |

### Using `search_depth=advanced`

Best for queries seeking specific information:

```json  theme={null}
{
  "query": "How many countries use Monday.com?",
  "search_depth": "advanced",
  "chunks_per_source": 3,
  "include_raw_content": true
}
```

## Filtering Results

### By date

| Parameter                 | Description                                             |
| ------------------------- | ------------------------------------------------------- |
| `time_range`              | Filter by relative time: `day`, `week`, `month`, `year` |
| `start_date` / `end_date` | Filter by specific date range (format: `YYYY-MM-DD`)    |

```json  theme={null}
{ "query": "latest ML trends", "time_range": "month" }
{ "query": "AI news", "start_date": "2025-01-01", "end_date": "2025-02-01" }
```

### By topic

Use `topic` to filter by content type. Set to `news` for news sources (includes `published_date` metadata):

```json  theme={null}
{ "query": "What happened today in NY?", "topic": "news" }
```

### By domain

| Parameter         | Description                           |
| ----------------- | ------------------------------------- |
| `include_domains` | Limit to specific domains             |
| `exclude_domains` | Filter out specific domains           |
| `country`         | Boost results from a specific country |

```json  theme={null}
// Restrict to LinkedIn profiles
{ "query": "CEO background at Google", "include_domains": ["linkedin.com/in"] }

// Exclude irrelevant domains
{ "query": "US economy trends", "exclude_domains": ["espn.com", "vogue.com"] }

// Boost results from a country
{ "query": "tech startup funding", "country": "united states" }

// Wildcard: limit to .com, exclude specific site
{ "query": "AI news", "include_domains": ["*.com"], "exclude_domains": ["example.com"] }
```

<Note>Keep domain lists short and relevant for best results.</Note>

## Response Content

### `max_results`

Limits results returned (default: `5`). Setting too high may return lower-quality results.

### `include_raw_content`

Returns full extracted page content. For comprehensive extraction, consider a two-step process:

1. Search to retrieve relevant URLs
2. Use [Extract API](/documentation/best-practices/best-practices-extract#2-two-step-process-search-then-extract) to get content

### `auto_parameters`

Tavily automatically configures parameters based on query intent. Your explicit values override automatic ones.

```json  theme={null}
{
  "query": "impact of AI in education policy",
  "auto_parameters": true,
  "search_depth": "basic" // Override to control cost
}
```

<Note>
  `auto_parameters` may set `search_depth` to `advanced` (2 credits). Set it
  manually to control cost.
</Note>

## Exact Match

Use `exact_match` only when searching for a specific name or phrase that must appear verbatim in the source content. Wrap the phrase in quotes within your query:

```json  theme={null}
{
  "query": "\"John Smith\" CEO Acme Corp",
  "exact_match": true
}
```

Because this narrows retrieval, it may return fewer results or empty result fields when no exact matches are found. Best suited for:

* **Due diligence** — finding information on a specific person or entity
* **Data enrichment** — retrieving details about a known company or individual
* **Legal/compliance** — locating exact names or phrases in public records

## Async & Performance

Use async calls for concurrent requests:

```python  theme={null}
import asyncio
from tavily import AsyncTavilyClient

tavily_client = AsyncTavilyClient("tvly-YOUR_API_KEY")

async def fetch_and_gather():
    queries = ["latest AI trends", "future of quantum computing"]
    responses = await asyncio.gather(
        *(tavily_client.search(q) for q in queries),
        return_exceptions=True
    )
    for response in responses:
        if isinstance(response, Exception):
            print(f"Failed: {response}")
        else:
            print(response)

asyncio.run(fetch_and_gather())
```

## Post-Processing

### Using metadata

Leverage response metadata to refine results:

| Field         | Use case                           |
| ------------- | ---------------------------------- |
| `score`       | Filter/rank by relevance score     |
| `title`       | Keyword filtering on headlines     |
| `content`     | Quick relevance check              |
| `raw_content` | Deep analysis and regex extraction |

### Score-based filtering

The `score` indicates relevance between query and content. Higher is better, but the ideal threshold depends on your use case.

```python  theme={null}
# Filter results with score > 0.7
filtered = [r for r in results if r['score'] > 0.7]
```

### Regex extraction

Extract structured data from `raw_content`:

```python  theme={null}
import re

# Extract location
text = "Company: Tavily, Location: New York"
match = re.search(r"Location: (\w+)", text)
location = match.group(1) if match else None  # "New York"

# Extract all emails
text = "Contact: john@example.com, support@tavily.com"
emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
```
