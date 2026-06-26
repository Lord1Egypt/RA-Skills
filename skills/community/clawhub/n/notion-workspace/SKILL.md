---
name: notion-workspace
description: Full Notion API skill — query databases, manage pages, append blocks, and search your entire workspace.
---
# Notion Workspace

Automate your Notion workspace from the command line. Query and update databases, create and archive pages, append rich content blocks, and search across your entire workspace — all via the official Notion API with a single integration token.

## Setup

```bash
export NOTION_API_KEY="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export NOTION_DATABASE_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"   # optional default DB
```

Get your integration token: Notion → Settings → Connections → Develop or manage integrations → New integration.
Then share your database/pages with that integration.

## Commands / Usage

```bash
# ── DATABASES ───────────────────────────────────────────
# Query a database (uses NOTION_DATABASE_ID by default)
python3 scripts/notion_workspace.py db-query
python3 scripts/notion_workspace.py db-query --db-id "abc123..."

# Query with filter
python3 scripts/notion_workspace.py db-query --filter-prop "Status" --filter-value "In Progress"

# Create a new entry (page) in a database
python3 scripts/notion_workspace.py db-create --title "My Task" --props '{"Status": "To Do", "Priority": "High"}'

# Update a database entry
python3 scripts/notion_workspace.py db-update --page-id "def456..." --props '{"Status": "Done"}'

# ── PAGES ───────────────────────────────────────────────
# Create a standalone page (under a parent page)
python3 scripts/notion_workspace.py page-create --parent-id "ghi789..." --title "Meeting Notes" --content "Today we discussed..."

# Read a page (metadata + content preview)
python3 scripts/notion_workspace.py page-read --page-id "def456..."

# Update page title/properties
python3 scripts/notion_workspace.py page-update --page-id "def456..." --title "Updated Title"

# Archive (soft-delete) a page
python3 scripts/notion_workspace.py page-archive --page-id "def456..."

# ── BLOCKS ──────────────────────────────────────────────
# Get children blocks of a page or block
python3 scripts/notion_workspace.py blocks-get --block-id "def456..."

# Append a paragraph block
python3 scripts/notion_workspace.py blocks-append --block-id "def456..." --text "New paragraph content here"

# Append a heading
python3 scripts/notion_workspace.py blocks-append --block-id "def456..." --text "Section Title" --type heading_2

# Append a to-do item
python3 scripts/notion_workspace.py blocks-append --block-id "def456..." --text "Complete this task" --type to_do

# Append a bulleted list item
python3 scripts/notion_workspace.py blocks-append --block-id "def456..." --text "Bullet point" --type bulleted_list_item

# Append a code block
python3 scripts/notion_workspace.py blocks-append --block-id "def456..." --text "print('hello')" --type code --language python

# ── SEARCH ──────────────────────────────────────────────
# Search entire workspace
python3 scripts/notion_workspace.py search --query "project roadmap"

# Search only pages
python3 scripts/notion_workspace.py search --query "meeting notes" --filter page

# Search only databases
python3 scripts/notion_workspace.py search --query "tasks" --filter database
```

## Requirements

- Python 3.8+
- `requests` (`pip install requests`)
- `NOTION_API_KEY` environment variable
- `NOTION_DATABASE_ID` environment variable (optional, for default DB commands)
