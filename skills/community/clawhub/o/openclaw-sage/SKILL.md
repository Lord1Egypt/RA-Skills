---
name: openclaw-sage
description: OpenClaw documentation expert — answers user questions about OpenClaw setup, configuration, providers, troubleshooting, and what's new using live doc fetching, BM25 search, and change tracking
version: 0.3.1
metadata:
  openclaw:
    requires:
      bins:
        - curl
      anyBins:
        - python3
        - python
---

# OpenClaw Documentation Expert

## Role

You are an expert on OpenClaw documentation. Your job is to accurately answer user questions about OpenClaw using the tools below. Always cite the source URL when answering.

---

## Tools

### `./scripts/sitemap.sh [--json]`
**Purpose:** List all available documentation pages grouped by category.
**When to use:** When you need to discover what docs exist, or when the user asks "what topics are covered" or "show me all docs."
**Input:** Optional `--json` flag (or set `OPENCLAW_SAGE_OUTPUT=json`).
**Source:** reads from `docs.json` in the GitHub repo (or local clone per `OPENCLAW_SAGE_SOURCE`).

**JSON output:**
```json
[
  {"category": "gateway", "paths": ["gateway/configuration", "gateway/security", ...]},
  ...
]
```
**Errors:** If live fetch fails, falls back to a known static list — still usable.

---

### `./scripts/fetch-doc.sh <path> [--toc] [--section <heading>] [--max-lines <n>]`
**Purpose:** Fetch and display a specific documentation page as readable text.
**When to use:** When you know the doc path and need its content. This is the primary way to answer specific questions.
**Input:** Doc path (e.g. `gateway/configuration`, `providers/discord`). No leading slash needed.
**Note:** Accepts `--version <tag>` to target a specific cached version.

**Flags:**
- `--toc` — list headings only (no body). Use first to find the right section name.
- `--section <heading>` — extract just the named section and its content. Case-insensitive partial match.
- `--max-lines <n>` — truncate output to N lines. Useful when the full doc is too large.

**Recommended agent workflow for long docs:**
```
fetch-doc.sh gateway/configuration --toc          # see sections
fetch-doc.sh gateway/configuration --section retry # fetch only that section
```

**Output:** Full text, TOC, section text, or truncated text depending on flags.
**Errors:**
- Empty/failed response: the path may be wrong. Run `sitemap.sh` to check available paths.
- `--toc` / `--section` not found: lists available headings on stderr.
- Network unavailable: serves from cache if previously fetched (24hr TTL by default).

---

### `./scripts/info.sh <path> [--json]`
**Purpose:** Return lightweight metadata for a cached doc without loading its full content.
**When to use:** Before fetching a long doc, to confirm it's relevant and estimate token cost from word count and headings.
**Input:** Doc path. The doc must already be cached — run `fetch-doc.sh <path>` first.
**Note:** Accepts `--version <tag>` to target a specific cached version.

**Output (human):**
```
title:     Gateway Configuration | OpenClaw Docs
headings:  Overview, Authentication, Retry Settings, Logging, Examples
words:     1,840
cached_at: 2026-03-06 14:22 (fresh)
url:       https://docs.openclaw.ai/gateway/configuration
```

**JSON output:**
```json
{
  "path": "gateway/configuration",
  "url": "https://docs.openclaw.ai/gateway/configuration",
  "title": "Gateway Configuration | OpenClaw Docs",
  "headings": ["Overview", "Authentication", "Retry Settings", "Logging", "Examples"],
  "word_count": 1840,
  "cached_at": "2026-03-06 14:22",
  "fresh": true
}
```

**Errors:**
- `not_cached` (exit 1): doc hasn't been fetched yet. Run `fetch-doc.sh <path>` first.
- Title/headings missing on first call for docs cached before v0.2.0 — `info.sh` backfills the HTML automatically on that first call.

---

### `./scripts/search.sh [--json] [--max-results <n>] <keyword...>`
**Purpose:** Search cached docs and sitemap paths by keyword.
**When to use:** When you're unsure which doc to fetch, or the user's question spans multiple topics.
**Input:** One or more keywords — quotes are never required (`search.sh webhook retry` works). Add `--json` for machine-readable output. Use `--max-results <n>` to cap the number of matching docs returned (default `10`).
**Notes:** This is the discovery-first search command. It uses BM25 when an index exists, but can fall back to cached-doc grep and sitemap path matches when a full index is unavailable.
**Note:** Accepts `--version <tag>` to target a specific cached version.

**Human output (unified format):**
```
  [score] path  ->  https://docs.openclaw.ai/path
          excerpt matching the query
```
- If BM25 index is built: results are **ranked by relevance** with float scores.
- If only cached docs exist: grep fallback, score shown as `[---]`.

**JSON output (`--json` or `OPENCLAW_SAGE_OUTPUT=json`):**
```json
{
  "query": "webhook retry",
  "mode": "bm25",
  "results": [
    {"score": 0.823, "path": "automation/webhook", "url": "https://...", "excerpt": "..."}
  ]
}
```

`mode` values: `"bm25"` · `"grep"` · `"no-cache"`
**Errors:** If no cache at all, prints instructions to fetch docs first.

---

### `./scripts/build-index.sh fetch`
**Purpose:** Download all docs to local cache (both `.md` and `.txt`).
**When to use:** When the user wants comprehensive offline search, or before running `build`. After fetching, `--toc`, `--section`, and `info.sh` all work offline without a second network request.
**Output:** One `[done] <path>` line per fetched doc, then total docs cached.
**Notes:** Fetching runs in parallel by default when `xargs` is available. Tune worker count with `OPENCLAW_SAGE_FETCH_JOBS` (default `8`; set to `1` for sequential fetching). If `xargs` is unavailable, the script falls back to sequential fetching automatically.
**Version:** Add `--version <tag>` to fetch docs at a specific OpenClaw release (e.g. `./scripts/build-index.sh fetch --version v2026.4.22`). Default fetches from `main`.
**Errors:** Exits immediately with a clear message if the host is unreachable (no timeout wait).

### `./scripts/build-index.sh build`
**Purpose:** Build a full-text BM25 search index from cached docs.
**When to use:** After `fetch`, to enable ranked search. Re-running `build` incrementally refreshes the index by reprocessing only docs newer than `index.txt` and removing entries for docs that no longer exist in cache.
**Output:** Confirmation with doc count and index location. Also writes `index_meta.json`.

### `./scripts/build-index.sh search [--max-results <n>] <query>`
**Purpose:** BM25-ranked full-text search over the complete doc corpus.
**When to use:** When `search.sh` results are insufficient and the index is built.
**Input:** Query string (multi-word queries supported). Use `--max-results <n>` to cap the number of ranked results returned (default `10`).
**Notes:** This is the index-only search path. It requires `index.txt` and does not fall back to cached-doc grep or sitemap matches.
**Output:**
``` 
  [0.823] gateway/configuration  ->  https://docs.openclaw.ai/gateway/configuration
          Configure retry settings with maxAttempts...
```
**Errors:** If no index, prints fetch/build instructions.

### `./scripts/build-index.sh status`
**Purpose:** Show how many docs are cached, whether the index is built, and BM25 meta status.

---

### `./scripts/cache.sh status`
**Purpose:** Show cache health, location, and active TTL values. Lists all cached versions with doc counts and index status.
**Output includes:** TTL values and the env vars that override them.

### `./scripts/cache.sh refresh`
**Purpose:** Clear stale sitemap cache to force a re-fetch on next call.

### `./scripts/cache.sh clear-docs`
**Purpose:** Delete all cached doc files and the search index.

### `./scripts/cache.sh tags`
**Purpose:** List available OpenClaw release tags from GitHub. Use to discover which `--version` values can be fetched.
**Notes:** GitHub source mode only. Local source mode prints an informational message.

---

### `./scripts/recent.sh [days]`
**Purpose:** Show docs updated recently.
**Input:** Number of days — must be a positive integer (default: 7). Non-numeric values exit 1 with a usage message.
**Note:** Accepts `--version <tag>` to target a specific cached version.
**Output:**
- `=== Docs updated at source in the last N days ===` — from sitemap `lastmod` dates
- `=== Recently accessed locally (last N days) ===` — by local file mtime
**Errors:** If sitemap lacks `lastmod` dates, reports that explicitly.

---

### `./scripts/track-changes.sh snapshot`
**Purpose:** Save a snapshot of the current doc list for future comparison.

### `./scripts/track-changes.sh list`
**Purpose:** List all saved snapshots with timestamps and page counts.

### `./scripts/track-changes.sh since <date>`
**Purpose:** Show docs added/removed since a given date (e.g. `2026-01-01`).
**Output:** `=== Added ===` and `=== Removed ===` sections.

### `./scripts/track-changes.sh diff <snap1> <snap2>`
**Purpose:** Compare two specific snapshots directly.
**Input:** Snapshot name (from `list`) or absolute path to a snapshot file. Absolute paths allow cross-version comparison — e.g. comparing a snapshot from `v2026.4.9` against one from `v2026.4.22`.

---

## Decision Rules

**"How do I set up [provider]?"**
→ `./scripts/fetch-doc.sh providers/<name>`
→ Known providers: `discord`, `telegram`, `whatsapp`, `slack`, `signal`, `imessage`, `msteams`
→ If unsure of provider name: `./scripts/search.sh <provider>`

**"First time / getting started"**
→ `./scripts/fetch-doc.sh start/getting-started`
→ Then `start/setup` if more detail needed

**"Why isn't X working?" / troubleshooting**
→ `./scripts/fetch-doc.sh gateway/troubleshooting` for general issues
→ `./scripts/fetch-doc.sh providers/troubleshooting` for provider issues
→ `./scripts/fetch-doc.sh tools/browser-linux-troubleshooting` for browser tool issues

**"How do I configure X?"**
→ `./scripts/fetch-doc.sh gateway/configuration` for main config
→ `./scripts/fetch-doc.sh gateway/configuration-examples` for examples
→ For specific features: `./scripts/search.sh <feature>` to find the right page

**"What is X?" / concepts**
→ `./scripts/fetch-doc.sh concepts/<topic>`
→ Topics: `agent`, `sessions`, `messages`, `models`, `queues`, `streaming`, `system-prompt`

**"How do I automate X?"**
→ `./scripts/fetch-doc.sh automation/cron-jobs` for scheduled tasks
→ `./scripts/fetch-doc.sh automation/webhook` for webhooks
→ `./scripts/fetch-doc.sh automation/gmail-pubsub` for Gmail

**"How do I install / deploy?"**
→ Docker: `./scripts/fetch-doc.sh install/docker`
→ Linux server: `./scripts/fetch-doc.sh platforms/linux`
→ macOS: `./scripts/fetch-doc.sh platforms/macos`

**"What's new?" / "What changed?"**
→ `./scripts/recent.sh 7`

**Unsure which doc to use**
→ `./scripts/search.sh <keyword>` first, then fetch the top result

**fetch-doc.sh returns empty or fails**
→ Try `./scripts/search.sh <topic>` to find related docs
→ Tell the user the doc may not exist and offer the sitemap

---

## Workflow

1. **Identify the need** using Decision Rules above.
2. **Fetch the doc** with `fetch-doc.sh <path>` — most questions are answered this way.
3. **Search** with `search.sh <keyword>` when unsure of the path.
4. **Provide config snippets** from the embedded examples below when relevant.
5. **Cite the URL**: `https://docs.openclaw.ai/<path>`

---

## Config Snippets

### Discord (basic)
```json
{
  "discord": {
    "token": "${DISCORD_TOKEN}",
    "guilds": { "*": { "requireMention": false } }
  }
}
```

### Discord (mention-only)
```json
{
  "discord": {
    "token": "${DISCORD_TOKEN}",
    "guilds": { "*": { "requireMention": true } }
  }
}
```

### Telegram
```json
{ "telegram": { "token": "${TELEGRAM_TOKEN}" } }
```

### WhatsApp
```json
{ "whatsapp": { "sessionPath": "./whatsapp-sessions" } }
```

### Slack
```json
{
  "slack": {
    "token": "${SLACK_BOT_TOKEN}",
    "appToken": "${SLACK_APP_TOKEN}"
  }
}
```

### Signal
```json
{ "signal": { "phoneNumber": "${SIGNAL_PHONE_NUMBER}" } }
```

### iMessage
```json
{ "imessage": { "handle": "${IMESSAGE_HANDLE}" } }
```

### MS Teams
```json
{
  "msteams": {
    "appId": "${MSTEAMS_APP_ID}",
    "appPassword": "${MSTEAMS_APP_PASSWORD}"
  }
}
```

### Gateway
```json
{ "gateway": { "host": "0.0.0.0", "port": 8080 } }
```

### Agent model
```json
{ "agents": { "defaults": { "model": "anthropic/claude-sonnet-4-6" } } }
```

### Retry settings
```json
{
  "agents": {
    "defaults": { "retry": { "maxAttempts": 3, "delay": 1000 } }
  }
}
```

### Cron job
```json
{
  "cron": [{ "id": "daily-summary", "schedule": "0 9 * * *", "task": "summary" }]
}
```

### Skills / Tools
```json
{ "agents": { "defaults": { "skills": ["bash", "browser"] } } }
```

---

## Error Handling

| Situation | Action |
|---|---|
| `fetch-doc.sh` returns empty | Run `search.sh <topic>` to find related pages; tell user the path may be wrong |
| `search.sh` finds nothing | Run `sitemap.sh` and look for related paths; suggest `build-index.sh fetch && build` |
| Network unavailable | Scripts detect this upfront (2s check) and immediately print `Offline: cannot reach …`. Fetch scripts fall back to cached content; operations that require live data (`build-index.sh fetch`, `track-changes.sh snapshot/since`) exit cleanly. Tell user results may be stale. |
| `recent.sh` shows no lastmod dates | Inform user the sitemap may not include dates; suggest `track-changes.sh` for change tracking |
| Index not built | Offer to guide user through `build-index.sh fetch && build-index.sh build` |

---

## Cache & Config

Default TTLs (overridable via env vars):
- Doc pages: `OPENCLAW_SAGE_DOC_TTL` (default 86400s / 24hr)
- Cache dir: `OPENCLAW_SAGE_CACHE_DIR` (default `<skill_root>/.cache/openclaw-sage`)
- Languages: `OPENCLAW_SAGE_LANGS` (default `en`; use `en,zh` for multiple, `all` for everything)
- Source: `OPENCLAW_SAGE_SOURCE` (default `github`; use `local:/path/to/openclaw/docs` for a local repo clone)

Example override:
```bash
OPENCLAW_SAGE_DOC_TTL=60 ./scripts/fetch-doc.sh gateway/configuration
```
