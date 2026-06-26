# Zhipu GLM Web Search — API Reference

## Endpoints

### REST API (cURL mode)

```
POST https://open.bigmodel.cn/api/paas/v4/web_search
Authorization: Bearer <ZHIPU_API_KEY>
Content-Type: application/json
```

### MCP Broker (mcporter mode)

```
SSE: https://open.bigmodel.cn/api/mcp-broker/proxy/web-search/mcp?Authorization=<ZHIPU_API_KEY>
```

- **Transport**: SSE (Server-Sent Events)
- **Auth**: API key as URL query parameter `Authorization=`
- **⚠️ Do NOT use**: `https://open.bigmodel.cn/api/mcp/web_search_prime/mcp` (deprecated; returns 401 on tools/call)

## Search Engines

| REST API Name | MCP Tool Name | Description |
|---------------|---------------|-------------|
| `search_pro` | `webSearchPro` | Advanced multi-engine search (**recommended**) |
| `search_pro_quark` | `webSearchQuark` | Quark engine, Chinese content |
| `search_pro_sogou` | `webSearchSogou` | Sogou engine, China domestic |
| `search_std` | `webSearchStd` | Basic standard search |

## Parameters

| Parameter | REST API | MCP | Type | Default | Description |
|-----------|----------|-----|------|---------|-------------|
| `search_query` | ✅ | ✅ | string | — | Search text (≤70 chars recommended) |
| `search_engine` | ✅ | — (tool name) | enum | — | Engine selection |
| `search_intent` | ✅ | ❌ | boolean | false | Enable intent recognition |
| `count` | ✅ | ✅ | integer | 10 | Results 1-50 |
| `search_recency_filter` | ✅ | ✅ | enum | noLimit | Time range filter |
| `content_size` | ✅ | ✅ | enum | medium | Summary detail level |
| `search_domain_filter` | ✅ | ✅ | string | — | Domain whitelist |

### Time Range Values

`noLimit` · `oneYear` · `oneMonth` · `oneWeek` · `oneDay`

### Content Size Values

- `medium` — 400-600 character summaries
- `high` — up to 2500 character summaries (higher cost)

## cURL Examples

### Basic

```bash
curl -s POST https://open.bigmodel.cn/api/paas/v4/web_search \
  -H "Authorization: Bearer $ZHIPU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"search_query":"AI news","search_engine":"search_pro","count":10}'
```

### With All Options

```bash
curl -s POST https://open.bigmodel.cn/api/paas/v4/web_search \
  -H "Authorization: Bearer $ZHIPU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "latest AI developments",
    "search_engine": "search_pro_quark",
    "search_intent": true,
    "count": 20,
    "search_recency_filter": "oneWeek",
    "content_size": "high",
    "search_domain_filter": "arstechnica.com"
  }'
```

## Common Issues

### "Api key not found" (MCP mode)

Wrong endpoint. Use the `mcp-broker/proxy` URL, not the deprecated `web_search_prime` endpoint.

### "Tool not found: web_search_prime"

The broker endpoint uses different tool names (`webSearchPro`, etc.). Use `webSearchPro` instead.

### Empty results `[]`

- Verify your Zhipu account plan supports web search
- Check quota at <https://open.bigmodel.cn>
- Try a different query or engine

### mcporter not found

Install it: `npm i -g mcporter`
Or use cURL fallback by setting `ZHIPU_API_KEY` env var.

## Official Docs

- Web Search: <https://docs.bigmodel.cn/cn/guide/tools/web-search>
- MCP Server: <https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server>
