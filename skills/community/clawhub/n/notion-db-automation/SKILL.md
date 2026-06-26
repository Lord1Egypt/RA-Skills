---
name: notion-db-automation
description: Automate common Notion database operations like batch page creation, data filtering, content generation, and export. Use when you need to automate workflows with Notion databases, bulk process entries, or sync data between Notion and other tools.
---

# Notion Database Automation

Automate repetitive tasks with Notion databases. Save hours of manual work by scripting common database operations.

## Core Capabilities

### 1. **Query and filter database entries**
- Filter by any property type (text, select, date, checkbox, number)
- Sort by any column
- Fetch all matching entries with pagination handled automatically

### 2. **Batch create pages**
- Create multiple database entries from CSV/JSON data
- Auto-set all property types including relations and rollups
- Generate page content with AI

### 3. **Batch update entries**
- Update existing pages based on filters
- Bulk change property values
- Archive or delete multiple entries

### 4. **Export database**
- Export entire database to CSV/JSON/Markdown
- Preserve all property types
- Ready for analysis or backup

### 5. **Create database from template**
- Quickly spin up new databases from predefined schemas
- Common templates included (task tracker, content calendar, CRM)

## Supported Property Types

- ✅ Text & Title
- ✅ Number
- ✅ Select & Multi-select
- ✅ Date
- ✅ Checkbox
- ✅ People
- ✅ URL
- ✅ Email
- ✅ Phone
- ✅ Relation
- ✅ Rollup (read-only)

## Quick Start

### Prerequisites
1. Create a Notion integration at https://www.notion.so/my-integrations
2. Get your API token
3. Share your database with the integration

### Example: Query a database

```python
from scripts.notion_client import NotionDBClient

client = NotionDBClient(api_token="YOUR_TOKEN")
entries = client.query_database(
    database_id="YOUR_DB_ID",
    filter={
        "property": "Status",
        "select": {
            "equals": "To Do"
        }
    },
    sorts=[{"property": "Created", "direction": "descending"}]
)

for entry in entries:
    print(entry["properties"]["Name"]["title"])
```

### Example: Create multiple pages from CSV

```python
from scripts.batch_create import create_from_csv

create_from_csv(
    api_token="YOUR_TOKEN",
    database_id="YOUR_DB_ID",
    csv_file="data.csv"
)
```

## Common Workflows

### Content Calendar Automation
1. Import a list of article topics from a spreadsheet
2. Auto-create calendar entries in Notion with scheduled publish dates
3. Add status = "Scheduled" automatically

### Task Management Automation
1. Filter tasks due today
2. Send summary to your email/chat
3. Mark old tasks as archived automatically

### CRM Lead Processing
1. When new leads come in, create Notion entries automatically
2. Assign properties based on source
3. Add AI-generated summary of the lead

## Scripts

### `scripts/notion_client.py`
Wrapper around the Notion API with simplified interface for common operations.

### `scripts/batch_create.py`
Batch create database entries from CSV or JSON.

### `scripts/batch_update.py`
Batch update entries matching filter conditions.

### `scripts/export_csv.py`
Export entire Notion database to CSV file.

### `templates/`
Pre-built database schemas for common use cases:
- `content_calendar.json` - Content calendar for bloggers/marketers
- `task_tracker.json` - Simple task tracker
- `crm_basic.json` - Basic CRM for small business

## Authentication

The skill expects your Notion API token to be provided. You can:
- Pass it directly in code
- Set it as environment variable `NOTION_API_TOKEN`
- Use OpenClaw secrets for secure storage

## When to use this skill

✅ **Use when:**
- You have repetitive tasks to do on a Notion database
- You need to import bulk data into Notion
- You want to export Notion data for analysis
- You need automated daily/weekly summaries from Notion

❌ **Don't use when:**
- You just need to manually edit a few pages (use the Notion UI)
- You don't have a Notion API token
- The database is not shared with your integration
