---
name: page-fetch
description: "Extract readable content from webpages with a stable, low-dependency workflow. Use when the user asks to open, inspect, summarize, translate, verify, or quote a web page, article, blog post, documentation page, or similar URL. Prefer this skill when cross-model reliability matters: fetch raw HTML first, inspect embedded data next, and escalate to browser rendering only when lightweight methods fail." 
---

# Page Fetch

Use this skill to extract webpage content in a reproducible way that works well across different models and avoids browser dependence unless necessary.

This skill is built for reliability first:

- start with lightweight deterministic fetches
- inspect embedded page data before escalating
- use browser rendering only as a fallback
- report the extraction method and any access limits clearly

## What this skill is for

Use this skill when a user says things like:

- "看一下这个网页的内容"
- "Open this article and summarize it"
- "Tell me what this page says"
- "Translate this webpage"
- "Check whether this page mentions X"
- "Quote the main points from this documentation page"

This skill is best for:

- news articles
- blog posts
- documentation pages
- product pages
- general public webpages

This skill is not magic. If a page is blocked by login, CAPTCHA, region restrictions, or aggressive anti-bot controls, report that clearly.

## Design goal

The core goal is **cross-model reliability**.

Different LLMs often choose different ad-hoc ways to read webpages. This skill reduces that variance by giving them a standard path:

1. Route `mp.weixin.qq.com` links to the dedicated WeChat extractor first.
2. Try the lightweight deterministic extractor for general webpages.
3. Inspect embedded page data when available.
4. Use a real browser only when necessary.
5. Tell the user which path worked and what the limits were.

## Workflow

### Step 1: Use the unified runner by default

For routine webpage reads, run the wrapper first:

```bash
python3 scripts/page_fetch.py "https://example.com/article" --format json
```

What it does:

- routes `mp.weixin.qq.com` to the dedicated WeChat extractor first
- uses lightweight HTML extraction for general pages
- escalates to browser rendering only when needed
- does **not** persist files unless `--save-json` is explicitly passed
- never defaults to writing transient JSON into the current working directory

Persistence rule:

- default: no disk writes
- only save when the caller explicitly passes `--save-json`
- when saving is requested without `--output`, write to a non-workspace report path chosen by the caller or local runtime convention
- do not write transient artifacts into the workspace root

### Step 2: Direct script usage when debugging or forcing a method

Use direct scripts only when you need to debug or force a particular extraction path.

#### WeChat public articles

```bash
python3 scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/..." --format json
```

What it does:

- uses a WeChat mobile-style request header
- extracts article metadata from page meta tags and script variables
- reads the article body from `#js_content` / `.rich_media_content`
- reports explicit access limits when the page is replaced by verification or anti-bot flows
- does not persist files; it only returns structured extraction output

What to look for in the output:

- `title`
- `author`
- `account_nickname`
- `published_time`
- `text`
- `method`
- `access_limited`
- `access_limit_reason`

#### General lightweight fetch

```bash
python3 scripts/fetch_page.py "https://example.com/article" --format json
```

What it does:

- fetches raw HTML via `requests`
- extracts metadata from HTML/meta tags
- inspects JSON-LD
- inspects embedded payloads such as `__NEXT_DATA__`
- falls back to DOM paragraph extraction

What to look for in the output:

- `title`
- `author`
- `published_time`
- `text`
- `method`
- `notes`

#### Browser-render fallback

If the lightweight path returns thin, broken, or clearly incomplete content, run:

```bash
python3 scripts/render_page.py "https://example.com/article" --format json
```

What it does:

- launches headless Chromium via Node Playwright
- waits for the page to render
- extracts title, metadata, and readable text from the rendered DOM

Use this only when needed. It is slower and heavier than the first-pass extractor.

### Step 3: Report method and limitations

Always tell the user which method worked:

- `wechat-dom`
- `wechat-access-limited`
- `json-ld`
- `embedded-data:__NEXT_DATA__`
- `dom-paragraphs`
- `browser-render:playwright`

Also mention known limitations when relevant:

- text was truncated
- metadata only
- browser runtime unavailable
- login wall / CAPTCHA / region restriction
- anti-bot blocking

## Output contract

When using this skill, aim to return the following whenever possible:

- page title
- author and publish/update time
- the main body text or a concise faithful summary
- the extraction method used
- any missing sections, uncertainty, or access limitations

Do **not** imply full page access if only metadata or fragments were recovered.

## Scripts

### `scripts/page_fetch.py`

Purpose:

- unified no-persist entry point
- routes WeChat vs general webpages automatically
- escalates to browser rendering only when lightweight extraction is insufficient
- only saves JSON when `--save-json` is explicitly requested

Typical usage:

```bash
python3 scripts/page_fetch.py "https://example.com/article" --format json
```

Optional explicit persistence:

```bash
python3 scripts/page_fetch.py "https://example.com/article" --format json --save-json --output ./example.json
```

Output fields:

- all fields returned by the selected extraction path
- `notes` including runner step trace
- `saved_to` only when explicit persistence is requested

### `scripts/fetch_wechat_article.py`

Purpose:

- WeChat public article extraction without persistence
- optimized for `mp.weixin.qq.com` article pages

Typical usage:

```bash
python3 scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/..." --format json --max-chars 12000
```

Output fields:

- `url`
- `final_url`
- `status_code`
- `title`
- `description`
- `author`
- `account_nickname`
- `published_time`
- `method`
- `text`
- `content_html`
- `excerpt`
- `notes`
- `access_limited`
- `access_limit_reason`

### `scripts/fetch_page.py`

Purpose:

- deterministic first-pass extraction
- optimized for cost, speed, and portability

Typical usage:

```bash
python3 scripts/fetch_page.py "https://example.com/article" --format json --max-chars 8000
```

Output fields:

- `url`
- `final_url`
- `status_code`
- `title`
- `description`
- `author`
- `published_time`
- `method`
- `text`
- `excerpt`
- `notes`

### `scripts/render_page.py`

Purpose:

- browser-render fallback for JS-heavy or client-rendered pages

Typical usage:

```bash
python3 scripts/render_page.py "https://example.com/article" --format json --wait-ms 2500
```

Important notes:

- requires Node Playwright for browser fallback
- requires Chromium installed via Playwright for browser fallback
- requires system shared libraries for headless Chromium when browser fallback is used
- returns explicit machine-readable failure states when unavailable or broken

## References

Read these when you need more context than the main workflow:

- `references/strategy.md`
  - default extraction strategy
  - failure-to-next-action mapping
- `references/browser-runtime.md`
  - browser fallback runtime expectations
  - common failure modes
  - operational guidance

## Guardrails

- Prefer lightweight fetches over browser automation.
- Do not silently switch to expensive browser rendering for every page.
- Do not bluff when access is blocked.
- For routine reads, do not save page contents to disk unless the user explicitly wants export or archival.
- If output must be saved, prefer a caller-chosen report/output path rather than workspace-root artifacts.

## Quick examples

### Example A: WeChat public article

If the URL is `mp.weixin.qq.com`, try `fetch_wechat_article.py` first. If it returns article body text, use that directly. If it reports access limits, say so plainly.

### Example B: standard news article

If `fetch_page.py` returns a solid body via `embedded-data:__NEXT_DATA__` or `dom-paragraphs`, use that result directly.

### Example C: JS-rendered docs site

If `fetch_page.py` returns thin text or metadata only, escalate to `render_page.py`.

### Example D: blocked page

If browser rendering fails because of login, CAPTCHA, or anti-bot controls, report the limitation plainly and, when appropriate, look for an alternate accessible source.
