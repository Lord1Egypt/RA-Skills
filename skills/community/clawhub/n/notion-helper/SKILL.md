---
name: notion-integration
description: Work with Notion databases, pages, and APIs. Use when user needs to create, read, update, or delete Notion pages and databases; automate Notion workflows; sync data between Notion and other apps; or build integrations with Notion.
---

# Notion Integration

Manage Notion workspaces via API for automation and integration.

## Quick Start

```bash
# Install Notion client
pip install notion-client

# Set API key
export NOTION_TOKEN="secret_xxx"
```

## Core Features

- **Database Operations**: Create, query, update databases
- **Page Management**: Create, read, update, delete pages
- **Block Operations**: Add/update content blocks
- **User Info**: Get workspace user information

## Script Usage

```bash
# Query a database
python scripts/notion.py query --database-id <id>

# Create a page
python scripts/notion.py create-page --database-id <id> --title "Task Name"

# Get page content
python scripts/notion.py get-page --page-id <id>
```

## Setup

1. Create integration at https://www.notion.so/my-integrations
2. Share database/page with integration
3. Set NOTION_TOKEN environment variable

## Examples

See `references/examples.md` for detailed use cases.
