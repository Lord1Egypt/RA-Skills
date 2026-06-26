# Changelog

## 1.0.0 — 2026-04-28
### Added
- Initial release
- Automated daily backup using OpenClaw's built-in `backup create`
- Backups stored in ~/openclaw_backups/ as timestamped .tar.gz archives
- Backup contents: config, credentials, session history, workspace, skills
- Archive verification via `openclaw backup verify`
- Cleanup old backups by age (--days flag, dry-run by default)
- Optional daily cron at 04:00 HKT
- Portable — works on any machine with OpenClaw installed, no extra deps
