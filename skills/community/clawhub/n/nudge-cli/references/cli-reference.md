# Nudge CLI Reference

All commands support `--json` for machine-readable output.

## Task Commands

### Create a task
```bash
nudge task add --desc "Finish the PR review" --duration 30 --why "Team is blocked" --secret-id s-1
nudge task add --desc "Ship feature" --duration 60 --punishment post_to_beeper_whatsapp --targets "!roomid:..."
```

**Flags:**
- `--desc` (required): Task description
- `--duration` (default 60): Minutes until deadline
- `--why`: Why this matters (used in reminders — always ask for this)
- `--punishment`: Action name (default: from config or desktop_notification)
- `--targets`: Comma-separated recipient IDs
- `--secret-id`: Secret from the bank to use as punishment content
- `--custom-punishment-message`: Custom punishment text

**Returns:** Task object with `id`, `deadline`, `warning_intervals` (for scheduling reminders).

### Complete a task
```bash
nudge task complete task-1
nudge task done task-1      # alias
```
Sends all-clear messages via the punishment action. Idempotent — completing an already-completed task is a no-op.

### Fail a task
```bash
nudge task fail task-1
```
Executes the punishment: sends the secret/message to all targets via the configured action. Falls back to desktop notification if the action fails.

### Cancel a task
```bash
nudge task cancel task-1
```
No messages sent. Use only for legitimate reasons (task became irrelevant).

### Check status
```bash
nudge task status           # all active tasks with time remaining
nudge task status task-1    # specific task
```

### List and history
```bash
nudge task list             # active tasks
nudge task list --all       # include history
nudge task history          # full history
nudge task history --limit 5
```

## Secrets Commands

```bash
nudge secrets add --secret "I cry during Disney movies" --severity medium
nudge secrets list
nudge secrets pick                    # least-used secret
nudge secrets pick --severity spicy   # least-used spicy secret
```

Severities: `mild`, `medium`, `spicy`

## Motivation Commands

```bash
nudge motivation list                       # all quotes
nudge motivation list --phase reminder_late # phase-filtered
nudge motivation add --quote "Ship it" --attribution "Me" --phase reminder_late
```

Phases: `task_created`, `reminder_early`, `reminder_mid`, `reminder_late`, `task_completed`, `task_failed`

## Punishment Commands

```bash
nudge punishment list                       # show available actions
nudge punishment health post_to_beeper_whatsapp  # test connectivity
nudge punishment setup post_to_beeper_whatsapp --token abc123 --default-group "!room:..."
nudge punishment setup post_to_beeper_whatsapp --add-contact "Alice=!room:..."
```

## Config Commands

```bash
nudge config show
nudge config set default_punishment post_to_beeper_whatsapp
```

## Cleanup

```bash
nudge cleanup --yes    # cancel all active tasks
```

## Global Flags

- `--json`: JSON output envelope `{"ok": true, "command": "...", "data": {...}}`
- `--data-dir`: Override data directory (default: `~/.nudge`)
