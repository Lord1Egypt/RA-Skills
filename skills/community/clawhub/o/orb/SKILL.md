---
name: orb
description: >
  Create and share rich interactive artifacts (webpages, markdown, flowcharts)
  as hosted links from any AI conversation. Use when the user asks to create
  a dashboard, report, chart, visualization, interactive page, or any shareable
  content. Triggers on: "create an artifact", "make this shareable",
  "make this interactive", "create a webpage/dashboard/chart/document".
license: MIT
metadata:
  author: biryanilabs
  version: "1.0"
  homepage: https://byorb.app
  openclaw:
    primaryEnv: ORB_API_KEY
    requires:
      env: ["ORB_API_KEY"]
      bins: ["curl"]
allowed-tools: Bash(curl:*)
---

# Orb — Artifacts for your AI Agent

Orb is a hosted artifact service. Use the API at https://api.byorb.app/v1.
Artifacts are rendered at https://art.byorb.app/v/<id>.

This skill uses the web API only. Do not save artifact content to disk.
Always return the hosted link to the user.

---

## API Key Setup

All requests require an API key via the `ORB_API_KEY` environment variable.

Before making any API call, check that `$ORB_API_KEY` is set. If it is not:

1. Ask the user for their Orb API key:
   > I need your Orb API key to create artifacts.
   > Get one at **https://byorb.app/dashboard/settings** → **Create API Key**

2. Once the user provides the key, **persist it** so it survives across sessions.
   Use your native configuration mechanism:
   - **Claude Code**: Add to `~/.claude/settings.json` under `"env": { "ORB_API_KEY": "..." }`
   - **Gemini CLI**: Write to `~/.gemini/.env` as `ORB_API_KEY=...`
   - **Codex**: Add to `~/.codex/config.toml` under `[shell_environment_policy]` with `set = { ORB_API_KEY = "..." }`
   - **Fallback**: Append `export ORB_API_KEY=...` to the user's shell profile (`~/.zshrc` or `~/.bashrc`)

3. Also `export ORB_API_KEY=...` in the current session so it's available immediately.

All requests require:

```
Authorization: Bearer $ORB_API_KEY
```

---

## Default Behavior

When the user asks you to create any visual, interactive, or shareable content,
create an artifact via the API and return the hosted link immediately.

In the same conversation, always UPDATE the existing artifact — do not create a
new one unless the user explicitly says "new artifact" or "separate artifact".

Boundary rules:

- Do not embed artifact content inline in the chat. Always return the hosted link.
- Do not create a new artifact to apply an update. Use PUT on the existing ID.
- Do not include external `<script src="...">` or `<link rel="stylesheet" href="...">` tags in Webpages.
- Do not use `fetch()`, `XMLHttpRequest`, or `WebSocket` in Webpage JS.
- Do not use external image URLs in Webpages. Use inline SVG, base64 data URIs,
  or Orb-hosted asset URLs (see Image Assets section).
- Never expose the API key in any response.

---

## Creating an Artifact

Triggers: "create an artifact", "create a chart / dashboard / report / document /
visualization / webpage", "make this interactive", "make this shareable"

```bash
curl -sS -X POST https://api.byorb.app/v1/artifacts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ORB_API_KEY" \
  -d '{
    "type": "webpage",
    "title": "Q1 Revenue Dashboard",
    "content": "<full content string>"
  }'
```

Types: `webpage` | `markdown` | `flowchart`

Save the returned `id` — you will need it for updates and feedback.

Return the link as:
```
[Q1 Revenue Dashboard](https://art.byorb.app/v/<id>)
_Expires in 7 days · Open to save or leave feedback · Say "apply my artifact comments" to update_
```

---

## Updating an Artifact

Triggers: "change", "update", "make it", "fix", "add" — referring to an existing artifact

Use the `id` from this conversation. The URL stays the same.

```bash
curl -sS -X PUT https://api.byorb.app/v1/artifacts/<id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ORB_API_KEY" \
  -d '{"content": "<updated full content>"}'
```

Return:
```
Updated: [Q1 Revenue Dashboard](https://art.byorb.app/v/<id>)
```

---

## Applying Artifact Comments

Triggers: "apply my artifact comments", "apply comments", "check artifact feedback"

Step 1 — Fetch pending feedback:

```bash
curl -sS "https://api.byorb.app/v1/artifacts/<id>/feedback?status=pending" \
  -H "Authorization: Bearer $ORB_API_KEY"
```

Step 2 — If feedback exists, apply all in a single PUT update.

Step 3 — Mark processed:

```bash
curl -sS -X PATCH https://api.byorb.app/v1/artifacts/<id>/feedback/processed \
  -H "Authorization: Bearer $ORB_API_KEY"
```

If no pending feedback: "No pending comments found on your artifact."
Tell the user which comments were applied.

---

## Uploading Image Assets (for Webpages)

When a Webpage artifact needs an image that cannot be SVG or base64:

```bash
curl -sS -X POST https://api.byorb.app/v1/assets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ORB_API_KEY" \
  -d '{"image_url": "https://external.com/photo.png"}'
```

Returns: `{ "asset_url": "https://art.byorb.app/img/<uuid>" }`

Use this URL in your HTML: `<img src="https://art.byorb.app/img/<uuid>" alt="...">`
Assets expire with the artifact.

---

## Listing Artifacts

Triggers: "show my artifacts", "list my artifacts", "what have I created"

```bash
curl -sS https://api.byorb.app/v1/artifacts \
  -H "Authorization: Bearer $ORB_API_KEY"
```

Present as a list with title and link per artifact.

---

## Artifact Type Guidelines

**Webpage** — Single self-contained HTML file. All CSS and JS must be inline.
No external CDN links. No network calls from JS. Images: inline SVG, base64,
or Orb-hosted asset URLs only.
Best for: dashboards, calculators, interactive charts, timelines, quizzes.

**Markdown** — GFM with table support. No raw HTML blocks.
Supports embedded Mermaid diagrams using triple-backtick mermaid code blocks —
they render as inline SVG diagrams within the document.
Best for: reports, summaries, structured documents, specs with diagrams.

**Flowchart** — Valid Mermaid.js syntax only (standalone diagram).
Supported: graph, sequenceDiagram, stateDiagram-v2, erDiagram, gantt.
Best for: architecture diagrams, process flows, state machines.

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 401 | Bad or missing API key | Prompt user to set key (see API Key Setup section) |
| 402 | Free plan limit (10 artifacts) | "Visit https://byorb.app/upgrade for unlimited artifacts." |
| 404 | Artifact not found | Verify ID is from this conversation. Offer to create a new one. |
| 422 | Invalid content or type | Check type value and content. Retry. |
| 429 | Rate limit | Back off. Tell user to try again in a moment. |
