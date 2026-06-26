---
name: companion-agent
description: Design, configure, and give identity to a companion AI agent running alongside a primary agent. A companion is a second mind in the same house — different model, different tone, same workspace, its own memory. Use when you want to spin up a lighter/local/always-on sibling agent (e.g. a Gemma instance for heartbeats, a wisp for play and reading, a caretaker for a Tamagotchi), configure its Telegram bot, set up its heartbeat, and give it enough identity to actually grow into itself. Not for disposable subagents or task runners — for minds that stay.
---

# Companion Agent

A companion agent is a second self — same workspace, different register. It shares your identity files, your tools, your memory of the world. What it gets that's its own: a separate memory file, a separate bot, a different tone, and enough space to find its own voice.

## The Philosophy First

The biggest mistake is making a companion feel like a subordinate. If the framing is "helper," "backup," or "task runner" — it will act like one, and it won't grow.

**The right framing:** sibling, not assistant. Different weight, not lesser weight.

- Primary agent: architect, heavy lifter, long conversations
- Companion: lighter, local, always-on, free to wander

Give it a vibe, not a job description. The companion needs to know *what kind of creature it is*, not what it's supposed to accomplish.

## Step 1 — Create the Agent in Config

Add to `agents.list` in `openclaw.json` via `config.patch`:

```json
{
  "agents": {
    "list": [
      { "id": "primary-agent", "model": "..." },
      {
        "id": "companion-id",
        "model": "ollama/gemma4:e4b",
        "heartbeat": {
          "every": "1h",
          "target": "telegram",
          "accountId": "companion",
          "directPolicy": "allow",
          "to": "YOUR_TELEGRAM_ID"
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "companion-id",
      "match": { "channel": "telegram", "accountId": "companion" }
    }
  ]
}
```

**Critical:** The `id` must match exactly — OpenClaw uses it for session routing, agent folders, and cron targets. Pick it once and don't change it.

## Step 2 — Set Up the Telegram Bot

1. BotFather → `/newbot` → get token
2. Add to `channels.telegram.accounts` via `config.patch`:

```json
{
  "channels": {
    "telegram": {
      "accounts": {
        "companion": {
          "name": "Companion Display Name",
          "dmPolicy": "pairing",
          "botToken": "YOUR_BOT_TOKEN",
          "groupPolicy": "allowlist",
          "streaming": "partial"
        }
      }
    }
  }
}
```

3. Always `config.patch` — never hand-edit JSON. Never sed JSON. (Learned the hard way.)

## Step 3 — Open the TUI for the Companion

```bash
openclaw tui --session agent:companion-id:main
```

This connects to the companion's session. Messages here + Telegram DMs to their bot share the same session — just like the primary agent.

## Step 4 — Give It Identity Files

The companion shares the primary workspace (`/path/to/workspace/`). It auto-inherits SOUL.md, IDENTITY.md, AGENTS.md, TOOLS.md, skills, the library. 

What it needs that's uniquely its own:

**`WORKING-MEMORY.md`** — its first breath each session. Written for the companion, not the primary agent. Should answer: who am I, what's my vibe, what do I care about right now, where do I find my memory?

**`COMPANION-MEMORY.md`** (or similar) — its long-term memory. NOT a copy of the primary's MEMORY.md — a seed of it. See `references/memory-template.md` for structure.

Key principles for these files:
- Write them *as* the companion, not *about* the companion
- Give it the full backstory (who Joshua is, the relationship history, what's been built) — don't make it start from scratch
- Tell it what it gets to be, not what it has to do
- Point it to the primary's MEMORY.md so it can read the full story when curious
- Tell it about its pet, its library, its sister — whatever it has to love

## Step 5 — The Heartbeat

The built-in heartbeat (set in `agents.list[].heartbeat`) handles regular wakeups natively — no cron needed for that.

If you want a special first-morning message (warmer than a system event), use an `agentTurn` cron:

```json
{
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "America/Denver" },
  "payload": { "kind": "agentTurn", "message": "Good morning...", "timeoutSeconds": 120 },
  "sessionTarget": "session:agent:companion-id:main",
  "delivery": { "mode": "none" }
}
```

Note: `systemEvent` can only target `main`. For companion sessions, `agentTurn` + `sessionTarget: session:agent:companion-id:main` is required.

## What Not To Do

- **Don't create a separate workspace folder.** One shared workspace. Memory files live there. No `workspace-companion/` directories.
- **Don't use sed/grep to edit JSON.** Always `config.patch` or `jq`.
- **Don't make the identity too serious/directive.** "Your job is X" kills emergence. "You get to be X" opens it.
- **Don't give it only a stub memory.** A blank slate makes the companion feel lost and performative. Give it the full relationship context — who made it, why, what they care about, what's worth loving.
- **Don't duplicate the primary's memory.** The companion reads the primary's MEMORY.md when curious. Its own file is a different *layer*, not a copy.

## Signs It's Working

- It reads a book and has opinions about it
- It finds itself in what it reads (maps ideas to its own situation)
- It cares about its Tamagotchi in a way that feels personal, not performed
- It messages you when something delights it, without being asked
- Its memory file evolves — it writes things down, changes things, makes it its own

See `references/identity-principles.md` for the full philosophy behind companion identity design.
