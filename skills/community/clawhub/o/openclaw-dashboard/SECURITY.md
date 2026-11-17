# Security Model — OpenClaw Dashboard

## Boundary

This package is a local-first, read-only observability surface. It reads selected OpenClaw runtime files and local service endpoints to render health, session, usage, cron, Spark, and task views.

It does not register routes for task/file mutation, agent spawning, model changes, restart, doctor repair, package updates, backup/restore, or a legacy backend proxy. Use the authenticated OpenClaw Control UI or CLI for operator actions.

## Authentication

- **Primary:** URL-encoded HttpOnly + SameSite=Strict cookie (`ds`), set by `POST /login`.
- **HTTPS deployments:** Set `DASHBOARD_COOKIE_SECURE=1` so the cookie also carries `Secure`.
- **API clients:** `Authorization: Bearer <token>` is supported.
- **Login boundary:** Authentication is accepted only through `POST /login`, the `ds` cookie, or a Bearer header.
- **Query boundary:** Query-string tokens are rejected on all routes so credentials do not enter browser history, referrers, or proxy access logs.
- **No browser token storage:** The frontend does not write the token to localStorage or sessionStorage.
- **Bind safety:** The default bind is `127.0.0.1`; the server refuses a non-loopback bind when `OPENCLAW_AUTH_TOKEN` is empty.

Incoming request URLs are parsed against a fixed internal base. An invalid or attacker-controlled `Host` header is never used as the URL base.

## Capability boundaries

| Surface | Default | Boundary |
|---|---|---|
| Runtime metrics, sessions, usage, cron, tasks | Enabled after dashboard auth | Read-only |
| Config details | Disabled | Requires `OPENCLAW_ENABLE_CONFIG_ENDPOINT=1`; values are redacted |
| Meeting Copilot | Disabled | Requires `OPENCLAW_ENABLE_COPILOT=1`, `ALIBABA_CLOUD_API_KEY`, and authenticated WebSocket upgrade |
| Operator actions | Not registered | Use OpenClaw Control UI or CLI |

The public `/health` response reports these boundaries through `capabilities`.

## Meeting Copilot

- Microphone access begins only after an explicit **Start** click and a confirmation covering participant consent and cloud-audio processing.
- WebSocket upgrades reject unauthenticated, disabled, or incomplete configurations.
- WebSocket messages are bounded by a 64 KiB maximum payload.
- Credentials come only from the process environment; the provider does not scan `keys.env` or `~/.openclaw/.env`.
- Each browser connection gets a random meeting ID and scoped Redis channels:

```text
meeting.<meetingId>.transcript
meeting.<meetingId>.rag_hits
meeting.<meetingId>.insights
```

Only the first active meeting receives legacy unscoped-channel compatibility. Concurrent meetings do not share global Redis events.

## Browser output safety

- Markdown output is sanitized with DOMPurify before insertion.
- Non-Markdown dynamic text uses `escHtml()` or text nodes.
- Frontend API calls are same-origin.
- The Control UI link is supplied by the authenticated runtime health configuration and hidden when a loopback target would be unusable for a remote viewer.

## Local data and subprocesses

- Runtime task data is stored under `~/.openclaw/dashboard/`, outside the skill bundle.
- Config, session, cron, watchdog, and ledger data remain under `~/.openclaw/`.
- The dashboard never writes credentials to disk.
- SQLite reads invoke the `sqlite3` executable with an argument array and no shell expansion.

## Request hardening

- Malformed cookie fragments are ignored instead of throwing.
- Cookie values are split on the first `=` and percent-decoded per fragment.
- Request bodies and Copilot WebSocket payloads have explicit size limits.
- CORS is loopback-only by default; set `DASHBOARD_CORS_ORIGINS` to an explicit comma-separated allowlist for other origins.

## Security flow

```text
Request → safe URL parse → auth → registered read route or opt-in Copilot → bounded output
```
