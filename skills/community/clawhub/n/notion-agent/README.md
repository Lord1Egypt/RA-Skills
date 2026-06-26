# Notion Agent - OpenClaw Skill

Notion integration for OpenClaw agents. Manage pages, databases, and blocks via CLI.

## Features

- ✅ **Page CRUD** — Create, read, update, delete (archive) pages
- ✅ **Database queries** — Query, filter, sort, add entries
- ✅ **Block manipulation** — Append paragraphs, to-dos, headings, code blocks
- ✅ **Workspace search** — Find pages and databases
- ✅ **Error handling** — Clear messages for auth, permissions, not-found errors
- ✅ **Zero dependencies** — Uses `requests` only (no Notion SDK)

## Installation

1. Ensure `uv` is installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Set your Notion integration token:
   ```bash
   export NOTION_TOKEN=secret_abc123...
   ```

3. Test the CLI:
   ```bash
   uv run scripts/notion.py --help
   ```

## Quick Start

```bash
# Create a page
uv run scripts/notion.py page create \
  --parent <parent_page_id> \
  --title "My Page" \
  --content "Hello from OpenClaw!"

# Search for pages
uv run scripts/notion.py search "meeting" --type page

# Query a database
uv run scripts/notion.py db query <db_id>

# Append a block
uv run scripts/notion.py block append <page_id> \
  --type paragraph \
  --text "New paragraph"
```

## Architecture

```
notion-agent/
├── scripts/notion.py      # Main CLI (argparse-based)
├── lib/
│   ├── client.py          # API client wrapper
│   ├── pages.py           # Page operations
│   ├── databases.py       # Database operations
│   ├── blocks.py          # Block operations
│   └── search.py          # Search operations
├── SKILL.md               # OpenClaw skill definition
├── README.md              # This file
└── pyproject.toml         # Python dependencies
```

## Notion API

- **Version:** 2022-06-28
- **Docs:** https://developers.notion.com/reference/intro
- **Auth:** Integration token (not OAuth)

## Contributing

This skill uses:
- Python 3.11+
- `requests` library only (no external SDKs)
- Direct REST API calls to Notion

## License

MIT-0 (Public Domain)
