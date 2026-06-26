# Scheduling — basic reminders and tasks

Use this for ordinary one-shot, exact-time, calendar, and deferred-agent
task pokes.

## One-shot

```bash
poke --remind "Take out the trash." --once 10m \
  --channel discord --target user:1
```

## Exact time

```bash
poke --remind "Leave for airport." --at "16:55" \
  --channel discord --target user:1
```

## Recurring calendar

`--on-calendar` takes a systemd OnCalendar expression.

```bash
poke --remind "Trash day." --on-calendar "Sun *-*-* 19:00:00" \
  --channel discord --target user:1
```

## Deferred agent task

Use `--task` when the future fire should ask an agent to do work, not
just send fixed reminder text. Include `--agent`.

```bash
poke --task "Check email and surface urgent items." \
  --on-calendar "Mon..Fri *-*-* 09:00:00" \
  --agent agy --channel discord --target user:1
```

## Duplicate check

Before creating a reminder, check the relevant scope:

```bash
poke --list --channel CH --target TGT --agent AG
```

If an active reminder already matches the user's intent, do not create a
duplicate. Use `sub-skills/management.md` for inspection and cleanup.

## Creation sanity check

For unusual schedules, run the same create command with `--dry-run`
first. It validates and previews without writing state.

```bash
poke <create-args> --dry-run
```
