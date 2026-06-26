---
name: ollang-revision
description: Manage revisions for Ollang orders — create, list, and delete revision requests. Use when the user wants to report subtitle errors, sync issues, or other problems with a completed order.
---

# Ollang Revision Management

Create, retrieve, and delete revision requests for orders.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

---

## Create a Revision

**POST** `https://api-integration.ollang.com/integration/revision/{orderId}`

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orderId` | string | Yes | The order to create a revision for |

### Request Body (JSON)
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Revision type (see below) |
| `time` | string | Yes | Timestamp in `HH:MM:SS` format |
| `description` | string | No | Additional details about the issue |

### Revision Types
| Value | Description |
|-------|-------------|
| `missingSubtitle` | Missing subtitle segment |
| `wrongSubtitle` | Incorrect subtitle content |
| `syncError` | Subtitle timing/sync issue |
| `formatError` | Formatting problem |
| `other` | Other issue |

### Response (201)
```json
{
  "id": "string",
  "createdAt": "ISO8601",
  "type": "string",
  "time": "HH:MM:SS",
  "description": "string"
}
```

### Example
```bash
curl -X POST https://api-integration.ollang.com/integration/revision/ORDER_ID \
  -H "X-Api-Key: $OLLANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "syncError",
    "time": "00:02:35",
    "description": "Subtitle appears 2 seconds late"
  }'
```

---

## Get All Revisions for an Order

**GET** `https://api-integration.ollang.com/integration/revision/{orderId}`

### Response (200)
Array of revision objects with `id`, `createdAt`, `type`, `time`, `description`.

### Example
```bash
curl -X GET https://api-integration.ollang.com/integration/revision/ORDER_ID \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

---

## Delete a Specific Revision

**DELETE** `https://api-integration.ollang.com/integration/revision/{orderId}/{revId}`

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orderId` | string | Yes | The order ID |
| `revId` | string | Yes | The revision ID to delete |

### Response
- **204 No Content** — Revision deleted successfully

### Example
```bash
curl -X DELETE https://api-integration.ollang.com/integration/revision/ORDER_ID/REV_ID \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

---

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Determine the action: create, list, or delete a revision
3. For **create**: ask for `orderId`, `type`, `time` (HH:MM:SS), and optional `description`
4. For **list**: ask for `orderId` and display all revisions in a table
5. For **delete**: ask for `orderId` and `revId`, confirm before deleting
6. Return confirmation and the revision details

## Error Codes
- `400` - Invalid parameters or orderId/revId mismatch
- `401` - Invalid or missing API key
- `403` - Access denied
- `404` - Order or revision not found
