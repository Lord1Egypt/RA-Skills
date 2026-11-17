# Changelog

Versioning: **SemVer 2.0.0** (semver.org) — MAJOR = breaking / MINOR = backwards-compatible feature / PATCH = backwards-compatible fix.
Format: **Keep a Changelog** (keepachangelog.com) — one section per version, newest first, ISO 8601 dates, changes grouped as Added / Changed / Deprecated / Removed / Fixed / Security. Log entries under `## [Unreleased]` as they happen; on release, retitle to `## [x.y.z] - YYYY-MM-DD` and reset an empty Unreleased at the top.

## [Unreleased]

## [0.1.1] - 2026-09-12

### Changed
- Publisher attribution corrected: the `author` field read `Evermind`, which was wrong for this package. It is now `TXJ · 天玄镜 (Tianxuanjing)` — the same publisher as the companion skill `evermind-ai-agent-memory`. No code, template, or behaviour change.

## [0.1.0] - 2026-09-12

### Added
- First release (0.1.0): one command flips the whole machine stack — VPN, background agents, local services, model tier — driven by a single YAML mode matrix. Ships `templates/modes_switch.py` (`work` / `--selftest` / `--list` / `--state`), `templates/watchdog.py` (repairs the current mode only, never revives what was switched off), `templates/modes.yaml` (the mode matrix), `references/patterns.md` (design notes + pitfalls). Pure Python standard library — no dependencies, no model calls, no API cost.
