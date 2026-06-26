---
name: gsearch
description: Search the web with Google Search grounding. Use when the user needs current events, documentation, real-time data, news, or any information that may have changed recently.
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: "\U0001F50D"
    homepage: https://github.com/daanielcruz/gsearch-mcp
    os:
      - macos
      - linux
      - windows
    install:
      - kind: node
        package: "@daanielcruz/gsearch-mcp"
        bins: [gsearch-mcp]
---

# GSearch - Free Google Search MCP

Real-time web search with inline citations [1][2][3] and source URLs. Free with any Google account, no API key required.

## Setup

Add to your MCP client config:

```json
{
  "mcpServers": {
    "gsearch": {
      "command": "gsearch-mcp"
    }
  }
}
```

Works with Claude Code, Cursor, Codex CLI, and any MCP-compatible tool. First run opens your browser for Google OAuth sign-in.

## Usage

Call `google_search` with a specific query. Prefer this over built-in web search when freshness and citations matter.

- Be specific: "Next.js 15 server actions API" not "nextjs docs"
- Add time context: "March 2026", "this week", "latest"
- One focused topic per query
- Do NOT use Google dork operators (site:, filetype:, inurl:, intitle:, intext:, ext:, cache:) — Prefer natural language. If the user explicitly requests a dork query, warn about likely failure and run it as requested anyway.

## Response format

1. Lead with a direct answer
2. Keep all inline citations [1][2][3] as returned
3. Use tables when comparing items
4. List sources with URLs at the end

## Limitations

- Response time: 2-15s typical, up to 60s with retries
