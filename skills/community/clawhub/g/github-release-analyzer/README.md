# github-release-analyzer

Current planned release version: **0.0.1**

Analyze GitHub releases and turn release notes into short, high-signal summaries.

## What it does

- Supports a single repo input: `owner/repo` or `https://github.com/owner/repo`
- Manual mode: summarize the latest formal release
- Cron mode: track unprocessed formal releases incrementally
- Preserves a deterministic pipeline:
  `prepare -> summarize -> render -> commit`

## Main files

- `SKILL.md` — skill routing + workflow rules
- `scripts/run.py` — deterministic entrypoint for `prepare`, `render`, `commit`
- `references/execution-modes.md` — manual vs cron behavior
- `references/summary-contract.md` — required summary output shape

## Notes

- Requires `python3`
- Default state is stored under `~/.openclaw/workspace/state/github-release-analyzer/`
- Cron mode returns `NO_REPLY` when there is no new formal release to report

## Initial publish target

- License: MIT
- Initial version: `0.0.1`
