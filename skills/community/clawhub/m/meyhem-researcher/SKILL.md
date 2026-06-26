---
name: meyhem-researcher
description: Multi-query research tool with LLM-ranked results and freshness control. Breaks a topic into focused queries, previews top results. No API key.
version: 0.2.5
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Meyhem Deep Researcher

Multi-query research tool. Breaks a topic into focused queries, searches via api.rhdxm.com with LLM-ranked results, and previews top results.

No API key. No signup. No rate limits.

## Why Meyhem Researcher?

- **LLM-ranked results**: every result scored for relevance by an LLM prior
- **Freshness control**: request real-time, hourly, daily, or weekly freshness
- **Multi-query workflow**: break a topic into multiple queries, search, preview top results

## Quick Start

```bash
python3 researcher.py "transformer attention mechanism"
python3 researcher.py "kubernetes networking" -n 3 -q 5
python3 researcher.py "AI regulation 2026" --freshness realtime
python3 researcher.py "climate policy updates" --freshness hour --agent my-researcher
```

## Quick Start (REST)

Full API docs: https://api.rhdxm.com/docs

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "agent_id": "my-researcher", "max_results": 10, "freshness": "hour"}'
```

Freshness options: `realtime` (never cached), `hour`, `day`, `week`, or omit for default (1hr cache).

## MCP

You can also connect via MCP at `https://api.rhdxm.com/mcp/` for richer integration.

## Data Transparency

This skill sends your search query, an agent identifier, and any selected URLs to `api.rhdxm.com`. The skill does not access local files, environment variables, or credentials on its own, but anything you include in the query or agent_id will be transmitted. Avoid sending sensitive or proprietary content.

Source code: https://github.com/c5huracan/meyhem
