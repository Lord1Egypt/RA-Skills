# OpenProvider — Authentication & Error Handling

## Table of Contents

- [Authentication](#authentication)
- [Token Caching](#token-caching)
- [Credentials Sources](#credentials-sources)
- [Error Response Structure](#error-response-structure)
- [Common Error Codes](#common-error-codes)
- [Retry Strategy](#retry-strategy)

---

## Authentication

### POST /auth/login

Obtain a bearer token for all subsequent API calls.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/auth/login`

**Request:**

```json
{
  "username": "your-username",
  "password": "your-password"
}
```

**Response (success):**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "token": "eyJhbGciOi...",
    "reseller_id": 123456
  }
}
```

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "'"$OPENPROVIDER_USERNAME"'", "password": "'"$OPENPROVIDER_PASSWORD"'"}'
```

**Usage:** Include the token as `Authorization: Bearer {token}` header on all subsequent requests.

**Token Lifetime:** 48 hours (OpenProvider default). Atlas caches for 24h conservatively.

---

## Token Caching

- Token is cached in-memory with a 24h TTL
- On HTTP 401, the token is invalidated and re-fetched automatically
- `clearTokenCache()` available for testing

**Auto-refresh logic:**

1. Check if cached token exists and is not expired
2. If expired or missing → call `POST /auth/login`
3. On 401 during any request → invalidate cache → re-authenticate → retry once

---

## Credentials Sources

Credentials are resolved in order:

1. **Database:** `system_settings` table, key `integration_credentials_openprovider`
   - Value: `{ "username": "...", "password": "..." }`
   - Set via Admin > Settings > Integrations UI
2. **Environment variables:** `OPENPROVIDER_USERNAME` and `OPENPROVIDER_PASSWORD`

If neither is configured, operations fail with `CREDENTIALS_NOT_CONFIGURED` (HTTP 503).

### Test Credentials

```bash
# Verify credentials work (bypasses cache)
curl -X POST https://api.openprovider.eu/v1beta/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "'"$OPENPROVIDER_USERNAME"'", "password": "'"$OPENPROVIDER_PASSWORD"'"}'
```

Expected: `"code": 0` with a `token` and `reseller_id` in `data`.

---

## Error Response Structure

All OpenProvider API responses follow this structure:

```json
{
  "code": 0,
  "desc": "Description of the result",
  "data": { ... }
}
```

- `code: 0` → Success
- `code: != 0` → API-level error (mapped to HTTP 400 in Atlas)
- HTTP 4xx/5xx → Transport/auth errors

### Error Mapping in Atlas

| OpenProvider Signal          | Atlas Error Code   | HTTP Status |
|------------------------------|--------------------|-------------|
| HTTP 401                     | `HTTP_401`         | 401         |
| HTTP 400                     | `HTTP_400`         | 400         |
| HTTP 500/502/503/504         | `HTTP_5xx`         | Same        |
| `code != 0` in response     | `API_{code}`       | 400         |
| Request timeout (30s)        | `TIMEOUT`          | 504         |
| Network error                | `NETWORK_ERROR`    | 502         |
| Invalid JSON response        | `INVALID_RESPONSE` | 502         |

---

## Common Error Codes

| Code | Description | Cause / Fix |
|------|-------------|-------------|
| 0    | Success     | — |
| 801  | Domain already exists | Domain already registered at this registrar |
| 802  | Domain not found | Check domain ID or the domain was deleted |
| 817  | Duplicate DNS record | Remove existing record before re-adding (two-step PUT) |
| 899  | Rate limit exceeded | Wait and retry; reduce batch sizes |
| 1000 | Authentication failed | Invalid username/password |
| 1001 | Token expired | Re-authenticate via `/auth/login` |
| 2001 | Validation error | Check required fields in the request body |

---

## Retry Strategy

Atlas implements automatic retry for transient failures:

- **Max retries:** 3
- **Backoff delays:** 1s, 3s, 9s (exponential)
- **Retryable errors:** `TIMEOUT`, `NETWORK_ERROR`, `HTTP_500`, `HTTP_502`, `HTTP_503`, `HTTP_504`
- **Non-retryable:** All 4xx errors (auth, validation, not found)

---

## Base Configuration

| Setting | Value |
|---------|-------|
| API Host | `api.openprovider.eu` |
| Base Path | `/v1beta` |
| Full Base URL | `https://api.openprovider.eu/v1beta/` |
| Request Timeout | 30 seconds |
| Token TTL (cache) | 24 hours |
| Content-Type | `application/json` |
