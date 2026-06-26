---
name: pipeworx-github
description: Search GitHub repos, view issues, and look up user profiles via the public REST API — no token required
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🐙"
    homepage: https://pipeworx.io/packs/github
---

# GitHub

Search repositories by keyword, get detailed repo metadata (stars, forks, language, license), browse open issues, and look up user profiles. Uses the public GitHub REST API — no authentication token needed for public data.

## Tools

- **`search_repos`** — Search repositories by keyword, optionally sorted by stars, forks, or updated date
- **`get_repo`** — Full details for a specific repo by owner/name (e.g., "facebook/react")
- **`list_repo_issues`** — Open, closed, or all issues for a repository
- **`get_user`** — Public profile for a GitHub username (e.g., "torvalds")

## Scenarios

- "Find the most starred Go CLI tools on GitHub" — search with `"cli tool language:go"`, sort by stars
- Checking a project's issue count and latest activity
- Looking up a contributor's profile and public repos
- Building a project discovery feature based on topic or language

## Example: search for React-related repos

```bash
curl -s -X POST https://gateway.pipeworx.io/github/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_repos","arguments":{"query":"react hooks","sort":"stars","limit":5}}}'
```

Each result includes: name, full_name, description, stars, forks, language, license, and URL.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-github": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/github/mcp"]
    }
  }
}
```

## Rate limits

Unauthenticated GitHub API requests are limited to 60/hour per IP. For heavier use, consider authenticated access through GitHub's own MCP server.
