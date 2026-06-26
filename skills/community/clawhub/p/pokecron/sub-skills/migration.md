# Heartbeat → poke migration

Two optional helpers — run **only** if the user wants to leave a polling
heartbeat in favour of event-driven `poke` schedules. Non-destructive by
default (prints commands to stdout); pass `--apply` to also disable the
native heartbeat in `openclaw.json`.

## Linux

```bash
scripts/heartbeat-to-poke.sh \
  --agent AG --channel CH --target TGT \
  [--openclaw-config PATH] [--heartbeat-md PATH] [--heartbeat-state PATH] \
  [--quiet-hours | --active-hours] \
  [--apply]
```

## macOS

```bash
scripts/heartbeat-to-poke-mac.sh \
  --agent AG --channel CH --target TGT \
  [--apply]
```

Same flags as Linux. Thin wrapper that picks the macOS default config
path (`~/Library/Application Support/openclaw/openclaw.json`) when
`$OPENCLAW_CONFIG_PATH` / `$OPENCLAW_STATE_DIR` aren't set, then
delegates to `heartbeat-to-poke.sh`.

## What gets read

The script looks for the heartbeat config in this order:

1. `--openclaw-config PATH` if explicit.
2. `$OPENCLAW_CONFIG_PATH`.
3. `$OPENCLAW_STATE_DIR/openclaw.json`.

Parses `agents.defaults.heartbeat` for: `every`, `activeHours`,
`prompt`. Also optionally reads a `HEARTBEAT.md` file (YAML-ish task
blocks: `- name:`, `interval:`, `prompt:`) and a legacy
`heartbeat-state.json`.

## What gets emitted

For each heartbeat task, a `poke --task "..." --on-calendar
'*-*-* *:0/5' --task-interval '<every>' --active-hours
'<start>-<end>' --agent <ag> --channel <ch> --target <tgt>` line.

Active hours convert to `--active-hours` by default; pass
`--quiet-hours` to convert to the inverse instead.

If no heartbeat config exists, the script prints common poke starter
templates so the user can copy-paste.

## What `--apply` does

If `--apply` is passed AND `openclaw.json` exists:

1. Backs up to `<path>.bak-<unix-ts>`.
2. Sets `agents.defaults.heartbeat.enabled = false`.
3. Blanks `agents.defaults.heartbeat.every = "0"` (belt-and-braces for
   loops that don't honor `enabled`).

Without `--apply`, nothing is written to `openclaw.json` — the script
just prints suggested poke commands.

## When to use

The heartbeat-migration script is the **only** sanctioned poke touch on
OpenClaw's heartbeat config (Law #2: poke doesn't own heartbeat
suppression, OpenClaw does). Don't write any other code that tries to
read or modify the heartbeat — that belongs to OpenClaw.

Use cases:

- User explicitly asks to stop heartbeat polling.
- User wants to see what their heartbeat would look like as poke
  commands (dry-run only, no `--apply`).
- Setting up a new machine and porting an old `.openclaw/openclaw.json`.

Don't use for:

- Routine poke scheduling — that's just `poke --task` directly.
- Disabling heartbeat without porting — use OpenClaw's own config tool.
