---
name: isitdown-now
description: Check whether major websites and online services are down, list confirmed outages, find reporting spikes, and retrieve measured uptime through the IsItDown.now API. Use for current service-status or outage-history questions; do not use it to diagnose a user's private network or to claim that one external measurement is conclusive.
---

# IsItDown.now

Use IsItDown.now for independent website-availability measurements, current confirmed outages, 30-day uptime, response times, and public report activity. The API is read-only and covers the services IsItDown.now monitors continuously.

Base URL: `https://isitdown.now`

## Choose the endpoint

- Overall network summary: `GET /api/v1/summary`. This is the only endpoint that works without a key.
- One monitored service: `GET /api/v1/status/<slug-or-domain>`.
- One monitored service with its report series, problem breakdown, and ten latest incidents: `GET /api/v1/status/<slug-or-domain>/detail`.
- Find valid slugs and domains: `GET /api/v1/services`.
- Filter the service directory: `GET /api/v1/services/<category>`.
- Confirmed outages happening now: `GET /api/v1/down`.
- Services with the most user reports in the past six hours: `GET /api/v1/trending`.

Use only these documented endpoints. Percent-encode path values and do not invent query parameters.

## Authentication

Send authenticated requests with:

```text
Authorization: Bearer <api-key>
```

Never put a key in a URL, output it to the user, commit it, or place it in browser-side code. Read it from the user's secret store or environment when available. If a key is missing, the summary endpoint can still answer broad questions. For any other endpoint, tell the user how to get a free key:

1. Open `https://isitdown.now/dashboard/api` and sign in.
2. Claim a domain the user controls.
3. Verify the domain with one offered method: a DNS TXT record, a meta tag, or the verification file.
4. Create a key and copy it when shown. The plaintext key is displayed only once.

The free tier permits 1,000 requests per UTC day across the account. Cache successful responses for at least 60 seconds and respect the `X-RateLimit-*` response headers.

## Call the API

Use the runtime's ordinary HTTP client. For example:

```bash
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer $ISITDOWN_API_KEY" \
  "https://isitdown.now/api/v1/status/github.com"
```

Treat non-2xx responses as errors. Handle these API error codes explicitly:

- `key_required` or HTTP 401: ask the user to configure a key in their secret store, without pasting it into chat, or use `/api/v1/summary` if that answers the question.
- `invalid_key` or HTTP 401: ask the user to replace or re-create the key.
- `quota_exceeded` or HTTP 429: report the reset at 00:00 UTC; do not retry in a loop.
- `rate_limited` or HTTP 429: stop and retry only after a reasonable delay or when the user asks.
- `unknown_service` or HTTP 404: call `/api/v1/services` to find the monitored domain. Do not treat an unknown service as down.

## Interpret results

For a service-status response, use `status`, `status_text`, `checked_at`, `response_ms`, `http_status`, `reports_24h`, `uptime_30d`, `current_outage`, and `url`.

- `down` means IsItDown.now confirmed an outage after two consecutive failed checks.
- `checking` means a failed check is awaiting confirmation.
- `reports` means the service answered IsItDown.now, but users are reporting problems. Reports alone never confirm an outage.
- `up`, `slow`, or `unknown` describe IsItDown.now's most recent external measurement, not the user's local connection.

State when the measurement was taken. Include the returned `url` as the evidence page. Distinguish confirmed outages from report spikes, and never present third-party measurements as the service provider's official status or as an uptime guarantee.

The REST API does not run on-demand checks of arbitrary domains. If the requested site is not in `/api/v1/services`, say that it is not continuously monitored. When an MCP client is available, the separate read-only server at `https://mcp.isitdown.now` can run a single live check through its `check_website` tool.
