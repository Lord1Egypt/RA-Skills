# Night Shift Security Model

Night Shift is a powerful queued execution framework. Treat it like a coding agent runner, not a passive note-taking skill.

## What Night Shift can do

When you approve and run plans, Night Shift may:

- read and write files inside the configured workspace
- create git branches and worktrees under `data/night-shift/worktrees/`
- run subprocesses for shell phases and verification commands
- call optional coding runners such as Cursor CLI (`agent`/`cursor`) or Claude Code (`claude`)
- run tests, linters, build commands, and smoke checks
- write checkpoints, reports, logs, and failure-memory records
- optionally send Telegram notifications if notification tokens are configured

## What Night Shift should not do by default

Night Shift should not:

- run against production repositories without review
- execute unreviewed public/external actions
- send notifications unless recipients and tokens are explicitly configured
- mark dry-runs as completed live work
- continue through every plan after a shared runner/preflight failure

## Required runtime dependencies

Required:

- `python3` 3.11+
- `git`
- writable workspace/data directory

Optional, depending on phase execution methods:

- Cursor CLI: `agent` or `cursor`
- Claude Code CLI: `claude`
- Telegram notification env vars

## Environment variables

Optional variables read by the skill:

- `OPENCLAW_WORKSPACE` — workspace root; defaults to the OpenClaw workspace that contains this skill
- `NIGHT_SHIFT_DATA_DIR` — Night Shift state directory; defaults to `$OPENCLAW_WORKSPACE/data/night-shift`
- `NIGHT_SHIFT_MODEL` — model hint for compatible runners
- `CURSOR_CLI` — explicit path to Cursor/agent CLI
- `CURSOR_API_KEY` — optional non-interactive Cursor auth, if supported by your CLI setup
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `NIGHT_SHIFT_CHAT_ID` — optional notifications

Never commit real tokens. Use a local env file such as `.night-shift.env` and keep it out of published packages.

## Safe first run

Use an isolated disposable workspace first:

```bash
export OPENCLAW_WORKSPACE=/tmp/night-shift-demo
python3 skills/night-shift/scripts/preflight.py --json
python3 skills/night-shift/scripts/executor.py dry-run
```

Dry-run is intended to be read-only. It should produce a preview report and must not mark plans complete or write success checkpoints.

## Background runner warning

Detached systemd/timer execution does not automatically inherit your interactive shell environment. Before live unattended execution, run preflight in the same user/service context. In particular, Cursor CLI phases need `HOME`, `PATH`, and a non-interactive auth strategy.

If preflight says Cursor/Claude is not ready, fix the environment or change the queued phases before running live execution.

## Verification command policy

Verification commands can execute subprocesses in the worktree. Prefer explicit, narrow commands such as:

- `python3 -m pytest`
- `npm test`
- `npm run lint`
- `ruff check .`

Avoid arbitrary shell pipelines unless you have reviewed the plan and trust the repository.

## Operational guidance

- Review generated plans before approval.
- Prefer dry-run before live execution.
- Start with one low-risk plan in a disposable workspace.
- Inspect reports and worktree diffs before merging.
- Keep production credentials out of worktrees.
