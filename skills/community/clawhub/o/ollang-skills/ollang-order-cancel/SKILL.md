---
name: ollang-order-cancel
description: Cancel an active Ollang order. Use when the user wants to cancel a translation, captioning, or dubbing order that hasn't been completed yet.
---

# Ollang Cancel Order

Cancel an active order. Only eligible orders (not yet completed or already cancelled) can be cancelled.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

## Endpoint

**POST** `https://api-integration.ollang.com/integration/orders/cancel/{orderId}`

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orderId` | string | Yes | The unique order identifier to cancel |

### Request Body
No request body required.

## Response
- **204 No Content** — Order successfully cancelled

## Example (curl)
```bash
curl -X POST https://api-integration.ollang.com/integration/orders/cancel/ORDER_ID \
  -H "X-Api-Key: $OLLANG_API_KEY"
```

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Ask for the `orderId` if not provided
3. Confirm the cancellation with the user before proceeding (this action may affect billing)
4. Send the cancel request
5. On success (204), confirm the order has been cancelled
6. On error, explain why the cancellation failed

## Error Codes
- `400` - Order is not eligible for cancellation (wrong status)
- `401` - Invalid or missing API key
- `403` - Access denied
- `404` - Order not found
- `409` - Order already cancelled
