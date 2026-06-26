# Changelog

All notable changes to the OpenClaw WebDAV Backup skill.

## [1.2.7] - 2026-04-06

### Added
- **Restore Verification Mode** - Added `--verify-restore` / `--test-restore` to validate backup recoverability without overwriting the live OpenClaw environment
  - Verifies backup archive integrity before restore testing
  - Validates `checksums.sha256` when present
  - Extracts workspace and extensions archives into a temporary directory
  - Verifies encrypted config can be decrypted and parsed as valid JSON
  - Leaves the existing `~/.openclaw` environment untouched

### Changed
- **Publish hygiene** - Moved internal `ROADMAP.md` out of the skill package so future ClawHub releases do not include internal planning notes

## [1.2.6] - 2026-04-06

### Added
- **Enterprise Notification Support** - Added WeCom (企业微信) and Feishu (飞书) notifications
  - New channels: `wecom`, `feishu` (in addition to existing `telegram`)
  - WeCom webhook integration with mention support (`BACKUP_NOTIFY_WECOM_KEY`, `BACKUP_NOTIFY_WECOM_MENTION`)
  - Feishu webhook integration with signature verification (`BACKUP_NOTIFY_FEISHU_TOKEN`, `BACKUP_NOTIFY_FEISHU_SECRET`)
  - Updated `env.backup.notify.example` with all three channel configurations
  - Unified notification script supports all channels via `BACKUP_NOTIFY_CHANNEL` variable

### Fixed
- **Fixed `set -e` with arithmetic expressions** - Replaced `((attempt++))` with `attempt=$((attempt + 1))` in upload retry loop to prevent premature exit
- **Fixed environment variable priority in notification script** - Environment variables now correctly override config file values for all notify settings (`BACKUP_NOTIFY`, `BACKUP_NOTIFY_CHANNEL`, `BACKUP_NOTIFY_*_TOKEN`, etc.)
- **Fixed remaining `((errors++))` expressions** - Changed to `errors=$((errors + 1))` in `verify_backup_integrity()` to avoid `set -e` arithmetic return code traps
- **Fixed explicit compressor selection** - `--compress=pzstd` and `--compress=pigz` now resolve correctly instead of falling through to the wrong branch

## [1.2.5] - 2026-04-06

### Added
- **Parallel Compression** - Multi-threaded compression support for faster backups
  - Auto-detects `pigz` (parallel gzip) and `pzstd` (parallel zstd)
  - Falls back to standard `gzip`/`zstd` if parallel tools not available
  - Configurable via `PARALLEL_JOBS` (default: auto-detect CPU cores)
  - New CLI option `--jobs=N` to specify thread count
  - Updated `--compress` to accept `pigz` and `pzstd` explicitly
  - Typically 3-5x faster on multi-core systems for large directories

## [1.2.4] - 2026-04-06

### Added
- **WebDAV Upload Retry** - Automatic retry with exponential backoff for failed uploads
  - Configurable via `UPLOAD_MAX_RETRIES` (default: 3)
  - Configurable via `UPLOAD_RETRY_DELAY_BASE` (default: 2s, exponential: 2, 4, 8s)
  - Logs retry attempts and successes
  - Prevents backup failures due to transient network issues

## [1.2.3] - 2026-04-06

### Bug Fixes
- **Fixed `local` keyword outside functions** - Removed `local` declarations from main script body (lines 520, 524, 540) that caused "local: can only be used in a function" errors
- **Fixed gzip compression** - Added missing `-z` option for gzip compression in `get_tar_compress_opts()` function
- **Fixed trap scope error** - Resolved `old_trap` unbound variable error by exporting `_OLD_TRAP` and properly resetting trap before function return

### Impact
- Fixes daily cron backup failures that started on 2026-04-04
- Restores WebDAV upload functionality
- Ensures backup archives are properly compressed

## [1.2.2] - 2026-04-03

### Security Fixes
- **Path Safety** - Added path validation before `rm -rf` operations
- **Concurrent Safety** - File locking (`flock`) for snapshot operations to prevent race conditions
- **Sensitive Data Masking** - Auto-mask API keys/tokens in diff output

### Reliability Improvements
- **Error Handling** - Detailed curl error messages with HTTP status codes
- **Pre-backup Disk Check** - Verify available space before starting backup
- **Integrity Verification** - Automatic backup integrity check before restore
- **Log Rotation Safety** - File locking to prevent concurrent rotation conflicts
- **SHA-256 Checksums** - Generate and verify checksums for all backup files

### Optimizations
- **Pipefail Mode** - Added `inherit_errexit` for stricter error detection in pipelines
- **Compression Options** - Support for `gzip` (default) and `zstd` compression
- **Cleanup Library** - Centralized temp file management (`lib/cleanup.sh`)

## [1.2.0] - 2026-04-03

### Added
- **Diff Preview** - Compare current vs backup before restore
  - `openclaw-restore.sh --from <backup> --diff` - Preview changes
  - `openclaw-restore.sh --diff-format full` - Detailed comparison
  - `openclaw-diff.sh` - Standalone diff tool
  - Shows added/removed/modified files
  - Config-only diff mode for sensitive data review

- **Portable Package Export** - Export for cross-environment migration
  - `openclaw-export.sh` - Create portable tar.gz package
  - Includes workspace, extensions, config, and migration scripts
  - Generates `MIGRATION.md` guide
  - Creates `manifest.json` with requirements

- **Environment Templating** - Template environment-specific values
  - Auto-extracts gateway bind address, remote URL, model gateway
  - Generates `migrate.env.template` with all variables
  - Creates `openclaw.json.template` with placeholders
  - Supports `envsubst` for variable substitution

- **Operation Logging** - Structured logging with audit trail
  - `lib/logging.sh` - Reusable logging library
  - Log levels: DEBUG, INFO, WARN, ERROR
  - Operation start/end tracking with duration
  - Audit logging for security-sensitive operations
  - Automatic log rotation

- **Migration Scripts** - Automated migration support
  - `scripts/migrate.sh` - Apply portable package to target system
  - `scripts/check-compatibility.sh` - Verify target environment
  - Checks Node.js, npm, dependencies, disk space, ports
  - Interactive confirmation before overwrite

- **Dependency Check** - Pre-restore verification
  - `openclaw-restore.sh --check-deps` - Check system dependencies
  - Auto-check before restore (unless `--dry-run`)
  - Checks Node.js (>= 18.0.0), npm, system commands (tar, curl, openssl, git)
  - Verifies disk space (>= 500MB) and permissions
  - Network connectivity test (optional)
  - Summary with Pass/Warn/Fail counts

## [1.1.0] - 2026-04-03

### Added
- **Incremental Backup Support** - Multi-level backup strategies (Level 0/1/2)
  - Smart strategy: Sunday full backup, weekdays incremental
  - Daily strategy: First full, then auto-incremental
  - Hourly strategy: Level 0 → 1 → 2 chain for fine-grained increments
  - `--level` flag for manual level control
  - `--strategy` flag for strategy selection

- **Backup Version Management**
  - `openclaw-restore.sh --list` - List all backup versions with metadata
  - `openclaw-restore.sh --latest` - Auto-select latest backup
  - `openclaw-restore.sh --delete <timestamp>` - Delete specific backup
  - `openclaw-restore.sh --delete-old <days>` - Bulk delete old backups
  - Interactive mode - Select backup by number

- **Backup Integrity Verification**
  - Automatic integrity check after every backup
  - Validates tar.gz archive structure
  - Verifies manifest.txt and metadata files
  - Aborts on corruption to prevent storing bad backups

- **Configuration Health Check**
  - New `openclaw-healthcheck.sh` script
  - Checks base environment, backup infrastructure
  - Validates dependencies (tar, curl, openssl)
  - Verifies configuration files
  - Tests existing backup integrity
  - Returns exit code 0/1 for automation

### Enhanced
- Updated SKILL.md with comprehensive documentation
- Added README.md as quick reference
- Improved error handling with FAILED_STAGE tracking
- Better dry-run support across all operations

## [1.0.0] - 2026-03-26

### Initial Release
- Local backup with tar.gz compression
- Config encryption with AES-256-CBC
- WebDAV upload support
- Local and remote retention policies
- Telegram notifications
- Restore from local backup
- Cron scheduling support
