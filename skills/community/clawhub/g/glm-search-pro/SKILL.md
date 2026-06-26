---
name: glm-search-pro
description: >
  Web search via Zhipu GLM — supports both MCP (mcporter) and cURL (REST API) backends.
  Provides multi-engine search (Pro, Sogou, Quark, Std) with intent recognition, time range
  filtering, domain filtering, and configurable result count/detail level.
  Use when the agent needs to search the web, look up current information, find news,
  or retrieve online resources. Works from China without VPN.
  Trigger on: "search the web", "web search", "look up", "find online", "latest news",
  "search for", "google for", "联网搜索", "在线搜索", "查最新", "搜索一下".
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["ZHIPU_API_KEY"], "bins": ["curl", "python3"] },
      },
  }
---

# GLM Search Pro

Web search powered by Zhipu GLM, with dual-backend support: **cURL** (REST API, preferred) and **MCP** (via mcporter).

## Credentials

This skill requires a **Zhipu API key**, provided via the `ZHIPU_API_KEY` environment variable.

### cURL mode (preferred)

No setup required. The key is read from `$ZHIPU_API_KEY` at runtime and sent via HTTP `Authorization: Bearer` header. In cURL mode, no files are written to disk.

### MCP mode (advanced)

If you need MCP mode, `setup.sh` will write a config file to disk:

| File | What it contains | Permissions |
|------|-----------------|-------------|
| `~/.openclaw/config/mcporter/mcporter.json` | MCP server URL with API key as query param | `600` (owner-only) |
| `~/.openclaw/config/mcporter/` directory | Parent directory | `700` (owner-only) |

**Important**: The Zhipu MCP broker endpoint requires the API key as a URL query parameter (`Authorization=<key>`). This is how their SSE endpoint works — the key cannot be passed via HTTP header for MCP connections. Setup writes this to `mcporter.json` with `600` permissions. If this is not acceptable, use cURL mode only (which passes the key via `Authorization` header at runtime and writes nothing to disk).

### What this skill reads

| Source | When | Purpose |
|--------|------|---------|
| `$ZHIPU_API_KEY` env var | Every search (cURL mode), and during setup (MCP mode) | API key |

### Recommendation

For maximum security, use cURL mode and skip `setup.sh`. MCP mode is provided as a convenience but requires persisting the key on disk due to the Zhipu MCP broker's authentication design.

## Quick Start

```bash
# Set your API key
export ZHIPU_API_KEY="your-api-key"

# Search (cURL mode, no setup needed)
bash scripts/glm-search.sh "your query"

# With options
bash scripts/glm-search.sh -q "latest AI news" -c 20 -r oneWeek -e quark
```

## Backends

The script auto-selects the best available backend:

1. **cURL mode** (preferred) — `curl` + `ZHIPU_API_KEY` env var. Key sent via HTTP header. Nothing written to disk.
2. **MCP mode** (advanced) — `mcporter` + config from `setup.sh`. Key stored in config file for MCP broker auth.

Force a specific mode with `--curl` or `--mcp`.

## Search Engines

| Engine | Flag | Best For |
|--------|------|----------|
| Pro | `-e pro` | General purpose, best quality (**default**) |
| Quark | `-e quark` | Advanced scenarios, Chinese content |
| Sogou | `-e sogou` | China domestic content |
| Std | `-e std` | Basic search, Q&A |

## Parameters

| Flag | Long | Default | Description |
|------|------|---------|-------------|
| `-q` | `--query` | — | Search text (required, ≤70 chars recommended) |
| `-c` | `--count` | 10 | Number of results (1-50) |
| `-e` | `--engine` | pro | `pro`, `sogou`, `quark`, `std` |
| `-r` | `--recency` | noLimit | `noLimit`, `oneYear`, `oneMonth`, `oneWeek`, `oneDay` |
| `-s` | `--size` | medium | `medium` (400-600 chars) or `high` (up to 2500) |
| `-i` | `--intent` | off | Enable search intent recognition (cURL only) |
| `-d` | `--domain` | — | Restrict results to specific domain |
| | `--curl` | — | Force cURL backend |
| | `--mcp` | — | Force MCP backend |

## Examples

```bash
# Basic search (cURL mode auto-selected)
glm-search "OpenClaw framework"

# Recent news, more results
glm-search -q "AI news" -c 20 -r oneWeek

# Chinese content via Sogou
glm-search -q "最新科技新闻" -e sogou -r oneDay

# Domain-specific search
glm-search -q "Python async" -d docs.python.org

# Intent recognition (cURL only)
glm-search -i "What is machine learning"
```

## Response Format

```json
{
  "id": "task-id",
  "created": 1704067200,
  "search_result": [
    {
      "title": "Page Title",
      "content": "Page summary...",
      "link": "https://example.com",
      "media": "Source Name",
      "refer": "ref_1",
      "publish_date": "2026-04-27"
    }
  ]
}
```

## Architecture

```
glm-search (script)
├── cURL mode (preferred)
│   └── curl + $ZHIPU_API_KEY → Authorization: Bearer header → Zhipu REST API
└── MCP mode (advanced, requires setup)
    └── mcporter → config from setup.sh → Zhipu MCP Broker SSE endpoint
```

## Setup (MCP mode only)

```bash
export ZHIPU_API_KEY="your-api-key"
bash scripts/setup.sh
```

This is **only needed for MCP mode**. cURL mode works immediately with `ZHIPU_API_KEY` set.

## Configuring the API Key for OpenClaw Gateway

The skill requires `ZHIPU_API_KEY` to be available in the Gateway process environment.
If `openclaw skills check` shows `△ needs setup` for this skill, the key is missing.

### Systemd (Linux, recommended)

If the Gateway runs as a systemd user service:

```bash
# Edit the service override
systemctl --user edit openclaw-gateway

# Add the following in the editor:
[Service]
Environment=ZHIPU_API_KEY=your-api-key-here

# Then reload and restart
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

Or create the file manually:

```bash
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
cat > ~/.config/systemd/user/openclaw-gateway.service.d/override.conf << 'EOF'
[Service]
Environment=ZHIPU_API_KEY=your-api-key-here
EOF
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

### Docker / manual

Set the environment variable before starting the Gateway:

```bash
export ZHIPU_API_KEY="your-api-key-here"
```

Or add it to your `.env` / `docker-compose.yml` as appropriate.

### Verify

After restarting, confirm the skill is ready:

```bash
openclaw skills check
# Should show: ✓ glm-search-pro (no longer "needs setup")
```

## Prerequisites

- **Zhipu API key** — <https://open.bigmodel.cn> (set as `ZHIPU_API_KEY` env var)
- **curl** — pre-installed on most systems
- **python3** — used by setup.sh for JSON config generation
- **mcporter** (optional, for MCP mode) — `npm i -g mcporter` (invoked via `npx`)

## Troubleshooting

See `references/api-notes.md` for detailed API reference and common issues.
