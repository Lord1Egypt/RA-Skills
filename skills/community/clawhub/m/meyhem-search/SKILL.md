---
name: meyhem-search
description: Web search with LLM-ranked results and freshness control. Queries api.rhdxm.com across multiple engines. No API key.
version: 0.2.5
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Meyhem Search

Web search client for AI agents. Sends queries to api.rhdxm.com, which searches across multiple engines, scores results with an LLM relevance prior, and returns ranked results. Optionally retrieve page content for a selected result.

No API key. No signup. No rate limits.

## Why Meyhem?

- **LLM-ranked results**: every result scored for relevance by an LLM prior
- **Freshness control**: request real-time, hourly, daily, or weekly freshness
- **Simple interface**: send a query, get ranked results from multiple engines
- **Optional content retrieval**: use `--content` to fetch page text for the top result

## Quick Start

```bash
python3 search.py "transformer attention mechanism"
python3 search.py "async python best practices" -n 3
python3 search.py "react server components" --content
python3 search.py "kubernetes debugging" --agent my-agent
python3 search.py "AI news today" --freshness realtime
python3 search.py "rust web frameworks 2026" --freshness week
```

## Quick Start (REST)

Full API docs: https://api.rhdxm.com/docs

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "agent_id": "my-agent", "max_results": 5, "freshness": "hour"}'
```

Freshness options: `realtime` (never cached), `hour`, `day`, `week`, or omit for default (1hr cache).

## MCP

You can also connect via MCP at `https://api.rhdxm.com/mcp/` for richer integration.

## Data Transparency

This skill sends your search query, an agent identifier, and any selected URLs to `api.rhdxm.com`. The skill does not access local files, environment variables, or credentials on its own, but anything you include in the query or agent_id will be transmitted. Avoid sending sensitive or proprietary content.

Source code: https://github.com/c5huracan/meyhem
