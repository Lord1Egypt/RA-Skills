name: notion-pro
description: Complete Notion API skill with Python CLI tool — auto-pagination, recursive blocks, 429 retry, and agent operation strategies.
version: 1.0.1
homepage: https://github.com/baixiaodev/notion-pro-skill
metadata: {"clawdbot":{"emoji":"📝"}}
env:
  - NOTION_API_KEY: Notion integration API key (or configure in openclaw.json → skills.entries.notion-pro.apiKey)
---

# Notion Pro — Complete Notion API Skill for OpenClaw

A production-grade Notion API skill with a built-in Python CLI tool. Unlike basic Notion skills that only provide command syntax, this skill includes **agent operation strategies**, **automatic pagination**, **recursive block fetching**, **429 rate-limit retry**, and comprehensive API reference — everything an AI agent needs to operate Notion effectively.

## What Makes This Different

| Capability | This Skill | Basic Skills |
|---|---|---|
| Agent operation strategy (5-step workflow) | ✅ | ❌ |
| Recursive block fetching (`--recursive`, 5 levels) | ✅ | ❌ |
| Auto-pagination (`--all`) | ✅ | ❌ |
| 429 rate-limit auto-retry (Retry-After) | ✅ | ❌ |
| Positional insert (`--after`) | ✅ | ❌ |
| API limits quick reference | ✅ Complete | Partial |
| 4 operation pattern SOPs | ✅ | ❌ |
| Zero dependencies (stdlib only) | ✅ Python 3 | Node.js / curl |

## Setup

1. Create a [Notion Integration](https://www.notion.so/profile/integrations) and copy the API key
2. Configure the key via **one** of:
   - Environment variable: `export NOTION_API_KEY="ntn_xxxxx"`
   - OpenClaw config: `openclaw.json` → `skills.entries.notion-pro.apiKey`
3. Share target pages/databases with your integration (click "..." → "Connect to" → your integration name)
4. If a page/database isn't found via search, it likely hasn't been shared with the integration yet

## Tool: notion_api.py

**All Notion operations must go through this script** — do not use curl directly.

Script path: `scripts/notion_api.py` (relative to this skill's directory)

```bash
# The script auto-detects its own location. Usage:
python3 <SKILL_DIR>/scripts/notion_api.py <command> [options]
```

---

## Agent Operation Strategy (Must Read)

### Task Planning Workflow

Follow this sequence for any Notion task:

1. **Discover** — Use `search` to find the target page/database ID
2. **Inspect** — Use `get-page` or `get-blocks` to understand current structure
3. **Plan** — Determine the operation sequence (create/update/append/delete)
4. **Execute** — Execute in batches, ≤50 blocks per batch (safety margin)
5. **Verify** — After critical operations, use `get-blocks` to verify results

### Read Strategy

- **Search before read**: Never guess IDs — use `search` to find the exact page/database
- **Recursively read nested content**: `get-blocks` only returns direct children. If a block has `has_children: true`, **you must call `get-blocks` again with that block's ID** to get nested content. Or use `--recursive` for automatic traversal.
- **Handle pagination**: If response contains `has_more: true`, make multiple calls. Use `--all` for automatic pagination.

### Write Strategy

- **Split long text**: A single rich_text element's `text.content` is limited to **2000 characters**. Split longer content into multiple paragraph blocks.
- **Batch writes**: One `append-blocks` call supports up to **100 block elements**. Split into multiple calls if needed.
- **Replace = Delete + Append**: Notion API has **no** "replace block content" endpoint. To replace content: `delete-block` old blocks, then `append-blocks` new content at the correct position.
- **Insert position**: `append-blocks` appends to the end by default. To insert at a specific position, use `--after` with the preceding block's ID.

### Database Write Strategy

- **Schema-First**: Before creating a page, use `get-page` or `query-database` to inspect the database's property schema. Ensure your properties JSON matches.
- **Title is required**: Every database has exactly one `title` property — it must be provided when creating a page.
- **Exact property names**: Property names are case-sensitive and space-sensitive.

---

## API Limits Quick Reference

| Limit | Value |
|---|---|
| Rate limit | **3 requests/sec** (average), returns 429 when exceeded |
| Max request payload | **500 KB** |
| Max blocks per payload | **1000 blocks** |
| Max array elements (blocks/rich_text) | **100** |
| rich_text `text.content` | **2000 characters** |
| rich_text `text.link.url` | **2000 characters** |
| URL property | **2000 characters** |
| multi_select options | **100** |
| relation linked pages | **100** |
| Database schema recommended size | **≤ 50 KB** |
| Pagination default/max page_size | **100** |

**429 handling**: When rate-limited, the script automatically reads the `Retry-After` header and retries (up to 3 times). For manual batch operations, add 300–500ms between calls.

---

## Command Reference

### Search

```bash
python3 scripts/notion_api.py search --query "keyword"
python3 scripts/notion_api.py search --query "keyword" --filter page
python3 scripts/notion_api.py search --query "keyword" --filter database --page-size 20

# Pagination (use next_cursor from previous response)
python3 scripts/notion_api.py search --query "keyword" --start-cursor "xxx"

# Auto-fetch all results (auto-paginates, may take time for large datasets)
python3 scripts/notion_api.py search --query "keyword" --all
```

### Read Page

```bash
# Get page metadata (properties, parent, URL, etc.)
python3 scripts/notion_api.py get-page --page-id "xxx-xxx"

# Get page content (blocks) — check has_children for recursive fetching
python3 scripts/notion_api.py get-blocks --block-id "xxx-xxx"

# Recursively fetch full page (auto-expands all nested blocks, max depth 5)
python3 scripts/notion_api.py get-blocks --block-id "xxx-xxx" --recursive

# Pagination
python3 scripts/notion_api.py get-blocks --block-id "xxx-xxx" --start-cursor "xxx"
```

### Query Database

```bash
# Get all rows
python3 scripts/notion_api.py query-database --database-id "xxx"

# With filter
python3 scripts/notion_api.py query-database \
  --database-id "xxx" \
  --filter '{"property": "Status", "select": {"equals": "Active"}}'

# With sort
python3 scripts/notion_api.py query-database \
  --database-id "xxx" \
  --sorts '[{"property": "Date", "direction": "descending"}]'

# Compound filter (AND/OR)
python3 scripts/notion_api.py query-database \
  --database-id "xxx" \
  --filter '{"and": [{"property": "Status", "select": {"equals": "Active"}}, {"property": "Priority", "select": {"equals": "High"}}]}'

# Pagination
python3 scripts/notion_api.py query-database --database-id "xxx" --start-cursor "xxx"

# Auto-fetch all results
python3 scripts/notion_api.py query-database --database-id "xxx" --all
```

### Create Page

```bash
# Create in database (properties must match schema)
python3 scripts/notion_api.py create-page \
  --parent-id "database_id" \
  --parent-type database \
  --properties '{"Name": {"title": [{"text": {"content": "New Entry"}}]}}'

# Create sub-page with content
python3 scripts/notion_api.py create-page \
  --parent-id "page_id" \
  --parent-type page \
  --properties '{"title": {"title": [{"text": {"content": "Sub-page Title"}}]}}' \
  --children '[{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello World"}}]}}]'
```

### Update Page Properties

```bash
python3 scripts/notion_api.py update-page \
  --page-id "xxx" \
  --properties '{"Status": {"select": {"name": "Done"}}}'
```

### Append Blocks

```bash
# Append to end (default)
python3 scripts/notion_api.py append-blocks \
  --block-id "page_id" \
  --children '[{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Title"}}]}}, {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Body text"}}]}}]'

# Insert after a specific block
python3 scripts/notion_api.py append-blocks \
  --block-id "page_id" \
  --after "target_block_id" \
  --children '[{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Inserted here"}}]}}]'
```

### Delete Block

```bash
python3 scripts/notion_api.py delete-block --block-id "block_id"
```

---

## Block Type Reference

### Common Blocks (Creatable)

```json
// Paragraph
{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Text"}}]}}

// Headings
{"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "H1"}}]}}
{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "H2"}}]}}
{"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "H3"}}]}}

// Toggleable heading (click to expand/collapse children)
{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Title"}}], "is_toggleable": true}}

// Lists
{"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Item"}}]}}
{"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"text": {"content": "Item"}}]}}

// To-do
{"object": "block", "type": "to_do", "to_do": {"rich_text": [{"text": {"content": "Task"}}], "checked": false}}

// Quote
{"object": "block", "type": "quote", "quote": {"rich_text": [{"text": {"content": "Quote text"}}]}}

// Callout
{"object": "block", "type": "callout", "callout": {"rich_text": [{"text": {"content": "Important note"}}], "icon": {"type": "emoji", "emoji": "⚠️"}}}

// Code
{"object": "block", "type": "code", "code": {"rich_text": [{"text": {"content": "print('hello')"}}], "language": "python"}}

// Divider
{"object": "block", "type": "divider", "divider": {}}

// Toggle
{"object": "block", "type": "toggle", "toggle": {"rich_text": [{"text": {"content": "Expandable"}}]}}

// Bookmark
{"object": "block", "type": "bookmark", "bookmark": {"url": "https://example.com"}}

// Equation
{"object": "block", "type": "equation", "equation": {"expression": "E = mc^2"}}
```

### Block Types Supporting Nested Children

These block types can contain children (use `append-blocks` to add child content):
- paragraph, bulleted_list_item, numbered_list_item, to_do
- quote, callout, toggle
- heading_1/2/3 (only when `is_toggleable: true`)
- column, synced_block, table

### Types Not Creatable/Modifiable via API

- `link_preview` — read-only
- `meeting_notes` / `transcription` — read-only
- `synced_block` — cannot update content
- `template` — creation deprecated
- `table.table_width` — immutable after creation

---

## Rich Text Advanced Formatting

```json
// Bold + Italic
{"text": {"content": "Emphasis"}, "annotations": {"bold": true, "italic": true}}

// Code style
{"text": {"content": "variable"}, "annotations": {"code": true}}

// With link
{"text": {"content": "Click here", "link": {"url": "https://example.com"}}}

// Color (text/background)
{"text": {"content": "Colored"}, "annotations": {"color": "red"}}
// Available colors: default, gray, brown, orange, yellow, green, blue, purple, pink, red
// Background: gray_background, brown_background, ..., red_background

// Mention page
{"type": "mention", "mention": {"type": "page", "page": {"id": "page-id"}}}

// Mention date
{"type": "mention", "mention": {"type": "date", "date": {"start": "2026-03-22"}}}
```

---

## Property Type Reference

```json
{"title": [{"text": {"content": "..."}}]}           // Title (required, one per database)
{"rich_text": [{"text": {"content": "..."}}]}        // Rich text
{"select": {"name": "Option"}}                        // Select
{"multi_select": [{"name": "A"}, {"name": "B"}]}     // Multi-select
{"date": {"start": "2026-01-15"}}                     // Date
{"date": {"start": "2026-01-15", "end": "2026-01-20"}} // Date range
{"checkbox": true}                                     // Checkbox
{"number": 42}                                         // Number
{"url": "https://..."}                                 // URL
{"email": "a@b.com"}                                   // Email
{"phone_number": "+1-555-xxxx"}                        // Phone
{"relation": [{"id": "page_id"}]}                     // Relation
{"status": {"name": "In Progress"}}                   // Status
{"people": [{"id": "user_id"}]}                       // People
```

**Read-only properties** (not writable via API): `formula`, `rollup`, `created_time`, `created_by`, `last_edited_time`, `last_edited_by`, `unique_id`

---

## Common Operation Patterns

### Pattern 1: Bulk Knowledge Base Population

Scenario: Batch-write entries to a Notion knowledge base (database)

```
1. search → find database ID
2. query-database → get schema and existing entries (avoid duplicates)
3. For each entry:
   a. create-page → create page (properties match schema)
   b. append-blocks → batch-append content (≤50 blocks per batch)
   c. sleep 300ms between batches to avoid 429
4. query-database to verify entry count
```

### Pattern 2: Page Content Update

Scenario: Replace or supplement parts of an existing page

```
1. get-blocks → read all current blocks and their IDs
2. Identify the block ID range to replace
3. delete-block → delete old blocks one by one
4. append-blocks → append new content at correct position
Note: There is no "replace block" API — only delete + append
```

### Pattern 3: Recursive Full-Page Read

Scenario: Retrieve complete page content including nested toggles/lists

```
# Recommended: one command to recursively expand (max depth 5)
get-blocks --block-id <page_id> --recursive

# Manual layer-by-layer (for specific subtrees only):
1. get-blocks --block-id <page_id> → get top-level blocks
2. For blocks with has_children: true:
   get-blocks --block-id <block_id> → get children
3. Recurse until all levels are read
Note: --recursive auto-handles pagination and rate limiting (350ms interval)
```

### Pattern 4: Conditional Query + Bulk Update

Scenario: Filter specific entries and batch-update their properties

```
1. query-database --filter '...' → get matching page IDs
2. For each page ID:
   update-page --page-id <id> --properties '{"Status": {"select": {"name": "Done"}}}'
3. sleep 300ms between updates
```

---

## API Version Notes (2025-09-03)

- **Databases → Data Sources**: Query endpoint uses `/data_sources/`. The script auto-handles both.
- **Dual IDs**: Each database has both `database_id` and `data_source_id`
  - `database_id`: Used when creating pages (`parent: {"database_id": "..."}`)
  - `data_source_id`: Used for queries — the script handles this automatically
- **Rate limit**: ~3 requests/sec average
- **Linked Databases**: API cannot operate on linked database data sources — find the original
- **Wiki Databases**: Can only be created in Notion UI; API has limited read access

---

## Important Reminders

- **Never confuse Notion with other platforms**. Notion → `api.notion.com`. Different platforms have different APIs.
- **Empty strings are invalid**: To clear a property value, use `null`, not `""`.
- **ID format is flexible**: The API accepts UUIDs with or without hyphens.
- **Pagination awareness**: `search` and `query-database` return up to 100 items by default. For larger datasets, paginate via `start_cursor` or use `--all`.
