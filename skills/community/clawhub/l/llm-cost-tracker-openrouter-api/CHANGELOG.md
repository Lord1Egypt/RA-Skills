# Changelog

All notable changes to this skill are documented here.

## 1.1.2 (2026-05-28)
- Added `--days` flag to `collect_usage.py` to allow multi-day collection.
- Fixed HKT/UTC logic gap by using a 48-hour window in scheduled runs.
- Improved collection reliability for rolling 24h reports.
- Excluded local `usage.db` from snapshots (C7 fix).

## 1.1.1
- Added: scripts/setup.py
- Updated: SKILL.md, version.txt

## 1.1.0 (2026-04-30)

### Changed
- Clarified billing rules: use `usage.cost.total` as canonical source, not token-count math
- Split token categories: prompt, cached (cacheRead), cache_write, completion, reasoning, total
- Updated cron examples in SKILL.md with `--no-deliver` flag for collect cron
- Removed "forward output exactly" requirement from report triggers

### Added
- 90-day time window in addition to 24h/7d/30d/365d
- `/365d` trend line in Telegram report format

## 1.0.0 (2026-04-05)

- Initial release
- Track and report LLM token usage and cost via OpenRouter
- Support for 24h rolling and 7d/30d/365d calendar windows
- SQLite append-only DB with deduplication