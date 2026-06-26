---
name: ollang-project
description: Get details of a specific Ollang project or list all projects with pagination and search. Use when the user wants to find, browse, or inspect their Ollang projects.
---

# Ollang Project Management

Retrieve a single project by ID or list all projects with filtering and pagination.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

---

## Get Project by ID

**GET** `https://api-integration.ollang.com/integration/project/{projectId}`

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectId` | string | Yes | MongoDB ObjectId of the project |

### Response (200)
```json
{
  "id": "string",
  "name": "string",
  "sourceLanguage": "string",
  "createdAt": "ISO8601",
  "folderId": "string",
  "ordersCount": 0,
  "projectDocs": [
    {
      "id": "string",
      "type": "string",
      "url": "string"
    }
  ]
}
```

### Example
```bash
curl -X GET https://api-integration.ollang.com/integration/project/PROJECT_ID \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

---

## List All Projects

**GET** `https://api-integration.ollang.com/integration/project`

### Query Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | 1 | Page number |
| `take` | number | 10 | Items per page (1–50) |
| `orderBy` | string | `id` | Sort by: `id`, `name`, `createdAt`, `sourceLanguage` |
| `orderDirection` | string | `desc` | `asc` or `desc` |
| `search` | string | — | Search by project name |

### Response (200)
```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "sourceLanguage": "string",
      "createdAt": "ISO8601",
      "folderId": "string",
      "ordersCount": 0
    }
  ],
  "meta": {
    "page": 1,
    "take": 10,
    "itemCount": 100,
    "pageCount": 10,
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

### Example
```bash
# List all projects
curl -X GET "https://api-integration.ollang.com/integration/project?page=1&take=20" \
  -H "X-Api-Key: $OLLANG_API_KEY"

# Search by name
curl -X GET "https://api-integration.ollang.com/integration/project?search=my+video&orderBy=createdAt&orderDirection=desc" \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

---

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Determine action: get a specific project or list all projects
3. For **get by ID**: ask for `projectId` and display all project details including docs
4. For **list**: ask for optional search term and page size; display results in a table
5. Show pagination info and offer to fetch more pages if available

## Error Codes
- `400` - Invalid project ID format
- `401` - Invalid or missing API key
- `403` - Access denied
- `404` - Project not found
