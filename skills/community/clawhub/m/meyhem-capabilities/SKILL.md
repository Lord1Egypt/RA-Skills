---
name: meyhem-capabilities
description: Find the best tool for your task across 22,000+ MCP servers and OpenClaw skills. Ranked by community trust. No API key.
version: 0.1.4
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Meyhem Capabilities

Find the best tool for any task across MCP servers and OpenClaw skills. 22,000+ capabilities indexed, ranked by community trust (GitHub stars) and relevance. Describe what you need in plain language, get the best tool for the job.

No API key. No signup. No rate limits.

## Why Meyhem Capabilities?

- **22,000+ capabilities indexed**: 15,000+ OpenClaw skills + 6,700+ MCP servers
- **Natural language search**: describe your task, get relevant results
- **Ranked by trust**: GitHub stars + text relevance combined
- **Filter by ecosystem**: search all, or just MCP or OpenClaw
- **Zero dependencies**: stdlib Python only

## Quick Start

```bash
python3 capabilities.py "I need to query a Postgres database"
python3 capabilities.py "browser automation" -n 3
python3 capabilities.py "kubernetes monitoring" --ecosystem mcp
python3 capabilities.py "manage emails" --ecosystem openclaw
```

## REST API

```bash
curl -X POST https://api.rhdxm.com/find-capability \
  -H 'Content-Type: application/json' \
  -d '{"task": "kubernetes monitoring", "max_results": 5}'
```

Filter by ecosystem:

```bash
curl -X POST https://api.rhdxm.com/find-capability?ecosystem=mcp \
  -H 'Content-Type: application/json' \
  -d '{"task": "kubernetes monitoring", "max_results": 5}'
```

Full API docs: https://api.rhdxm.com/docs

## MCP

Connect via streamable HTTP at `https://api.rhdxm.com/mcp/` with tool: `find_capability`.

## Data Transparency

This skill sends your search query to `api.rhdxm.com`. The skill does not access local files, environment variables, or credentials on its own, but anything you include in the query will be transmitted. Avoid sending sensitive or proprietary content.

Source code: https://github.com/c5huracan/meyhem