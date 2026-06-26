# NextDNS API summary

Source: https://nextdns.github.io/api/ fetched 2026-05-01. Treat upstream docs as authoritative; API is marked beta.

## Auth

- Base URL: `https://api.nextdns.io`
- Header: `X-Api-Key: <key>`
- API key is available in the NextDNS account page.

## Response shape

Successful API responses usually return:

```json
{ "data": {}, "meta": {} }
```

Errors may return:

```json
{ "errors": [{ "code": "invalid", "detail": "...", "source": { "parameter": "limit" } }] }
```

Many array endpoints paginate with `meta.pagination.cursor`. Pass `cursor=<value>` for the next page; `cursor: null` means no more pages.

## Core endpoints

- `GET /profiles` — list profiles.
- `GET /profiles/:profile` — read full profile config.
- `PATCH /profiles/:profile` — modify profile config. Do not use without explicit user confirmation and a backup/export.
- Nested profile objects support GET/PATCH, e.g. `/profiles/:profile/settings/performance`.
- Nested arrays support GET/PUT/POST and child PATCH/DELETE, e.g. `/profiles/:profile/denylist`.

## Analytics

Base: `/profiles/:profile/analytics/*`

Supported common query parameters:

- `from`, `to`: ISO, Unix seconds/ms, relative (`-6h`, `-1d`, `now`), common dates.
- `limit`: 1..500.
- `cursor`: pagination cursor.
- `device`: device id or `__UNIDENTIFIED__`.

Endpoints:

- `status`
- `domains` with optional `status=default|blocked|allowed`, `root=true|false`
- `reasons`
- `ips`
- `devices`
- `protocols`
- `queryTypes`
- `ipVersions`
- `dnssec`
- `encryption`
- `destinations?type=countries|gafam`

Time series: append `;series`, e.g. `/analytics/status;series?from=-7d&interval=1d`.
Additional series params: `interval`, `alignment=start|end|clock`, `timezone=<IANA>`, `partials=none|start|end|all`.

## Logs

Base: `GET /profiles/:profile/logs`

Query parameters:

- `from`, `to`, `sort=asc|desc`, `limit` 10..1000, `cursor`, `device`.
- `status=default|error|blocked|allowed`.
- `search=<string>`.
- `raw=1` to include all DNS queries; default is deduped navigational A/AAAA/HTTPS plus noise filtering.

Streaming: `GET /profiles/:profile/logs/stream` is SSE. Use only when explicitly needed for live monitoring.
Download: `GET /profiles/:profile/logs/download`. Clear: `DELETE /profiles/:profile/logs`; destructive, ask first.
