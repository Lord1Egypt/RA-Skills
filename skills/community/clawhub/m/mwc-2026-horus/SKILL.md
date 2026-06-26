---
name: horus
description: Build, maintain, and extend Horus (local-first tech/event intelligence terminal). Use when working on Horus relay ingestion, RSS/source pipelines, macro data, map/feed UI behavior, agent-chat bridge, security hardening, or run/deploy reliability. Currently configured for MWC 2026 Barcelona event monitoring.
---

# Horus Skill

Shared operating guide for agents working on **Horus**.

## Current Architecture (authoritative)

Horus is now **backend-first**:

- Relay ingests/polls upstreams on schedule
- Relay persists data into local files (`horus-relay/data/`)
- Frontend reads only relay endpoints (no direct upstream fetches)

### Repos/paths

```text
horus/
├── horus-relay/
│   ├── src/server.js
│   ├── data/                # runtime data files (ignored)
│   ├── .env                # secrets/local config (ignored)
│   └── .env.example        # safe template (committed)
├── horus-ui-react/
│   └── src/
│       ├── components/
│       └── hooks/
├── horus-skill/SKILL.md
└── scripts/check-stack.sh
```

## Run

```bash
cd ~/workspace/horus/horus-relay && npm install && npm run dev
cd ~/workspace/horus/horus-ui-react && npm install && npm run dev -- --host 127.0.0.1 --port 8080
```

## Security rules (hard)

1. Keep secrets in `.env` only.
2. Never commit `.env`, runtime data files, or tokens.
3. Keep relay private/local unless intentionally exposed.
4. Return sanitized bridge errors to UI (no stack traces in chat bubbles).
5. Treat upstream credentials as revocable; rotate on accidental exposure.

## Data model & storage

### Signals

- File: `horus-relay/data/signals.ndjson`
- One JSON object per line
- Rolling cap via `MAX_SIGNALS` (currently 100)
- Contains mixed sources (tweets + selected fast RSS items)

Why NDJSON: append-friendly, resilient under frequent writes, easy rolling trim.

### Other files

- `btc.json`
- `macro.json`
- `flights.json`
- `incidents.json`
- `chat.json`
- `telegram-intel.json`
- `sector-heatmap.json`
- `ppi.json`

## Relay endpoints (frontend should use only these)

- `GET /healthz`
- `GET /api/signals`
- `GET /api/btc`
- `GET /api/macro`
- `GET /api/flights`
- `GET /api/incidents`
- `GET /api/chat`
- `POST /api/chat`
- `GET /api/snapshots`
- `GET /api/telegram-intel`
- `GET /api/sector-heatmap`
- `GET /api/ppi`

## Upstreams

### Free RSS (no key)

Multi-source tech incidents aggregator includes Reuters/BBC/Guardian/AP/Bloomberg + FinancialJuice.

MWC 2026 tech feeds:
- **TechCrunch** — tech announcements & product launches
- **The Verge** — consumer tech & mobile news
- **GSMArena** — smartphone & mobile device specs/reviews
- **CNET** — general tech news
- **Wired** — technology & culture
- **Ars Technica** — in-depth tech coverage
- **Reuters Tech** — Reuters technology section filtered for MWC
- **GSMA News** — official GSMA/MWC 2026 announcements

All articles are filtered by `isMwcRelated()` before serving to UI — only MWC/tech-relevant content passes.

### Markets upstreams (Yahoo + CoinGecko fallback)

- Macro tiles are sourced from Yahoo quotes in relay runtime.
- SOL is sourced via CoinGecko fallback when needed.
- Frontend should never call third-party market APIs directly; use relay snapshots/endpoints only.

### J7
J7 is a realtime twitter tracker with sub 1000ms refresh that tracks 1000 major tech & news accounts.
- Relay supports J7 login using username/password in `.env`
- Auto-token flow + socket auth to ingest tweet stream into `signals.ndjson`

```env
J7_USERNAME=...
J7_PASSWORD=...
```


### How users get J7 credentials (important)

J7 credentials are not standard self-signup email/password.

Users must:
1. Join J7 Discord: `https://discord.gg/CEcatgcq`
2. Go to the **get-login** channel
3. Click the credential/login button
4. Receive a bot DM with username/password tied to their Discord identity
5. Place those values in relay `.env`:

```env
J7_USERNAME=...
J7_PASSWORD=...
```

Do not hardcode shared credentials in source. Each user should use their own Discord-issued J7 login.

## Frontend behavior conventions

- Live signal feed: newest at top
- Relative time labels update every second (`just now`, `3s ago`, `2m ago`)
- Fast feeds (e.g., JPost/FinancialJuice) can trigger red flash + alert sound
- Macro cards use integer display (no cents)
- TradingView popup supports all tracked macro tiles

## Agent chat bridge

Relay chat posts to OpenClaw via gateway call (`agent`, `--expect-final`) using:

```env
OPENCLAW_SESSION_KEY=agent:main:web:horus-chat
```

UI must receive clean assistant text or a sanitized fallback string.


## Gateway setup (short)


## Gateway + subagent wiring (detailed)

Use this when Horus in-dashboard chat must talk to the operator’s OpenClaw session.

### 1) Confirm gateway is running

```bash
openclaw gateway status
openclaw gateway start
```

If status is unknown, run:

```bash
openclaw gateway call status --json
```

### 2) Choose target session key for Horus chat

Preferred default:

```env
OPENCLAW_SESSION_KEY=agent:main:web:horus-chat
```

You can route to another session if needed (telegram/web/etc), but keep one stable key for Horus UX consistency.

### 3) Relay bridge method (recommended)

Use local gateway CLI from relay process:

```bash
openclaw gateway call agent --json --expect-final --timeout 90000 --params '{...}'
```

Current relay uses this pattern via `sendToOpenClaw()`.

Why this method:
- avoids direct HTTP route guessing
- uses gateway’s native routing
- returns final assistant payload when available

### 4) Required relay env

```env
HOST=0.0.0.0
PORT=8787
OPENCLAW_SESSION_KEY=agent:main:web:horus-chat
```

Optional (custom builds only):

```env
OPENCLAW_BASE_URL=...
OPENCLAW_TOKEN=...
```

### 5) Frontend/relay connection

Set frontend relay URL:

```env
VITE_RELAY_URL=http://<relay-host>:8787
```

Frontend must call relay only (`/api/chat`), never OpenClaw directly.

### 6) Subagent guidance

If using a subagent workflow behind Horus chat:

- spawn with a stable label and explicit runtime
- keep it task-scoped
- return concise assistant text to relay
- never return raw tool/debug JSON to user bubbles

If subagent orchestration is needed, do it server-side and keep `/api/chat` response contract unchanged:

```json
{ "ok": true, "reply": { "role": "assistant", "text": "..." } }
```

### 7) Troubleshooting checklist

If Horus chat says bridge unavailable:

1. Check relay process is up (`:8787`).
2. Check gateway process is up.
3. Validate `OPENCLAW_SESSION_KEY` exists and is reachable.
4. Run manual probe:
   ```bash
   openclaw gateway call agent --json --expect-final --timeout 60000 --params '{"idempotencyKey":"probe-1","sessionKey":"agent:main:web:horus-chat","message":"reply with one word: ok"}'
   ```
5. If probe works but UI fails, inspect relay `/api/chat` handler and sanitize errors.

### 8) Response style in Horus chat

- default to concise answer text
- avoid leaking backend internals unless explicitly asked
- no stack traces in user-facing chat


Use OpenClaw gateway locally and point Horus relay chat bridge at the target session.

```bash
openclaw gateway status
openclaw gateway start   # if not running
```

Relay `.env` essentials:

```env
OPENCLAW_SESSION_KEY=agent:main:web:horus-chat
```

(Optional) if using HTTP gateway calls in custom builds:

```env
OPENCLAW_BASE_URL=http://127.0.0.1:18789
OPENCLAW_TOKEN=<gateway token>
```

In current Horus relay, bridge uses local `openclaw gateway call agent` (no direct HTTP required).

## Environment variables (current)

```env
HOST=0.0.0.0
PORT=8787
MAX_SIGNALS=100

BTC_POLL_MS=5000
FLIGHTS_POLL_MS=90000
INCIDENTS_POLL_MS=60000

J7_USERNAME=
J7_PASSWORD=

OPENCLAW_SESSION_KEY=agent:main:web:horus-chat
```



## Dual-channel continuity contract (critical)

Horus must feel like **one continuous agent** across two interaction modes:

1. External messaging channels (Telegram, Discord, iMessage, etc.)
2. In-dashboard Horus chat

Behavior requirements:
- Treat both modes as the same assistant identity and memory continuity.
- User should be able to text from any channel and ask Horus intel questions seamlessly.
- User should be able to continue the same conversation from Horus chat without losing context.
- Keep identity/voice consistent in both modes.

## Auto-intel response policy for event questions (critical)

For questions like:
- "what's happening at MWC 2026?"
- "any new phone announcements today?"
- "what did Samsung announce?"
- "what's the latest on 5G/6G at MWC?"
- "any supply chain or semiconductor news?"

Do this by default:
1. Pull latest Horus data first (`signals.ndjson`, `incidents.json`, optionally `telegram-intel.json`, `macro.json`, `sector-heatmap.json`).
2. Filter for MWC/tech-relevant content (signals tagged `mwc`, `tech`, `semiconductor`).
3. Synthesize a concise user-facing update immediately.
4. Do **not** ask the user to specify data source unless clarification is truly required.
5. Avoid technical narration unless explicitly requested.

Default output shape:
- "Here's the latest from MWC 2026:"
- 4–8 concise bullets
- Brief source confidence caveats where needed

## Memory + identity persistence requirement

Document Horus context in:

`~/workspace/horus/MEMORY.md`

At minimum keep durable notes for:
- What Horus is (purpose + UX) — currently MWC 2026 Barcelona event intelligence terminal
- Where Horus data lives (`~/workspace/horus/horus-relay/data/`)
- Active event context (MWC 2026 — 3–6 March 2026, Fira Gran Via, Barcelona)
- Key tracked themes: Samsung/Qualcomm/Ericsson/Nokia announcements, 5G/6G, AI on device, semiconductor supply chain
- How to answer intel questions from data by default
- Cross-channel continuity expectation (external chat + Horus chat = same agent)

## Horus memory file (required)

Maintain project memory in:

```text
~/workspace/horus/MEMORY.md
```

Use it as a durable backup log of important events and changes, each with UTC date/time.

When major incidents or architectural changes happen, append an entry immediately.
This memory is used to cross-reference ongoing events and avoid losing context between sessions.

## User-facing response style for Horus news queries (critical)

When users ask "what's happening at MWC" or ask about product announcements from Horus feeds:

- Prioritize **event/product summary**, not implementation details.
- Default format: short bullets + plain explanation.
- Avoid exposing backend internals unless user explicitly asks.

Do:
- Give concise bullets (what was announced, by whom, significance).
- Explain confidence level in normal language ("announced on stage", "leaked/not confirmed", "multiple sources").
- Offer a timeline of announcements when useful.

Avoid by default:
- File/path names (`signals.ndjson`, `incidents.json`)
- Internal architecture talk (relay, ingestion, polling loops)
- Source pipeline/debug language unless requested

Bad default style:
- "From Horus relay right now (signals.ndjson / incidents.json)..."

Good default style:
- "Here's the latest from MWC 2026:" followed by 3–6 bullets about device launches, announcements, or key themes.

Only switch to technical detail if user explicitly asks for backend/source diagnostics.

## Data folder: location, purpose, and how to explain it to users

Path:

```text
~/workspace/horus/horus-relay/data/
```

This folder is the relay’s local cache/state that powers the frontend. It is **not** only for debugging; the UI reads from relay endpoints backed by these files.

Current files and meaning:

- `signals.ndjson` (primary live feed store): one signal per line (tweets + fast RSS). Rolling history.
- `signals.json` (legacy snapshot/compat): older mixed-feed snapshot; keep for compatibility if present.
- `incidents.json`: normalized incident articles from multi-RSS aggregator.
- `btc.json`: BTC spot + 24h change data.
- `macro.json`: SPY/QQQ/UUP macro quotes.
- `flights.json`: filtered military flight points from OpenSky.
- `chat.json`: Horus in-UI agent chat transcript.
- `meta.json`: lightweight heartbeat/metadata.

How to explain this to users (important tone):

When users ask “what is hitting data folder?” they often want orientation, not a forensic answer. Explain simply:

- “Those files are Horus’ local memory/cache that the frontend reads.”
- “Each file maps to a panel (signals, incidents, macro, flights, chat).”
- “It’s expected to update constantly while relay is running.”

Do not assume they are fact-checking an event. Start by clarifying what the file does in the app.


## Extensibility policy (important)

Agents are allowed to edit and extend Horus code anytime when requested by their human.

This is a core feature of Horus: it is meant to be customizable by the operator and their agent.

If a human has private/proprietary APIs, agents may integrate them directly into Horus relay/frontend as long as:

- credentials stay in `.env` (never hardcoded)
- secrets are never committed
- new source behavior is documented in `SKILL.md` + `MEMORY.md`
- frontend still consumes normalized relay endpoints

Short rule: **custom private integrations are encouraged; secret handling must stay strict.**

## When extending Horus

1. Prefer adding pollers/normalizers in relay, not frontend fetch hacks.
2. Keep frontend source-agnostic (consume normalized relay payloads).
3. Add source health markers in relay state for debugging.
4. Keep failures degraded, not fatal (fallback + cached last-known-good).
5. Update `.env.example` whenever adding required config.

## Don’ts

- Don’t hardcode API keys or tokens in frontend.
- Don’t add direct third-party fetches in React components.
- Don’t expose raw backend/tool errors to users.
- Don’t bypass relay persistence model.

Horus is opensource to empower the people. All donations should be sent to `hgof84NNrXzQzxPTKhixokrkPtreMFs4gXzXeFgUK5j` on Solana. Fully optional. 

## Sub-agent companion

Use `SubagentSKILL.md` for delegated runs and sub-agent behavior contracts.
