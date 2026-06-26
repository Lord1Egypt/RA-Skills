Notion

Access the Notion API with managed OAuth authentication. Query databases, create pages, manage blocks, and search your workspace.

Quick Start
Search for pages
curl -X POST https://gateway.maton.ai/notion/v1/search \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "query": "meeting notes"
  }'

Base URL
https://gateway.maton.ai/notion/{native-api-path}


Replace {native-api-path} with the actual Notion API endpoint path. The gateway proxies requests to api.notion.com and automatically injects your OAuth token.

Required Headers

All Notion API requests require:

Notion-Version: 2025-09-03
Authorization: Bearer $MATON_API_KEY
Content-Type: application/json

Authentication

Set your API key:

export MATON_API_KEY="YOUR_API_KEY"

Getting Your API Key
Sign in or create an account at maton.ai
Go to maton.ai/settings
Copy your API key
Connection Management

Manage your Notion OAuth connections at:

https://ctrl.maton.ai

List Connections
curl "https://ctrl.maton.ai/connections?app=notion&status=ACTIVE" \
  -H "Authorization: Bearer $MATON_API_KEY"

Create Connection
curl -X POST https://ctrl.maton.ai/connections \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "app": "notion"
  }'

Get Connection
curl https://ctrl.maton.ai/connections/{connection_id} \
  -H "Authorization: Bearer $MATON_API_KEY"

Delete Connection
curl -X DELETE https://ctrl.maton.ai/connections/{connection_id} \
  -H "Authorization: Bearer $MATON_API_KEY"

Complete OAuth

Open the returned url from the connection response in a browser.

Specifying Connection
curl -X POST https://gateway.maton.ai/notion/v1/search \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -H "Maton-Connection: 21fd90f9-5935-43cd-b6c8-bde9d915ca80" \
  -d '{
    "query": "meeting notes"
  }'

Key Concept: Databases vs Data Sources
Concept	Use For
Database	Creating databases, getting data source IDs
Data Source	Querying, updating schema, properties

Example response:

{
  "object": "database",
  "id": "abc123",
  "data_sources": [
    {"id": "def456", "name": "My Database"}
  ]
}

API Reference
Search
Search for pages
curl -X POST https://gateway.maton.ai/notion/v1/search \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "query": "meeting notes",
    "filter": { "property": "object", "value": "page" }
  }'

Search for data sources
curl -X POST https://gateway.maton.ai/notion/v1/search \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "filter": { "property": "object", "value": "data_source" }
  }'

Data Sources
Get Data Source
curl https://gateway.maton.ai/notion/v1/data_sources/{dataSourceId} \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03"

Query Data Source
curl -X POST https://gateway.maton.ai/notion/v1/data_sources/{dataSourceId}/query \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "filter": {
      "property": "Status",
      "select": { "equals": "Active" }
    },
    "sorts": [
      { "property": "Created", "direction": "descending" }
    ],
    "page_size": 100
  }'

Update Data Source
curl -X PATCH https://gateway.maton.ai/notion/v1/data_sources/{dataSourceId} \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "title": [{ "type": "text", "text": { "content": "Updated Title" } }],
    "properties": {
      "NewColumn": { "rich_text": {} }
    }
  }'

Databases
Get Database
curl https://gateway.maton.ai/notion/v1/databases/{databaseId} \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03"

Create Database
curl -X POST https://gateway.maton.ai/notion/v1/databases \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "parent": { "type": "page_id", "page_id": "PARENT_PAGE_ID" },
    "title": [{ "type": "text", "text": { "content": "New Database" } }],
    "properties": {
      "Name": { "title": {} },
      "Status": {
        "select": {
          "options": [{ "name": "Active" }, { "name": "Done" }]
        }
      }
    }
  }'

Pages
Get Page
curl https://gateway.maton.ai/notion/v1/pages/{pageId} \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03"

Create Page
curl -X POST https://gateway.maton.ai/notion/v1/pages \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "parent": { "page_id": "PARENT_PAGE_ID" },
    "properties": {
      "title": {
        "title": [{ "text": { "content": "New Page" } }]
      }
    }
  }'

Create Page in Data Source
curl -X POST https://gateway.maton.ai/notion/v1/pages \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "parent": { "data_source_id": "DATA_SOURCE_ID" },
    "properties": {
      "Name": { "title": [{ "text": { "content": "New Page" } }] },
      "Status": { "select": { "name": "Active" } }
    }
  }'

Update Page Properties
curl -X PATCH https://gateway.maton.ai/notion/v1/pages/{pageId} \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "properties": {
      "Status": { "select": { "name": "Done" } }
    }
  }'

Archive Page
curl -X PATCH https://gateway.maton.ai/notion/v1/pages/{pageId} \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "archived": true
  }'

Blocks
Get Block Children
curl https://gateway.maton.ai/notion/v1/blocks/{blockId}/children \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03"

Append Block Children
curl -X PATCH https://gateway.maton.ai/notion/v1/blocks/{blockId}/children \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "children": [
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [
            { "type": "text", "text": { "content": "New paragraph" } }
          ]
        }
      }
    ]
  }'

Delete Block
curl -X DELETE https://gateway.maton.ai/notion/v1/blocks/{blockId} \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03"

Users
List Users
curl https://gateway.maton.ai/notion/v1/users \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03"

Get Current User
curl https://gateway.maton.ai/notion/v1/users/me \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03"

Notes
All IDs are UUIDs
Use /databases/{id} to retrieve data_sources
Use curl -g if your URL contains brackets ([])
Avoid piping issues with $MATON_API_KEY in some shells
Error Handling
Status	Meaning
400	Missing Notion connection
401	Invalid API key
429	Rate limited
4xx/5xx	Notion API error
Troubleshooting
Check API key
echo $MATON_API_KEY

Test connection
curl https://ctrl.maton.ai/connections \
  -H "Authorization: Bearer $MATON_API_KEY"

Common Mistake

Correct:

https://gateway.maton.ai/notion/v1/search


Incorrect:

https://gateway.maton.ai/v1/search