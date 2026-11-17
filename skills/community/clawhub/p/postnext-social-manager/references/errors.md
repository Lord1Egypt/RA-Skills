# Response shapes and errors

## Success envelopes are inconsistent - check per endpoint

| Shape | Endpoints |
|-------|-----------|
| `{success, data}` | most Posts, all Analytics, asset create-url/complete/get, single-post GET |
| `{success, data, meta}` | `GET /api/posts` when `?page`/`?limit` is present |
| `{success, data, pagination}` | `GET /api/assets/mine` (pagination is top-level, not `meta`) |
| **bare array** | `GET /api/connections` |
| **flat object, no wrapper** | `GET /api/v1/account`; connection `/check`; `upload/single` and `upload/url` (`{message, asset}`) |

When parsing, do not assume a `data` key. The `postnext` helper unwraps `data` only when present.

## Error shapes - there are three

1. Standard: `{ "success": false, "error": { "message": "..." } }` (validation, quota 403).
2. String variant: `{ "success": false, "error": "Authentication required" }` (401, bad/missing key) or `{ "success": false, "error": "Analytics is a paid feature", "code": "ANALYTICS_PAID_ONLY" }` (paid-tier gates). Here `error` is a string, not an object.
3. Payment (402): a separate top-level shape:
   ```jsonc
   { "error": "PAYMENT_REQUIRED", "code": "SUBSCRIPTION_INACTIVE",
     "status": "past_due", "currency": "usd",
     "actions": { "retryUrl": "...", "updateCardUrl": "...", "downgradeUrl": "..." } }
   ```

## Status codes

| Code | Meaning | What to tell the user |
|------|---------|-----------------------|
| 401 | bad or missing `x-api-key` | check the key |
| 402 | subscription in a payment-failure state | fix billing (use `actions.updateCardUrl`) |
| 403 | posting not allowed on the plan, or monthly post quota reached | upgrade or wait for the quota to reset |
| 413 | media over the size cap (50 MB presigned) | use the multipart single path, or shrink |
| 415 | uploaded bytes do not match the declared type | re-upload with the correct contentType |
| 422 | unsupported media for platform (e.g. video on LinkedIn) | remove the video or pick another channel |
| 429 | rate limited | back off and retry |

## Known quirks (live-verified)

- **GET a missing or just-deleted post returns HTTP 500**, not 404: `{"success":false,"error":"Internal Server Error","message":"Post group not found"}`. Treat a 500 whose `message` is `Post group not found` as not-found.
- A 500 whose body still parses as `{success:false, ..., message}` is a handled not-found/edge case, not necessarily an outage.

## Rate limits

Roughly: standard 100 requests / 15 min; social endpoints ~50 / 15 min; auth ~5 / 60 min. On a 429, pause and retry rather than hammering.
