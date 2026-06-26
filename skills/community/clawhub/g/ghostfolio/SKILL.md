---
name: ghostfolio
description: Manage and query Ghostfolio portfolio data (performance, holdings, dividends) using API endpoints and token auth patterns.
metadata: {"openclaw":{"emoji":"👻","requires":{"env":["GHOSTFOLIO_TOKEN"]},"primaryEnv":"GHOSTFOLIO_TOKEN"}}
---

# Ghostfolio

Use this skill when the user asks about Ghostfolio portfolio metrics, holdings, dividends, or API troubleshooting.

## Environment Variables

```bash
# Prefer local access when available
export GHOSTFOLIO_BASE_URL="http://127.0.0.1:3333"
# Optional remote example:
# export GHOSTFOLIO_BASE_URL="https://rpi5.gate-mintaka.ts.net:8444"

# Long-lived token supplied by user/admin
export GHOSTFOLIO_TOKEN="..."

# Optional but recommended
export GHOSTFOLIO_TIMEZONE="Europe/Paris"
```

## Auth Modes

Ghostfolio setups can differ. Support both modes:

### Mode A — Direct bearer (works in some environments)

```bash
AUTH_HEADER="Authorization: Bearer $GHOSTFOLIO_TOKEN"
```

### Mode B — Anonymous exchange (required in some environments)

```bash
AUTH_TOKEN=$(curl -fsS "$GHOSTFOLIO_BASE_URL/api/v1/auth/anonymous" \
  -H 'Content-Type: application/json' \
  --data "{\"accessToken\":\"$GHOSTFOLIO_TOKEN\"}" \
| jq -r '.authToken')

[ -n "$AUTH_TOKEN" ] && [ "$AUTH_TOKEN" != "null" ] || {
  echo "Failed to obtain authToken" >&2
  exit 1
}

AUTH_HEADER="Authorization: Bearer $AUTH_TOKEN"
```

## Endpoint Templates

### Portfolio performance

```bash
curl -fsS "$GHOSTFOLIO_BASE_URL/api/v2/portfolio/performance?range=ytd" \
  -H "$AUTH_HEADER" \
  -H 'Accept: application/json' \
  -H "x-ghostfolio-timezone: $GHOSTFOLIO_TIMEZONE" \
| jq .
```

### Holdings

```bash
curl -fsS "$GHOSTFOLIO_BASE_URL/api/v1/portfolio/holdings?range=ytd" \
  -H "$AUTH_HEADER" \
  -H 'Accept: application/json' \
  -H "x-ghostfolio-timezone: $GHOSTFOLIO_TIMEZONE" \
| jq .
```

### Dividends

```bash
curl -fsS "$GHOSTFOLIO_BASE_URL/api/v1/portfolio/dividends?groupBy=month&range=ytd" \
  -H "$AUTH_HEADER" \
  -H 'Accept: application/json' \
  -H "x-ghostfolio-timezone: $GHOSTFOLIO_TIMEZONE" \
| jq .
```

## Quick connectivity + auth probe

```bash
# 1) Try direct bearer first
for ep in \
  '/api/v2/portfolio/performance?range=ytd' \
  '/api/v1/portfolio/holdings?range=ytd' \
  '/api/v1/portfolio/dividends?groupBy=month&range=ytd'
do
  code=$(curl -s -o /tmp/gf_probe.json -w '%{http_code}' "$GHOSTFOLIO_BASE_URL$ep" \
    -H "Authorization: Bearer $GHOSTFOLIO_TOKEN" \
    -H 'Accept: application/json' \
    -H "x-ghostfolio-timezone: $GHOSTFOLIO_TIMEZONE")
  echo "direct $ep -> $code"
done

# 2) If direct is 401/403, try anonymous exchange
AUTH_TOKEN=$(curl -fsS "$GHOSTFOLIO_BASE_URL/api/v1/auth/anonymous" \
  -H 'Content-Type: application/json' \
  --data "{\"accessToken\":\"$GHOSTFOLIO_TOKEN\"}" | jq -r '.authToken')

echo "anonymous exchange token present: $([ -n "$AUTH_TOKEN" ] && [ "$AUTH_TOKEN" != "null" ] && echo yes || echo no)"
```

## Troubleshooting

- `401 Unauthorized`
  - Token invalid for this auth mode, token expired, or wrong token type.
  - Try the other auth mode (direct vs anonymous exchange).

- `403 Forbidden`
  - Token recognized but not authorized for the requested resources.
  - Verify account/environment and permissions.

- Timezone inconsistencies
  - Send `x-ghostfolio-timezone` (or at least `Timezone`) explicitly.

- Connectivity issues
  - Prefer local URL (`http://127.0.0.1:3333`) if service runs locally.
  - For remote TLS diagnostics only, temporary `curl -k` can help.

## Safety Notes

- Never print or commit real tokens in logs/docs.
- Keep tokens in environment variables only.
- Use `curl -fsS` so HTTP/API errors are not silently ignored.
