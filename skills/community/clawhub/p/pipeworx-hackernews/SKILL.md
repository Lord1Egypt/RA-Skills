---
name: pipeworx-hackernews
description: Search and browse Hacker News — top stories, keyword search via Algolia, and individual item lookup
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📰"
    homepage: https://pipeworx.io/packs/hackernews
---

# Hacker News

Stay on top of tech news. Search HN stories via the Algolia-powered search API, pull the current top stories from the Firebase API, or fetch any individual story or comment by ID.

## Tools

- **`search_hn`** — Full-text search across HN stories. Filter by date range and control result count.
- **`get_top_stories`** — Current top stories on Hacker News with title, URL, score, and comment count.
- **`get_item`** — Fetch a specific story or comment by its numeric HN ID.

## Ideal for

- "What's trending on Hacker News today?"
- Searching for discussions about a specific technology or company
- Pulling top stories for a daily digest or newsletter
- Retrieving a specific story someone linked to by ID

## Example: search for discussions about Rust

```bash
curl -s -X POST https://gateway.pipeworx.io/hackernews/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_hn","arguments":{"query":"Rust programming language","sort":"points","limit":5}}}'
```

## Connect

```json
{
  "mcpServers": {
    "pipeworx-hackernews": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/hackernews/mcp"]
    }
  }
}
```
