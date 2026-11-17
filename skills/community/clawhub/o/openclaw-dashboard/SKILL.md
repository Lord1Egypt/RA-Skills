---
name: openclaw-dashboard
description: OpenClaw operations dashboard for sessions, usage and cost, cron runs, gateway health, DGX Spark work, Local API Hub, and opt-in meeting Copilot. Use when installing, operating, auditing, or extending the dashboard backend, frontend tabs, security model, or OpenClaw-aligned design.
metadata:
  openclaw:
    version: "2.0.2"
    emoji: "📊"
    homepage: https://github.com/JonathanJing/openclaw-dashboard
    requires:
      bins: [node, openclaw]
    primaryEnv: OPENCLAW_AUTH_TOKEN
    envVars:
      - name: OPENCLAW_AUTH_TOKEN
        required: true
        description: Authentication token required before the dashboard starts.
      - name: OPENCLAW_ENABLE_CONFIG_ENDPOINT
        required: false
        description: Opt in to redacted configuration inspection.
      - name: OPENCLAW_ENABLE_COPILOT
        required: false
        description: Opt in to meeting audio processing.
      - name: ALIBABA_CLOUD_API_KEY
        required: false
        description: Realtime provider credential used only when Copilot is enabled.
---

# OpenClaw Dashboard Skill

## Preview

The published screenshots use deterministic `?preview=1` sample data, never local host or workspace data.

![OpenClaw Dashboard overview](https://raw.githubusercontent.com/JonathanJing/openclaw-dashboard/71604d6831bb24b9e8340bf0d1153a9545c5a038/screenshots/overview-v2-light.png)

![OpenClaw Dashboard usage analytics](https://raw.githubusercontent.com/JonathanJing/openclaw-dashboard/71604d6831bb24b9e8340bf0d1153a9545c5a038/screenshots/usage-v2-dark.png)

<img src="https://raw.githubusercontent.com/JonathanJing/openclaw-dashboard/71604d6831bb24b9e8340bf0d1153a9545c5a038/screenshots/mobile-v2-dark.png" alt="OpenClaw Dashboard mobile layout" width="390">

## 🛠️ Installation

### 1. Ask OpenClaw (Recommended)
Tell OpenClaw: *"Install the openclaw-dashboard skill."* The agent will handle the installation and configuration automatically.

### 2. Manual Installation (CLI)
```bash
openclaw skills install @jonathanjing/openclaw-dashboard
```

## Mission

Keep this repository public-safe and easy to run. Prioritize:
1. Secret sanitization
2. Minimal setup steps
3. Stable API/UI behavior

## Architecture (v2.0)

The dashboard uses a **modular backend + tab-based frontend** architecture.

**Backend entry point:** `backend/server.js`  
**Business logic:** `backend/providers/` — one file per data domain  
**Frontend:** `frontend/tabs/` + `frontend/shared/` — one JS file per tab  
**Runtime data:** stored in `~/.openclaw/dashboard/` (outside skill dir, not Git-tracked)

### Provider map
| Provider | Routes | Responsibility |
|---|---|---|
| `sessions.js` | `/ops/sessions`, `/api/sessions` | Session stats + model |
| `ledger.js` | `/ops/ledger/*`, `/api/cost/*` | SQLite token/cost data |
| `cron.js` | `/ops/cron`, `/ops/cron-costs`, `/cron/today` | Cron jobs + run history + cost breakdown |
| `watchdog.js` | `/ops/watchdog` | Watchdog state + timeline |
| `spark.js` | `/ops/dgx-status`, `/api/spark/*` | DGX Spark inference node |
| `system.js` | `/ops/system` | Host metrics (CPU/RAM/disk) |
| `local-api-hub.js` | `/ops/local-api-hub/*` | Unified local control-plane status |
| `spark-tasks.js` | `/api/spark/tasks/*` | DGX task history and PR Hunter output |
| `copilot.js` | `/api/copilot/status`, `/api/copilot/ws` | Opt-in realtime transcript/RAG/insights |
| `ground-truth.js` | `/api/ground-truth/*`, `/ops/models` | Model registry + colors |
| `tasks.js` | `/tasks`, `/tasks/:id`, `/logs` | Read-only task/history views |
| `config.js` | `/ops/config`, `/files`, `/skills` | Read-only config, file, and skill views |
| `ops-legacy.js` | `/ops/channels`, `/ops/alltime`, `/ops/audit`, `/memory` | Read-only compatibility views |

### Frontend tab map
| Tab | File | Key functions |
|---|---|---|
| Overview | `tabs/overview.js` | `loadSessions()`, `loadTasks()` |
| Cost | `tabs/cost.js` | `loadOpsChannels()`, `loadOpsAlltime()` |
| Cron | `tabs/cron.js` | `loadCronEnhanced()`, `loadCronCosts()`, `loadCronRuns()` |
| Health | `tabs/health.js` | `renderAgentMonitor()`, `loadSystemInfo()`, `renderWatchdogStatus()` |
| Spark | `tabs/spark-monitor.js` | `loadSparkMonitor()`, task history, GPU activity |
| Copilot | `tabs/copilot.js` | capability check, microphone stream, transcript/RAG/insights |
| Config | `tabs/config.js` | `loadConfig()`, `loadSkills()`, `loadFileList()` |
| Shared | `shared/api.js` | Auth, `apiFetch()`, watchdog renderers, toast, markdown |
| Shared | `shared/ui-utils.js` | `timeSince()`, task state |
| Shared | `shared/boot.js` | Init, week nav, chart renderers, confirm dialog |

## Apply when

Use this skill for:
- Dashboard feature requests (sessions, cost, cron, watchdog, operations)
- Backend route additions/fixes in `backend/providers/`
- Frontend behavior updates in `frontend/tabs/` or `frontend/shared/`
- README, setup, and environment simplification
- Public release checks for accidental sensitive data

## Key rules for agents editing this codebase

1. **No duplicate function definitions** across `api.js` and `ui-utils.js`. Shared utilities belong in `api.js` (loaded first). `ui-utils.js` only holds `timeSince()` and task state.
2. **Cross-tab function calls are implicit** — JS shares the same `window` scope. Keep shared helpers in `shared/` files.
3. **Runtime data goes to `~/.openclaw/dashboard/`**, not skill root. Path is set in `backend/lib/config.js` via `OPENCLAW_DASHBOARD_TASKS` env or default.
4. **`/ops/models` returns `{ registry: {...object...}, colors, displayNames, models }`** — `registry` must be an object keyed by alias, not an array.
5. **`/ops/cron-costs` returns `{ summary, jobs, dailyTrend, review, rows }`** — all five keys required for Cron tab to render correctly.
6. **`hideStale` query param** on `/ops/sessions` filters sessions with no activity for 7+ days.
7. **Frontend API calls are same-origin**. Never reintroduce a hardcoded dashboard/gateway port list.
8. **Copilot is opt-in**. Require `OPENCLAW_ENABLE_COPILOT=1`, an API key, authenticated WebSocket upgrade, and safe dependency failure states.
9. **Parse request URLs against a fixed internal base**. Never build a URL from the request `Host` header.
10. **Treat query-token login as a compatibility handoff only**. Set the cookie and redirect before serving HTML; never accept query tokens on API routes.
11. **Parse cookies per fragment**. Split on the first `=`, catch percent-decoding errors, and encode cookie values when setting them.
12. **Keep the shipped dashboard read-only**. Do not add task/file mutations, restart/doctor actions, model changes, package updates, backup/restore, or legacy proxying.
13. **Scope Copilot Redis events by meeting ID**. Permit unscoped legacy channels only for the first active meeting.
14. **Track the launcher and test harness**. Keep `start.sh` and `scripts/test-dashboard.js` in both Git and `package.json#files`.
15. **Use theme tokens in canvas rendering**. Never hardcode light-only chart text or borders.

## OpenClaw design alignment

- Reuse the current Control UI tokens: Inter/system typography, layered neutral surfaces, thin borders, 10–14px radii, red primary accent, semantic green/yellow/red/blue.
- Keep the desktop shell as left navigation + sticky topbar; use bottom navigation on narrow screens.
- Prefer flat cards and strong information hierarchy over gradients, glow, or decorative motion.
- Support dark and light modes, visible focus states, reduced motion, and responsive layouts.
- Keep IDs and `data-tab` contracts stable when changing navigation or visual structure.

## Public-safety guardrails

- Never hardcode tokens, API keys, cookies, or host-specific secrets.
- Require `OPENCLAW_AUTH_TOKEN`; do not start the dashboard without authentication.
- Never commit machine-specific absolute paths.
- Prefer `process.env.*` and safe defaults based on `HOME`.
- Keep examples as placeholders (`your_token_here`, `/path/to/...`).
- If uncertain, redact first and ask the user before exposing details.
- Keep sensitive behaviors opt-in (do not silently load local secret files).

## Runtime access declaration

The bundled server can access local OpenClaw files for dashboard views:
- Sessions, cron runs, watchdog state under `~/.openclaw/...`
- Local workspace files under `OPENCLAW_WORKSPACE`
- Task data in `~/.openclaw/dashboard/tasks.json`
- Task attachments in `~/.openclaw/dashboard/attachments/`

High-sensitivity features are disabled by default and require explicit env flags:
- `OPENCLAW_ENABLE_CONFIG_ENDPOINT=1` to expose `/ops/config`
- `OPENCLAW_ENABLE_COPILOT=1` plus `ALIBABA_CLOUD_API_KEY` to enable meeting Copilot

Network security:
- CORS restricted to loopback by default.
- Auth via HttpOnly cookie (`ds`) or `Authorization: Bearer` header.
- Set `DASHBOARD_COOKIE_SECURE=1` only when the dashboard origin uses HTTPS.
- Set `OPENCLAW_CONTROL_UI_URL` to the complete runtime URL when Gateway TLS or `gateway.controlUi.basePath` is enabled.
- Set `DASHBOARD_CORS_ORIGINS` (comma-separated) for external origins.

## Default implementation workflow

1. Identify which provider or tab file owns the feature.
2. Implement the smallest change that preserves behavior.
3. Check: does any other tab/shared file also define the same function? If yes, deduplicate.
4. Run a sensitive-string scan before finalizing.
5. Run `npm test`, `git diff --check`, and `npm pack --dry-run --json`.
6. Ensure docs match the actual runtime defaults.

## Sensitive-data checks

Before final response, scan for:
- `token=`, `OPENCLAW_AUTH_TOKEN`, `OPENCLAW_HOOK_TOKEN`
- `API_KEY`, `SECRET`, `PASSWORD`, `COOKIE`
- absolute paths like `/Users/`, `C:\\`, machine names, personal emails

If found: replace with env-based values or placeholders, and mention what was sanitized.

## Files to touch most often

- `backend/providers/*.js` — server behavior and API routes
- `frontend/tabs/*.js` — tab-specific UI logic
- `frontend/shared/api.js` — auth, fetch, shared renderers
- `backend/lib/config.js` — path and env configuration
- `README.md` — quick start and operator docs
- `env.example.txt` — ClawHub-compatible public-safe environment template
- `env.example` — compatibility mirror for Git/npm workflows
