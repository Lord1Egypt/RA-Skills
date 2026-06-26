---
name: ollang-order-rerun
description: Rerun an Ollang order to regenerate translations using the latest AI models. Use when the user wants to refresh or redo a completed translation order.
---

# Ollang Rerun Order

Rerun an existing order to regenerate its output using the latest available AI models.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

## Endpoint

**POST** `https://api-integration.ollang.com/integration/orders/{orderId}/rerun`

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orderId` | string | Yes | The unique order identifier to rerun |

### Request Body
Optional empty object `{}` or no body.

## Response (200)
```json
{
  "success": true,
  "message": "string",
  "orderId": "string"
}
```

## Example (curl)
```bash
curl -X POST https://api-integration.ollang.com/integration/orders/ORDER_ID/rerun \
  -H "X-Api-Key: $OLLANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Ask for the `orderId` if not provided
3. Confirm with the user — rerunning will regenerate the translation (may consume credits)
4. Send the rerun request
5. On success, confirm the order has been queued for reprocessing
6. Suggest using `ollang-order-get` to monitor the order status

## Error Codes
- `400` - Order is not eligible for rerun
- `401` - Invalid or missing API key
- `403` - Access denied
- `404` - Order not found
