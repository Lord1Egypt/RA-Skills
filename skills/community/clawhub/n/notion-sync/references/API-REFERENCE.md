# Notion Sync API Reference

Detailed technical reference for all Notion sync scripts and utilities.

## Credential setup

### Notion Token

All scripts require `NOTION_API_KEY`, supplied through the host runtime's
secret manager. The portable client uses direct HTTPS and supports Node.js 18+.

With OpenClaw, use its protected secret workflow:

1. List secret metadata with the `secrets` tool.
2. If missing, request `NOTION_API_KEY` as `kind: secret` with
   `allowedHosts: ["api.notion.com"]`.
3. Run the script with Gateway-hosted exec after the secret exists.

OpenClaw injects an opaque environment sentinel. The scripts detect it and use
the Gateway proxy, allowing substitution only for `https://api.notion.com`.
Never inspect or print the environment variable.

Removed in v3: `--token`, `--token-file`, `--token-stdin`, and automatic
`~/.notion-token` loading. See [MIGRATION-V3.md](MIGRATION-V3.md).

## JSON Output Mode

All scripts accept `--json` to emit machine-readable output and suppress stderr progress logs.

- Success output is JSON
- Errors are JSON objects: `{ "error": "..." }`

## Path Safety Mode

Scripts that read/write local files are restricted to the current working directory by default.

- Applies to: `md-to-notion.js`, `notion-to-md.js`, `watch-notion.js`, `add-to-database.js`
- Write-path checks resolve symlink ancestors before enforcement to prevent workspace escape via nested missing directories
- External inputs require `--allow-read-path <exact-path>`; external outputs
  require `--allow-write-path <exact-path>`
- Each authorization is mode-specific and matches one canonical path only; it
  does not grant access to parent, child, or sibling paths

## Scripts Reference

### search-notion.js

Search pages and databases by title or content.

**Signature:**
```bash
node scripts/search-notion.js "<query>" [--filter page|database] [--limit 10] [--json]
```

**Options:**
- `query` (required): Search term
- `--filter`: Restrict to `page` or `database`
- `--limit`: Max results, 1-100 (default: 10)

**Returns:** JSON array of matching pages/databases with id, title, url, lastEdited

### query-database.js

Query database contents with advanced filters and sorting.

**Signature:**
```bash
node scripts/query-database.js <database-id> [--filter <json>] [--sort <json>] [--limit 10] [--json]
```

**Filter Patterns:**

| Type | Example |
|------|---------|
| Select equals | `{"property": "Status", "select": {"equals": "Done"}}` |
| Multi-select contains | `{"property": "Tags", "multi_select": {"contains": "AI"}}` |
| Date after | `{"property": "Date", "date": {"after": "2024-01-01"}}` |
| Checkbox | `{"property": "Published", "checkbox": {"equals": true}}` |
| Number | `{"property": "Count", "number": {"greater_than": 100}}` |

**Sort Format:**
```json
[{"property": "Date", "direction": "descending"}]
```

**Options:**
- `--limit`: Max results, 1-100 (default: 10)

### update-page-properties.js

Update database page properties.

**Signature:**
```bash
node scripts/update-page-properties.js <page-id> <property-name> <value> [--type <type>] [--json]
```

**Property Types:**
- `select`: Single selection (e.g., Status)
- `multi_select`: Multiple tags (comma-separated)
- `checkbox`: Boolean (true/false)
- `number`: Numeric value
- `url`: URL string
- `email`: Email address
- `date`: ISO date (YYYY-MM-DD)
- `rich_text`: Plain text (automatically split to Notion's 2,000-character per-item limit)

### batch-update.js

Batch update a property across multiple pages.

**Signatures:**
```bash
# Query + update
node scripts/batch-update.js <database-id> <property-name> <value> --filter '<json>' [--type <type>] [--dry-run] [--limit 100]

# IDs from stdin
echo "page-id-1\npage-id-2" | node scripts/batch-update.js --stdin <property-name> <value> [--type <type>] [--dry-run] [--limit 100]
```

**Options:**
- `--filter <json>`: Notion database query filter (required in query mode)
- `--stdin`: read page IDs (one per line) from stdin instead of querying a database
- `--type <type>`: `select`, `multi_select`, `checkbox`, `number`, `url`, `email`, `date`, `rich_text`
- `--dry-run`: no writes; prints page IDs + current values to stderr and returns preview JSON
- `--limit <n>`: positive integer max pages to process (default: 100)

**Behavior:**
- Refuses query-mode updates without `--filter` to avoid accidental whole-database changes
- Uses database `data_source_id` when available
- Supports query pagination (`has_more` + `next_cursor`) up to `--limit`
- Adds 300ms delay between updates to reduce 429 rate limits
- Emits progress to stderr and JSON results to stdout (`[{id, url, updated}]`)

### md-to-notion.js

Convert markdown to Notion page.

**Signature:**
```bash
node scripts/md-to-notion.js "<markdown-file>" "<parent-page-id>" "<title>" [--json] [--allow-read-path <exact-path>]
```

**Supported Markdown:**
- Headings: `#`, `##`, `###`
- Bold: `**text**`
- Italic: `*text*`
- Links: `[text](url)`
- Lists: `- item`
- Code: fenced blocks with ```lang ... ``` or ~~~lang ... ~~~
- Dividers: `---`

**Output:** Notion page URL and ID

**Rich text safety:** markdown rich_text segments are automatically split to Notion's 2000-character per-item limit (plain, bold, italic, and links).

**Code fence safety:** unclosed fenced code blocks (``` or ~~~) at end-of-file are still emitted as Notion `code` blocks instead of being dropped, and fence-like lines with info strings inside code blocks are preserved as content.

**Rate Limiting:** 350ms between batch uploads (100 blocks per batch)

### notion-to-md.js

Convert Notion page to markdown.

**Signature:**
```bash
node scripts/notion-to-md.js <page-id> [output-file] [--json] [--allow-write-path <exact-path>]
```

**Output:** Writes markdown to file or stdout

**Title resolution:** Uses the page's actual Notion `title`-type property (works even when the property key is not literally `title`).

### watch-notion.js

Monitor page for changes.

**Signature:**
```bash
node scripts/watch-notion.js [--state-file <path>] <page-id> <local-path> [--json] [--allow-read-path <exact-path>] [--allow-write-path <exact-path>]
```

**State File:** Default `memory/notion-watch-state.json` (relative to cwd), overridable with `--state-file` (supports `~` expansion)

**State Schema:**
```json
{
  "pages": {
    "<page-id>": {
      "lastEditedTime": "ISO timestamp",
      "lastChecked": "ISO timestamp",
      "title": "Page Title"
    }
  }
}
```

**Returns:** JSON with `hasChanges`, `localDiffers`, `actions`

### get-database-schema.js

Inspect database structure.

**Signature:**
```bash
node scripts/get-database-schema.js <database-id> [--json]
```

**Returns:** JSON with database properties and their types

### delete-notion-page.js

Archive page (soft delete).

**Signature:**
```bash
node scripts/delete-notion-page.js <page-id> --confirm-archive [--json]
```

**Note:** Sets `archived: true`, doesn't permanently delete. The
`--confirm-archive` flag is mandatory so incomplete or inferred commands fail
before any API request.

## Notion API Utilities

### notion-utils.js

Shared utilities for all scripts.

**Exports:**

#### `notionRequest(path, method, body)`
Makes authenticated API requests to Notion.

**Parameters:**
- `path`: API endpoint (e.g., `/v1/pages`)
- `method`: HTTP method (GET, POST, PATCH, DELETE)
- `body`: Optional request body (object)

**Transport:** direct Node.js `https.request` by default. When an OpenClaw
protected sentinel is detected, the request uses a native proxy-aware
`https.Agent`. That agent receives only the Gateway-provided `HTTPS_PROXY`
value, so inherited `NO_PROXY` or lowercase proxy overrides cannot bypass
protected-secret egress.

**Returns:** Promise resolving to response JSON

**Error Handling:** Throws actionable messages for common failures:
- Missing token: guidance for the runtime-neutral `NOTION_API_KEY` migration
- 401: authentication/access guidance
- 404: page/database access/id guidance
- Network errors: connectivity guidance

#### `formatPropertyValue(type, value)`
Formats property values for Notion API write operations.

**Supported Types:**
- select, multi_select, checkbox, number, url, email, date, rich_text, title

**Returns:** Notion API property object

#### `normalizeId(id)`
Normalizes a Notion page/block ID to UUID format with hyphens.

**Input Formats:**
- With hyphens: `abc12345-6789-0123-4567-890abcdef012` (passes through)
- Without hyphens: `abc12345678901234567890abcdef012` (adds hyphens)
- Invalid length: returned as-is

**Returns:** UUID string with hyphens

## Rate Limits

Notion API limits:
- ~3 requests/second
- Scripts implement 350ms delays between batches
- Large operations (>100 blocks) auto-batch with delays

## Common Issues

### Authentication Errors

**Error:** `"Could not find page"`

**Solutions:**
1. Verify page/database is shared with your integration
2. Check page ID format (32 chars, no extra characters)
3. Confirm `NOTION_API_KEY` is available through your runtime's secret manager.
   With OpenClaw, also confirm it is protected, bound to `api.notion.com`, and
   running through Gateway-hosted exec.

### Property Update Failures

**Issue:** Property updates don't persist

**Cause:** Database is inline (embedded in a page) rather than standalone

**Solution:** Create standalone database or update properties manually in Notion UI

### Module Not Found

**Error:** protected-secret proxy support is unavailable

**Solution:** This applies only when an OpenClaw protected sentinel is present.
Use Node.js 22.21+ (22.x), 24.5+ (24.x), or 25+, and run through OpenClaw
Gateway-hosted exec with the egress proxy enabled.

## Page ID Extraction

From Notion URL:
```
https://notion.so/Page-Title-abc123-example-page-id-456def
                            └─────────── Extract this part ──────────┘
```

Both formats work:
- With hyphens: `abc123-example-page-id-456def`
- Without hyphens: `abc123examplepageid456def`

## Integration Permissions

Required Notion integration capabilities:
- ✓ Read content
- ✓ Update content
- ✓ Insert content
- ✓ Read comments (optional)

Share settings:
- Must explicitly share each page/database with the integration
- Child pages inherit parent permissions
- Databases require explicit sharing even if parent is shared
