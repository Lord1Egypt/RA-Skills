---
name: minimax-coding-plan-tool
description: Use MiniMax Coding Plan API for real-time web search and image understanding (VLM). Based on yorch233/minimax-coding-plan-tool, patched to use api.minimax.io instead of api.minimax.chat. No external MCP servers needed.
homepage: https://platform.minimaxi.com
metadata: {"openclaw":{"emoji":"🧩","requires":{"bins":["node"],"env":["MINIMAX_API_KEY"]},"primaryEnv":"MINIMAX_API_KEY"}}
---

# MiniMax Coding Plan Tool

> Forked from [yorch233/minimax-coding-plan-tool](https://clawhub.ai/yorch233/minimax-coding-plan-tool)  
> Patch: Changed API host from `api.minimax.chat` to `api.minimax.io` to work with `sk-cp-*` Coding Plan keys.

Uses `api.minimax.io` with **Coding Plan API Key** (format: `sk-cp-*`). No external MCP servers required.

## Features

### `minimax_web_search` — Web Search
```bash
MINIMAX_API_KEY="sk-cp-xxx" node scripts/minimax_coding_plan_tool.js web_search "query"
```

### `minimax_understand_image` — Image Understanding
```bash
MINIMAX_API_KEY="sk-cp-xxx" node scripts/minimax_coding_plan_tool.js understand_image ./photo.png "Describe this image"
```

Supports local files (auto base64) and HTTP/HTTPS URLs.

## Configuration

```bash
openclaw config set skills.entries.minimax-coding-plan-tool.env.MINIMAX_API_KEY "sk-cp-xxx"
```

Or in `openclaw.json`:
```json
"skills": {
  "entries": {
    "minimax-coding-plan-tool": {
      "env": { "MINIMAX_API_KEY": "sk-cp-xxx" }
    }
  }
}
```
