# openclaw-onboarding

A beginner onboarding skill for [OpenClaw](https://openclaw.ai) that turns a blank install into a useful, personalized assistant — automatically.

## What It Does

- **Auto-triggers** on your first session (no setup needed)
- Asks 5 short questions: name, channel, goal, timezone, and **preferred intro frequency**
- Sets up your `HEARTBEAT.md`, `USER.md`, and `SOUL.md` workspace files
- Schedules feature introductions at **your chosen pace** — daily, every few days, weekly, or any custom interval
- **Pause anytime**: say "stop onboarding" → intros stop
- **Resume anytime**: say `/openclaw-onboarding` or "resume onboarding" → picks up exactly where it left off
- **Change pace anytime**: say "make it daily" or "slow down to weekly" → cron job updates instantly

## Feature Curriculum (10 features, your pace)

| # | Feature |
|---|---------|
| 1 | Heartbeat & HEARTBEAT.md — always-on check-ins |
| 2 | Cron reminders (main session) — "remind me in 20 min" |
| 3 | Cron isolated reports — scheduled summaries to your chat |
| 4 | Skills — extending the agent with new capabilities |
| 5 | Multi-channel routing — same agent, every platform |
| 6 | Browser automation — agent controls a browser |
| 7 | Sub-agents — parallel workers for long tasks |
| 8 | Multi-agent setup — multiple personas on one gateway |
| 9 | Webhooks + Gmail trigger — external events wake the agent |
| 10 | MCP servers — connect any external tool |

### Frequency options

| You say | Schedule |
|---------|----------|
| "daily" | Every day at 10am — done in 10 days |
| "every 3 days" | Every 3 days — done in a month |
| "weekly" (default) | Every Sunday at 10am — done in 10 weeks |
| "every 2 weeks" | Bi-weekly — relaxed pace |
| Any custom interval | Agent converts it to a cron expression |

## Installation

### Option A — Copy to workspace (recommended for personal use)

```bash
# Clone this repo
git clone https://github.com/dukesky/openclaw-onboarding.git

# Copy the skill into your OpenClaw workspace
mkdir -p ~/.openclaw/workspace/skills/openclaw-onboarding
cp openclaw-onboarding/SKILL.md ~/.openclaw/workspace/skills/openclaw-onboarding/

# Start a new session — onboarding begins automatically
openclaw agent --message "Hello"
```

### Option B — Install via OpenClaw CLI (if published to ClawHub)

```bash
openclaw skills install openclaw-onboarding
```

### Option C — Shared across all agents on this machine

```bash
mkdir -p ~/.openclaw/skills/openclaw-onboarding
cp SKILL.md ~/.openclaw/skills/openclaw-onboarding/
```

## How It Works

The skill uses three OpenClaw mechanisms together:

1. **Always-loaded skill** (`metadata: {"openclaw": {"always": true}}`) — injected into every session's system prompt so the agent always knows to check onboarding state
2. **`ONBOARDING_PROGRESS.md` as state machine** — a single workspace file tracks status (`active` / `paused` / `complete`) and which features have been introduced
3. **`session:openclaw-onboarding` cron job** — a persistent-session weekly cron that remembers what it introduced last week and picks up the next feature

### State machine

```
ONBOARDING_PROGRESS.md missing  →  Phase 1: Discovery (immediate)
status: active                  →  Weekly intros running
status: paused                  →  Silent; resume with /openclaw-onboarding
status: complete                →  All 10 features introduced; done
```

## Pause, Resume, and Frequency Change

| What you say | What happens |
|---|---|
| "stop onboarding" / "pause onboarding" | Sets `status: paused`, disables cron |
| `/openclaw-onboarding` or "resume onboarding" | Re-enables cron, continues from next unchecked feature |
| `/openclaw-onboarding` when complete | Offers a deeper second pass on any topic |
| "make it daily" / "change to every 3 days" / "slow down to weekly" | Updates the cron schedule live, no restart needed |

## File Structure

```
~/.openclaw/workspace/
├── skills/
│   └── openclaw-onboarding/
│       └── SKILL.md            ← this skill
├── USER.md                     ← written during onboarding (name, channel, goal, timezone)
├── SOUL.md                     ← agent persona (written if missing)
├── HEARTBEAT.md                ← periodic checklist (written during onboarding)
└── ONBOARDING_PROGRESS.md      ← state tracker + feature curriculum with checkboxes
```

## Requirements

- [OpenClaw](https://openclaw.ai) installed and running
- A configured messaging channel (for weekly delivery) — or just use the built-in webchat

## License

MIT
