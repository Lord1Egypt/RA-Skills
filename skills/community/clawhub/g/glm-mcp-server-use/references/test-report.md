# Test Report

## Environment

- Workspace: `/Volumes/External/OpenClawWork/coder-workspace/temp/glm-mcp-server-use`
- Tooling: `mcporter` + GLM official MCP endpoints
- Report file: `tmp/glm-mcp-smoke-report.json`
- Auth mode: environment variable (`Z_AI_API_KEY`)

## What was tested

`python3 scripts/smoke_test_glm_mcp.py --config ./tmp/mcporter-glm.json`

### 1) Web Search MCP

- Server schema discovery: ✅
- Tool call (`web_search_prime`): ✅
- Notes:
  - Runtime tool name is `web_search_prime`
  - Required argument is `search_query`

### 2) Web Reader MCP

- Server schema discovery: ✅
- Tool call (`webReader`) on provided WeChat URL: ✅ (request successful)
- Content quality for this URL: ⚠️
  - Returned content appears to be anti-bot/verification-like snippet, not full article body
  - `anti_bot_likely = true`

### 3) Zread MCP

- Server schema discovery: ✅
- Tool call (`get_repo_structure` with `repo_name=microsoft/vscode`): ✅
- Notes:
  - Uses `repo_name` parameter naming

### 4) Vision MCP

- Server schema discovery: ✅
- Tool call (`analyze_image`) with local generated image: ✅
- Notes:
  - Local stdio server works with `npx -y @z_ai/mcp-server`

## Conclusion

- All 4 MCP servers are reachable and callable with valid API key.
- Reader MCP works technically, but specific WeChat article URL is likely protected by anti-bot behavior, so extracted body is incomplete.
