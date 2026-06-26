---
name: gog-cleanup
description: "Find GOG games installed but not played for 30+ days, email the list, and add Apple Reminders to consider uninstalling. One-command cleanup sweep for your backlog."
version: 1.0.0
author: john_doe
license: MIT
metadata:
  openclaw:
    emoji: "🧹"
    requires:
      bins: [himalaya, remindctl, jq]
    tags: [gog, gaming, cleanup, reminders, email]
---

# GOG Cleanup

Automated stale-game cleanup sweep: finds installed GOG games you haven't played in 30+ days, emails you a digest, and creates Apple Reminders so you can decide whether to uninstall.

## What It Does

1. Reads your GOG library from `config/gog_library.json`
2. Filters for **installed** games whose `last_played` is 30+ days ago (or never played)
3. Sends a formatted digest email via `himalaya`
4. Adds each stale game to the **Gaming** list in Apple Reminders via `remindctl`

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| `jq` | JSON parsing | `brew install jq` |
| `himalaya` | Send email | `brew install himalaya` |
| `remindctl` | Apple Reminders | `brew install steipete/tap/remindctl` |

- Himalaya must be configured with a `personal` account (see `config/himalaya.toml`)
- Apple Reminders must have a **Gaming** list (auto-created if missing)

## Usage

### Run the full sweep (email + reminders)

```bash
bash scripts/gog-cleanup.sh
```

### Email only (skip reminders)

```bash
SKIP_REMINDERS=1 bash scripts/gog-cleanup.sh
```

### Reminders only (skip email)

```bash
SKIP_EMAIL=1 bash scripts/gog-cleanup.sh
```

### Custom stale threshold (default 30 days)

```bash
STALE_DAYS=60 bash scripts/gog-cleanup.sh
```

### Custom recipient (defaults to himalaya personal account email)

```bash
EMAIL_TO="other@example.com" bash scripts/gog-cleanup.sh
```

## Configuration

The script reads from workspace `config/`:

| File | Purpose |
|------|---------|
| `config/gog_library.json` | GOG game library with install status & last_played timestamps |
| `config/himalaya.toml` | Himalaya email account config (uses `personal` account) |
| `config/reminders_lists.json` | Reminders list structure (Gaming list) |

## Output

- **Email**: HTML-formatted digest sent to your personal inbox
- **Reminders**: One reminder per stale game in the Gaming list, prefixed with "🧹 Consider uninstalling:"
- **Console**: Summary of games found and actions taken

## Scheduling

To run weekly via cron:

```bash
# Add to crontab for Monday 9 AM
0 9 * * 1 /path/to/scripts/gog-cleanup.sh >> /tmp/gog-cleanup.log 2>&1
```

Or use OpenClaw's cron tool for agent-managed scheduling.

## Notes

- Games with `last_played: null` (never played) are always included
- Uninstalled games are always skipped regardless of last_played
- The script is idempotent — re-running won't duplicate reminders (existing reminders with the same title are skipped)
