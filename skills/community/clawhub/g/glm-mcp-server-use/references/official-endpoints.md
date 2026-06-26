# GLM Official MCP Servers - Endpoint Matrix

## OpenClaw Auth Convention

- Use environment variable auth directly (do not depend on Claude config files).
- Recommended:

```bash
export Z_AI_API_KEY="your_zai_api_key"
```

## 1) Vision MCP Server

- Doc: https://docs.z.ai/devpack/mcp/vision-mcp-server
- Type: Local stdio MCP server (`npx -y @z_ai/mcp-server`)
- Core value:
  - Image understanding (OCR, UI analysis, chart/diagram interpretation)
  - Video understanding (`analyze_video`)
  - Useful for debugging screenshots, UI reverse-engineering, visual QA
- Practical usefulness: **High** for coding workflows with screenshots/UI/video

## 2) Web Search MCP Server

- Doc: https://docs.z.ai/devpack/mcp/search-mcp-server
- Endpoint: `https://api.z.ai/api/mcp/web_search_prime/mcp`
- Type: Remote HTTP MCP server
- Core value:
  - Real-time web search for latest info
  - Can enrich coding agent with external references
- Practical usefulness: **High** for research, dependency comparison, latest release checks

## 3) Web Reader MCP Server

- Doc: https://docs.z.ai/devpack/mcp/reader-mcp-server
- Endpoint: `https://api.z.ai/api/mcp/web_reader/mcp`
- Type: Remote HTTP MCP server
- Core value:
  - Fetch and convert webpage into model-friendly text/markdown
  - Returns title/body/metadata/links
- Practical usefulness: **Medium-High**, but limited by anti-bot pages and paywalls

## 4) Zread MCP Server

- Doc: https://docs.z.ai/devpack/mcp/zread-mcp-server
- Endpoint: `https://api.z.ai/api/mcp/zread/mcp`
- Type: Remote HTTP MCP server
- Core value:
  - Open-source repo knowledge retrieval
  - Repo structure reading and file content access
- Practical usefulness: **High** for understanding unfamiliar repos quickly

## Quota Notes (from official docs)

- Lite: total 100 calls (search + reader; zread also included on zread page)
- Pro: total 1,000 calls
- Max: total 4,000 calls
- Vision additionally shares the 5-hour package prompt resource pool (per docs wording)

## Runtime Mapping Gotchas

Live schema inspection found naming differences vs doc prose examples:

- Search tool runtime name: `web_search_prime` (arg: `search_query`)
- Reader tool runtime name: `webReader`
- Zread args use `repo_name`
- Vision runtime tools include `analyze_image` / `analyze_video` (not `image_analysis` naming)
