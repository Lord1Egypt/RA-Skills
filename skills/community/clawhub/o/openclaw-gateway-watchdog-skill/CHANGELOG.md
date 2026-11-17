# Changelog

## [1.0.4] - 2026-08-03
### Security and disclosure
- Disclosed all four default probes, local state writes, background installation boundaries, and the narrow Spark token fallback.
- Replaced executable `source config.env` behavior with allowlisted data parsing.
- Corrected the cron template so it no longer implies that restart behavior exists.

## [1.0.3] - 2026-08-03
### Security
- Aligned the documentation with the read-only implementation: no config rewrite, restart, baseline promotion, or auto-heal.
- Declared current OpenClaw requirements and optional Discord egress variables.

## [1.0.2] - 2026-03-03
### Added
- Simplified installation instructions (Ask OpenClaw / CLI) to SKILL.md and README.md.

## [1.0.1] - 2026-02-23
### Changed
- Rename display name to Gateway Watchdog Discord.

## [1.0.0] - 2026-02-20
### Initial Release
- Discord-first watchdog for OpenClaw gateway incidents.
