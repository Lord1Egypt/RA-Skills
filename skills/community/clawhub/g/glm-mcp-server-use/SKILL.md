---
name: glm-mcp-server-use
description: GLM MCP Server Use for OpenClaw. Configure and use the 4 official Z.AI / GLM MCP servers (vision, web search, web reader, zread) with environment-variable API-key auth. Use for endpoint wiring, schema inspection, smoke tests, and troubleshooting MCP calls.
---

# GLM MCP Server Use

## Overview

This skill provides a practical workflow to install, validate, and use the 4 official GLM MCP servers in OpenClaw:

1. Vision MCP (local stdio via `@z_ai/mcp-server`)
2. Web Search MCP (remote HTTP)
3. Web Reader MCP (remote HTTP)
4. Zread MCP (remote HTTP)

It also includes scripts to read API key from environment variables, generate `mcporter` config, and run a smoke test.

## Quick Start

From this skill directory:

```bash
export Z_AI_API_KEY="your_zai_api_key"
python3 scripts/setup_glm_mcp_servers.py --config ./tmp/mcporter-glm.json
python3 scripts/smoke_test_glm_mcp.py --config ./tmp/mcporter-glm.json
```

Smoke test report will be written to `./tmp/glm-mcp-smoke-report.json`.

## API Key Resolution

`setup_glm_mcp_servers.py` resolves API key from environment variables in this order:

1. `Z_AI_API_KEY`
2. `ZAI_API_KEY`
3. `GLM_API_KEY`
4. `ZHIPU_API_KEY`
You can check key availability without exposing full token:

```bash
python3 scripts/get_zai_api_key.py --masked
```

## Installed MCP Entries

The setup script writes these mcporter servers:

- `web-search-prime` → `https://api.z.ai/api/mcp/web_search_prime/mcp`
- `web-reader` → `https://api.z.ai/api/mcp/web_reader/mcp`
- `zread` → `https://api.z.ai/api/mcp/zread/mcp`
- `zai-vision` → stdio `npx -y @z_ai/mcp-server` (with `Z_AI_API_KEY`, `Z_AI_MODE=ZAI`)

## Validation Workflow

### 1) Inspect real schemas first

```bash
mcporter --config ./tmp/mcporter-glm.json list web-reader --schema --json
mcporter --config ./tmp/mcporter-glm.json list web-search-prime --schema --json
mcporter --config ./tmp/mcporter-glm.json list zread --schema --json
mcporter --config ./tmp/mcporter-glm.json list zai-vision --schema --json
```

### 2) Minimal call examples

```bash
mcporter --config ./tmp/mcporter-glm.json call web-search-prime.web_search_prime search_query="GLM-5.1 release notes"
mcporter --config ./tmp/mcporter-glm.json call web-reader.webReader url="https://example.com"
mcporter --config ./tmp/mcporter-glm.json call zread.get_repo_structure repo_name="microsoft/vscode"
mcporter --config ./tmp/mcporter-glm.json call zai-vision.analyze_image image_source="/path/to/image.png" prompt="Describe key elements"
```

## Important Runtime Notes

- Actual tool names can differ from docs examples. Always trust `--schema` output from live server.
- Search tool currently exposes `web_search_prime` and requires `search_query`.
- Zread calls require `repo_name` (not `repo`).
- Web Reader may return anti-bot or verification content for protected pages (for example some WeChat links).

## Troubleshooting

- `Tool not found`: check exact tool name from `mcporter ... --schema --json`.
- `parameter error`: verify argument names match schema exactly.
- Empty/strange reader content: target page may block scraping or require interactive verification.
- Vision local server issues: verify Node.js >= 22 and rerun with latest `@z_ai/mcp-server`.

## Resources

- Server matrix and endpoint notes: `references/official-endpoints.md`
- Tested behavior record: `references/test-report.md`
- Scripts: `scripts/`
