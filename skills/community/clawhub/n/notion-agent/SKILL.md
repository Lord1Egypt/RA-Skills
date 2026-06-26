---
name: notion-agent
description: "Notion integration for OpenClaw. Manage pages, databases, and blocks via AI agent."
license: "MIT-0"
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "bins": ["uv"] },
        "primaryEnv": "NOTION_TOKEN",
      },
  }
---

# Notion Agent

OpenClaw skill for managing Notion workspaces via AI agents. Provides CLI commands for pages, databases, blocks, and search.

## Setup

1. **Create a Notion Integration:**
   - Go to https://www.notion.so/my-integrations
   - Click "New integration"
   - Give it a name (e.g., "OpenClaw")
   - Copy the "Internal Integration Token"

2. **Set environment variable:**
   ```bash
   export NOTION_TOKEN=your_integration_token_here
   ```

3. **Share pages/databases with your integration:**
   - Open the page or database in Notion
   - Click "..." → "Add connections"
   - Select your integration

## Usage

All commands use the pattern:
```bash
uv run {baseDir}/scripts/notion.py <command> [options]
```

### Page Operations

**Create a page:**
```bash
uv run {baseDir}/scripts/notion.py page create \
  --parent <parent_page_id> \
  --title "My New Page" \
  --content "Initial paragraph content"
```

**Get a page:**
```bash
uv run {baseDir}/scripts/notion.py page get <page_id>
```

**Update a page:**
```bash
uv run {baseDir}/scripts/notion.py page update <page_id> \
  --title "Updated Title"
```

**Delete (archive) a page:**
```bash
uv run {baseDir}/scripts/notion.py page delete <page_id>
```

**List child pages:**
```bash
uv run {baseDir}/scripts/notion.py page list --parent <page_id>
```

### Database Operations

**Query a database:**
```bash
# Simple query
uv run {baseDir}/scripts/notion.py db query <db_id>

# With filter
uv run {baseDir}/scripts/notion.py db query <db_id> --filter Name=Todo

# With sort
uv run {baseDir}/scripts/notion.py db query <db_id> --sort Priority:desc
```

**Add page to database:**
```bash
uv run {baseDir}/scripts/notion.py db add <db_id> \
  --props '{"Name":{"title":[{"text":{"content":"Task"}}]},"Status":{"select":{"name":"Done"}}}'
```

**List all databases:**
```bash
uv run {baseDir}/scripts/notion.py db list
```

### Block Operations

**Append paragraph:**
```bash
uv run {baseDir}/scripts/notion.py block append <page_id> \
  --type paragraph \
  --text "This is a paragraph"
```

**Append to-do:**
```bash
uv run {baseDir}/scripts/notion.py block append <page_id> \
  --type todo \
  --text "Task to complete" \
  --checked
```

**Append heading:**
```bash
uv run {baseDir}/scripts/notion.py block append <page_id> \
  --type heading1 \
  --text "Section Title"
```

**Append code block:**
```bash
uv run {baseDir}/scripts/notion.py block append <page_id> \
  --type code \
  --text "print('Hello, World!')" \
  --language python
```

**List child blocks:**
```bash
uv run {baseDir}/scripts/notion.py block children <block_id>
```

### Search

**Search workspace:**
```bash
# Search all
uv run {baseDir}/scripts/notion.py search "project plan"

# Search only pages
uv run {baseDir}/scripts/notion.py search "meeting notes" --type page

# Search only databases
uv run {baseDir}/scripts/notion.py search "tasks" --type database
```

## Error Handling

The CLI handles common errors:
- `NOTION_TOKEN not set` — Set the environment variable
- `Invalid NOTION_TOKEN` — Check your integration token
- `Resource not found` — Page/database doesn't exist or integration lacks access
- `Permission denied` — Share the resource with your integration

## API Reference

- **Base URL:** `https://api.notion.com/v1`
- **API Version:** `2022-06-28`
- **Authentication:** Bearer token via `NOTION_TOKEN`

## Limitations

- Uses `requests` library only (no Notion SDK)
- Simple filter/sort syntax (single property)
- Rich text limited to plain text content
- Database properties must be formatted as JSON

## Examples for AI Agents

**Create a meeting notes page:**
```bash
uv run {baseDir}/scripts/notion.py page create \
  --parent <workspace_root_id> \
  --title "Meeting Notes - 2026-03-10" \
  --content "Attendees: Team"
```

**Add task to project database:**
```bash
uv run {baseDir}/scripts/notion.py db add <project_db_id> \
  --props '{"Name":{"title":[{"text":{"content":"Fix bug #123"}}]},"Status":{"select":{"name":"In Progress"}},"Priority":{"select":{"name":"High"}}}'
```

**Build a structured page:**
```bash
PAGE_ID=$(uv run {baseDir}/scripts/notion.py page create --parent <parent> --title "Report" | jq -r .id)
uv run {baseDir}/scripts/notion.py block append $PAGE_ID --type heading1 --text "Executive Summary"
uv run {baseDir}/scripts/notion.py block append $PAGE_ID --type paragraph --text "Key findings..."
uv run {baseDir}/scripts/notion.py block append $PAGE_ID --type heading2 --text "Details"
uv run {baseDir}/scripts/notion.py block append $PAGE_ID --type todo --text "Review findings"
```

## Help

```bash
uv run {baseDir}/scripts/notion.py --help
uv run {baseDir}/scripts/notion.py page --help
uv run {baseDir}/scripts/notion.py db --help
uv run {baseDir}/scripts/notion.py block --help
```
