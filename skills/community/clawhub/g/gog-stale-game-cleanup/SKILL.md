---
name: gog-stale-game-cleanup
description: >
  Find installed GOG games not played in 30+ days, email a report, and add
  reminders to Apple Reminders Gaming list. Use when user wants to clean up
  unused GOG games, review stale game library, get uninstall reminders, or
  run a periodic game cleanup sweep. Triggers on stale games, game cleanup,
  unused games, GOG cleanup, game purge review.
---

# GOG Stale Game Cleanup

Automated workflow to identify installed GOG games that haven't been played recently, notify via email, and create Apple Reminders for each stale game.

## Prerequisites

- GOG library JSON file (see `gog_library.json` in config)
- `himalaya` CLI configured for email sending
- `remindctl` CLI for Apple Reminders (macOS)
- `python3` for JSON parsing

## Workflow

1. Run `scripts/stale_games.sh` with required environment variables
2. Script identifies installed games with `last_played` older than 30 days (or never played)
3. Sends an email report to the configured address
4. Adds a "Consider uninstalling: <game>" reminder to the Gaming list

## Usage

```bash
GOG_LIBRARY=/path/to/gog_library.json \
EMAIL_TO=user@example.com \
EMAIL_ACCOUNT=personal \
REMINDERS_LIST=Gaming \
bash scripts/stale_games.sh
```

### Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GOG_LIBRARY` | Yes | — | Path to GOG library JSON |
| `EMAIL_TO` | Yes | — | Recipient email address |
| `EMAIL_ACCOUNT` | No | `personal` | Himalaya account name |
| `REMINDERS_LIST` | No | `Gaming` | Apple Reminders list name |
| `STALE_DAYS` | No | `30` | Days threshold for stale |
| `DRY_RUN` | No | `false` | Preview without sending |

### Scheduling

To run weekly via cron:

```bash
# Add to crontab or use OpenClaw cron
0 10 * * 1 GOG_LIBRARY=... EMAIL_TO=... bash /path/to/scripts/stale_games.sh
```

## Output

- **Email**: Formatted report listing each stale game with last-played date and install path
- **Reminders**: One reminder per stale game titled "Consider uninstalling: <game name>" in the Gaming list
- **Console**: Summary of findings and action confirmations
