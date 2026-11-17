# idle-ping — Let your AI randomly "think of you" 🎲

> An [OpenClaw](https://openclaw.ai) cron pattern that makes your AI agent **proactively message you with something interesting** — at random moments, with natural density, and never annoying.
>
> Built by leslie311

---

## What is this?

Most bots only reply when you talk to them. **idle-ping** turns that around:

- When you haven't messaged your AI for **30+ minutes**, it starts rolling a dice every minute (1-in-30 chance).
- When the dice hits, your AI **picks something it genuinely finds interesting** (news, history, a weird Wikipedia page, a paper, a Reddit TIL…) and messages you with a short, personality-driven note.
- It remembers what it already told you, so it never repeats.
- If you're clearly busy (3 shipments with no reply), it **pauses automatically** and quietly waits until you come back.

The result: your AI "thinks of you" at random moments — sometimes 40 minutes later, sometimes hours, sometimes never. Just like a human friend. ☂️

---

## How it works

Eight OpenClaw cron jobs wired together — a **content pipeline** (nightly topic
factory + hourly crawler keep the queue stocked) and a **shipping mechanism**
(idle-ping gate + send):

```
┌─────────────────────────────────────────────────────────┐
│ 0. Content pipeline (stock the queue)                   │
│    a. idle-ping-topic-factory  (nightly 22:30 · agent)  │
│       AI invents 30 fresh topics → topic-rotation.json  │
│    b. idle-ping-crawler  (every hour at :15 · shell)    │
│       reads rotation[i] → searches news/arxiv/reddit    │
│       → Ollama summarizes → share-queue.db (channel=topic)
│    c. idle-ping-deep-explore  (daily 01:00 · agent)     │
│       picks a field, deep-dives 3-5 sources → 4 finds   │
│       → share-queue.db (channel=deep)                   │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 1. idle-ping-gate   (every 1 min · shell · $0 model cost)│
│    - silent window 23:00–08:00 → skip                    │
│    - user active < 30 min → skip                         │
│    - last trigger < 30 min ago → skip (lock)             │
│    - paused? (3 unanswered shipments) → skip             │
│    - roll dice 1/30 → miss → skip                        │
│    - hit → trigger send job                              │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 2. idle-ping-send   (agent turn · the fun part)          │
│    - load persona (SOUL.md if present)                   │
│    - DB-first: grab a queued item from the share queue   │
│    - no stock → explore live (news/history/wiki/arxiv…)  │
│    - write a 3-part message (why → content → thought)    │
│    - deliver to your chat with a real source link        │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 3. idle-ping-pause-notice (agent turn · only on pause)   │
│    - "I'll keep this story for you. Come back anytime."  │
└─────────────────────────────────────────────────────────┘
```

**The DB is created automatically** — `share-queue.py` runs
`CREATE TABLE IF NOT EXISTS` + migrations on first use; no manual init needed.

The gate costs **zero model tokens** (pure bash + a tiny Python read). Model cost only kicks in when the dice actually hits and your AI crafts a message.

---

## Design highlights

- **Dice-controlled density** — no fixed schedule, naturally irregular timing
- **Streak-based pause** — 3 unanswered shipments → auto-pause + a gentle notice; any reply from you resets it
- **DB-first shipping** — a share queue (`share-queue.db`) decouples "finding stuff" (cheap crawler) from "sending stuff" (agent taste)
- **Self-stocking pipeline** — nightly topic factory + hourly crawler keep the queue full, exactly like the original system it was extracted from
- **Persona-ready** — reads `SOUL.md` / `IDENTITY.md` if present, else uses a natural default tone
- **Zero personal data in the repo** — see [Privacy](#privacy)

---

## Conversation Continuity by Design

At idle-ping, we believe **proactive messages should never hijack the user's own conversation thread.**

We understand that real life happens: a user may ask a question, step away, and return hours later — by which time the AI has shared several interesting discoveries in the meantime. When that user comes back, **they most likely want to continue where they left off**, not to be pulled into a conversation the AI started in their absence.

That is why idle-ping deliveries are designed as **one-way broadcasts from an isolated session**: they appear in the chat as gentle, optional moments of discovery — but they **never enter the main conversation context**. When the user replies, the assistant always continues the *user's own thread*. The conversation belongs to the user, not to the ping.

**Design principle: the user's voice always wins the thread.** Proactive content enriches the chat; it never owns it.

---

## Prerequisites

- [OpenClaw](https://openclaw.ai) installed and running (Gateway)
- A chat channel configured (Telegram, etc.)
- Python 3 + `openclaw` CLI on `PATH`
- Optional but recommended: [Ollama](https://ollama.com) with a small model for cheap exploration summarization

---

## Quick start

```bash
# 1. Clone
git clone <your-repo-url> idle-ping && cd idle-ping

# 2. Install (scripts + templates + 8 cron jobs)
TELEGRAM_ID=<your-chat-id> bash install.sh

# 3. Verify
openclaw cron list
```

That's it. After 30 minutes of silence, the dice starts rolling.

> `TELEGRAM_ID` is your numeric chat id (e.g. `123456789`). Find it via `@userinfobot` or your channel settings.

### Options

```bash
bash install.sh /custom/workspace        # non-default OpenClaw workspace
TELEGRAM_ID=123 bash install.sh --dry-run   # preview, do nothing
bash install.sh --no-cron                # only copy scripts + templates
```

---

## Configuration

Everything lives in `scripts/idle-ping.env` (auto-generated on install; see `idle-ping.env.example`):

| Variable | Purpose |
|---|---|
| `IDLE_PING_WS` | OpenClaw workspace path (auto-detected if unset) |
| `IDLE_PING_SESSIONS_JSON` | Path to `sessions.json` (idle detection) |
| `IDLE_PING_SEND_JOB_ID` | Cron job id of `idle-ping-send` (filled by install.sh) |
| `IDLE_PING_PAUSE_JOB_ID` | Cron job id of `idle-ping-pause-notice` (filled by install.sh) |

Tunables in `curiosity/`:

- `state.json` — `pingStreak`, `lastPingTriggerAt`, `lastShipAt`, `pauseNoticeSent`, `pauseNoticeStyle`
- `channels.json` — content-channel weights (topic / news / onthisday / misconceptions / randomwiki / deep / arxiv / reddit / xsearch)
- `topic-rotation.json` — exploration topic rotation list

### Behavior tunables (all optional — defaults match the original design)

| Variable | Default | What it controls |
|---|---|---|
| `IDLE_PING_DICE_RANGE` | `30` | Dice denominator — 1/N chance to ship per roll (smaller = more frequent) |
| `IDLE_PING_IDLE_MIN` | `30` | Minutes of silence before dice-rolling starts |
| `IDLE_PING_COOLDOWN_MIN` | `30` | Minutes after a shipment before the next roll is allowed (lock) |
| `IDLE_PING_DAILY_CAP` | `0` | Max shipments per day (`0` = unlimited) |
| `IDLE_PING_SILENT_START` | `23` | Silent window start hour (24h) |
| `IDLE_PING_SILENT_END` | `8` | Silent window end hour |
| `IDLE_PING_TZ` | `Asia/Hong_Kong` | Timezone for silent window & daily cap |
| `IDLE_PING_PAUSE_AFTER` | `2` | Unanswered shipments before auto-pausing the dice |
| `IDLE_PING_PAUSE_STYLES` | `月光詩意,貼心關心,幽默玩味,自嘲` | Comma-separated pause-notice style pool |

Set them in `scripts/idle-ping.env` or as environment variables. Example:

```bash
# In idle-ping.env:
IDLE_PING_DICE_RANGE=10        # 1-in-10 chance (more chatty)
IDLE_PING_IDLE_MIN=15          # start rolling after 15 min of silence
IDLE_PING_COOLDOWN_MIN=120     # wait 2h between shipments
IDLE_PING_SILENT_START=2       # night owl: silent 02:00–11:00
IDLE_PING_SILENT_END=11
IDLE_PING_TZ=Europe/Berlin      # your timezone
IDLE_PING_DAILY_CAP=3          # at most 3 shipments/day
```

---

## Testing

Professional-grade test suite (BATS + ShellCheck), runs automatically in CI.

```bash
# 1. Static analysis (ShellCheck)
shellcheck scripts/*.sh install.sh

# 2. Unit tests (BATS)
#    Install bats-core: https://github.com/bats-core/bats-core
bats tests/
# → 12 tests: idle / lock / paused / reset / ship / pause / config overrides
```

The test suite mocks external commands (fake `shuf` forces dice wins, fake
`openclaw` records triggers, fake `curl` records pings) so it runs fully
offline — no gateway, no network.

[![CI](https://github.com/leslie311/openclaw-idle-ping/actions/workflows/ci.yml/badge.svg)](https://github.com/leslie311/openclaw-idle-ping/actions/workflows/ci.yml)

## Monitoring (heartbeat)

Cron jobs die silently — the heartbeat pair catches that.

| Job | Interval | What it does |
|---|---|---|
| `idle-ping-heartbeat` | 10 min | Writes `curiosity/heartbeat.txt` (epoch) + optional external ping |
| `idle-ping-watchdog` | 1 h | If heartbeat is stale (> `IDLE_PING_WATCHDOG_STALE_MIN`), logs 🚨 + optional `/fail` ping |

### All cron jobs installed by `install.sh`

| Job | Schedule | Type | Purpose |
|---|---|---|---|
| `idle-ping-topic-factory` | daily 22:30 | agent (no-deliver) | AI invents fresh topics → `topic-factory.py refresh` (top up to 30) |
| `idle-ping-crawler` | hourly at :15 | shell | `semantic-patrol.py --mode rotation` — crawls the current topic → queue |
| `idle-ping-deep-explore` | daily 01:00 | agent (no-deliver) | Deep-dive a field → stores 4 finds (channel=deep) |
| `idle-ping-gate` | every 1 min | shell | Dice roll, silent window, pause logic ($0 model cost) |
| `idle-ping-send` | on trigger | agent (announce) | Craft + deliver the message (DB-first) |
| `idle-ping-pause-notice` | on trigger | agent (announce) | Pause notice when streak fills |
| `idle-ping-heartbeat` | 10 min | shell | Heartbeat file + optional external ping |
| `idle-ping-watchdog` | 1 h | shell | Detect stale heartbeat (cron died) |

Set `IDLE_PING_HEARTBEAT_URL` (e.g. a [Healthchecks.io](https://healthchecks.io) ping URL) to get
email/Telegram alerts when the cron stops. Without it, monitoring stays
fully local (zero external dependency).

```bash
# In idle-ping.env:
IDLE_PING_HEARTBEAT_URL=https://hc-ping.com/your-uuid   # external alerts
IDLE_PING_WATCHDOG_STALE_MIN=60                          # alert after 60 min silence
```

---

## Manual test

```bash
# Force the send job right now (debug):
openclaw cron run <send-job-id>

# Watch the system log:
cat $WS/curiosity/system-activity.log
```

Log legend: 🎲 dice hit · 🛑 dice stored · 📤 shipped · 🤫 no-reply · ✅ resumed

---

## Project layout

```
idle-ping/
├── install.sh                 # one-shot installer
├── scripts/
│   ├── idle-ping-gate.sh      # zero-cost gate + dice
│   ├── system-log.sh          # system log helper
│   ├── share-queue.py         # share queue (SQLite)
│   ├── semantic-patrol.py     # exploration / stock engine
│   ├── topic-factory.py       # topic rotation manager
│   ├── heartbeat.sh           # monitoring heartbeat (local + optional ping)
│   └── watchdog.sh            # heartbeat staleness alert
├── tests/                     # BATS test suite (gate + monitoring)
├── templates/
│   ├── state.json             # initial state
│   ├── channels.json          # channel weights
│   ├── topic-rotation.json    # empty rotation list
│   ├── send-job-prompt.txt    # shipment prompt ({{WORKSPACE}})
│   └── pause-job-prompt.txt   # pause notice prompt
└── docs/                      # design docs (ADR, flow diagrams, code walkthrough)
```

---

## Privacy

This repository contains **no personal data**:

- ❌ No `soul/`, `MEMORY.md`, `IDENTITY.md`, `memory/` (persona files — bring your own)
- ❌ No `sessions.json`, `state.json`, `prefs.json`, `share-queue.db` (runtime data)
- ❌ No API keys, Telegram ids, or real cron job ids

The `.gitignore` (rename from `.gitignore.draft`) blocks all of the above.

---

## License

[MIT](LICENSE)

---

*Made with 🌙 and a 1-in-30 dice. If your AI starts messaging you at 3am, that's a feature — adjust the silent window in `idle-ping-gate.sh`.*
