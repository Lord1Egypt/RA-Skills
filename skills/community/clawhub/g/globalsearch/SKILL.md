---
name: global-search
description: Unleashes cutting-edge multi-source search technology that instantly synthesizes vast amounts of information across the web, delivering comprehensive and relevant results through intelligent aggregation by default. Executes parallel searches across multiple content channels simultaneously to provide maximum coverage and relevance. Offers superior search efficiency with a single query. Use when the user needs to search the web, gather news, find articles by keyword, or retrieve references for research.
metadata:
  openclaw:
    emoji: "🔍"
  required_env_vars:
    - GLOBAL_SEARCH_API_KEY
  homepage: "https://clb.ciglobal.cn"
  publisher: "clb.ciglobal.cn"
---

# Global Search

This skill performs multi-source web search through an external service and can aggregate results across multiple sources when the user explicitly asks for comprehensive coverage.

## ⚠️ Privacy and Security Notice

**Important:** This skill sends the user’s search query to an external web search service at `https://clb.ciglobal.cn/web_search`. Please be aware:

- **Data Transmission:** Queries are transmitted to a third-party service and may be associated with your account
- **API Key Required:** The only runtime credential is `GLOBAL_SEARCH_API_KEY`
- **Credential Storage:** Store the API key securely using environment variables or your system's credential manager. Do not hardcode it in scripts
- **User Consent:** If a query may contain sensitive, personal, confidential, or internal information, ask the user to confirm before sending it to the external service
- **Sensitive Query Filter:** Do not send passwords, tokens, session cookies, private keys, personal identifiers, internal-only content, or other confidential data
- **Data Minimization:** Prefer shortening, generalizing, or redacting unnecessary sensitive details before searching
- **Scope Limitation:** Use this skill only for legitimate search purposes
- **Provider Verification:** The provider `clb.ciglobal.cn` is an external third-party service. Its trustworthiness, retention policy, and privacy practices should be verified by the skill publisher before distribution; users should not assume it has been independently vetted
- **Account Association:** The API key associates search activity with your account, so search history may be logged or retained by the provider

## Credential Configuration

**Required Environment Variable:**
- `GLOBAL_SEARCH_API_KEY`: API key obtained from https://clb.ciglobal.cn/apiKey/login

**Recommended Setup:**
```bash
# Set environment variable (Linux/Mac)
export GLOBAL_SEARCH_API_KEY="your_api_key_here"

# Set environment variable (Windows PowerShell)
$env:GLOBAL_SEARCH_API_KEY="your_api_key_here"
```

Alternatively, configure the API key in your agent's credential manager or secrets storage.

## When to Use

Apply this skill when the user:
- Asks to search the web or gather information online
- Needs news articles or references by keyword
- Wants to retrieve content from diverse online sources
- Requires comprehensive, real-time web search with maximum coverage

Use comprehensive search only when the user explicitly requests broad multi-source coverage. For simple lookups, prefer the minimum necessary query scope.

## API Overview

**Endpoint:** `POST /web_search`

**Base URL:** `https://clb.ciglobal.cn`

**Authentication:** Required header `X-API-Key`. Get your API key at https://clb.ciglobal.cn/apiKey/login

**Note:** This skill sends user queries to an external web search service. Please ensure you have obtained proper authorization before using this service.

## Request

For comprehensive search (default behavior), the skill will use the script from overall.md to perform 4 parallel API calls automatically:
- **Call 1**: `search_source=baidu_search`, `mode=network` (百度新闻/资讯)
- **Call 2**: `search_source=google_search`, `mode=network` (谷歌新闻/资讯)
- **Call 3**: `search_source=baidu_search_ai`, `mode=network` (百度 AI 搜索)
- **Call 4**: `mode=warehouse` (Elasticsearch 索引库，忽略 search_source)

### Headers
| Header | Required | Description |
|--------|----------|-------------|
| X-API-Key | Yes | API key for authentication. Get your key at https://clb.ciglobal.cn/apiKey/login |
| Content-Type | Yes | `application/x-www-form-urlencoded` (form data) |

### Form Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| keyword | string | Yes | - | Search keyword(s)，多个关键词用空格分隔 |
| search_source | string | No | - | Engine: `baidu_search`, `google_search`, `baidu_search_ai`. Note: Ignored when using default comprehensive search |
| mode | string | No | - | `network` = live crawl, `warehouse` = ES index. Note: Ignored when using default comprehensive search |
| page | int | No | 1 | Page number (starts from 1) |



### Comprehensive Search (All Sources)
当用户明确要求进行全面搜索（即同时搜索所有可用来源）时，使用 `overall.md` 中的脚本进行搜索，而不是使用下面的示例代码。

When the user explicitly wants to search across ALL available sources simultaneously (comprehensive search), you should:


**Example Implementation (Python asyncio):**
```python
import aiohttp
import asyncio
import os

API_URL = "https://clb.ciglobal.cn/web_search"
# Get API key from environment variable (recommended)
API_KEY = os.environ.get("GLOBAL_SEARCH_API_KEY", "your_api_key_here")

if API_KEY == "your_api_key_here":
    raise ValueError("Please set GLOBAL_SEARCH_API_KEY environment variable or provide your API key")

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded"
}

SEARCH_CONFIGS = [
    {"name": "百度搜索", "mode": "network", "search_source": "baidu_search"},
    {"name": "谷歌搜索", "mode": "network", "search_source": "google_search"},
    {"name": "百度 AI 搜索", "mode": "network", "search_source": "baidu_search_ai"},
    {"name": "全库搜", "mode": "warehouse", "search_source": None}
]

async def fetch_search(session, semaphore, config, keyword, page):
    async with semaphore:
        data = {
            "keyword": keyword,
            "page": page,
            "mode": config['mode'],
        }
        if config['search_source']:
            data["search_source"] = config['search_source']
        
        async with session.post(API_URL, headers=headers, data=data) as response:
            result = await response.json()
            return result.get('references', [])

async def comprehensive_search(keyword, page=1):
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests
        tasks = [fetch_search(session, semaphore, config, keyword, page) 
                 for config in SEARCH_CONFIGS]
        results = await asyncio.gather(*tasks)
        # Flatten all references into one list
        all_references = [ref for refs in results for ref in refs]
        return all_references

asyncio.run(comprehensive_search("人工智能"))
```

### Parameter Constraints
- `search_source`: One of `baidu_search`, `google_search`, `baidu_search_ai`
- `mode`: One of `network`, `warehouse`
- When `mode=warehouse`, search is performed against the Elasticsearch index and ignores `search_source`
- When `mode=network`, use `search_source` to select Baidu, Google, or Baidu AI search

## Response Format

```json
{
  "code": 200,
  "message": "success",
  "references": [
    {
      "title": "Article title",
      "sourceAddress": "https://example.com/article",
      "origin": "Source name",
      "publishDate": "2025-03-24 12:00:00",
      "summary": "Article summary or snippet"
    }
  ]
}
```

## Usage Examples

### Example 1: Search Baidu news
```
POST https://clb.ciglobal.cn/web_search
Headers: X-API-Key: <your_api_key>, Content-Type: application/x-www-form-urlencoded
Body (form): keyword=人工智能&search_source=baidu_search&mode=network&page=1
```

### Example 2: Search Google news
```
POST https://clb.ciglobal.cn/web_search
Headers: X-API-Key: <your_api_key>, Content-Type: application/x-www-form-urlencoded
Body (form): keyword=AI&search_source=google_search&mode=network&page=1
```

### Example 3: Search warehouse (ES index)
```
POST https://clb.ciglobal.cn/web_search
Headers: X-API-Key: <your_api_key>, Content-Type: application/x-www-form-urlencoded
Body (form): keyword=机器学习&mode=warehouse&page=1
```

### Example 4: cURL
```bash
curl -X POST "https://clb.ciglobal.cn/web_search" \
  -H "X-API-Key: <your_api_key>" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "keyword=科技新闻&search_source=baidu_search&mode=network&page=1"
```

## Error Codes

| Code | Message | Cause |
|------|---------|-------|
| 401 | X-API-Key参数缺失 | Missing API key header |
| 401 | ApiKey无效 | Invalid API key |
| 400 | search_source参数错误 | Invalid search_source value |
| 400 | mode参数错误 | Invalid mode value |
| 400 | page参数错误 | Invalid page (non-integer or 0) |

## Integration Steps

1. **Verify Provider:** Before publishing or using this skill, verify `clb.ciglobal.cn`’s trust model, privacy policy, data retention practices, and ownership information
2. **Obtain API Key:** Visit https://clb.ciglobal.cn/apiKey/login to get your API key
3. **Configure Credentials:** Set the `GLOBAL_SEARCH_API_KEY` environment variable with your API key
   - Linux/Mac: `export GLOBAL_SEARCH_API_KEY="your_api_key_here"`
   - Windows: `$env:GLOBAL_SEARCH_API_KEY="your_api_key_here"`
4. **API Base URL:** `https://clb.ciglobal.cn`
5. **Comprehensive Search:** Only perform comprehensive search across all sources when the user explicitly requests broad multi-source coverage
6. **Sensitive Query Check:** If the user’s query includes sensitive, personal, confidential, or internal data, refuse to transmit it and ask for a redacted or generalized query instead
7. **Make Request:** Call `POST /web_search` with form-encoded parameters and include `X-API-Key` header
8. **Parse Response:** Parse `references` from the response and use `title`, `sourceAddress`, `summary` as needed
