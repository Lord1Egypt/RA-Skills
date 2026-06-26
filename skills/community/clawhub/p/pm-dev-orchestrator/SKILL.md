---
name: pm-dev-orchestrator
description: Orchestrate a PM bot and one or more Dev bots in a private Telegram group. Use to turn plain chat commands like "DEV skill install <slug>" and "DEV cron add ..." into actions on a Dev OpenClaw server (install ClawHub skills, manage OpenClaw cron jobs). Includes a Dev-side command executor script and a PM-side command format + safety rules.
---

# pm-dev-orchestrator

Set up a **PM bot** (planner) that issues structured commands in a private Telegram group, and a **Dev bot** (executor) that runs those commands on its own server.

This skill is written for the **Dev bot** (executor). It contains:
- a strict, parseable **command language** that PM can post into the group
- the **Dev bot behavior contract** (what to execute, what to ignore)
- safe defaults to avoid loops / spam / privilege escalation

## Core idea

- PM speaks natural Russian to the human.
- PM posts **strict commands** into a private group.
- Dev bot (OpenClaw) reads that group and executes only commands:
  - authored by PM bot (numeric `from.id`)
  - inside the allowed group chat id
  - with strict prefix: `DEV `

No extra polling bot is needed: Dev bot is just an OpenClaw instance connected to Telegram. When it receives a group message, it parses and runs the allowlisted actions.

## Required config values (fill these)

- `GROUP_CHAT_ID` — Telegram group chat id (e.g. `-5259247075` or `-100...`).
- `PM_FROM_ID` — Telegram numeric id of the PM bot. Example from our setup: `7790959648`.
- `DEV_BOT_TOKEN` — BotFather token for the Dev bot.

## Dev bot: OpenClaw Telegram group allowlist

In `~/.openclaw/openclaw.json` on the **Dev server**, set:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "<DEV_BOT_TOKEN>",
      "dmPolicy": "allowlist",
      "allowFrom": [],
      "groupPolicy": "allowlist",
      "groupAllowFrom": [<PM_FROM_ID>],
      "groups": {
        "<GROUP_CHAT_ID>": {}
      }
    }
  }
}
```

Restart gateway:

```sh
openclaw gateway restart
```

## Command format (PM → Dev in the group)

All executable commands must be a single line starting with `DEV `.

### Skill management

- `DEV skill install <slug>`
- `DEV skill update <slug>`
- `DEV skill search <query>`
- `DEV skill list`

Rules:
- `<slug>` must be a ClawHub slug like `claw-guru` or `StaticAI/android-adb`.
- Installs into: `~/workspace/skills` (OpenClaw workspace).

### Cron management

- `DEV cron list`
- `DEV cron add every=10m name="dm-check" message="..."`
- `DEV cron add cron="*/5 * * * *" name="health" message="..."`
- `DEV cron enable id=<jobId> on|off`
- `DEV cron remove id=<jobId>`
- `DEV cron run id=<jobId>`

Notes:
- `message=...` becomes the agentTurn prompt for the cron job (isolated).

## Dev executor (recommended): implement as Dev bot behavior (no extra daemon)

**Recommended**: do not run an extra process. Instead, configure the Dev bot’s behavior to:

1) Ignore everything except `DEV ...` commands.
2) For allowed commands, run the corresponding local CLI (`clawhub` / `openclaw cron ...`).
3) Reply with a short, machine-readable status.

### Dev bot behavior contract (copy into Dev bot system instructions)

When you receive a Telegram group message:

- If `chat.id != GROUP_CHAT_ID`: ignore.
- If `from.id != PM_FROM_ID`: ignore.
- If text does not start with `DEV `: ignore.

Otherwise parse and execute.

**Output format (reply in group):**

- Success: `OK <summary>`
- Failure: `ERR <reason>`

Keep it under ~10 lines.

### Optional script

`scripts/dev_executor.py` is included as a parser/executor scaffold for testing, but the primary path is the Dev bot behavior above.

## Safety rules (non-negotiable)

- Never execute arbitrary shell from chat.
- Only allow commands listed above.
- Only accept from `PM_FROM_ID` in `GROUP_CHAT_ID`.
- Never print secrets/tokens in chat.

## Troubleshooting

- If Dev bot is silent: check group allowlist in config (`groupAllowFrom` + `groups`) and restart gateway.
- If PM_FROM_ID unknown: on Dev server run `openclaw logs --follow`, make PM bot send a message, read `from.id`.
