# OpenClaw Dashboard

A local-first operations dashboard for OpenClaw. It combines system health, session activity, token and cost analytics, cron visibility, DGX Spark workloads, Local API Hub status, and an opt-in meeting Copilot.

## What is included

- **Overview** — today cost, tokens, alerts, watchdog, model mix, and active sessions
- **Usage** — model/source breakdowns, daily token and cost charts, and heatmaps
- **Cron** — run history, per-job costs, and daily trends
- **Health** — host status, watchdog signals, and runtime diagnostics
- **Spark** — DGX task history, GPU activity, token totals, and PR Hunter output
- **Copilot** — opt-in realtime transcript, PM insights, and RAG evidence
- **Config** — capabilities, installed skills, and workspace document views

The frontend follows the OpenClaw 2026.7 Control UI language: neutral layered surfaces, thin borders, red primary accent, left navigation on desktop, bottom navigation on small screens, and dark/light themes.

## Preview

These screenshots use the built-in `?preview=1` sample-data mode. No local hostnames, session names, tokens, or workspace details are included.

![OpenClaw Dashboard overview](https://raw.githubusercontent.com/JonathanJing/openclaw-dashboard/71604d6831bb24b9e8340bf0d1153a9545c5a038/screenshots/overview-v2-light.png)

![OpenClaw Dashboard usage analytics](https://raw.githubusercontent.com/JonathanJing/openclaw-dashboard/71604d6831bb24b9e8340bf0d1153a9545c5a038/screenshots/usage-v2-dark.png)

<img src="https://raw.githubusercontent.com/JonathanJing/openclaw-dashboard/71604d6831bb24b9e8340bf0d1153a9545c5a038/screenshots/mobile-v2-dark.png" alt="OpenClaw Dashboard mobile layout" width="390">

## Quick start

```bash
openclaw skills install @jonathanjing/openclaw-dashboard
cd ~/.openclaw/workspace/skills/openclaw-dashboard
cp env.example.txt .env
./start.sh
```

Open `http://127.0.0.1:18791/`.

Set `OPENCLAW_AUTH_TOKEN` in `.env` before exposing the dashboard beyond loopback. The launcher uses Node's env-file parser and starts `backend/server.js`.

Use the `/login` form for authentication. Query-string tokens are rejected so credentials do not enter browser history, referrers, or proxy access logs.

The header's **Control UI** link is supplied at runtime through `OPENCLAW_CONTROL_UI_URL`. Set the complete URL when your Gateway uses TLS, a non-default host, or `gateway.controlUi.basePath`.

## Architecture

```text
backend/
  server.js
  lib/
    config.js
    http-helpers.js
    sqlite-helper.js
  providers/
    sessions.js
    ledger.js
    cron.js
    watchdog.js
    system.js
    local-api-hub.js
    spark.js
    spark-tasks.js
    copilot.js
    config.js
    tasks.js

frontend/
  index.html
  shared/
    api.js
    boot.js
    styles.css
    ui-utils.js
  tabs/
    overview.js
    cost.js
    cron.js
    health.js
    spark-monitor.js
    copilot.js
    config.js
```

Runtime task data stays outside the skill directory:

```text
~/.openclaw/dashboard/
  tasks.json
  attachments/
```

## Core environment variables

| Variable | Default | Purpose |
|---|---|---|
| `DASHBOARD_HOST` | `127.0.0.1` | Bind address |
| `DASHBOARD_PORT` | `18791` | Dashboard port |
| `OPENCLAW_AUTH_TOKEN` | empty | Cookie/Bearer authentication |
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | Workspace root |
| `DASHBOARD_CORS_ORIGINS` | loopback only | Explicit allowed origins |
| `DASHBOARD_COOKIE_SECURE` | `0` | Add `Secure` to the auth cookie when this dashboard is served over HTTPS |
| `OPENCLAW_CONTROL_UI_URL` | `http://127.0.0.1:18789/` | Runtime Control UI link |
| `OPENCLAW_ENABLE_CONFIG_ENDPOINT` | `0` | Expose config details |

See `env.example.txt` for the complete list. `env.example` is retained as a compatibility mirror for Git/npm workflows.

## Meeting Copilot

Copilot is disabled by default. Enable it only when its dependencies are configured:

```bash
OPENCLAW_ENABLE_COPILOT=1
ALIBABA_CLOUD_API_KEY=your_alibaba_cloud_api_key
OPENCLAW_COPILOT_REDIS_URL=redis://127.0.0.1:6379
```

The browser requests confirmation and microphone access only after the operator clicks **Start**. The operator must confirm participant consent and cloud-audio disclosure before the stream begins. Its WebSocket upgrade requires dashboard authentication and rejects disabled or incomplete configurations.

Each connection receives a unique meeting ID and scoped Redis channels:

```text
meeting.<meetingId>.transcript
meeting.<meetingId>.rag_hits
meeting.<meetingId>.insights
```

For compatibility, only the first active meeting also publishes/subscribes on the original unscoped channels. Additional concurrent meetings never share those global channels.

## Security defaults

- Loopback bind by default; non-loopback bind is refused when no auth token is set
- Same-origin frontend API requests, so custom ports and reverse proxies work
- URL-encoded HttpOnly + SameSite=Strict cookie login; optional `Secure`; Bearer auth for API clients
- No API authentication through query parameters
- No automatic loading of `keys.env` or `~/.openclaw/.env`
- No task, file, restart, doctor, model-change, package-update, or legacy-proxy mutation routes
- Use the authenticated OpenClaw Control UI or CLI for operator actions
- Copilot and config-detail reads are opt-in
- Runtime data and secrets are excluded from the public skill bundle

See `SECURITY.md` for the complete threat model.

## Validation

```bash
npm test
```

The test suite checks startup, malformed Host/cookie resilience, cookie values containing `=`, token handoff redirects, read-only route boundaries, design contracts, tracked launch/test files, and public-safety patterns.

## License

MIT
