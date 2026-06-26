---
name: notion
description: |
  Notion API integration with managed OAuth. Query databases, search pages, and read workspace content. Write operations require explicit user confirmation of the target resource and connection. Use this skill when users want to interact with Notion workspaces, databases, or pages. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Notion

Access the Notion API with managed OAuth authentication. Query databases, search pages, and read workspace content. All write operations (creating, updating, or deleting pages, blocks, and databases) require explicit user confirmation specifying the target resource and connection before execution.

## Quick Start

**CLI:**

```bash
maton notion search 'meeting notes'
```

```bash
maton api '/notion/v1/search'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'meeting notes'}).encode()
req = urllib.request.Request('https://api.maton.ai/notion/v1/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Notion-Version', '2025-09-03')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/notion/{native-api-path}
```

Maton proxies requests to `api.notion.com` and automatically injects your OAuth token. Write operations (POST, PATCH, DELETE) must only be executed after the user confirms the target page/database ID and intended connection.

## Required Headers

All Notion API requests require the version header:

```
Notion-Version: 2025-09-03
```

## Installation

**NPM:**
```bash
npm install -g @maton-ai/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your Notion OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list notion --status ACTIVE
```

```bash
maton api -X GET /connections -f app=notion -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=notion&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create notion
```

```bash
maton api /connections -f app=notion
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'notion'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "notion",
    "method": "OAUTH2",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Notion connections, specify which one to use:

**CLI:**

```bash
maton notion search 'meeting notes' --connection {connection_id}
```

```bash
maton api /notion/v1/search --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'meeting notes'}).encode()
req = urllib.request.Request('https://api.maton.ai/notion/v1/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Notion-Version', '2025-09-03')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Key Concept: Databases vs Data Sources

In API version 2025-09-03, databases and data sources are separate:

| Concept | Use For |
|---------|---------|
| **Database** | Creating databases, getting data source IDs |
| **Data Source** | Querying, updating schema, updating properties |

Use `GET /databases/{id}` to get the `data_sources` array, then use `/data_sources/` endpoints:

```json
{
  "object": "database",
  "id": "abc123",
  "data_sources": [
    {"id": "def456", "name": "My Database"}
  ]
}
```

## Security & Permissions

- Access is scoped to pages, databases, blocks, users, and search within the connected Notion account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call:
  1. Confirm the exact target (page ID, database ID, block ID) with the user.
  2. Verify the correct connection ID when multiple connections exist.
  3. State whether the action is reversible or destructive.
- **Irreversible / high-risk operations** (require extra caution):
  - Deleting pages or blocks (archived, not permanently deleted, but may disrupt workflows)
  - Bulk updates across multiple pages or databases
  - Modifying shared workspace pages visible to other team members
- **Scope boundaries:**
  - Only operate on pages and databases the user explicitly names or identifies. Never enumerate or modify resources outside the current task context.
  - Use the least-privileged Notion connection available for the task.
  - Do not perform bulk or batch operations without explicit user approval for each batch.

## API Reference

### Search

Search for pages:

```bash
POST /notion/v1/search
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "query": "meeting notes",
  "filter": {"property": "object", "value": "page"}
}
```

Example:

```bash
maton notion search 'meeting notes' --filter page
```

Search for data sources:

```bash
POST /notion/v1/search
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "filter": {"property": "object", "value": "data_source"}
}
```

Example:

```bash
maton notion search --filter data_source
```

### Data Sources

#### Get Data Source

```bash
GET /notion/v1/data_sources/{dataSourceId}
Notion-Version: 2025-09-03
```

Example:

```bash
maton notion data-source view <dataSourceId>
```

#### Query Data Source

```bash
POST /notion/v1/data_sources/{dataSourceId}/query
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "filter": {
    "property": "Status",
    "select": {"equals": "Active"}
  },
  "sorts": [
    {"property": "Created", "direction": "descending"}
  ],
  "page_size": 100
}
```

Example:

```bash
maton notion data-source query <dataSourceId> \
  --filter '{"property":"Status","select":{"equals":"Active"}}' \
  --sorts '[{"property":"Created","direction":"descending"}]' \
  --page-size 100
```

#### Update Data Source

```bash
PATCH /notion/v1/data_sources/{dataSourceId}
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "title": [{"type": "text", "text": {"content": "Updated Title"}}],
  "properties": {
    "NewColumn": {"rich_text": {}}
  }
}
```

Example:

```bash
maton notion data-source update <dataSourceId> \
  --body '{"title":[{"type":"text","text":{"content":"Updated Title"}}],"properties":{"NewColumn":{"rich_text":{}}}}'
```

### Databases

#### Get Database

```bash
GET /notion/v1/databases/{databaseId}
Notion-Version: 2025-09-03
```

Example:

```bash
maton notion database view <databaseId>
```

#### Create Database

```bash
POST /notion/v1/databases
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "parent": {"type": "page_id", "page_id": "PARENT_PAGE_ID"},
  "title": [{"type": "text", "text": {"content": "New Database"}}],
  "properties": {
    "Name": {"title": {}}
  }
}
```

Example:

```bash
maton notion database create --parent-page PARENT_PAGE_ID --title 'New Database'
```

In API version 2025-09-03, `POST /databases` only accepts the title property — any other entries in `properties` are silently dropped. To define a schema, follow up with `PATCH /data_sources/{dataSourceId}` (see [Update Data Source](#update-data-source)) using the `data_sources[0].id` returned by the create call.

### Pages

#### Get Page

```bash
GET /notion/v1/pages/{pageId}
Notion-Version: 2025-09-03
```

Example:

```bash
maton notion page view <pageId>
```

#### Create Page

```bash
POST /notion/v1/pages
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "parent": {"page_id": "PARENT_PAGE_ID"},
  "properties": {
    "title": {"title": [{"text": {"content": "New Page"}}]}
  }
}
```

Example:

```bash
maton notion page create --parent-page PARENT_PAGE_ID --title 'New Page'
```

#### Create Page in Data Source

```bash
POST /notion/v1/pages
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "parent": {"data_source_id": "DATA_SOURCE_ID"},
  "properties": {
    "Name": {"title": [{"text": {"content": "New Page"}}]},
    "Status": {"select": {"name": "Active"}}
  }
}
```

Example:

```bash
maton notion page create --data-source DATA_SOURCE_ID --title 'New Page' \
  --properties '{"Status":{"select":{"name":"Active"}}}'
```

#### Update Page Properties

```bash
PATCH /notion/v1/pages/{pageId}
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "properties": {
    "Status": {"select": {"name": "Done"}}
  }
}
```

Example:

```bash
maton notion page update {pageId} --properties '{"Status":{"select":{"name":"Done"}}}'
```

#### Update Page Icon

```bash
PATCH /notion/v1/pages/{pageId}
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "icon": {"type": "emoji", "emoji": "🚀"}
}
```

Example:

```bash
maton notion page update {pageId} --icon 🚀
```

Or with an image URL:

```bash
maton notion page update {pageId} --icon https://example.com/icon.png
```

#### Archive Page

```bash
PATCH /notion/v1/pages/{pageId}
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "archived": true
}
```

Example:

```bash
maton notion page archive {pageId}
```

### Blocks

#### Get Block Children

```bash
GET /notion/v1/blocks/{blockId}/children
Notion-Version: 2025-09-03
```

Example:

```bash
maton notion block children <blockId>
```

#### Append Block Children

```bash
PATCH /notion/v1/blocks/{blockId}/children
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "New paragraph"}}]
      }
    }
  ]
}
```

Example:

```bash
maton notion block append <blockId> \
  --children '[{"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"New paragraph"}}]}}]'
```

#### Delete Block

```bash
DELETE /notion/v1/blocks/{blockId}
Notion-Version: 2025-09-03
```

Example:

```bash
maton notion block delete <blockId>
```

### Users

#### List Users

```bash
GET /notion/v1/users
Notion-Version: 2025-09-03
```

Example:

```bash
maton notion user list
```

#### Get Current User

```bash
GET /notion/v1/users/me
Notion-Version: 2025-09-03
```

Example:

```bash
maton notion whoami
```

## Filter Operators

- `equals`, `does_not_equal`
- `contains`, `does_not_contain`
- `starts_with`, `ends_with`
- `is_empty`, `is_not_empty`
- `greater_than`, `less_than`

## Block Types

- `paragraph`, `heading_1`, `heading_2`, `heading_3`
- `bulleted_list_item`, `numbered_list_item`
- `to_do`, `code`, `quote`, `divider`

## Pagination

Notion uses cursor-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton notion data-source query <dataSourceId> --paginate
```

## Code Examples

### CLI

```bash
# Search for pages matching a query
maton notion search 'roadmap'

# View a specific page
maton notion page view 0123456789abcdef0123456789abcdef

# Query a data source with a filter
maton notion data-source query <dataSourceId> --filter '{"property":"Status","select":{"equals":"Active"}}'

# Filter with jq — e.g., only pages (responses are wrapped in {"results": [...]})
# Note: --jq requires --json
maton notion search 'roadmap' --json --jq '.results | map(select(.object == "page"))'
```

### JavaScript

```javascript
const response = await fetch('https://api.maton.ai/notion/v1/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Notion-Version': '2025-09-03'
  },
  body: JSON.stringify({ query: 'meeting' })
});
```

### Python

```python
import os
import requests

response = requests.post(
    'https://api.maton.ai/notion/v1/search',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Notion-Version': '2025-09-03'
    },
    json={'query': 'meeting'}
)
```

## Notes

- All IDs are UUIDs (with or without hyphens)
- Use `GET /databases/{id}` to get the `data_sources` array containing data source IDs
- Creating databases requires `POST /databases` endpoint
- Delete blocks returns the block with `archived: true`
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Notion connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Notion API |

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `notion`. For example:

- Correct: `https://api.maton.ai/notion/v1/search`
- Incorrect: `https://api.maton.ai/v1/search`

## Resources

- [Notion API Introduction](https://developers.notion.com/reference/intro)
- [Search](https://developers.notion.com/reference/post-search.md)
- [Query Database](https://developers.notion.com/reference/post-database-query.md)
- [Get Page](https://developers.notion.com/reference/retrieve-a-page.md)
- [Create Page](https://developers.notion.com/reference/post-page.md)
- [Update Page](https://developers.notion.com/reference/patch-page.md)
- [Append Block Children](https://developers.notion.com/reference/patch-block-children.md)
- [Filter Reference](https://developers.notion.com/reference/post-database-query-filter.md)
- [LLM Reference](https://developers.notion.com/llms.txt)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
