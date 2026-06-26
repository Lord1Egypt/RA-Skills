# Changelog

## 1.1.0 - 2026-03-19

- Added `scripts/weekly-verify.sh` for fleet-wide verification, retention pruning, and orphan cleanup
- Added `scripts/monthly-drill.sh` for dry-run restore drills with Telegram-friendly pass/fail output
- Added `scripts/pre-change-snapshot.sh` for fast operational-only rollback snapshots before config changes
- Added `.github/workflows/verify-backup.yml` to validate generated backup archives on every push
- Documented workflow usage and scheduling in `SKILL.md` and `README.md`
- Updated backup manifest version to `1.1.0`

## 1.0.0 - 2026-03-19

- Initial release
- Added backup, restore, verify, GitHub push, and schedule scripts
- Added restore and inventory references
- Added repo template `.gitignore`
