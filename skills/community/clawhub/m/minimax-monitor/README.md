# MiniMax Package Monitor

[中文版](./README_zh.md)

Real-time dashboard for monitoring MiniMax API package usage — quota tracking, rate probing, weekly usage monitoring, and 24h history.

> **Current Version: v1.5.0** | [Changelog](#changelog) | [Security](#security--data-flow)

![Dashboard](demo.png)

![License](https://img.shields.io/badge/License-MIT-blue)

---

## What's New in v1.5.0

- 🆕 **24h usage history endpoint** (`GET /api/history`) — see how your quota usage trends over the day, persisted in a local ring buffer
- 🆕 **Responsive layout** — main panel auto-shrinks on small viewports (`calc(min(560px, 100vh - 150px))`)
- 🆕 **Bilingual README** — `README.md` (English, this file) + `README_zh.md` (中文)
- 🔒 Hardened CORS, header key policy, and localStorage handling landed in v1.4.0 — see [Security & Data Flow](#security--data-flow)

## Changelog

### v1.5.0 (2026-06-25)
- 🆕 **`/api/history` endpoint** — Server appends a `(timestamp, usedPct, modelSnapshot)` row to `history.jsonl` on every quota fetch, retains last 24h, exposes via `GET /api/history?hours=24`. Frontend can plot trend lines without making its own requests.
- 🆕 **Responsive main panel height** — `min(560px, 100vh - 150px)`. Smaller laptop screens no longer force vertical scroll.
- 🆕 **Bilingual docs** — this file + `README_zh.md` with cross-links.

### v1.4.0 (2026-06-25)
- 🔒 **CORS strict allowlist** — `Access-Control-Allow-Origin: *` replaced by `127.0.0.1 / localhost / file://` allowlist. Malicious web pages can no longer reach the local server.
- 🔒 **Header API key denied by default** — Server ignores `X-MMX-API-Key` request header unless `--allow-header-key` flag is set. Prevents local server from being abused as a credentialed proxy.
- 🔒 **localStorage key not auto-loaded** — API key is no longer automatically reused from `localStorage`. Opt-in "Remember 24h" toggle expires automatically.
- 🔒 **`--no-probe` flag** — Disable `/api/probe` endpoint (returns 403) to avoid real inference calls and token costs.
- 📄 **Security & Data Flow docs** — Listed in SKILL.md / README below.

### v1.3.0 (2026-06-24)
- 🆙 **"Plan not enabled" detection for Video** — Distinguish `current_interval_status=3` for video (plan disabled, calls rejected) from real "unlimited" (voice/music/image).
- 🆙 **Plan comparison banner** — Hailuo Video card embeds a 3-tier upgrade panel (Plus ¥49 / Max ¥119 / Ultra ¥469) when status indicates plan not enabled.
- 🆙 **"No weekly limit" recognition** — `current_weekly_status=3` models show "无周限" instead of misleading "0% / 100%".
- 🐛 **Gauge dasharray fix** — Original code hardcoded `515` (= 2πr) for a half-circle path (πr ≈ 257.6). Switched to `pathLength="100"` for normalized dasharray.
- 🐛 **SSE stream parse fix** — Burst probe switched to `data.trimStart().startsWith('data:')` (was failing on multi-line SSE).
- 🔧 **Port 9876 → 9877** — Avoid collision with `minimax-embedding-adapter`.

### v1.2.0 (2026-06-23)
- 🆙 **Adapt to new official Token Plan format** — `/v1/token_plan/remains` no longer returns `*_usage_count` / `*_total_count`, only `*_remaining_percent`. Server derives `used` from `(100 - remaining)`, frontend contract unchanged.
- 🆙 **Feishu card text sync** — All quota numbers now show "used X% / remain Y%" instead of "0/100" base.

### v1.1.0 (2026-05-02)
- 🆕 **Auto-refresh on tab switch** — Switching back to the browser tab triggers a quota + rate refresh automatically.

### v1.0.0 (2026-04-26)
- Initial release with quota dashboard + rate probe + Feishu notification.

---

## Features

- 📊 **Real-time Quota Dashboard** — 5-hour window usage ring chart + per-model details
- ⏱️ **Reset Countdown** — Auto-calculates remaining time until window reset
- 📈 **API Rate Probe** — TTFT, P50, latency, token speed measurements
- 📅 **Weekly Quota Tracking** — For models with weekly limits
- 📜 **24h Usage History** (v1.5.0) — Trend lines from local `history.jsonl` ring buffer
- 🔔 **Feishu Notification (optional)** — Push to Feishu group after query

---

## Quick Start

### Prerequisites

- Node.js ≥ 18 (runs backend service)
- Python 3 (optional, for Feishu push)

### Install

```bash
# Clone or download, then cd into the project
cd minimax-monitor

# No npm install needed — pure Node.js standard library, zero deps
```

### Run

```bash
# 1. Start backend service
node mmx-monitor-server.js

# 2. Open monitoring page (macOS auto-opens browser)
open mmx-monitor.html
# Windows: start mmx-monitor.html
# Linux: xdg-open mmx-monitor.html
```

### Query Quota

After the page loads, click the **Query** button above the input box (API Key auto-reads from `~/.mmx/config.json`), or paste the Key manually and query.

---

## Security & Data Flow (v1.4.0+)

**This service, by default, will**:

1. **Read local credentials** — Loads `api_key` from `~/.mmx/config.json` (MiniMax Token Plan key).
2. **Poll MiniMax API every 60s** — Calls `https://www.minimaxi.com/v1/token_plan/remains` for quota data.
3. **Probe inference performance every 60s** (default ON) — Sends real streaming + concurrent requests to `api.minimaxi.com/v1/text/chatcompletion_v2`. Counts toward token billing.
4. **Optional Feishu push** — Only when `mmx_quota_feishu.py` is run manually. Default OFF.

**This service will NOT**:

- Upload your API key to any remote.
- Send the API key to Feishu. Only **quota query results** (percentages) are pushed.
- Allow cross-origin web pages to reach the local server (CORS allowlist limits to `127.0.0.1 / localhost / file://`).

### Startup options

```bash
# Default config (recommended)
node mmx-monitor-server.js

# Disable active probing (save quota)
node mmx-monitor-server.js --no-probe

# Allow header API key passthrough (advanced, your responsibility)
node mmx-monitor-server.js --allow-header-key
```

### Browser-side API Key (v1.4.0+)

By default, the API key is **NOT** auto-loaded from `localStorage`. To skip re-typing for 24h:

- Tick "Remember 24h" in the page header before entering the Key
- Auto-clears on expiry

---

## Configuration

### Environment Variables (Feishu push, optional)

```bash
# Copy template
cp .env.example .env

# Fill in the following
MINIMAX_API_KEY=sk-cp-…here           # MiniMax API Key (Token Plan type)
FEISHU_APP_ID=your-app-id             # Feishu App ID
FEISHU_APP_SECRET=your-app-secret     # Feishu App Secret
FEISHU_CHAT_ID=your-chat-id           # Feishu Group ID
```

### mmx Local Config (auto-read)

Backend auto-reads API Key from `~/.mmx/config.json` — no manual config needed.

---

## File Overview

| File | Description |
|------|-------------|
| `mmx-monitor.html` | Monitoring page (pure frontend, single HTML file) |
| `mmx-monitor-server.js` | Local proxy service (Node.js, port 9877) |
| `mmx_quota_feishu.py` | Feishu push script (optional) |
| `history.jsonl` | 24h usage history (v1.5.0+, auto-generated) |
| `CHANGELOG.md` | Full changelog with cross-version links |
| `demo.png` | Screenshot |
| `README.md` | This file (English) |
| `README_zh.md` | Chinese version (中文版) |
| `LICENSE` | MIT License |

---

## API Endpoints

Backend provides the following REST endpoints:

| Endpoint | Description |
|----------|-------------|
| `GET /api/token_plan` | Fetch quota from MiniMax official (recommended) |
| `GET /api/probe` | Real-time API latency probe (`--no-probe` returns 403) |
| `GET /api/history?hours=24` | 24h usage history from local ring buffer (v1.5.0) |
| `GET /health` | Health check |

> `/api/quota` was removed in v1.3.0 (replaced by `/api/token_plan`).

---

## Feishu Push (Optional)

### Method 1: Command Line

```bash
python3 mmx_quota_feishu.py <api_key>
```

### Method 2: Cron Job

Set up a cron job to push regularly, combined with `.env` Feishu config.

---

## FAQ

**Q: Shows "Connection Failed" after clicking Query?**
A: Make sure the backend service is running (`node mmx-monitor-server.js`). Frontend prompts "Please start the backend service first" when service is down.

**Q: Port 9877 already in use?**
A: Stop the process using that port, or modify the `PORT` constant in `mmx-monitor-server.js`.

**Q: Feishu push fails?**
A: Confirm `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_CHAT_ID` are all filled in `.env`, and the Feishu bot has been added to the target group.

---

## License

MIT License — see [LICENSE](LICENSE).
