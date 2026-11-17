# REST API and deployment

A FastAPI server exposes the same operations over HTTP, for agents or
services that can't run Python.

```bash
pip install "gsuite-sdk[api,cli]"
export GSUITE_API_KEY="$(openssl rand -hex 32)"
gsuite auth login                 # the server uses the saved token
gsuite serve --port 8080          # binds 127.0.0.1; --host 0.0.0.0 to expose it
```

Every endpoint except `/health` needs the `X-API-Key` header matching
`GSUITE_API_KEY`. With no key set the server rejects every request, unless
`GSUITE_ALLOW_NO_API_KEY=true` (only when access is restricted another way).
Interactive docs: `http://127.0.0.1:8080/docs`.

```bash
curl -H "X-API-Key: $GSUITE_API_KEY" "http://127.0.0.1:8080/gmail/messages/unread?limit=10"
curl -H "X-API-Key: $GSUITE_API_KEY" "http://127.0.0.1:8080/calendar/events/today"
curl -G -H "X-API-Key: $GSUITE_API_KEY" "http://127.0.0.1:8080/drive/files" \
     --data-urlencode "query=name contains 'invoice'"
curl -H "X-API-Key: $GSUITE_API_KEY" "http://127.0.0.1:8080/sheets/SPREADSHEET_ID/values/Data!A1:D20"
curl -H "X-API-Key: $GSUITE_API_KEY" "http://127.0.0.1:8080/tasks/lists/@default/tasks"
curl -H "X-API-Key: $GSUITE_API_KEY" "http://127.0.0.1:8080/contacts/search?q=ana"
```

Route groups: `/gmail` (messages, threads, drafts, labels, filters, reply,
forward, attachments), `/calendar` (events, quickAdd, freebusy, calendars),
`/drive` (files, upload, content, copy, move, trash, folders, permissions),
`/sheets` (values, batchGet/batchUpdate, worksheets, format, freeze, protect,
upsert, dropdown, conditional format, export), `/tasks`, `/contacts`.

Errors are RFC 9457 `application/problem+json`: 401 bad or missing key or
Google login, 403 permission/scope, 404 not found, 422 invalid input, 429 rate
limit (with `Retry-After`), 502 Google error. Every response has an
`X-Request-ID`.

## Running on Cloud Run

Store the token in Secret Manager instead of `tokens.db`:

```bash
pip install "gsuite-sdk[all]"
gsuite auth login
gsuite auth export > token.json          # upload it as the secret's first version
```

Then run the container (`api/Dockerfile` in the repo) with
`GSUITE_TOKEN_STORAGE=secretmanager`, `GSUITE_GCP_PROJECT_ID=...`,
`GSUITE_TOKEN_SECRET_NAME=...` and `GSUITE_API_KEY=...`. Refreshed tokens are
written back to the secret.

## Other settings

| Variable | Meaning |
|---|---|
| `GSUITE_REQUEST_TIMEOUT` | Seconds per Google request (default 30) |
| `GSUITE_MAX_RETRIES` / `GSUITE_RETRY_DELAY` | Retries with exponential backoff for rate limits and 5xx |
| `GSUITE_RATE_LIMIT` / `GSUITE_RATE_LIMIT_BURST` | Requests per second to Google, per process (off by default) |
| `GSUITE_CORS_ORIGINS` | Comma-separated origins for browsers (CORS off by default) |
| `GSUITE_LOG_FORMAT` | `json` for one JSON object per line (Cloud Logging) |
