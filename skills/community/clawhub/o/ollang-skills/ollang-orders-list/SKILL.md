---
name: ollang-orders-list
description: List and search Ollang orders with pagination, filtering by type/name/date, and sorting. Use when the user wants to browse, search, or filter their translation orders.
---

# Ollang List Orders

Retrieve a paginated list of orders with filtering and sorting options.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

## Endpoint

**GET** `https://api-integration.ollang.com/integration/orders`

## Query Parameters

### Pagination
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pageOptions[page]` | number | 1 | Page number |
| `pageOptions[take]` | number | 10 | Items per page (1–50) |
| `pageOptions[orderBy]` | string | `id` | Sort field: `id`, `name`, `createdAt` |
| `pageOptions[orderDirection]` | string | `desc` | `asc` or `desc` |

### Filters
| Parameter | Type | Description |
|-----------|------|-------------|
| `pageOptions[search]` | string | Search across order names |
| `filter[type]` | string | `cc`, `subtitle`, `document`, `aiDubbing`, `studioDubbing`, `proofreading`, `other`, `revision` |
| `filter[name]` | string | Filter by exact name |
| `filter[createdAtRange][from]` | ISO 8601 | Date range start |
| `filter[createdAtRange][to]` | ISO 8601 | Date range end |

## Response (200)

```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "sourceLanguage": "string",
      "targetLanguage": "string",
      "status": "string",
      "type": "string",
      "createdAt": "ISO8601",
      "clientId": "string",
      "projectId": "string"
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

## Example (curl)

> **Important:** Always use the `-g` (`--globoff`) flag with curl when query params contain brackets `[]`.
> Without it, curl misinterprets brackets as URL glob range specifiers and returns exit code 3 (URL malformed).

```bash
# List all orders (default pagination)
curl -g "https://api-integration.ollang.com/integration/orders" \
  -H "X-Api-Key: $OLLANG_API_KEY"

# Filter by type and date range
curl -g "https://api-integration.ollang.com/integration/orders?filter[type]=subtitle&filter[createdAtRange][from]=2024-01-01T00:00:00Z&filter[createdAtRange][to]=2024-12-31T23:59:59Z&pageOptions[take]=25" \
  -H "X-Api-Key: $OLLANG_API_KEY"

# Search by name
curl -g "https://api-integration.ollang.com/integration/orders?pageOptions[search]=my+video" \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Ask what filters they want to apply (if any): type, name search, date range
3. Build the query string with the appropriate parameters
4. **Always include `-g` flag** in curl commands — bracket params like `pageOptions[page]` cause exit code 3 without it
5. Display results in a table format: ID, Name, Type, Status, Languages, Created At
6. Show pagination info and offer to fetch the next page if `hasNextPage` is true

## Error Codes
- `400` - Invalid query parameters
- `401` - Invalid or missing API key
