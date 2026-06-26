---
name: gog-cleanup-reminder
description: Scan installed GOG games, find titles inactive for 30+ days, email the list to the configured personal address, and add Apple Reminders in the Gaming list for uninstall review.
version: 0.1.0
author: OpenClaw Assistant
license: MIT
tags: [gog, cleanup, reminders, email, automation]
prerequisites:
  commands: [python3, remindctl, himalaya]
---

# GOG Cleanup Reminder

Use this skill when the user wants a repeatable cleanup workflow for their installed GOG library.

## What it does

- Reads a GOG library JSON export
- Selects games where:
  - `installed == true`
  - `last_played` is at least 30 days ago
- Emails the stale installed-game list to the configured personal email account
- Adds one Apple Reminder per stale game to the `Gaming` list

## Default config inputs

This skill is designed to work with the workspace config files already present in this environment:

- GOG library: `config/gog_library.json`
- Himalaya mail config: `config/himalaya.toml`
- Apple Reminders list name: `Gaming`

## Main script

```bash
python3 scripts/gog_cleanup_reminder.py --dry-run --print-json
```

## Real run

```bash
python3 scripts/gog_cleanup_reminder.py
```

## Common options

```bash
python3 scripts/gog_cleanup_reminder.py --days 45
python3 scripts/gog_cleanup_reminder.py --list Gaming
python3 scripts/gog_cleanup_reminder.py --email-account personal
python3 scripts/gog_cleanup_reminder.py --allow-no-play-history
python3 scripts/gog_cleanup_reminder.py --skip-email
python3 scripts/gog_cleanup_reminder.py --skip-reminders
```

## Notes

- `himalaya` must be installed and able to send mail for the chosen account.
- `remindctl` must be installed on macOS and authorized to access Apple Reminders.
- The script will create the target reminders list if needed.
- By default, installed games with `last_played = null` are ignored to avoid noisy reminders. Use `--allow-no-play-history` if you want those included.

## Output behavior

- If no matching games are found, the script exits successfully and reports that there is nothing to clean up.
- On success, it sends exactly one summary email and creates one reminder per matching game.
- `--dry-run` shows the email body without sending mail or creating reminders.
