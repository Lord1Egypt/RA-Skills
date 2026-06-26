# Claude Code wrapper for webtop-galim

Use this repository from Claude Code as a local homework/tasks toolkit for:
- Webtop / SmartSchool
- Galim Pro
- Ofek

## Goal

Give Claude Code a simple, repeatable way to:
1. load local credentials
2. run the existing scripts
3. summarize results in Hebrew
4. avoid re-explaining the setup each time

## Repository root

```bash
/root/.openclaw/workspace/skills/webtop-galim
```

## Required local env

Default env file:

```bash
/root/.openclaw/workspace/.env/webtop-galim.env
```

Legacy env is also supported automatically:

```bash
/root/.openclaw/workspace/.env/galim.env
```

Load it before running anything:

```bash
set -a
. /root/.openclaw/workspace/.env/webtop-galim.env
set +a
```

If `OFEK_KIDS_JSON` is not set, use the helper wrapper below. It builds the JSON automatically from:
- `OFEK_NAME_CHILD1`, `OFEK_USERNAME_CHILD1`, `OFEK_PASSWORD_CHILD1`
- `OFEK_NAME_CHILD2`, `OFEK_USERNAME_CHILD2`, `OFEK_PASSWORD_CHILD2`

The wrapper also maps legacy names automatically when present:
- `*_YUVAL` → `*_CHILD1`
- `*_SHIRA` → `*_CHILD2`

## Preferred entrypoint

Use the wrapper script instead of calling Python files directly when possible:

```bash
bash scripts/claude-code-wrapper.sh report
bash scripts/claude-code-wrapper.sh expanded --days 30 --limit 5
bash scripts/claude-code-wrapper.sh ofek --json
bash scripts/claude-code-wrapper.sh galim --json
bash scripts/claude-code-wrapper.sh webtop
bash scripts/claude-code-wrapper.sh sync --days 30
```

## Direct script mapping

- `webtop` → `scripts/webtop_fetch_summary.py`
- `galim` → `scripts/galim_fetch_tasks.py`
- `ofek` → `scripts/fetch_tasks.py`
- `report` → `scripts/unified_report.py`
- `expanded` → `scripts/expanded_report.py`
- `sync` → `scripts/sync_galim_calendar.py`

## Recommended Claude Code workflow

For a normal status check:
1. Run `bash scripts/claude-code-wrapper.sh expanded --days 30 --limit 5`
2. Summarize urgent items in Hebrew
3. Highlight overdue items first
4. If requested, run `bash scripts/claude-code-wrapper.sh sync --days 30`

## Ofek detailed reporting

The Ofek fetcher now returns more than counters when visible items exist on the page.

Current detailed extraction can include:
- activity title
- subject
- teacher
- due date
- visible urgent / overdue activity sections

Use these commands when you want detailed Ofek output:

```bash
bash scripts/claude-code-wrapper.sh ofek
bash scripts/claude-code-wrapper.sh ofek --json
bash scripts/claude-code-wrapper.sh expanded --days 30 --limit 8
```

For parent-facing summaries, prefer `expanded` because it combines:
- Galim structured tasks
- Ofek counters
- Ofek visible detailed activities
- Webtop summary

## Good Claude Code prompts

- `Open CLAUDE.md in this repo and run the expanded report, then summarize urgent tasks in Hebrew.`
- `Use scripts/claude-code-wrapper.sh to run Ofek and Galim checks and give me a concise summary.`
- `Run the calendar sync from this repo and report how many events were created or updated.`

## Notes

- Use `students.myofek.cet.ac.il`, not `myofek.cet.ac.il`.
- Prefer `expanded` for human review.
- Prefer `sync` only when calendar credentials are already configured.
- If a command fails, report the real error and do not guess missing data.
