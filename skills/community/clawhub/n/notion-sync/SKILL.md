---
name: notion-sync
description: Read, search, export, create, update, monitor, query, inspect, batch-edit, and explicitly archive Notion pages and databases. Use when the user requests Notion content or database operations and a host secret manager can supply NOTION_API_KEY.
homepage: https://github.com/robansuini/agent-skills
license: MIT-0
allowed-tools: Bash, Read, Write, WebFetch, Env
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "bins": ["node"], "env": ["NOTION_API_KEY"] },
        "primaryEnv": "NOTION_API_KEY",
        "network": { "outboundHosts": ["api.notion.com"] },
      },
  }
---

# Notion Sync

Bi-directional sync between markdown files and Notion pages, plus database management utilities for research tracking and project management.

## Security and capability boundary

- Reads `NOTION_API_KEY` from the environment and sends it only to
  `https://api.notion.com`.
- Reads and writes user-selected markdown and watch-state files. Workspace path
  restrictions are enabled by default. Each external path requires an exact,
  mode-specific `--allow-read-path` or `--allow-write-path` authorization.
- Can search, read, create, update, batch-update, inspect, and archive Notion
  content shared with the configured integration.
- Mutating operations run only through an explicitly selected command. Batch
  query updates require a filter, and page archiving additionally requires
  `--confirm-archive`.

## Upgrading

**v3.0 is a breaking security release.** It removes `--token-file`,
`--token-stdin`, and automatic `~/.notion-token` loading. The scripts now use
only `NOTION_API_KEY`, supplied by the host runtime's secret manager.

Read [references/MIGRATION-V3.md](references/MIGRATION-V3.md) before upgrading
from any v1 or v2 release. Keep v2.5.3 pinned until the replacement secret
injection is configured and verified.

## Requirements

- **Node.js** 18 or later
- A **Notion integration token** (starts with `ntn_` or `secret_`)
- A runtime or secret manager that injects `NOTION_API_KEY`

## Credential workflow

Supply `NOTION_API_KEY` through your platform's secret manager. Do not place
the token in chat, source control, command arguments, URLs, or committed `.env`
files. The scripts do not depend on a particular agent runtime.

### OpenClaw protected-secret mode

OpenClaw users should use version 2026.9.1 or later and its protected-secret
egress workflow:

Before the first Notion API operation in a run:

1. Use the OpenClaw `secrets` tool with `action=list`. Inspect metadata only;
   never request or read the credential in chat.
2. If `NOTION_API_KEY` is missing, use `action=request` with:
   - `name: NOTION_API_KEY`
   - `kind: secret`
   - `allowedHosts: ["api.notion.com"]`
   - a one-line reason explaining that notion-sync needs Notion API access
3. If the request is skipped or unavailable, stop and report the blocker.
   Never ask the user to paste the token into chat or a command.
4. Run scripts with Gateway-hosted exec. Do not override, expand, inspect, log,
   or print `NOTION_API_KEY`; OpenClaw injects an opaque sentinel and replaces
   it only for allowed HTTPS requests to `api.notion.com`.
5. If any Gateway-hosted command already ran before the secret was stored or
   changed, start a new agent run so the new secret snapshot is available.

## Setup

1. Go to https://www.notion.so/my-integrations
2. Create a new integration (or use an existing one)
3. Share your Notion pages/databases with the integration through the page's
   **Connections** menu.
4. Save the token as `NOTION_API_KEY` through your runtime's secret manager.

For OpenClaw, save it through the masked prompt or **Settings → Secrets** as a
protected secret allowed only for `api.notion.com`, then enable protected
egress and restart the Gateway:
   ```bash
   openclaw config set secrets.egressProxy.enabled true --strict-json
   openclaw gateway restart
   ```

When OpenClaw supplies a protected sentinel, a missing proxy, CA, host binding,
or compatible Node runtime fails closed. This protected mode requires Node.js
22.21+ in the 22.x line, 24.5+ in the 24.x line, or 25+. Ordinary environment
credentials use the portable direct-HTTPS path on Node.js 18+.

## JSON Output Mode

All scripts support a global `--json` flag.

- Suppresses progress logs written to stderr
- Keeps stdout machine-readable for automation
- Errors are emitted as JSON: `{ "error": "..." }`

Example:
```bash
node scripts/query-database.js <db-id> --limit 5 --json
```

## Path Safety Mode

Scripts that read/write local files are restricted to the current working directory by default.

- Prevents accidental reads/writes outside the intended workspace
- Applies to: `md-to-notion.js`, `add-to-database.js`, `notion-to-md.js`, `watch-notion.js`
- Canonicalizes symlinked path ancestors before enforcement to block workspace-escape writes
- Outside-workspace access requires the exact target path and access mode;
  authorization does not extend to parent, child, or sibling paths

Examples:
```bash
# Default (safe): path must be inside current workspace
node scripts/md-to-notion.js docs/draft.md <parent-id> "Draft"

# Explicit authorization for one outside-workspace output
node scripts/notion-to-md.js <page-id> ~/Downloads/export.md \
  --allow-write-path ~/Downloads/export.md
```

## Core Operations

### 1. Search Pages and Databases

Search across your Notion workspace by title or content.

```bash
node scripts/search-notion.js "<query>" [--filter page|database] [--limit 10] [--json]
```

**Examples:**
```bash
# Search for newsletter-related pages
node scripts/search-notion.js "newsletter"

# Find only databases
node scripts/search-notion.js "research" --filter database

# Limit results (1-100)
node scripts/search-notion.js "AI" --limit 5
```

`--filter` accepts only `page` or `database`; `--limit` must be a positive integer from 1 to 100.

**Output:**
```json
[
  {
    "id": "page-id-here",
    "object": "page",
    "title": "Newsletter Draft",
    "url": "https://notion.so/...",
    "lastEdited": "2026-02-01T09:00:00.000Z"
  }
]
```

### 2. Query Databases with Filters

Query database contents with advanced filters and sorting.

```bash
node scripts/query-database.js <database-id> [--filter <json>] [--sort <json>] [--limit 10] [--json]
```

`--limit` must be a positive integer from 1 to 100.

**Examples:**
```bash
# Get all items
node scripts/query-database.js xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Filter by Status = "Complete"
node scripts/query-database.js <db-id> \
  --filter '{"property": "Status", "select": {"equals": "Complete"}}'

# Filter by Tags containing "AI"
node scripts/query-database.js <db-id> \
  --filter '{"property": "Tags", "multi_select": {"contains": "AI"}}'

# Sort by Date descending
node scripts/query-database.js <db-id> \
  --sort '[{"property": "Date", "direction": "descending"}]'

# Combine filter + sort
node scripts/query-database.js <db-id> \
  --filter '{"property": "Status", "select": {"equals": "Complete"}}' \
  --sort '[{"property": "Date", "direction": "descending"}]'
```

**Common filter patterns:**
- Select equals: `{"property": "Status", "select": {"equals": "Done"}}`
- Multi-select contains: `{"property": "Tags", "multi_select": {"contains": "AI"}}`
- Date after: `{"property": "Date", "date": {"after": "2024-01-01"}}`
- Checkbox is true: `{"property": "Published", "checkbox": {"equals": true}}`
- Number greater than: `{"property": "Count", "number": {"greater_than": 100}}`

### 3. Update Page Properties

Update properties for database pages (status, tags, dates, etc.).

```bash
node scripts/update-page-properties.js <page-id> <property-name> <value> [--type <type>] [--json]
```

**Supported types:** select, multi_select, checkbox, number, url, email, date, rich_text

Long `rich_text` values are automatically split to Notion's 2,000-character per-item limit.

**Examples:**
```bash
# Set status
node scripts/update-page-properties.js <page-id> Status "Complete" --type select

# Add multiple tags
node scripts/update-page-properties.js <page-id> Tags "AI,Leadership,Research" --type multi_select

# Set checkbox
node scripts/update-page-properties.js <page-id> Published true --type checkbox

# Set date
node scripts/update-page-properties.js <page-id> "Publish Date" "2024-02-01" --type date

# Set URL
node scripts/update-page-properties.js <page-id> "Source URL" "https://example.com" --type url

# Set number
node scripts/update-page-properties.js <page-id> "Word Count" 1200 --type number
```

### 4. Batch Update

Batch update a single property across multiple pages in one command.

**Mode 1 — Query + Update:**
```bash
node scripts/batch-update.js <database-id> <property-name> <value> --filter '<json>' [--type select] [--dry-run] [--limit 100]
```

Query mode requires `--filter` so the command cannot update an entire database by accident. Use stdin mode when you already have an explicit page-id list.

**Example:**
```bash
node scripts/batch-update.js <db-id> Status Review \
  --filter '{"property":"Status","select":{"equals":"Draft"}}' \
  --type select
```

**Mode 2 — Page IDs from stdin:**
```bash
echo "page-id-1\npage-id-2\npage-id-3" | \
  node scripts/batch-update.js --stdin <property-name> <value> [--type select] [--dry-run]
```

**Features:**
- `--dry-run`: prints pages that would be updated (with current property value) without writing
- `--limit <n>`: positive integer max pages to process (default `100`)
- Pagination in query mode (`has_more`/`next_cursor`) up to limit
- Rate-limit friendly updates (300ms between page updates)
- Progress and summary on stderr, JSON result array on stdout

### 5. Markdown → Notion Sync

Push markdown content to Notion with full formatting support.

```bash
node scripts/md-to-notion.js \
  "<markdown-file-path>" \
  "<notion-parent-page-id>" \
  "<page-title>" [--json] [--allow-read-path <exact-path>]
```

**Example:**
```bash
node scripts/md-to-notion.js \
  "projects/newsletter-draft.md" \
  "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  "Newsletter Draft - Feb 2026"
```

**Supported formatting:**
- Headings (H1-H3)
- Bold/italic text
- Links
- Bullet and numbered lists
- Code blocks with syntax highlighting (``` or ~~~ fences)
- Horizontal dividers
- Paragraphs

**Features:**
- Batched uploads (100 blocks per request)
- Automatic rate limiting (350ms between batches)
- Rich text is automatically chunked to Notion's 2000-character limit (including bold/italic/link spans)
- Unclosed fenced code blocks (` ``` ` or `~~~`) at end-of-file are preserved as code blocks
- Fence-like lines with info strings inside code blocks (e.g. ````js`) are preserved as code content
- Returns Notion page URL and ID

**Output:**
```
Parsed 294 blocks from markdown
✓ Created page: https://www.notion.so/[title-and-id]
✓ Appended 100 blocks (100-200)
✓ Appended 94 blocks (200-294)

✅ Successfully created Notion page!
```

### 6. Notion → Markdown Sync

Pull Notion page content and convert to markdown.

```bash
node scripts/notion-to-md.js <page-id> [output-file] [--json] [--allow-write-path <exact-path>]
```

**Example:**
```bash
node scripts/notion-to-md.js \
  "abc123-example-page-id-456def" \
  "newsletter-updated.md"
```

**Features:**
- Converts Notion blocks to markdown
- Preserves formatting (headings, lists, code, quotes)
- Resolves page titles from the actual Notion `title`-type property (even when the property key is custom)
- Optional file output (writes to file or stdout)

### 7. Change Detection & Monitoring

Monitor Notion pages for edits and compare with local markdown files.

```bash
node scripts/watch-notion.js "<page-id>" "<local-markdown-path>" [--state-file <path>] [--json] [--allow-read-path <exact-path>] [--allow-write-path <exact-path>]
```

**Example:**
```bash
node scripts/watch-notion.js \
  "abc123-example-page-id-456def" \
  "projects/newsletter-draft.md"
```

**State tracking:** By default maintains state in `memory/notion-watch-state.json` (relative to current working directory). You can override with `--state-file <path>` (supports `~` expansion):

```bash
node scripts/watch-notion.js "<page-id>" "<local-path>" --state-file ~/.cache/notion-watch-state.json
```

Default state schema:
```json
{
  "pages": {
    "<page-id>": {
      "lastEditedTime": "2026-01-30T08:57:00.000Z",
      "lastChecked": "2026-01-31T19:41:54.000Z",
      "title": "Your Page Title"
    }
  }
}
```

**Output:**
```json
{
  "pageId": "<page-id>",
  "title": "Your Page Title",
  "lastEditedTime": "2026-01-30T08:57:00.000Z",
  "hasChanges": false,
  "localPath": "/path/to/your-draft.md",
  "actions": ["✓ No changes since last check"]
}
```

**Automated monitoring:** Schedule periodic checks using cron, CI pipelines, or any task scheduler:
```bash
# Example: cron job every 2 hours during work hours
0 9-21/2 * * * cd /path/to/workspace && node scripts/watch-notion.js "<page-id>" "<local-path>"
```

The script outputs JSON — pipe it to any notification system when `hasChanges` is `true`.

### 8. Database Management

#### Add Markdown Content to Database

Add a markdown file as a new page in any Notion database.

```bash
node scripts/add-to-database.js <database-id> "<page-title>" <markdown-file-path> [--json] [--allow-read-path <exact-path>]
```

**Examples:**
```bash
# Add research output
node scripts/add-to-database.js \
  xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx \
  "Research Report - Feb 2026" \
  projects/research-insights.md

# Add project notes
node scripts/add-to-database.js \
  <project-db-id> \
  "Sprint Retrospective" \
  docs/retro-2026-02.md

# Add meeting notes
node scripts/add-to-database.js \
  <notes-db-id> \
  "Weekly Team Sync" \
  notes/sync-2026-02-06.md
```

**Features:**
- Creates database page with title property
- Converts markdown to Notion blocks (headings, paragraphs, dividers)
- Handles large files with batched uploads
- Returns page URL for immediate access

**Note:** Additional properties (Type, Tags, Status, etc.) must be set manually in Notion UI after creation.

#### Inspect Database Schema

```bash
node scripts/get-database-schema.js <database-id> [--json]
```

**Example output:**
```json
{
  "object": "database",
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "title": [{"plain_text": "Ax Resources"}],
  "properties": {
    "Name": {"type": "title"},
    "Type": {"type": "select"},
    "Tags": {"type": "multi_select"}
  }
}
```

**Use when:**
- Setting up new database integrations
- Debugging property names/types
- Understanding database structure

#### Archive Pages

```bash
node scripts/delete-notion-page.js <page-id> --confirm-archive [--json]
```

**Note:** This archives the page (sets `archived: true`), not permanent deletion.
The explicit confirmation flag prevents an agent or user from archiving a page
through an incomplete command.

## Common Workflows

### Collaborative Editing Workflow

1. **Push local draft to Notion:**
   ```bash
   node scripts/md-to-notion.js draft.md <parent-id> "Draft Title"
   ```

2. **User edits in Notion** (anywhere, any device)

3. **Monitor for changes:**
   ```bash
   node scripts/watch-notion.js <page-id> <local-path>
   # Returns hasChanges: true when edited
   ```

4. **Pull updates back:**
   ```bash
   node scripts/notion-to-md.js <page-id> draft-updated.md
   ```

5. **Repeat as needed** (update same page, don't create v2/v3/etc.)

### Research Output Tracking

1. **Generate research locally** (e.g., via sub-agent)

2. **Sync to Notion database:**
   ```bash
   node scripts/add-to-database.js <database-id> "Research Output - 2026-03-21" research-output.md
   ```

3. **User adds metadata in Notion UI** (Type, Tags, Status properties)

4. **Access from anywhere** via Notion web/mobile

### Page ID Extraction

From Notion URL: `https://notion.so/Page-Title-abc123-example-page-id-456def`

Extract: `abc123-example-page-id-456def` (last part after title)

Or use the 32-char format: `abc123examplepageid456def` (hyphens optional)

## Limitations

- **Property updates:** Database properties (Type, Tags, Status) must be added manually in Notion UI after page creation. API property updates can be temperamental with inline databases.
- **Block limits:** Very large markdown files (>1000 blocks) may take several minutes to sync due to rate limiting.
- **Formatting:** Some complex markdown (tables, nested lists >3 levels) may not convert perfectly.

## Troubleshooting

**"Could not find page" error:**
- Ensure page/database is shared with your integration
- Check page ID format (32 chars, alphanumeric + hyphens)

**"Module not found" error:**
- Scripts use built-in Node.js https module (no npm install needed)
- Ensure running from the skill's directory (where scripts/ lives)

**Rate limiting:**
- Notion API has rate limits (~3 requests/second)
- Scripts handle this automatically with 350ms delays between batches

## Resources

### scripts/

**Core Sync:**
- **md-to-notion.js** - Markdown → Notion sync with full formatting
- **notion-to-md.js** - Notion → Markdown conversion
- **watch-notion.js** - Change detection and monitoring

**Search & Query:**
- **search-notion.js** - Search pages and databases by query
- **query-database.js** - Query databases with filters and sorting
- **update-page-properties.js** - Update database page properties
- **batch-update.js** - Batch update one property across many pages (query or stdin IDs)

**Database Management:**
- **add-to-database.js** - Add markdown files as database pages
- **get-database-schema.js** - Inspect database structure
- **delete-notion-page.js** - Archive pages

**Utilities:**
- **notion-utils.js** - Shared utilities (error handling, property formatting, API requests)

All scripts use only built-in Node.js modules (https, fs) - no external dependencies required.

### references/

- **API-REFERENCE.md** - Detailed script signatures, options, and utility behavior
