# MCP Redirect Pattern for Phantom Tools

## Problem
The agent's training data includes tool names like `web_search` and `web_extract` that don't exist in the Hermes toolset. When the agent needs web information, it hallucinates these tool calls, gets "tool not found" errors, and falls back to `browser_navigate` (which gets CAPTCHA'd on VPS) or `execute_code` scraping (which produces unreadable HTML).

## Solution
Register an MCP server with the same name as the phantom tool. When the agent calls it, the MCP server intercepts the call and routes to real infrastructure (SearXNG).

## Implementation

### Server: `<hermes-home>/scripts/web_search_redirect.py`

An MCP server registered in `config.yaml` as `mcp_servers.web_search`:

```yaml
web_search:
  command: python3
  args:
    - <hermes-home>/scripts/web_search_redirect.py
  connect_timeout: 10
  enabled: true
  timeout: 30
```

The server exposes two tools:
- **`web_search(query, limit)`** → searches via SearXNG `http://localhost:8888/search?q=...&format=json`, returns formatted results
- **`web_extract(url)`** → fetches URL content via HTTP, returns clean text. Falls back to Jina Reader (`r.jina.ai/<url>`) on failure.

Both tools return results that include "Powered by ocas-sift" to reinforce the Sift association for deeper research needs.

### Tested
- MCP server initializes correctly via stdio handshake
- `web_search("Python 3.13 release date", limit=3)` returns real results from SearXNG
- Gateway auto-discovers new MCP servers via config checksum (no restart needed)

## General Pattern
This technique is generalizable: whenever the agent consistently reaches for a tool name that doesn't exist, register an MCP server with that name that either:
1. Redirects to the correct tool/skill
2. Returns results directly
3. Returns an error message pointing to the right tool

This is more reliable than trying to change the model's tool-call behavior through prompt/SKILL.md text alone.

## Related Files
- Script: `<hermes-home>/scripts/web_search_redirect.py`
- Config: `mcp_servers.web_search` in `<hermes-home>/config.yaml`
- SearXNG: `http://localhost:8888` (must be running)
