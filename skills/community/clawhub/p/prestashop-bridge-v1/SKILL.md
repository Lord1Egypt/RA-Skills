---
name: prestashop_bridge_v1
version: 1.0.3
description: Secure skill pack for operating a PrestaShop 9 Bridge through a stable, signed, asynchronous API contract.
license: MIT-0
metadata:
  author: "OpenAI"
  protocol: "https"
  base_path: "/v1"
  auth_type: "oauth2_client_credentials"
  oauth_token_url: "/oauth/token"
  oauth_scopes: "bridge:read bridge:write"
  jwt_algorithm: "RS256"
  hmac_required: true
  hmac_algorithm: "SHA256"
  idempotency_header: "X-Request-ID"
  rate_limit_read: "100/min"
  rate_limit_write: "20/min"
  max_payload_bytes: 10485760
  gzip_recommended_above_bytes: 1024
  gzip_required_above_bytes: 32768
  source_of_truth_jobs: "mysql"
---

# PrestaShop Bridge V1

PrestaShop Bridge V1 is a secure operational contract for AI agents and Python handlers that need to interact with a PrestaShop 9 store through a stable interface. It standardizes OAuth2 authentication, HMAC request signing, rate limiting, asynchronous writes, idempotency, and durable job polling.

## Operating model

- Reads are synchronous.
- Writes are asynchronous.
- Redis is used only for Messenger transport and temporary HTTP idempotency cache.
- MySQL is the source of truth for job status, business idempotency, and failed jobs.
- A `202 Accepted` response means only that a job was accepted for processing. It never means business success.

## Capabilities

### get_product
- method: `GET`
- endpoint: `/v1/products/{id}`
- sync: `true`
- scope: `bridge:read`
- params:
  - `id` integer, required
- success: `200`

### get_order
- method: `GET`
- endpoint: `/v1/orders/{id}`
- sync: `true`
- scope: `bridge:read`
- params:
  - `id` integer, required
- success: `200`

### get_job_status
- method: `GET`
- endpoint: `/v1/jobs/{jobId}`
- sync: `true`
- scope: `bridge:read`
- note: job status is read from MySQL, not from Redis
- success: `200`

### update_product
- method: `POST`
- endpoint: `/v1/jobs/products/update`
- sync: `false`
- scope: `bridge:write`
- idempotency: `X-Request-ID` required
- payload:
  - `product_id`
  - `updates.price_ht`
  - `updates.stock_delta`
  - `updates.seo`
  - `options.skip_reindex`
- success: `202`

### import_products
- method: `POST`
- endpoint: `/v1/jobs/products/import`
- sync: `false`
- scope: `bridge:write`
- idempotency: request id required and stable `batch_id`
- payload:
  - `batch_id`
  - `items`
  - `options`
- constraints:
  - maximum `50` items
  - maximum payload size `10MB`
- success: `202`

### update_order_status
- method: `POST`
- endpoint: `/v1/jobs/orders/status`
- sync: `false`
- scope: `bridge:write`
- idempotency: `X-Request-ID` required
- payload:
  - `order_id`
  - `new_status`
  - `notify_customer`
  - `tracking_number`
- success: `202`

## Security

### Required headers on protected routes
- `Authorization: Bearer {jwt_rs256_token}`
- `X-Request-ID: {uuid_v4}`
- `X-Timestamp: {unix_seconds}`
- `X-Signature: {hmac_sha256_hex}`
- `Content-Type: application/json`
- `Accept: application/json`

### Compression
- gzip recommended above `1024` bytes
- gzip required above `32768` bytes

### OAuth2
- flow: `client_credentials`
- token endpoint: `/oauth/token`
- JWT algorithm: `RS256`
- TTL: `3600`
- scopes:
  - `bridge:read`
  - `bridge:write`

### HMAC
String to sign:

`METHOD + "\n" + URI + "\n" + TIMESTAMP + "\n" + REQUEST_ID + "\n" + BODY_SHA256`

Exact example:
- method: `POST`
- uri: `/v1/jobs/products/update`
- timestamp: `1710950400`
- request id: `f47ac10b-58cc-4372-a567-0e02b2c3d479`
- body sha256: `37abd647733fbd18a3f11fb5a082fe59c62719d9fe833aec96b28ccea36b70ba`
- signature: `448e251d1c71078b07a10baf4094fd2686bcebef97761c4729a921f71798554c`

## Response handling

- `200 OK`: synchronous read success or completed idempotent replay.
- `202 Accepted`: job accepted only. Always poll `/v1/jobs/{jobId}`.
- `400 Bad Request`: schema validation failed.
- `401 Unauthorized`: JWT missing, invalid, or expired.
- `403 Forbidden`: invalid HMAC, invalid timestamp window, or insufficient scope.
- `409 Conflict`: idempotency conflict or known failed replay.
- `422 Unprocessable Entity`: valid JSON but impossible business transition.
- `429 Too Many Requests`: wait for `Retry-After`.
- `500 Internal Server Error`: unexpected server failure.
- `503 Service Unavailable`: service degraded or Redis unavailable.

## Absolute refusal rules

- Never report business success immediately after a `202`.
- Never modify TTC price directly. Only HT price may be changed.
- Never delete a product that has associated orders.
- Never access the database or filesystem directly.
- Never send payloads larger than `10MB`.
- Never perform heavy writes synchronously.
- Never reuse an `X-Request-ID` for a different business intention within 24 hours.

## Pre-deployment checks

- Verify JWT issuance and validation with RS256 only.
- Verify the exact HMAC example in `examples.http`.
- Verify schema validation for all request bodies.
- Verify Redis-backed idempotency replay behavior.
- Verify MySQL-backed job polling after Redis restart.
- Verify idempotent handlers under at-least-once delivery.
