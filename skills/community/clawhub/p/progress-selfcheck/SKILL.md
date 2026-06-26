# progress-selfcheck-skill

## What this skill does
A robust progress self-check system for OpenClaw:

- Sends a periodic progress selfcheck to **Feishu** (DM target configurable)
- Writes selfcheck artifacts to `output/` for **Webchat pull**
- Maintains a **task ledger** (append-only JSONL) for conversational tasks
- Auto-reactivates stale tasks (safe local-only commands), with `repeatable` support
- Shows a clean summary: running cron jobs, recent completions, alerts, unfinished tasks

## Install
Copy this folder into your OpenClaw workspace:

- `C:\Users\Administrator\.openclaw\workspace\skills\progress-selfcheck-skill`

Then configure and add cron jobs (see below).

## Configuration
Edit:
- `config/progress_selfcheck_config.json`

Key fields:
- `workdir`: OpenClaw workspace path (default `${HOME}/.openclaw/workspace`)
- `feishu.account`: e.g. `main`
- `feishu.target`: **required**. Replace `user:ou_xxx_replace_me` with your own Feishu DM target.
  - Example: `user:ou_xxxxx...`
- `stale_minutes`: stale threshold for auto-reactivate (default 5)
- `max_reactivate_per_run`: default 2
- `display_limits`: max items for each section

## Cron job snippet
See `templates/cron_jobs_snippet.json` and merge into `~/.openclaw/cron/jobs.json`.

Suggested schedules:
- progress selfcheck: every 15 minutes 08:00-23:00
- ledger compact: weekly Sunday 03:40

## Commands
- Run selfcheck now:
  - `python skills/progress-selfcheck-skill/scripts/progress_selfcheck_and_send.py --limit 5`

- Add a task:
  - `python skills/progress-selfcheck-skill/scripts/task_ledger.py add --title "..." --auto true --repeatable true --next "python ..."`

- Reactivate stale tasks now:
  - `python skills/progress-selfcheck-skill/scripts/task_reactivate.py --stale-min 5 --max 2`

## Safety
Auto-reactivation is **local-only**:
- blocks URLs and `openclaw message send`
- intended to prevent "said working but not actually doing"

## Notes for publishing
This skill is designed to be publishable. Remove machine-specific paths by configuration.
