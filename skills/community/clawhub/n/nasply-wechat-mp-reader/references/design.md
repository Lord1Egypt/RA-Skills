# WeChat MP Reader Design

## Goal

Build a reusable skill that can:
1. Accept a WeChat Official Account article URL and extract the full article.
2. Accept an account name and try to resolve the account.
3. List recent or historical articles for that account.
4. Manage and validate MP backend session state.
5. Normalize output for downstream agents and workflows.

## Confirmed upstream logic from we-mp-rss analysis

The running project resolves and fetches through the WeChat MP backend stack rather than an official public-content API:

- **Search account by name**
  - `https://mp.weixin.qq.com/cgi-bin/searchbiz`
  - parameters include: `action=search_biz`, `query`, `token`, `ajax=1`
- **Fetch article list by account fakeid**
  - primary: `https://mp.weixin.qq.com/cgi-bin/appmsgpublish`
  - parameters include: `sub=list`, `sub_action=list_ex`, `fakeid`, `token`, `ajax=1`
- **Legacy/alternate article-list endpoint**
  - `https://mp.weixin.qq.com/cgi-bin/appmsg`
  - parameters include: `action=list_ex`, `fakeid`, `token`, `ajax=1`
- **Fetch article content**
  - article URL itself, then parse `#js_content`
  - browser-assisted fetch is used in `web` mode when needed
- **Fetch engagement stats (optional)**
  - `http://mp.weixin.qq.com/mp/getappmsgext`
  - requires session-bound cookies/tokens and is fragile
- **Refresh/get new MP backend session**
  - QR login flow in `driver/wx_api.py`
  - persisted in `/app/data/wx.lic` via `driver/token.py`

## Recommended architecture

### 1) Auth / session layer
- Load session from env or local file
- Validate session via backend probe
- Persist session for reuse
- Surface `present / valid / reason`

### 2) Source resolver
- Input: article URL or account name
- Output: account metadata (`biz`, `fakeid`, `name`, `avatar`, `signature`)

### 3) Article indexer
- Input: account identifier (`biz` or `fakeid`)
- Output: article metadata list (`title`, `url`, `publish_time`, `cover`, `summary`)

### 4) Content fetcher
- Input: article URL
- Output: raw HTML + parsed main body

### 5) Normalizer
- Input: raw parsed content
- Output: cleaned HTML + Markdown + image list + metadata

### 6) Stats provider (optional)
- Input: article URL + session material if available
- Output: read/like counters
- Warning: fragile, expiring, best-effort only

## Current prototype scope

Implemented now:
- URL parsing
- article-page fetch
- session resolution from env/file
- session validity check
- account-name search via backend when session is valid
- `fakeid` recovery by matching article-derived account info against search results
- article-list fetch via `fakeid`
- QR-login-based session acquisition and polling inside the skill
- automatic local Playwright WebKit fallback when direct HTTP article fetch looks non-canonical (verification page / shell page / mixed JS page)
- normalized article output with title / author / publish_time / account_name / content / images when fallback succeeds

Not yet implemented:
- persistent biz↔fakeid cache
- stronger body cleanup across more article variants
- further hardening the local Playwright WebKit fetcher across more article variants

## Data model

### Session
```json
{
  "present": true,
  "valid": false,
  "reason": "invalid session",
  "base_resp": {}
}
```

### Account
```json
{
  "name": "",
  "biz": "",
  "fakeid": "",
  "avatar": "",
  "signature": ""
}
```

### Article
```json
{
  "title": "",
  "url": "",
  "publish_time": "",
  "publish_time_raw": "",
  "author": "",
  "account_name": "",
  "content_html": "",
  "content_markdown": "",
  "images": []
}
```

## Operational cautions

1. WeChat pages and internal endpoints are brittle.
2. Search-by-name is less reliable than resolution from an existing article URL.
3. `getappmsgext`-style stats flows should never block the main extraction path.
4. The skill should expose partial success cleanly.
5. Account-list discovery requires a valid logged-in WeChat MP session (`cookie` + `token`).
6. Session presence is not enough; invalid sessions must be reported explicitly.
7. Direct HTTP article fetches may return verification pages or mixed shell pages; treat browser fallback as part of the normal article-resolution path, not an edge case.
8. Current article fallback depends on local Playwright WebKit being installed and runnable on the host; keep host browser dependencies healthy.
