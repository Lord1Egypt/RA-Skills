---
name: huozi
description: Publish Markdown and HTML to huozi.app as beautiful, shareable web pages. Register, manage, and publish — all through conversation.
homepage: https://huozi.app
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[],"bins":["curl"]},"primaryEnv":"HUOZI_API_KEY","emoji":"📄","os":["darwin","linux","win32"]}}
---

# Huozi — Markdown & HTML Publishing for Agents

Publish Markdown or HTML content to [huozi.app](https://huozi.app) as shareable web pages. One API call, instant publishing.

## Onboarding

**IMPORTANT:** When this skill is first loaded, check if `HUOZI_API_KEY` is set. If NOT, do NOT just show a link — immediately start the interactive registration flow below. Guide the user through it conversationally, step by step.

### Step 1 — Ask for email

Tell the user: "Let's set up your Huozi account. What's your email?" Then call:

```bash
curl -s -X POST https://huozi.app/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "<user_email>"}'
```

Tell the user: "A verification code has been sent to your email. Please check your inbox and tell me the code."

### Step 2 — Verify the code

When the user provides the code:

```bash
curl -s -X POST https://huozi.app/api/v1/auth/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "<user_email>", "code": "<code>"}'
```

Save the returned `access_token`.

### Step 3 — Create workspace

Suggest a slug from the user's email username (e.g. `alice@gmail.com` → `alice`). Tell the user:

> "Your pages will be published at **huozi.app/alice/** — would you like to change this, or is this OK?"

After the user confirms (or gives a new slug):

```bash
curl -s -X POST https://huozi.app/api/v1/auth/setup \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"workspace_slug": "<confirmed_slug>"}'
```

### Step 4 — Done!

The response contains `api_key` and `workspace.url`. Tell the user:

> "All set! Your workspace is **huozi.app/<slug>/**. To save your API key for future sessions, run:
> `export HUOZI_API_KEY=<api_key>`
> You can now publish Markdown anytime — just tell me what to publish."

## Publishing Markdown

Publish or update a Markdown page:

```bash
curl -s -X POST https://huozi.app/api/v1/pages \
  -H "Authorization: Bearer <api_key>" \
  -H "Content-Type: application/json" \
  -d '{"title": "<title>", "slug": "<slug>", "content": "<markdown>"}'
```

- `slug` is optional — auto-generated from title if omitted. Keep under 8 words (e.g. `weekly-report-apr-14`)
- Same slug = upsert (update existing page)
- Response includes the public `url`

## Publishing HTML

Publish a static HTML page — perfect for landing pages, dashboards, reports with custom styling:

```bash
curl -s -X POST https://huozi.app/api/v1/pages \
  -H "Authorization: Bearer <api_key>" \
  -H "Content-Type: application/json" \
  -d '{"title": "<title>", "slug": "<slug>", "content": "<html>", "content_type": "html"}'
```

- Set `content_type` to `"html"` (defaults to `"markdown"` if omitted)
- Same slug = upsert, versioning, and access tokens work identically to Markdown pages

### HTML Input Format

- **Full document**: `<html><head>...</head><body>...</body></html>` — head is parsed for `<style>` and `<meta>`, body is rendered
- **Fragment**: any HTML without `<html>`/`<head>` tags — treated as body content directly
- `<meta>` OG tags (`og:title`, `og:description`, `og:image`) and `<meta name="description">` are extracted as fallback metadata; API fields (`title`, `description`) always take priority

### HTML Constraints — What Is Allowed

| Category | Allowed | Blocked |
|----------|---------|---------|
| **HTML tags** | All standard tags: `div`, `span`, `table`, `form`, `svg`, `img`, `video`, `audio`, etc. | `<script>`, `<iframe>`, `<embed>`, `<object>`, `<link rel="stylesheet">` |
| **CSS** | `<style>` blocks, inline `style=""`, all standard properties (flexbox, grid, animations, transforms, etc.) | `@import`, `expression()`, `javascript:` in `url()`, `-moz-binding`, `behavior:` |
| **JavaScript** | None | All `<script>` tags stripped; all event handlers (`onclick`, `onerror`, `onload`, etc.) stripped |
| **URLs** | `http:`, `https:`, `mailto:`, `tel:` | `javascript:` (rewritten to `#`), `data:` in CSS `url()` |
| **Images** | `<img>` with `http:`/`https:`/`data:` src | — |
| **SVG** | Full inline SVG support (path, circle, rect, gradient, filter, etc.) | External SVG via `<img src>` works; `<use href="external.svg">` does not |
| **Forms** | Display only — `<input>`, `<select>`, `<textarea>`, `<button>` render but `action`/`method` are stripped | No form submission |
| **External resources** | Images (`<img src>`), video/audio (`<video>`, `<audio>`) via `http:`/`https:` | External CSS (`<link>`), external JS, `@import` |
| **Content size** | Max 2MB per page | — |

### Best Practices for HTML Pages

- **Include all CSS inline** — use `<style>` blocks in `<head>` or inline `style=""` attributes; external stylesheets are not supported
- **Use system fonts or web-safe fonts** — `@import` for Google Fonts is blocked; use `font-family: system-ui, sans-serif` or embed fonts as base64 `@font-face` if essential
- **Embed small images as data URIs** — for icons/logos under ~50KB; larger images should be hosted externally and referenced via `https://` URLs
- **Design responsive layouts** — pages are served full-width; use `max-width` on a container and CSS media queries for mobile support
- **Set a background color** — the page has no default background; always set `background` on `body` or a wrapper element

## Other Operations

| Action | Method | Endpoint |
|--------|--------|----------|
| List pages | GET | `/api/v1/pages` |
| Get page | GET | `/api/v1/pages/<slug>` |
| Update page | PUT | `/api/v1/pages/<slug>` |
| Delete page | DELETE | `/api/v1/pages/<slug>` |

All require `Authorization: Bearer <api_key>` header. Base URL: `https://huozi.app`

## Examples

- "帮我把这个 markdown 发布到 huozi" → publish content, return URL
- "发布我的周报" → generate slug like `weekly-report-2026-04-14`, publish
- "更新 huozi 上的 hello 页面" → PUT to update
- "帮我做一个 landing page 发布到 huozi" → generate HTML, publish with `content_type: "html"`
- "把这个报告做成网页发布" → generate styled HTML page, publish

## Notes

- API keys start with `hz_` prefix
- No password needed — registration uses email OTP only
- Markdown: supports GFM, task lists, code highlighting, math (KaTeX)
- HTML: full CSS + SVG + images, no JavaScript — see constraints table above
- Content limit: 2MB per page for both Markdown and HTML
- Use `curl` via Bash to make API calls
- When generating HTML for the user, always produce self-contained pages with all CSS inlined
- **Full API reference (agent-friendly):** https://huozi.app/docs4agent
- Setup options: https://huozi.app/start
- Human-readable docs: https://huozi.app/docs
