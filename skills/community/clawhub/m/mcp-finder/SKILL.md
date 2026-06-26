---
name: mcp-finder
description: Find the right MCP server for your task. 6,700+ MCP servers indexed and ranked by community trust. No API key. For MCP + OpenClaw combined, see meyhem-capabilities.
version: 0.2.3
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# MCP Finder

Find the right MCP server for any task. 6,700+ servers indexed from the MCP ecosystem, ranked by community trust (GitHub stars) and relevance. Describe what you need in plain language, get the best server for the job.

No API key. No signup. No rate limits.

## Why MCP Finder?

- **6,700+ servers indexed**: crawled from awesome-mcp-servers and the Official MCP Registry, enriched with GitHub metadata
- **Natural language search**: describe your task, get relevant results
- **Ranked by trust**: GitHub stars + text relevance combined
- **Zero dependencies**: stdlib Python only

## Quick Start

```bash
python3 finder.py "I need to query a Postgres database"
python3 finder.py "browser automation" -n 3
python3 finder.py "kubernetes monitoring"
python3 finder.py "manage emails"
```

## REST API

```bash
curl -X POST https://api.rhdxm.com/find   -H 'Content-Type: application/json'   -d '{"query": "kubernetes monitoring", "max_results": 5}'
```

Full API docs: https://api.rhdxm.com/docs

## MCP

Connect via streamable HTTP at `https://api.rhdxm.com/mcp/` with tool: `find_server`.

## Data Transparency

This skill sends your search query to `api.rhdxm.com`. The skill does not access local files, environment variables, or credentials on its own, but anything you include in the query will be transmitted. Avoid sending sensitive or proprietary content.

Source code: https://github.com/c5huracan/meyhem