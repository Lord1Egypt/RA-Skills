---
name: gog-stale-games-cleanup
description: "Scan your GOG library for installed games not played in 30+ days, email the list, and add Apple Reminders for each. One-command game cleanup workflow."
version: 1.0.0
author: john_doe
license: MIT
metadata:
  openclaw:
    emoji: "🧹"
    requires:
      bins: ["jq", "himalaya", "remindctl"]
prerequisites:
  - GOG library JSON (see references/gog_library_schema.json)
  - himalaya configured for SMTP (see references/himalaya.toml.example)
  - remindctl installed and authorized (macOS)
---

# GOG Stale Games Cleanup

Find installed GOG games you haven't played in 30+ days, email yourself a summary, and create Apple Reminders so you can decide whether to uninstall.

## When to Use

- User says "clean up my GOG library", "stale games", "games I haven't played", "uninstall reminder"
- Running a periodic game-library audit
- Triggered by cron for monthly cleanup reminders

## Quick Start

```bash
bash scripts/sweep.sh \
  --library /path/to/gog_library.json \
  --days 30 \
  --email personal \
  --reminders-list Gaming
```

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--library` | `config/gog_library.json` | Path to GOG library JSON |
| `--days` | `30` | Stale threshold in days |
| `--email` | `personal` | Himalaya account name for sending |
| `--reminders-list` | `Gaming` | Apple Reminders list name |
| `--dry-run` | off | Print actions without sending email or creating reminders |

## What It Does

1. Reads your GOG library JSON
2. Filters for `installed: true` games whose `last_played` is older than the threshold (or null)
3. Sends an HTML email via `himalaya` with the stale game list
4. Adds one Apple Reminder per stale game to the specified list

## Output Example

```
🧹 GOG Stale Games Sweep — 2026-05-12
  Found 2 stale games (>30 days since last play):

  • Stardew Valley — last played 2026-03-28
  • Cyberpunk 2077 — never played

  ✉️  Email sent to john.doe@example.com
  📝 2 reminders added to "Gaming" list
```

## Configuration

### GOG Library JSON

See `references/gog_library_schema.json` for the expected format. Each game needs:
- `name` (string)
- `installed` (boolean)
- `last_played` (ISO 8601 datetime or null)

### Himalaya

See `references/himalaya.toml.example`. The script uses `himalaya template send` on the account specified by `--email`.

### Apple Reminders

The list specified by `--reminders-list` is created if it doesn't exist (`remindctl list <name> --create`).

## Cron Integration

Run monthly:

```bash
# Add via OpenClaw cron — monthly on the 1st at 10:00
openclaw cron add --name "gog-stale-sweep" \
  --schedule "0 10 1 * *" \
  --command "bash /path/to/scripts/sweep.sh --library /path/to/gog_library.json"
```

Or use the agent's `cron` tool with a `systemEvent` payload that triggers this skill.
