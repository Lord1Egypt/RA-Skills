# Servers Reference

Servers are collaborative workspaces where content is organized. Each document, sheet, or slide can belong to a server or to your personal files (no server).

## List Servers

**REST API:**

```
GET /v1/servers
```

No query parameters. Returns all servers accessible to your API key. No specific scope required.

```bash
curl https://api.mila.gg/v1/servers \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `list_servers`

No parameters.

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "xK9mP2wQ",
      "name": "Engineering",
      "uuid": "abc123",
      "description": "Engineering team workspace",
      "profile_image_url": null,
      "created_at": "2026-01-15T10:00:00.000Z",
      "updated_at": "2026-02-20T14:30:00.000Z"
    }
  ]
}
```

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `id` | string | Server ID. Use this as `server_id` when creating or filtering content. |
| `name` | string | Server display name |
| `uuid` | string | Server UUID |
| `description` | string or null | Server description |
| `profile_image_url` | string or null | URL to the server's profile image |
| `created_at` | string | ISO 8601 creation timestamp |
| `updated_at` | string | ISO 8601 last update timestamp |

## Using server IDs

Server IDs are used in two ways:

### Filtering content by server

All list endpoints (`GET /documents`, `GET /sheets`, `GET /slides`) accept an optional `server_id` query parameter:

| Value | Effect |
|---|---|
| *(omitted)* | Returns all accessible content (personal + all servers) |
| `personal` | Returns only personal files (not in any server) |
| `<server_id>` | Returns only content in that specific server |

```bash
# All documents across personal files and all servers
curl https://api.mila.gg/v1/documents \
  -H "Authorization: Bearer mila_sk_your_key_here"

# Only personal documents
curl "https://api.mila.gg/v1/documents?server_id=personal" \
  -H "Authorization: Bearer mila_sk_your_key_here"

# Only documents in a specific server
curl "https://api.mila.gg/v1/documents?server_id=xK9mP2wQ" \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

MCP tools: Use the `server_id` parameter on `list_documents`, `list_sheets`, or `list_slides`.

### Creating content in a server

Pass `server_id` in the request body when creating documents, sheets, or slides:

```bash
curl -X POST https://api.mila.gg/v1/documents \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sprint Planning",
    "content": "<h1>Sprint 24</h1><p>Goals for this sprint...</p>",
    "server_id": "xK9mP2wQ"
  }'
```

If `server_id` is omitted or `null`, the content is saved to your personal files. If the server doesn't exist or you don't have access, you get a `400` error.
