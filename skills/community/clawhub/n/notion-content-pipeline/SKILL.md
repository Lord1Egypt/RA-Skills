---
name: notion-content-pipeline
version: 1.0.3
metadata:
  {
    "openclaw": {
      "emoji": "📝",
      "requires": { "bins": ["python3"], "env": ["NOTION_API_KEY"] },
      "network": { "outbound": true, "reason": "Syncs markdown content to/from Notion API. No other external calls." }
    }
  }
description: "Two-way markdown ↔ Notion sync for blog and content workflows. Use when: pushing local .md files to Notion for editing, pulling Notion edits back to local files, managing a content pipeline database with statuses (Seed → Draft → Review → Published), or tracking local file ↔ Notion page mappings. Supports batch push-all, per-file push/pull, and pipeline DB creation with Platform/Status/Hook properties."
---
**Last used:** 2026-03-24
**Memory references:** 2
**Status:** Active


# notion-content-pipeline

Push local `.md` files to Notion and pull edits back. Track a content pipeline DB with
statuses (Seed → Draft → Review → Published).

---

## Key Database IDs

| Database | ID |
|---|---|
| **Content Pipeline DB** (blog posts, n8n trigger) | `322eb552-581a-8111-8f6a-d042dd048ec8` |
| **Tweet Pipeline DB** (cron trigger) | `314c9a82-0734-81be-ac58-ddd878576cf0` |

Use the Content Pipeline DB ID when pushing blog posts via the blog-to-social pipeline (status: In Review → Approved).

---

## When to Use This / When NOT to Use This

**Use this skill when:**
- Pushing a local `.md` draft to Notion for Nissan to review/edit in Notion UI
- Pulling Nissan's Notion edits back to a local file
- Advancing a post through the content pipeline (Draft → Humanized → In Review)
- Creating or querying the Content Pipeline tracking database

**Do NOT use this skill when:**
- Writing a quick one-off note to Notion — use the Notion API directly with a simple `curl`
- Reading from arbitrary Notion databases (this skill is scoped to the content pipeline DB and markdown sync)
- Posting to LinkedIn/Twitter — that's the `buffer-publisher` skill
- The post hasn't been written yet — draft first, then push

**Boundary with direct Notion API calls:**
This skill wraps the Notion API with markdown conversion and sync-map tracking. Use it when you need the full sync workflow. For raw Notion API queries (e.g., fetching a database row, reading a page property), calling the API directly with `curl` or `httpx` is simpler and doesn't need this skill.

---

## ⚠️ Credentials — Critical

```bash
# CORRECT — use this 1Password item:
NOTION_API_KEY=$(op read "op://OpenClaw/bg2gpqhpta6an5n4prn2zzycya/credential")

# DO NOT use the old item (dead as of early 2026):
# op://OpenClaw/Notion API Key/credential  ← this vault item is stale/deleted
```

API version header required: `Notion-Version: 2022-06-28`

---

## Scripts

- `scripts/notion_content_sync.py` — push/pull individual files or all at once
- `scripts/create_pipeline_db.py` — create a Notion database for content pipeline tracking
- `scripts/pipeline_advance.py` — **full round-trip advance**: pull → humanize → fact-check → push → status update

## Configuration

```bash
NOTION_API_KEY=secret_...        # Notion integration token (from 1Password item above)
NOTION_PARENT_PAGE_ID=<uuid>     # Parent page ID for sandbox + pipeline DB
NOTION_SYNC_MAP=~/.notion_sync_map.json  # Where to store file ↔ page ID mapping
CONTENT_DIR=./content            # Directory containing .md files
```

Or pass `--sandbox-id` and `--sync-map` as CLI flags.

## Quick Start

```bash
# Push a single file to Notion
python3 scripts/notion_content_sync.py push content/my-post.md

# Push all .md files in content/
python3 scripts/notion_content_sync.py push-all

# Pull Notion edits back to local file
python3 scripts/notion_content_sync.py pull content/my-post.md

# List all tracked pages with Notion URLs
python3 scripts/notion_content_sync.py list

# Create the Content Pipeline database
python3 scripts/create_pipeline_db.py
```

---

## What a Successful Push Looks Like

```
Pushing content/my-post.md → Notion...
✅ Created page: "My Post Title"
   Notion URL: https://www.notion.so/My-Post-Title-abc123def456...
   Page ID: abc123de-f456-7890-abcd-ef1234567890
   Sync map updated: content/my-post.md → abc123de-f456-7890-abcd-ef1234567890
```

If you see `✅ Created page` with a Notion URL and the sync map updates, the push succeeded.

**Overwrite (push to existing page):**
```
Pushing content/my-post.md → Notion...
Archiving existing page abc123de-... (overwrite mode)
✅ Created page: "My Post Title" (fresh)
   Notion URL: https://www.notion.so/My-Post-Title-xyz789...
```

**Failure indicators:**
- `401 Unauthorized` → API key wrong or expired — check the 1Password item
- `404 Not Found` on parent page → `NOTION_PARENT_PAGE_ID` is wrong or the page was deleted
- `400 Bad Request` with block validation error → likely a markdown parsing issue (see Known Bug below)

---

## Sync Map

File ↔ Notion page ID mapping stored in JSON. Example:
```json
{
  "content/my-post.md": "abc123-...",
  "content/other-post.md": "def456-..."
}
```

Default location: `./notion_sync_map.json` (override with `NOTION_SYNC_MAP` env var).

## Overwrite Behaviour

On `push`, if the file is already tracked, the existing Notion page is archived and
a fresh page is created. This avoids block-count drift from repeated pushes.

Use `--no-overwrite` to skip if already pushed.

---

## Known Bug: Annotation Parser (Fixed 2026-03-20)

**Bug:** The markdown→Notion block converter incorrectly parsed inline annotations (bold, italic, code spans) when they appeared at the start of a paragraph. This caused a `400 Bad Request` from the Notion API with an error like `"annotations object is invalid"`.

**Fix applied 2026-03-20:** The annotation parser now correctly handles leading annotations by initialising the text accumulator before the first annotation span, not after.

**If you see annotation-related 400 errors:** Pull the latest version of `scripts/notion_content_sync.py`. If the error persists, check whether the markdown contains unusual Unicode or nested emphasis (`**_bold italic_**`) which may still trip the parser.

---

## Pipeline DB Schema

Created by `create_pipeline_db.py`:
- **Title** — post title
- **Slug** ⚠️ — URL slug used by n8n to publish to reddi.tech (e.g. `my-openclaw-chronicles-statistical-proof`). **MANDATORY** — n8n reads `props.Slug?.rich_text` and sends it to the publish API. If empty, n8n silently skips the page even when Status = Approved ✅.
- **Platform** — Blog / LinkedIn / Both
- **Status** — Seed → Draft → Humanized → In Review → Approved ✅ → In Publishing 🚀 → Published
- **Hook** — one-sentence pitch
- **Est. Read Time** — < 1 min / 2-3 min / 5-7 min / 10+ min
- **Published URL** — final URL once live (set by n8n after successful publish)
- **PR URL** — GitHub PR URL (set by n8n)
- **Source** — where the idea came from

### ⚠️ Slug field — how to set it

When pushing a blog post to the Content Pipeline DB, always set the Slug property:

```python
"Slug": {"rich_text": [{"type": "text", "text": {"content": slug}}]}
```

Slug format rules:
- Lowercase, hyphens only (no underscores, no spaces)
- Derived from the post title: strip punctuation, replace spaces with hyphens
- Must be unique across all blog posts
- n8n uses this to: (1) build the reddi.tech URL, (2) name the MDX file in the repo, (3) create the GitHub PR

**Lesson learned 2026-03-28:** The Slug property was missing from the DB schema entirely. n8n ran every 15 minutes, found the Approved page, extracted an empty slug string, and silently skipped publishing. Added Slug as a required field to the DB schema and set it on the page to unblock publishing.

---

## pipeline_advance.py — Automated Round-Trip

```bash
# Full advance: pull → humanize → fact-check → push → status
python3 scripts/pipeline_advance.py advance content/my-post.md

# Skip steps individually
python3 scripts/pipeline_advance.py advance content/my-post.md --skip-humanize
python3 scripts/pipeline_advance.py advance content/my-post.md --skip-factcheck

# Preview without making changes
python3 scripts/pipeline_advance.py advance content/my-post.md --dry-run
```

### What it does

1. **Pulls** Notion edits back to your local `.md` file
2. **Humanizes** — applies mechanical AI-pattern fixes in Python (em dash → comma,
   "utilize" → "use", filler openers, copula avoidance, curly quotes). Flags
   rule-of-three and AI-vocab patterns for LLM review. Writes a `.humanizer.diff`
   alongside the file.
3. **Fact-checks** — runs `skills/fact-checker/scripts/fact_check.py` if available;
   otherwise skips gracefully. Report saved as `.factcheck.txt`.
4. **Pushes** the humanized file back to Notion (archives old page, creates fresh one).
5. **Updates status** in the Content Pipeline DB:
   - `Draft` → `Humanized` (after humanize + fact-check)
   - `Humanized` → `In Review` (after fact-check only)
   - Never advances past `In Review` — that's Nissan's decision.

### Extra Env Var

```bash
NOTION_PIPELINE_DB_ID=322eb552-581a-8111-8f6a-d042dd048ec8  # optional, hardcoded fallback
```

---

## Common Mistakes

1. **Using the wrong 1Password item for the API key**
   - ❌ `op://OpenClaw/Notion API Key/credential` → dead item, returns empty or wrong credential
   - ✅ `op://OpenClaw/bg2gpqhpta6an5n4prn2zzycya/credential`

2. **Missing `Notion-Version` header**
   - The Notion API requires `Notion-Version: 2022-06-28` on all requests
   - Scripts include this, but if you're making raw API calls, don't omit it

3. **Parent page not shared with the integration**
   - If you get 404 on push, check that the Notion integration has access to the parent page
   - In Notion: open the parent page → Connections → add your integration

4. **Pushing without pulling first (when round-tripping)**
   - If Nissan edited in Notion and you push without pulling first, you'll overwrite their edits
   - Always `pull` before `push` if the page may have been edited in Notion

5. **Sync map out of date after manual Notion changes**
   - If a Notion page was manually deleted, the sync map still references its old ID
   - The next push will fail with 404, then auto-create a new page and update the map
   - This is handled gracefully — don't manually edit the sync map JSON

6. **Annotation parser 400 errors on old script versions**
   - See Known Bug section above — ensure `notion_content_sync.py` is post-2026-03-20

7. **Missing Slug field → n8n silently skips Approved pages** (2026-03-28)
   - n8n reads `props.Slug?.rich_text` — if the field doesn't exist on the DB or the page, it gets an empty string and skips publishing without error
   - Always set `Slug` when creating a page in the Content Pipeline DB
   - If a page is stuck at Approved ✅ and n8n isn't picking it up, check the Slug field first

---

## See Also

- `references/api_notes.md` — Notion API quirks and block type reference
