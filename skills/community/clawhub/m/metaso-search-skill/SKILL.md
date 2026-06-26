---
name: metaso-search
description: Search the web using Metaso AI Search API. Use for live information, documentation, or research topics.
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python"], "env": ["METASO_API_KEY"] }, "primaryEnv": "METASO_API_KEY" } }
---

# Metaso Search

Search the web via Metaso AI Search API.

## Usage

```bash
python skills/metaso-search/scripts/search.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| q | str | yes | - | Search query |
| scope | str | no | webpage | Search scope: webpage, news, paper, etc. |
| size | int | no | 10 | Number of results (1-50) |
| page | int | no | 1 | Page number |
| conciseSnippet | bool | no | false | Return concise snippet |
| includeSummary | bool | no | false | Include AI summary |
| includeRawContent | bool | no | false | Fetch raw content from sources |

## Examples

```bash
# Basic search
python scripts/search.py '{"q":"OpenClaw AI"}'

# With options
python scripts/search.py '{
  "q": "人工智能最新进展",
  "size": 5,
  "includeSummary": true
}'
```

## API Reference

- **官方文档**: https://metaso.cn/search-api/playground
- **Endpoint**: `https://metaso.cn/api/v1/search`
- **Method**: POST
- **Auth**: Bearer token in `Authorization` header
- **Content-Type**: `application/json`

## Request Example

```bash
curl --location 'https://metaso.cn/api/v1/search' \
--header 'Authorization: Bearer YOUR_API_KEY' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
  "q": "搜索关键词",
  "scope": "webpage",
  "size": 10,
  "includeSummary": false,
  "includeRawContent": false,
  "conciseSnippet": false
}'
```

## Response Example

```json
{
  "credits": 3,
  "searchParameters": {
    "q": "搜索关键词",
    "scope": "webpage",
    "size": 10
  },
  "webpages": [
    {
      "title": "标题",
      "link": "https://example.com",
      "snippet": "摘要内容",
      "score": "high",
      "date": "2026-03-22"
    }
  ],
  "total": 25
}
```

## Current Status

✅ Ready to use
