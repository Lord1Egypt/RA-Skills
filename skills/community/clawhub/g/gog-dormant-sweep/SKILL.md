---
name: gog-dormant-sweep
description: "Scan GOG library for installed games not played in 30+ days, email a summary report via himalaya, and add per-game reminders to Apple Reminders Gaming list. Use when: (1) user wants to clean up or review dormant GOG games, (2) user asks for a game cleanup reminder, (3) user wants dormant game notification automation. Requires: GOG library JSON, himalaya CLI for email, remindctl CLI for Apple Reminders."
---

# GOG Dormant Game Sweep

Automated workflow: find installed GOG games not played recently → email report → add Apple Reminders.

## Quick Start

```bash
python3 scripts/sweep.py --library config/gog_library.json --email john.doe@example.com
```

## Script: `scripts/sweep.py`

### Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--library` | `config/gog_library.json` | Path to GOG library JSON |
| `--days` | `30` | Dormancy threshold (days) |
| `--email` | None | Recipient email (required unless `--no-email`) |
| `--himalaya-account` | `personal` | Himalaya account to send from |
| `--reminders-list` | `Gaming` | Apple Reminders list name |
| `--no-email` | false | Skip email |
| `--no-reminders` | false | Skip reminders |
| `--dry-run` | false | Print report only, no side effects |

### Library JSON Format

Expects the same schema as `config/gog_library.json`: an object with a `games` array where each game has `name`, `installed` (bool), `last_played` (ISO 8601 or null), and `install_path`.

### Workflow

1. Parse library JSON → filter `installed: true` games where `last_played` is older than `--days` (or null/never)
2. Compose email body with game list and send via `himalaya message write`
3. For each dormant game, run `remindctl add --title "Consider uninstalling: <name>" --list <list>`

### Example

Full run with all options:
```bash
python3 scripts/sweep.py \
  --library config/gog_library.json \
  --days 30 \
  --email john.doe@example.com \
  --himalaya-account personal \
  --reminders-list Gaming
```

Dry run to preview:
```bash
python3 scripts/sweep.py --dry-run --days 60
```