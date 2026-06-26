# MISO — Mission Inline Skill Orchestration

## What is MISO?
MISO is a **Mission Control** style visibility system for OpenClaw.
It tracks autonomous and multi-agent work in Telegram with one unified progress format.

### Use when
- Multiple agents run in parallel
- You need approval gates (`AWAITING APPROVAL`)
- You want mission state visible from chat list with emoji reactions

### Core states
- `INIT` → `RUNNING` → `PARTIAL` → `AWAITING APPROVAL` → `COMPLETE` (`ERROR` if needed)
- Reactions: `🔥`, `👀`, `🎉`, `❌`

### Message format (Android-safe)
Plain text format:

🤖 MISSION CONTROL
——————————————
📋 {mission}
⏱ {elapsed} ∣ 🧩 {done}/{total} agents ∣ {state}
- Issue: #{issue-number}
- Owner: SHUNSUKE AI
- Goal: {goal}
- Next: {next action}
🌸 powered by miyabi

### Slash command flow
- `/task-start`
- `/task-plan`
- `/task-close`
- `/agent analyze`
- `/agent execute`
- `/agent review`
- `/agent status`

### Why this is stable
- Same format across all missions
- Easy to copy/paste from mobile
- Low friction visibility from chat list without opening full context

## Slash Commands

See `SLASH-COMMANDS.md` for concise command usage.

### Telegram bot custom slash commands
Register these Telegram menu commands via bot API:
- `/miso_start`
- `/miso_plan`
- `/miso_close`
- `/miso_status`
- `/miso_task_start`
- `/miso_task_plan`
- `/miso_task_close`

To apply now:

```powershell
pwsh .\scripts\set-telegram-commands.ps1 -BotToken "<YOUR_TELEGRAM_BOT_TOKEN>"
```

### Quick reference (one-screen)

**Instant operation table**

- `/miso_start` or `/miso_task_start` → initialize mission format (owner/issue/goal)
- `/miso_plan` or `/miso_task_plan` → output execution breakdown (analysis/plan/execute/verify)
- `/miso_close` or `/miso_task_close` → complete summary format (result/risk/notify)
- `/miso_status` → quick status/approval check
- `/agent analyze` → mission context and impact classification
- `/agent execute` → start multi-agent run mode
- `/agent review` → review/quality check pass template
- `/agent status` → run-state readback and next action

This format is optimized for mobile and copy-paste operations.
