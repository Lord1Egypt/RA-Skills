# HealthClaw Skill

**Connect your iPhone/Apple Watch health data to OpenClaw for AI-powered analysis.**

HealthClaw streams Apple Health data (heart rate, HRV, sleep, steps, workouts) to your
OpenClaw agent via a local webhook server. Once connected, your agent can calculate
recovery scores, detect health anomalies, answer questions about your health trends,
and proactively alert you when something looks off.

---

## How It Works

```
iPhone / Apple Watch
        ↓  (HealthKit → background sync)
  iOS App (HealthClaw)
        ↓  (HTTPS POST)
  Webhook Server  ←  npx healthclaw-webhook-server
        ↓
  health-data.jsonl  (append-only log)
        ↓
  OpenClaw Agent  (queries, crons, alerts)
```

### Key concepts

| Concept | Description |
|---------|-------------|
| **Pairing** | One-time setup: server issues a time-limited token (2 min), iOS app scans or opens the deep-link, exchanges it for a permanent API token stored securely on the server |
| **Data sync** | iOS app POSTs individual records to `/api/health-sync` or bulk batches to `/api/health-sync/batch`. Each record contains a `type`, `value`, `unit`, `startDate`, `endDate`, and optional `metadata` |
| **Deduplication** | Every record gets a deterministic ID from `(type, startDate, endDate, value)`. The server keeps a SQLite dedupe index — re-syncing the same data is always safe, duplicates are silently dropped |
| **Storage** | All data is appended to `health-data.jsonl` in a platform-appropriate user directory (`~/Library/Application Support/healthclaw-webhook` on macOS) |

---

## Setup

### 1. Start the webhook server

```bash
npx healthclaw-webhook-server
```

The server starts on port 3000 by default. Keep it running (consider a LaunchAgent / systemd service for persistence).

Optional environment variables:
```bash
PORT=3000                         # Server port
HEALTHCLAW_DATA_DIR=~/custom/path # Override data directory
ADMIN_TOKEN=your-secret           # Protect admin endpoints
```

### 2. Expose to the internet (for iOS sync)

The iOS app needs to reach your server from outside your local network.

#### Option A: Tailscale Funnel (recommended)

Tailscale Funnel gives your machine a stable public HTTPS URL tied to your Tailscale
domain — no dynamic DNS, no port forwarding needed.

```bash
# 1. Install Tailscale and log in (skip if already done)
#    https://tailscale.com/download
tailscale login

# 2. Enable Funnel for port 3000
tailscale funnel --bg 3000
```

Your public URL will be:
```
https://<machine-name>.<tailnet-name>.ts.net
```

To find it:
```bash
tailscale funnel status
# or
tailscale status --json | grep DNSName
```

> **Note:** Funnel runs in the background (`--bg`). It persists across reboots.
> To stop it: `tailscale funnel --bg --off`

#### Option B: Cloudflare Tunnel

```bash
# Install cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
cloudflared tunnel --url http://localhost:3000
# Cloudflare prints a randomly-assigned https://xxxxx.trycloudflare.com URL
```

> URLs are ephemeral — you'll need to re-pair the iOS app each time you restart the tunnel.

#### Option C: ngrok

```bash
ngrok http 3000
# ngrok prints a https://xxxxx.ngrok-free.app URL
```

> Same caveat as Cloudflare — URL changes on restart unless you have a paid plan.

Note your public URL — you'll need it in the next step when generating the pairing link.

### 3. Generate a pairing link

```bash
curl -X POST https://your-public-url/admin/generate-pairing
```

Response:
```json
{
  "pairingToken": "abc123...",
  "deepLink": "healthclaw://pair?url=...&token=...",
  "openUrl": "https://your-public-url/pair/open?token=...",
  "expiresInSeconds": 120
}
```

Open `openUrl` on your iPhone, or paste `deepLink` into Safari. The page has a button
that opens the HealthClaw app directly.

> **Token expires in 2 minutes.** If it expires, run the curl command again.

### 4. Install the iOS app

The HealthClaw iOS companion app handles background HealthKit syncing.

**Current status:** App is pending App Store review.

**TestFlight (beta):** <https://testflight.apple.com/join/SXDjT6vC>

Once installed, open the app and follow the pairing flow. After pairing, the app will
sync data automatically in the background — no need to keep it open.

### 5. Verify the connection

```bash
curl https://your-public-url/health
# → { "status": "ok", "paired": true, ... }
```

Check that data is flowing:
```bash
tail -f ~/Library/Application\ Support/healthclaw-webhook/health-data.jsonl
```

---

## Data Format

Each line in `health-data.jsonl` is a JSON record:

```json
{
  "type": "HeartRate",
  "value": 62,
  "unit": "count/min",
  "startDate": "2025-01-15T07:32:00Z",
  "endDate": "2025-01-15T07:32:00Z",
  "metadata": { "context": "resting" }
}
```

Common types: `HeartRate`, `RestingHeartRate`, `HeartRateVariabilitySDNN`,
`StepCount`, `SleepAnalysis`, `ActiveEnergyBurned`, `DistanceWalkingRunning`, and more.

---

## Use Cases

| Example | Description |
|---------|-------------|
| [Recovery Score](examples/recovery-score.md) | Daily HRV + RHR + sleep score with cron job setup |
| [Health Alerts](examples/health-alerts.md) | Proactive anomaly detection with configurable thresholds |

---

## Multi-User Setup

By default, the server runs in single-user (legacy) mode. To support multiple users
(e.g. family members, clients), create users via the Admin API. Each user gets an
isolated data directory — no data mixing between users.

### Create a user

```bash
curl -X POST https://your-public-url/admin/users \
  -H "Content-Type: application/json" \
  -H "x-admin-token: your-secret" \
  -d '{"name": "alice"}'
```

Response (token is shown **once only** — save it):
```json
{
  "userId": "usr_a1b2c3d4",
  "token": "64-char-hex-token...",
  "name": "alice",
  "createdAt": "2026-03-14T12:00:00.000Z"
}
```

### List users

```bash
curl https://your-public-url/admin/users \
  -H "x-admin-token: your-secret"
```

Returns `[{ userId, name, createdAt }]` — tokens are never included in list responses.

### Using the token

The returned token is the API key the iOS app uses for syncing. Set it as the
`x-api-token` header when pairing or syncing. Each user's data is automatically
routed to their own directory:

```
{appDataRoot}/users/{userId}/health-data.jsonl
{appDataRoot}/users/{userId}/dedupe.db
```

### Legacy compatibility

The existing single-device permanent token continues to work. Its data stays at the
original path (`{appDataRoot}/health-data.jsonl`). No migration is needed — both
modes work side by side.

### Reading per-user data (OpenClaw skill integration)

When querying health data for a specific user, read from their per-user path:

```bash
# Single (legacy) user — default path
cat ~/Library/Application\ Support/healthclaw-webhook/health-data.jsonl

# Multi-user — per-user path
cat ~/Library/Application\ Support/healthclaw-webhook/users/usr_a1b2c3d4/health-data.jsonl
```

---

## API Reference

Full API spec: [`webhook-server/docs/API_SPEC.md`](../webhook-server/docs/API_SPEC.md)

Key endpoints:
- `GET  /health` — server status + pairing state
- `POST /admin/generate-pairing` — create a new pairing link
- `POST /api/pair?token=<token>` — complete device pairing (called by iOS app)
- `POST /api/health-sync` — ingest a single record
- `POST /api/health-sync/batch` — ingest up to 5000 records in one request
- `POST /admin/users` — create a new user (returns token once)
- `GET  /admin/users` — list all users (no tokens)
- `GET  /admin/device-info` — check paired device metadata
