# Changelog

All notable changes to SOUL Backup will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-05

### Added
- openclaw.json backup with automatic sanitization of sensitive fields
- Sensitive field patterns: token, key, secret, password, apikey, api_key, auth, credential, bearer
- Sanitized backup saved as `openclaw.sanitized.json` with `[REDACTED]` placeholders
- Manual restoration instructions for openclaw.json
- CONTRIBUTING.md with contribution guidelines
- .gitignore to exclude backups/ and temporary files
- examples/automated-backup.sh for cron-based daily backups
- examples/pre-deployment-hook.sh for git pre-push hooks
- tests/test.mjs with minimal unit tests for backup/restore/validate
- CHANGELOG.md to track version history

### Changed
- Updated README.md with openclaw.json backup strategy
- Updated SKILL.md with security notes and openclaw.json handling
- Updated RUNBOOK.md with openclaw.json restoration instructions
- Updated RELEASE_CHECKLIST.md with new deliverables
- Restore script now detects sanitized openclaw.json and prompts user

### Security
- Sensitive fields in openclaw.json are automatically redacted during backup
- No API keys or tokens are stored in backup files
- Manual key restoration required after restore (prevents accidental key exposure)

## [1.0.0] - 2026-03-05

### Added
- Initial release
- Backup SOUL files (SOUL.md, USER.md, AGENTS.md, IDENTITY.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md)
- Restore from any backup with dry-run preview
- Validate backup integrity with SHA-256 checksums
- List all backups with metadata
- Named backups for milestones
- Single-file restore
- Automatic pre-restore backups for rollback
- Zero dependencies (Node.js built-ins only)
- Cross-platform support (macOS, Linux, Windows WSL)
