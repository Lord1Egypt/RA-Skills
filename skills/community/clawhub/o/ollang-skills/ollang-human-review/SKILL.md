---
name: ollang-human-review
description: Request or cancel human review for an Ollang order. Human review assigns a professional linguist to review AI-generated translations. Use when the user wants to upgrade an order to human review or cancel an in-progress human review.
---

# Ollang Human Review

Request professional linguist review for an order, or cancel an in-progress human review.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

---

## Request Human Review

**POST** `https://api-integration.ollang.com/integration/orders/{orderId}/human-review`

Upgrades an AI-generated order to include professional human review. Charges additional credits.

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orderId` | string | Yes | The order to request human review for |

### Request Body
No request body required.

### Response
- **204 No Content** — Human review successfully requested

### Example
```bash
curl -X POST https://api-integration.ollang.com/integration/orders/ORDER_ID/human-review \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

---

## Cancel Human Review

**POST** `https://api-integration.ollang.com/integration/orders/{orderId}/cancel-human-review`

Cancels a human review that is currently in progress. Refunds credits and reverts to AI-only output.

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orderId` | string | Yes | The order to cancel human review for |

### Request Body
No request body required.

### Response (200)
```json
{
  "success": true,
  "message": "string",
  "orderId": "string"
}
```

### Example
```bash
curl -X POST https://api-integration.ollang.com/integration/orders/ORDER_ID/cancel-human-review \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

---

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Ask for the `orderId` if not provided
3. Determine action: **request** or **cancel** human review
4. For **request**: warn that this will charge additional credits; confirm before proceeding
5. For **cancel**: confirm before proceeding (credits will be refunded, reverts to AI-only)
6. Execute and report the outcome

## Error Codes
- `400` - Order not eligible (wrong status or not applicable)
- `401` - Invalid or missing API key
- `403` - Access denied
- `404` - Order not found
