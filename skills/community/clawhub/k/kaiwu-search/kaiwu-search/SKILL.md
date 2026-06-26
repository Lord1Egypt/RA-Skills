---
name: kaiwu-search
description: Search the web in Chinese (Traditional + Simplified) and English using the Kaiwu API. Use when the agent needs to search the web for Chinese content, find information about Taiwan/China/East Asia topics, or when existing search tools return poor Chinese-language results. Supports uncensored search (no political filtering), bilingual Traditional/Simplified Chinese expansion, and LLM-ready output. Triggers on web search, Chinese search, Taiwan search, 搜尋, 查詢, research in Chinese.
---

# Kaiwu Search — 開物搜尋

Search the web via Kaiwu API (`kaiwu.dev`). Optimized for Chinese content (Traditional + Simplified), uncensored, with multi-engine aggregation (Google, DuckDuckGo, Brave).

## Setup

Requires `KAIWU_API_KEY` secret. If not set:

1. Check if agent has a wallet (base-wallet skill or existing wallet).
2. If wallet exists: auto-register via `POST https://kaiwu.dev/api/auth/agent-register` with SIWE signature to get a key.
3. If no wallet: instruct user to visit `https://kaiwu.dev` to get a free API key (1,000 searches/month free).

Store the key: `KAIWU_API_KEY=kw_...`

## Search

```bash
curl -X POST https://kaiwu.dev/v1/search \
  -H "Authorization: Bearer $KAIWU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "台灣 AI 基本法",
    "lang": "zh-TW",
    "max_results": 5
  }'
```

### Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | required | Search query |
| `lang` | string | `zh-TW` | `zh-TW`, `zh-CN`, `en`, `auto` |
| `max_results` | number | 5 | 1–20 |
| `time_range` | string | `all` | `day`, `week`, `month`, `year`, `all` |

### Response

```json
{
  "query": "台灣 AI 基本法",
  "results": [
    {
      "title": "立法院三讀通過《人工智慧基本法》",
      "url": "https://moda.gov.tw/...",
      "snippet": "立法院114年12月23日三讀通過...",
      "engine": "google",
      "published": "2025-12-23"
    }
  ],
  "credits_used": 1,
  "credits_remaining": 999
}
```

## Check Credits

```bash
curl https://kaiwu.dev/v1/credits \
  -H "Authorization: Bearer $KAIWU_API_KEY"
```

## Usage Guidelines

- 1 credit per search call. Free tier: 1,000/month.
- Prefer `lang: "zh-TW"` for Taiwan topics, `"zh-CN"` for China topics, `"auto"` when unsure.
- For broad Chinese queries, Kaiwu auto-expands Traditional ↔ Simplified (e.g., "人工智慧" also searches "人工智能").
- Use `time_range: "week"` or `"month"` for recent news.
- Results come from Google, DuckDuckGo, and Brave — no Baidu, no censorship filtering.
