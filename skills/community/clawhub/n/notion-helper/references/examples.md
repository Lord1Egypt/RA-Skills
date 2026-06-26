# Notion Integration Examples

## Setup

1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the "Internal Integration Token" (starts with `secret_`)
4. Export it: `export NOTION_TOKEN='secret_xxx'`
5. Share your database with the integration (click ... on database > Add connections > Select your integration)

## Example 1: Query a Database

```bash
# Get all items from a todo database
python scripts/notion.py query --database-id YOUR_DATABASE_ID
```

## Example 2: Create a Task

```bash
# Create a new task in a database
python scripts/notion.py create-page \
  --database-id YOUR_DATABASE_ID \
  --title "Finish project report"
```

## Example 3: Update Task Status

```bash
# Update a page's status
python scripts/notion.py update-page \
  --page-id YOUR_PAGE_ID \
  --properties '{"Status": {"select": {"name": "Done"}}}'
```

## Example 4: Use in Python Code

```python
from notion_client import Client

notion = Client(auth=os.environ['NOTION_TOKEN'])

# Query database
results = notion.databases.query(
    database_id="YOUR_DATABASE_ID",
    filter={"property": "Status", "select": {"equals": "In Progress"}}
)

# Create page
notion.pages.create(
    parent={"database_id": "YOUR_DATABASE_ID"},
    properties={
        "Name": {"title": [{"text": {"content": "New Task"}}]},
        "Status": {"select": {"name": "To Do"}}
    }
)
```

## Common Use Cases

- **Task Management**: Sync tasks between Notion and other tools
- **Content Calendar**: Manage content schedules in Notion
- **CRM**: Track customers and deals
- **Knowledge Base**: Automated documentation

## Finding Database ID

From the database URL:
`https://notion.so/{username}/{database_id}?v={view_id}`

The database ID is the 32-character string after the username/.
