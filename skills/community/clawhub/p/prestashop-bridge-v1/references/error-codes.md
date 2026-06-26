# Error Codes

## Standard business errors
- `PRODUCT_NOT_FOUND`
- `INVALID_PRICE`
- `STOCK_INSUFFICIENT`
- `SKU_ALREADY_EXISTS`
- `ORDER_ALREADY_SHIPPED`
- `INVALID_STATUS_TRANSITION`
- `RATE_LIMIT_EXCEEDED`
- `MAINTENANCE_MODE`
- `IDEMPOTENCY_CONFLICT`
- `IMAGE_HASH_MISMATCH`

## Error payload shape
Every business error should follow the normalized error response schema and include:
- `error_code`
- `message`
- `context`
- `retryable`
- optional `job_id`
