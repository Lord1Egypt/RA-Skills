---
name: ollang-folder
description: List and browse Ollang folders with pagination and search. Use when the user wants to see their folder structure, find a folder ID, or organize projects into folders.
---

# Ollang Folder Management

Retrieve a paginated list of folders for organizing projects.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

## Endpoint

**GET** `https://api-integration.ollang.com/integration/folder`

## Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | 1 | Page number |
| `take` | number | 10 | Items per page (1–50) |
| `orderBy` | string | `id` | Sort by: `id`, `name`, `createdAt` |
| `orderDirection` | string | `desc` | `asc` or `desc` |
| `search` | string | — | Search by folder name |

## Response (200)

```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "hexColor": "#B6B6B6",
      "type": "default",
      "createdAt": "ISO8601",
      "projectCount": 0
    }
  ],
  "meta": {
    "page": 1,
    "take": 10,
    "itemCount": 50,
    "pageCount": 5,
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

## Example (curl)
```bash
# List all folders
curl -X GET "https://api-integration.ollang.com/integration/folder?page=1&take=20" \
  -H "X-Api-Key: $OLLANG_API_KEY"

# Search for a folder
curl -X GET "https://api-integration.ollang.com/integration/folder?search=marketing&orderBy=name&orderDirection=asc" \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Ask for optional search term or page size
3. Display results in a table: ID, Name, Type, Color, Project Count, Created At
4. Folder IDs can be used when uploading files (`folderId` parameter in `ollang-upload`)
5. Show pagination info and offer to fetch more if available

## Error Codes
- `400` - Invalid query parameters
- `401` - Invalid or missing API key
- `500` - Server error
