---
name: keyapi-google-search
description: Perform Google web and image searches — retrieve ranked web results with titles, snippets, and URLs, or search for images with country and language targeting, result count control, and page-based pagination.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🔍"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-google-search

> Perform Google web and image searches — retrieve ranked web results or search for images with geographic, language, and result-count controls.

This skill provides Google search intelligence using the KeyAPI MCP service. It enables keyword-based web search returning ranked results with titles, URLs, and snippets, and image search with country/language targeting and page-based pagination — all through a unified, cache-first workflow.

Use this skill when you need to:
- Retrieve ranked Google web search results for any keyword query
- Search Google Images for visual content matching a keyword
- Target searches to a specific country or language
- Control result count (up to 100 for web, up to 20 per page for images)
- Paginate through image search results

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **KEYAPI_TOKEN** | A valid API token from [keyapi.ai](https://keyapi.ai/). Register at the site to obtain your free token. Set it as an environment variable: `export KEYAPI_TOKEN=your_token_here` |
| **Node.js** | v18 or higher |
| **Dependencies** | Run `npm install` in the skill directory to install `@modelcontextprotocol/sdk` |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## MCP Server Configuration

All tool calls in this skill target the KeyAPI Google MCP server:

```
Server URL : https://mcp.keyapi.ai/google/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform google --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Ranked web search results | `web_search` | Content research, competitive analysis, SERP monitoring |
| Image search results | `image_search` | Visual content discovery, brand image monitoring, asset research |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Select the Right Search Node

- **Web content research**: Use `web_search` for any query requiring text results, URLs, and page snippets.
- **Visual content research**: Use `image_search` for queries requiring image URLs and visual asset discovery.

> **`web_search` — No Pagination**
>
> `web_search` returns results in a single call. Use the `num` parameter (1–100) to control how many results are returned. There is no `page` parameter — all results are delivered at once.

> **`image_search` — Page-Based Pagination**
>
> `image_search` supports `page` (1-indexed) and `num` (1–20 per page) for pagination. To retrieve more results, increment the `page` value while keeping `num` consistent.

> **Language and Region Targeting**
>
> The two endpoints use different parameter conventions for targeting:
>
> | Endpoint | Language param | Format | Example |
> |---|---|---|---|
> | `web_search` | `lr` | Language-region code | `en-US`, `zh-CN`, `de-DE` |
> | `image_search` | `lr` | Language prefix code | `lang_en`, `lang_zh-CN`, `lang_de` |
> | `image_search` | `gl` | Two-letter country code | `us`, `cn`, `de` |
>
> For `web_search`, `lr` controls both language and regional relevance. For `image_search`, use `gl` for country targeting and `lr` for language filtering — they are independent controls.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform google --schema web_search
node scripts/run.js --platform google --schema image_search
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform google --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform google --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — web search (English, US, top 10 results):**

```bash
node scripts/run.js --platform google --tool web_search \
  --params '{"q":"best noise cancelling headphones 2025","lr":"en-US","num":10}' --pretty
```

**Example — web search (more results in one call):**

```bash
node scripts/run.js --platform google --tool web_search \
  --params '{"q":"competitor analysis tools","lr":"en-US","num":50}' --pretty
```

**Example — image search (first page):**

```bash
node scripts/run.js --platform google --tool image_search \
  --params '{"q":"wireless earbuds product photography","gl":"us","lr":"lang_en","num":20,"page":1}' --pretty
```

**Example — image search (next page):**

```bash
node scripts/run.js --platform google --tool image_search \
  --params '{"q":"wireless earbuds product photography","gl":"us","lr":"lang_en","num":20,"page":2}' --pretty
```

**Example — web search in a non-English market:**

```bash
node scripts/run.js --platform google --tool web_search \
  --params '{"q":"无线耳机推荐","lr":"zh-CN","num":10}' --pretty
```

**Pagination reference:**

| Endpoint | Pagination | Notes |
|---|---|---|
| `web_search` | None | Use `num` (1–100) to set result count. All results returned in one call. |
| `image_search` | `page` (1-indexed) | Use `num` (1–20) per page. Increment `page` for next batch. |

**Parameter reference:**

| Endpoint | Parameter | Description | Example values |
|---|---|---|---|
| Both | `q` | Search query (required) | `"best headphones"` |
| `web_search` | `num` | Result count (1–100, default 10) | `10`, `50`, `100` |
| `web_search` | `lr` | Language and region (default `en-US`) | `en-US`, `zh-CN`, `de-DE`, `ja-JP` |
| `image_search` | `num` | Results per page (1–20, default 10) | `10`, `20` |
| `image_search` | `page` | Page number (1-indexed, default 1) | `1`, `2`, `3` |
| `image_search` | `gl` | Country code for geo-targeting (default `us`) | `us`, `uk`, `de`, `cn` |
| `image_search` | `lr` | Language filter (default `lang_en`) | `lang_en`, `lang_zh-CN`, `lang_de` |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── web_search/
    │   └── {params_hash}.json
    └── image_search/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured search intelligence report:

**For web search results:**
1. **SERP Overview** — Total result count, top-ranking domains, result type distribution (organic, featured snippets, knowledge panels).
2. **Content Analysis** — Key themes across top results, common title patterns, snippet sentiment.
3. **Competitive Landscape** — Dominant domains, content authority signals, outranking opportunities.
4. **Research Findings** — Synthesized answer from top results relevant to the query intent.

**For image search results:**
1. **Image Inventory** — Result count, image source domains, image type distribution (product photos, infographics, logos).
2. **Visual Themes** — Common subjects, color patterns, composition styles.
3. **Source Attribution** — Top domains providing images, licensing signals where available.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **`web_search` has no pagination** | Use `num` (max 100) to retrieve all desired results in one call. There is no `page` parameter for web search. |
| **`image_search` pagination** | Use `page` (1-indexed) with consistent `num` to paginate through image results. |
| **`lr` format difference** | `web_search` uses `en-US` format; `image_search` uses `lang_en` format. Do not mix them. |
| **`gl` is image-search only** | The `gl` country-targeting parameter is available on `image_search` only, not `web_search`. |
| **`num` limits** | `web_search`: 1–100. `image_search`: 1–20 per page. |
| **Success check** | `code = 0` → success. Any other value → failure. Always check the response code before processing data. |
| **Retry on 500** | If `code = 500`, retry the identical request up to 3 times with a 2–3 second pause between attempts before reporting the error. |
| **Cache first** | Always check the local `.keyapi-cache/` directory before issuing a live API call. |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue workflow normally |
| `400` | Bad request — invalid or missing parameters | Ensure `q` is provided; check `num` range (web: 1–100, image: 1–20); verify `lr` format |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
