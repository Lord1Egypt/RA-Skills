---
name: pipeworx-bluesky
description: Read Bluesky profiles, posts, feeds, followers, and threads via the AT Protocol — 8 tools, mostly public endpoints
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🦋"
    homepage: https://pipeworx.io/packs/bluesky
---

# Bluesky

Tap into the Bluesky social network through the AT Protocol. Most tools work without authentication against the public API — you can read profiles, browse feeds, list followers, and view threads. Post search requires BYO credentials.

## All 8 tools

| Tool | Auth | Purpose |
|------|------|---------|
| `get_profile` | Public | User profile by handle (e.g., `jay.bsky.team`) |
| `get_posts` | Public | Recent posts from a user's feed |
| `search_posts` | Auth required | Search posts by keyword |
| `get_feed` | Public | Browse a feed generator (default: What's Hot) |
| `get_followers` | Public | List a user's followers |
| `get_follows` | Public | List accounts a user follows |
| `get_thread` | Public | Full thread from a post's AT URI |
| `resolve_handle` | Public | Resolve a handle to its DID |

## When to use

- Monitoring mentions of a brand or project on Bluesky
- Analyzing follower/following graphs for social network research
- Pulling recent posts from a specific user to summarize or quote
- Building a Bluesky dashboard that aggregates multiple feeds

## Example: reading someone's recent posts

```bash
curl -s -X POST https://gateway.pipeworx.io/bluesky/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_posts","arguments":{"handle":"jay.bsky.team","limit":5}}}'
```

Each post includes the text, timestamp, like count, repost count, and reply count.

## Authentication note

`search_posts` requires Bluesky credentials. Pass them as query parameters on the gateway URL:

```
https://gateway.pipeworx.io/bluesky/mcp?bsky_handle=you.bsky.social&bsky_app_password=xxxx-xxxx-xxxx
```

All other tools work anonymously.

## MCP client config

```json
{
  "mcpServers": {
    "pipeworx-bluesky": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/bluesky/mcp"]
    }
  }
}
```
