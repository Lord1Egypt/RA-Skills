---
name: gog-dormant-cleanup
description: "Find installed GOG games not played in 30+ days, email a summary report, and add each game to Apple Reminders as a cleanup nudge. Use when: user wants to clean up their GOG library, find dormant/unused games, get reminded about unplayed games, or automate a gaming cleanup workflow. Triggers: 'dormant games', 'GOG cleanup', 'unplayed games', 'game cleanup reminder', 'clean up my library'."
---

# GOG Dormant Game Cleanup

Automated workflow to surface idle installed GOG games and nudge the user to consider uninstalling.

## Workflow

1. **Scan** the GOG library JSON for installed games whose `last_played` is older than the cutoff (default 30 days).
2. **Email** a formatted summary to the user's personal himalaya account.
3. **Remind** by adding each dormant game to Apple Reminders under the `Gaming` list.

## Script

Run `scripts/gog_dormant_cleanup.sh`:

```bash
scripts/gog_dormant_cleanup.sh <cutoff_days> <library_json> [himalaya_account] [reminders_list]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| cutoff_days | 30 | Days of inactivity to qualify as dormant |
| library_json | (required) | Path to GOG library JSON (see config format below) |
| himalaya_account | personal | Himalaya account name for sending email |
| reminders_list | Gaming | Apple Reminders list name |

### Environment Variables

- `DRY_RUN=1` — print actions without sending email or creating reminders.

### GOG Library JSON Format

The script expects a JSON file with this structure:

```json
{
  "games": [
    {
      "name": "Game Title",
      "installed": true,
      "last_played": "2026-03-28T19:45:00",
      "install_path": "/path/to/game"
    }
  ]
}
```

Games with `installed: false` are skipped. `last_played` may be `null` (never played).

## Prerequisites

- `jq` — JSON parsing
- `himalaya` — email delivery (optional; skips email if absent)
- `remindctl` — Apple Reminders (optional; skips reminders if absent)

## Scheduling

To run weekly via cron:

```bash
# Every Monday at 9 AM
0 9 * * 1 /path/to/gog_dormant_cleanup.sh 30 /path/to/gog_library.json
```

Or use OpenClaw's cron tool for managed scheduling.