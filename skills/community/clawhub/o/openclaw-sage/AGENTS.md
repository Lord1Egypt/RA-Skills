# AGENTS.md — Quick Reference for AI Agents

This is a condensed reference for AI agents using the openclaw-sage skill. For full tool documentation see [`SKILL.md`](SKILL.md).

---

## What This Skill Does

Gives you access to OpenClaw documentation via shell scripts. Docs are fetched from the [OpenClaw GitHub repo](https://github.com/openclaw/openclaw) as Markdown, cached locally, and searchable with BM25 ranking. You can query docs at any OpenClaw release tag with `--version`.

---

## Decision Tree

| User asks about... | First call |
|---|---|
| Setup / getting started | `fetch-doc.sh start/getting-started` |
| A specific provider (Discord, Telegram, etc.) | `fetch-doc.sh providers/<name>` |
| Configuration | `fetch-doc.sh gateway/configuration --toc` → then `--section` |
| Troubleshooting | `fetch-doc.sh gateway/troubleshooting` |
| A concept (sessions, models, queues...) | `fetch-doc.sh concepts/<topic>` |
| Automation / cron / webhooks | `fetch-doc.sh automation/<topic>` |
| Installation / deployment | `fetch-doc.sh install/docker` or `platforms/<os>` |
| What's new / recent changes | `cache.sh tags` → fetch a version and compare |
| Unsure which doc to use | `search.sh <keyword>` |
| Doc cached, want to check relevance before reading | `info.sh <path>` |
| Docs for a specific OpenClaw release | `build-index.sh fetch --version v2026.4.22` |

---

## Tool Chaining Patterns

### Check before you fetch
```bash
./scripts/info.sh gateway/configuration          # 1. Check word count + headings
./scripts/fetch-doc.sh gateway/configuration --section retry  # 2. Fetch only what you need
```

### Long doc — read only what you need
```bash
./scripts/fetch-doc.sh gateway/configuration --toc              # 1. See sections
./scripts/fetch-doc.sh gateway/configuration --section retry    # 2. Fetch that section
```

### Discovery → fetch
```bash
./scripts/search.sh --json webhook retry     # 1. Find relevant docs (quotes optional)
./scripts/fetch-doc.sh automation/webhook    # 2. Fetch the top result
```

### Unknown path
```bash
./scripts/sitemap.sh --json   # list all paths by category, then fetch
```

### Compare docs across two OpenClaw releases
```bash
./scripts/cache.sh tags                                              # 1. See available tags
./scripts/build-index.sh fetch --version v2026.4.9                  # 2. Fetch old version
./scripts/build-index.sh fetch --version v2026.4.22                 # 3. Fetch new version
diff <(./scripts/fetch-doc.sh --version v2026.4.9 gateway/configuration) \
     <(./scripts/fetch-doc.sh --version v2026.4.22 gateway/configuration)  # 4. Diff
```

---

## Tool Reference

```bash
# Sitemap
./scripts/sitemap.sh                          # all doc paths, grouped by category
./scripts/sitemap.sh --json                   # [{category, paths[]}]
./scripts/sitemap.sh --version v2026.4.9      # paths at a specific release

# Doc metadata (cache only — does not fetch)
./scripts/info.sh <path>                      # title, headings, word count, cache age
./scripts/info.sh <path> --json               # {path, url, title, headings[], word_count, cached_at, fresh}
./scripts/info.sh --version v2026.4.9 <path>  # metadata for a specific version

# Fetch a doc
./scripts/fetch-doc.sh <path>                       # full plain text
./scripts/fetch-doc.sh <path> --toc                 # headings only
./scripts/fetch-doc.sh <path> --section <heading>   # one section (partial, case-insensitive)
./scripts/fetch-doc.sh <path> --max-lines 80        # truncated
./scripts/fetch-doc.sh --version v2026.4.9 <path>   # doc at a specific release

# Search — multi-word queries work without quotes
./scripts/search.sh webhook retry                   # BM25 ranked if index built, grep fallback otherwise
./scripts/search.sh --json webhook retry            # {query, mode, results[]}
./scripts/search.sh --version v2026.4.9 webhook     # search a specific version's index

# Full index (run once, then use build-index.sh search for best results)
./scripts/build-index.sh fetch                      # download all docs (latest)
./scripts/build-index.sh fetch --version v2026.4.22 # download docs at a specific tag
./scripts/build-index.sh build                      # build BM25 index
./scripts/build-index.sh build --version v2026.4.22 # build index for a specific version
./scripts/build-index.sh search webhook retry       # multi-word, no quotes needed

# Cache management
./scripts/cache.sh status                    # list all cached versions, doc counts, index status
./scripts/cache.sh tags                      # list available OpenClaw release tags from GitHub
./scripts/cache.sh refresh                   # clear docs.json cache to force re-fetch
./scripts/cache.sh clear-docs               # remove all cached docs and index for active version

# What's recently accessed locally
./scripts/recent.sh 7                        # docs accessed locally in last 7 days
./scripts/recent.sh --version v2026.4.9 7   # for a specific cached version
```

---

## JSON Output

Set `OPENCLAW_SAGE_OUTPUT=json` globally, or pass `--json` per call.

**`search.sh --json` response:**
```json
{
  "query": "webhook retry",
  "mode": "bm25",
  "results": [
    {
      "score": 0.823,
      "path": "automation/webhook",
      "url": "https://docs.openclaw.ai/automation/webhook",
      "excerpt": "Configure retry with maxAttempts..."
    }
  ]
}
```

`mode` values: `"bm25"` (ranked, index built) · `"grep"` (unranked, no index) · `"no-cache"` (nothing cached yet)

**`info.sh --json` response:**
```json
{
  "path": "gateway/configuration",
  "url": "https://docs.openclaw.ai/gateway/configuration",
  "title": "Configuration",
  "headings": ["Overview", "Authentication", "Retry Settings"],
  "word_count": 1840,
  "cached_at": "2026-04-24 10:22",
  "fresh": true
}
```
Error (not cached): `{"error": "not_cached", "path": "...", "url": "..."}` with exit 1.

**`sitemap.sh --json` response:**
```json
[
  { "category": "gateway", "paths": ["gateway/configuration", "gateway/security"] },
  { "category": "providers", "paths": ["providers/discord", "providers/telegram"] }
]
```

---

## Error Recovery

| Error | Recovery |
|---|---|
| `fetch-doc.sh` returns empty or fails | Run `search.sh <topic>` to find the right path; check `sitemap.sh` |
| `--section` not found | Error message lists available sections — retry with correct name |
| `search.sh` returns no results | Run `build-index.sh fetch && build-index.sh build` for full coverage |
| Network unavailable | Scripts serve cached content automatically; results may be stale |
| No `.md` cache for `--toc`/`--section` | Run `fetch-doc.sh <path>` first (without flags) to populate the cache |

---

## Source URL

Always cite the source when answering: `https://docs.openclaw.ai/<path>`
