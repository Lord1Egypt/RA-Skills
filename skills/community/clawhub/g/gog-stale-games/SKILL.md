---
name: gog-stale-games
description: "Scan your GOG library for installed games not played in 30+ days, email the list, and add reminders to consider uninstalling. One-command cleanup workflow."
version: 1.0.0
author: john_doe
license: MIT
metadata:
  openclaw:
    emoji: "🧹"
    requires:
      bins: ["himalaya", "remindctl"]
---

# GOG Stale Games Cleaner

Find installed GOG games you haven't played in 30+ days, email yourself a report, and create Apple Reminders so you can decide whether to uninstall.

## When to Use

- User wants to clean up their GOG library
- User asks about stale / unused / forgotten installed games
- User wants a periodic cleanup reminder workflow
- Phrases like "stale games", "game cleanup", "haven't played in a while"

## When NOT to Use

- Browsing or searching the GOG catalog → use the `gog` skill
- Managing game installs/uninstalls directly → GOG Galaxy client only
- Scheduling the scan itself → use cron after the skill runs once

## Prerequisites

1. **GOG library data** — a JSON file at `config/gog_library.json` in the workspace (exported from GOG Galaxy or manually maintained). Must contain `games[]` with `installed` (bool) and `last_played` (ISO-8601 or null).
2. **Himalaya** — CLI email client configured with a `personal` account (`himalaya --version`).
3. **remindctl** — Apple Reminders CLI (`remindctl status`). macOS only.
4. **Gaming list** — an Apple Reminders list named `Gaming` (created automatically if missing).

## Configuration

All paths are relative to the OpenClaw workspace root unless absolute.

| Variable | Default | Description |
|---|---|---|
| `GOG_LIBRARY_PATH` | `config/gog_library.json` | Path to GOG library JSON |
| `STALE_DAYS` | `30` | Days since last play to count as stale |
| `REMINDERS_LIST` | `Gaming` | Apple Reminders list name |
| `EMAIL_ACCOUNT` | `personal` | Himalaya account to send from |
| `EMAIL_TO` | *(from account)* | Recipient email; defaults to account address |

## Script

The main script is `scripts/gog-stale-scan.sh`. Run it directly or let the agent invoke it.

```bash
# Dry run (print only, no email/reminders)
bash scripts/gog-stale-scan.sh --dry-run

# Full run
bash scripts/gog-stale-scan.sh

# Custom stale threshold
STALE_DAYS=60 bash scripts/gog-stale-scan.sh
```

## What It Does

1. Reads `config/gog_library.json`
2. Filters for `installed: true` games whose `last_played` is >30 days ago (or null)
3. Prints a formatted table to stdout
4. Sends an HTML email via `himalaya` to your personal account
5. Adds one Apple Reminders entry per stale game to the `Gaming` list with a note: "Consider uninstalling — last played YYYY-MM-DD"

## Cron Scheduling (Optional)

After a successful run, schedule it monthly:

```
0 10 1 * *  # 10 AM on the 1st of each month
```

Use the cron tool with an `agentTurn` payload that invokes this skill.

## Output Example

```
🧹 Stale GOG Games (not played in 30+ days)
─────────────────────────────────────────────
  Stardew Valley          last played 2026-03-28
  Baldur's Gate 3         last played 2026-04-01
─────────────────────────────────────────────
2 stale games found. Email sent. 2 reminders added to Gaming.
```
