# OpenMail Error Reference

All errors return a JSON body:
```json
{
  "error": {
    "code": "invalid_api_key",
    "message": "The API key provided is invalid or has been revoked."
  }
}
```

---

## Error codes

| HTTP | Code | Meaning | Action |
|---|---|---|---|
| 401 | `invalid_api_key` | Key missing, malformed, or revoked | Stop. Tell the user their API key is invalid. Direct them to console.openmail.sh → Settings → API Keys. |
| 403 | `forbidden` | Key valid but lacks permission for this resource | Stop. The inbox may belong to a different account. |
| 404 | `not_found` | Inbox or message does not exist | Check `OPENMAIL_INBOX_ID`. Re-run `openmail inbox list --json` to verify. |
| 409 | `conflict` | Duplicate request (e.g. same `client_id` for inbox creation) | Treat as success — the resource already exists. Fetch and use the existing one. |
| 422 | `validation_error` | Request body is malformed | Log the `message` field and fix the request. Do not retry without changes. |
| 429 | `rate_limited` | Too many requests | Wait for the `Retry-After` header value (seconds) before retrying. Default: 10 seconds. |
| 500 | `server_error` | OpenMail internal error | Retry up to 3 times with exponential backoff: 2s, 4s, 8s. If still failing, tell the user. |
| 503 | `service_unavailable` | Temporary outage | Same as 500. |

---

## Retry guidance

Only retry on `429`, `500`, and `503`. Never retry on `401`, `403`, `404`,
or `422` — these indicate a problem with the request itself, not a transient
failure.

Maximum 3 retries per request. After 3 failures, stop and report to the user.

---

## Credential troubleshooting

If you receive `401`:

1. Check the key is present: `echo $OPENMAIL_API_KEY`
2. Confirm it starts with `om_live_` (production) or `om_test_` (test)
3. Direct the user to generate a fresh key at console.openmail.sh
