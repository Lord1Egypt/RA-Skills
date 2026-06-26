---
name: openclaw-webdav-backup
description: Backup and restore an OpenClaw workspace with incremental backups, integrity verification, health checks, optional config encryption and optional WebDAV upload. Supports full/incremental backup strategies (smart/daily/hourly), backup version management (list/select/delete), and configuration health diagnostics. Use when users want OpenClaw backup, restore, VM migration/disaster recovery, encrypted config backups, WebDAV-based offsite copies, scheduled backups, or backup integrity monitoring. Users must provide their own WebDAV service and credentials.
---

# OpenClaw WebDAV Backup

Lightweight backup/restore skill for OpenClaw.

It covers:
- local backup archives (full and incremental)
- multi-level backup strategies (smart, daily, hourly)
- optional encryption for `openclaw.json`
- optional WebDAV upload
- restore from local backup archives
- backup version management (list, select, delete)
- backup integrity verification
- configuration health checks
- lightweight scheduled backup guidance
- optional Telegram notifications for backup success/failure

It does **not** provide WebDAV storage. The user must supply their own WebDAV endpoint and credentials.

## When to use this skill

Use this skill when the user asks to:
- back up OpenClaw (full or incremental)
- restore OpenClaw from backup
- migrate OpenClaw to a new VM or machine
- protect backup configs with encryption
- upload backups to a self-provided WebDAV target
- schedule daily or periodic backups
- receive Telegram notifications for scheduled backup success/failure
- prepare a simple disaster-recovery workflow
- check backup configuration health
- verify backup integrity
- manage backup versions (list, delete old backups)

## Implementation layout

Canonical implementation lives inside the skill:
- `scripts/openclaw-backup.impl.sh`
- `scripts/openclaw-restore.impl.sh`

Thin wrapper scripts may also exist in the workspace and call these implementations. Keep the skill scripts as the source of truth.

## Default workflow

### 1. Local backup (full)
```bash
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh
```

### 2. Incremental backup with smart strategy
Auto-determines level based on day:
- Sunday: Level 0 (full backup)
- Monday-Saturday: Level 1 (incremental)

```bash
# Smart strategy (recommended for cron)
BACKUP_STRATEGY=smart bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh

# Or explicitly set level
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh --level=1
```

### 3. Encrypted backup + WebDAV upload
🔴 CHECKPOINT: Confirm with the user before uploading to any remote WebDAV target. This operation sends potentially sensitive data (including encrypted configs) to an external server. Only proceed after explicit user confirmation.

Prepare `.env.backup` with the user's own WebDAV settings, then run:
```bash
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh --encrypt-config --upload
```
Only do real upload after confirming the user wants to write to the remote WebDAV target.

### 4. Restore from a local backup set
🛑 STOP: Restore will overwrite current workspace files. Before proceeding, confirm with the user:
  1. The backup path is correct
  2. They have a current backup of the current state (in case rollback is needed)
  3. They understand this is a destructive operation on the workspace directory

```bash
bash skills/openclaw-webdav-backup/scripts/openclaw-restore.sh --from backups/openclaw/latest --decrypt-config
```

## ⚠️ Failure Mode Encoding

If any backup, upload, restore, or notification operation fails, follow the table below:

| Trigger Condition | First-Line Fix | If Still Failing (Fallback) |
|------------------|---------------|---------------------------|
| WebDAV upload fails (curl error) | Retry with `--retry 3`, verify `.env.backup` credentials | Fall back to local-only backup, notify user with error details |
| Backup integrity check fails (`tar -tzf` error) | Report specific archive corruption path, do NOT proceed with restore | Suggest manual inspection of the backup directory and logs |
| Encryption fails (openssl unavailable) | Check `openssl version` and install if missing | Fall back to unencrypted backup with a clear security warning |
| Restore source missing or corrupted | Verify backup path exists with `ls -la` | List available backups for user to select an alternative |
| Disk space insufficient for backup | Run `df -h .` and suggest cleanup | Abort with available-space-required message and suggestions |
| Notification send fails (Telegram/WeCom/Feishu) | Check network, verify token/key in `.env.backup.notify` | Log failure locally and continue; backup itself is not affected |
| Compression tool unavailable (pigz/pzstd) | Auto-fallback to gzip/zstd (single-threaded) | Log warning about degraded performance, proceed with gzip |

## Backup Strategies

The skill supports multiple backup strategies via `BACKUP_STRATEGY` environment variable:

| Strategy | Description | Level Behavior |
|----------|-------------|----------------|
| `full` (default) | Always full backup | Level 0 |
| `weekly` | Weekly full backup | Level 0 |
| `daily` | Daily with auto-incremental | Level 0 once, then Level 1 |
| `smart` | Recommended for production | Sunday=Level 0, Mon-Sat=Level 1 |
| `hourly` | Fine-grained incremental | Level 0 → 1 → 2 chain |

### Level Explanation

- **Level 0**: Full backup (tar creates complete archive + snapshot file)
- **Level 1**: Incremental backup (only files changed since Level 0)
- **Level 2**: Incremental backup (only files changed since Level 1)

### Cron Examples

```bash
# Smart strategy: Sunday full, weekdays incremental
0 0 * * 0 BACKUP_STRATEGY=smart /path/to/openclaw-backup.sh --upload
30 3 * * 1-6 BACKUP_STRATEGY=smart /path/to/openclaw-backup.sh --upload

# Weekly full only
0 3 * * 0 BACKUP_STRATEGY=weekly /path/to/openclaw-backup.sh --upload

# Daily with auto-level detection
0 3 * * * BACKUP_STRATEGY=daily /path/to/openclaw-backup.sh
```

### Manual Level Control

Override auto-detection with `--level` flag:
```bash
bash openclaw-backup.sh --level=0  # Force full backup
bash openclaw-backup.sh --level=1  # Force incremental (level 1)
```

## Compression Options

The skill supports multiple compression tools with automatic detection of parallel variants:

| Option | Tool | Threads | Notes |
|--------|------|---------|-------|
| `gzip` | gzip | 1 | Standard, widely available |
| `pigz` | pigz | N | Parallel gzip, 3-5x faster |
| `zstd` | zstd | 1 | High compression ratio |
| `pzstd` | pzstd | N | Parallel zstd, fastest option |

### Auto-Detection

By default, the skill auto-detects the best available compressor:
```bash
# Prefers pigz > gzip, pzstd > zstd
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh
```

### Explicit Selection

Force a specific compressor:
```bash
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh --compress=pigz
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh --compress=pzstd
```

### Parallel Jobs

Control the number of compression threads (default: auto-detect CPU cores):
```bash
# Use 8 threads explicitly
PARALLEL_JOBS=8 bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh

# Or via CLI
bash skills/openclaw-webdav-backup/scripts/openclaw-backup.sh --jobs=8
```

### Installation

Install parallel compression tools for best performance:
```bash
# Ubuntu/Debian
sudo apt-get install pigz zstd

# macOS
brew install pigz zstd

# CentOS/RHEL
sudo yum install pigz zstd
```

## Backup Notifications

The skill supports multiple notification channels for backup success/failure alerts.

### Supported Channels

| Channel | Status | Configuration |
|---------|--------|---------------|
| Telegram | ✅ Ready | Bot token + Chat ID |
| WeCom (企业微信) | ✅ Ready | Webhook key |
| Feishu (飞书) | ✅ Ready | Webhook token |

### Quick Setup

1. Copy the example config:
```bash
cp references/env.backup.notify.example .env.backup.notify
```

2. Edit `.env.backup.notify` with your channel settings:

#### Telegram Setup
```bash
BACKUP_NOTIFY=1
BACKUP_NOTIFY_CHANNEL="telegram"
BACKUP_NOTIFY_TELEGRAM_CHAT_ID="123456789"
BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN="123456:your-bot-token"  # Optional, can auto-detect
```

#### WeCom (企业微信) Setup
```bash
BACKUP_NOTIFY=1
BACKUP_NOTIFY_CHANNEL="wecom"
BACKUP_NOTIFY_WECOM_KEY="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
BACKUP_NOTIFY_WECOM_MENTION="13800138000,13900139000"  # Optional: mobile numbers
```
*Get webhook key from: Group Settings → Add Robot → Copy Webhook URL key*

#### Feishu (飞书) Setup
```bash
BACKUP_NOTIFY=1
BACKUP_NOTIFY_CHANNEL="feishu"
BACKUP_NOTIFY_FEISHU_TOKEN="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
BACKUP_NOTIFY_FEISHU_SECRET="your-secret"  # Optional: if signature enabled
```
*Get webhook token from: Group Settings → Add Bot → Copy Webhook URL token*

### Notification Content

Notifications include:
- Backup status (✅ success / ❌ failure)
- Timestamp and backup type
- Local backup location
- Encryption status
- WebDAV upload status
- Retention settings

## 🚫 Anti-Patterns & Blacklist

Do NOT do the following when using or maintaining this skill:

| 🚫 Anti-Pattern | Why | Correct Approach |
|----------------|-----|----------------|
| Commit `.env.backup` or `.env.backup.secret` to git | Leaks WebDAV credentials and encryption keys permanently | Add to `.gitignore`; only share via secure channel |
| Hardcode real credentials in example files | Examples get copied into scripts and committed | Always use placeholder values (`your_webdav_url`, `your_password`) |
| Run restore without user confirmation | Overwrites the current workspace irreversibly | Use `--dry-run` first, then confirm with user |
| Delete old backups without asking | User may need older backups for audit/recovery | List available versions, let user choose which to delete |
| Upload unencrypted `openclaw.json` to remote | Contains API keys, tokens, and secrets | Always use `--encrypt-config` before `--upload` |
| Run destructive operations without `--dry-run` | No way to preview what will happen | Always offer dry-run first; restore supports `--dry-run` flag |
| Include real tokens in `.env.backup.notify` examples | Notification tokens can be misused if leaked | Use placeholder values in docs; store real values separately |

## 🔴 Critical Checkpoints

The following operations require explicit user confirmation before proceeding:

| Operation | Checkpoint | Risk Level |
|-----------|-----------|------------|
| WebDAV upload | Confirm remote target and data sensitivity | 🔴 High |
| Restore from backup | Confirm backup path, destructive nature, current state backup | 🔴 High |
| Encrypted config backup | Confirm encryption password is recoverable | 🟡 Medium |

## Important behavior notes

- `openclaw.json` may contain secrets, tokens, and API keys
- prefer `--encrypt-config` before remote upload
- `.env.backup` stores WebDAV connection settings and should not be committed
- `.env.backup.secret` is optional; it is only a convenience carrier for `BACKUP_ENCRYPT_PASS`
- `.env.backup.notify` is optional and enables backup notifications when configured
- restore depends on the **decryption password itself**, not on the secret file specifically
- for encrypted backups, `.env.backup.secret` and the password are **either/or**: either keep the file, or remember/provide the password
- workspace backups exclude `.env.backup` and `.env.backup.secret`
- local and remote retention are supported through `LOCAL_KEEP` and `REMOTE_KEEP`

## Read references when needed

- For usage, included files, and backup examples: read `references/backup.md`
- For restore/decrypt flow and restore checks: read `references/restore.md`
- For automation with cron/systemd: read `references/scheduling.md`
- For migration/disaster-recovery planning: read `references/migration-plan.md`
- For common user questions and boundary clarifications: read `references/faq.md`
- For config template examples: read `references/env.backup.example`, `references/env.backup.secret.example`, and `references/env.backup.notify.example`

## Validated behaviors

This skill has been validated against a real OpenClaw setup for:
- local backup creation
- encrypted config backup
- WebDAV upload
- local and remote retention
- restore drill to a simulated fresh-machine home directory
- cron-based scheduled backup
- Telegram notification on backup success
- backup integrity verification
- configuration health checks

## Health Check & Integrity Verification

### Configuration Health Check

Run `scripts/openclaw-healthcheck.sh` to diagnose backup environment:

```bash
bash skills/openclaw-webdav-backup/scripts/openclaw-healthcheck.sh
```

Checks performed:
| Check | Description |
|-------|-------------|
| Base Environment | workspace dir, state dir, openclaw.json, extensions |
| Backup Infrastructure | backup root, snapshot dir, existing backups |
| Dependencies | tar, curl, openssl availability |
| Configuration | .env.backup, .env.backup.secret variables |
| Backup Integrity | Validates all existing tar.gz archives |

Exit codes:
- `0` - All checks passed
- `1` - One or more critical checks failed

### Backup Integrity Verification

Every backup automatically runs integrity checks:

1. **Archive validation** - `tar -tzf` verifies archive structure
2. **Manifest verification** - Confirms manifest.txt exists
3. **Metadata check** - Confirms workspace.meta exists

Failed integrity checks will abort the backup with error status.

To manually verify a specific backup:
```bash
tar -tzf backups/openclaw/2026-04-02-030000/workspace.tar.gz >/dev/null && echo "Valid" || echo "Corrupted"
```

### Restore with Integrity Check

When restoring, verify the backup before extraction:

```bash
# Check integrity first
bash scripts/openclaw-restore.sh --from <backup_dir> --dry-run

# Then perform actual restore
bash scripts/openclaw-restore.sh --from <backup_dir>
```

## Private-share checklist

Before sharing this skill privately, verify:
- no real `.env.backup` or `.env.backup.secret` is included
- no real WebDAV URL, username, password, token, or backup passphrase remains in tracked files
- examples use placeholder values only
- docs state clearly that WebDAV storage is user-provided
- restore wording states password and secret file are either/or, not both required
- references match actual script behavior

## Scope

This skill intentionally stays lightweight. It supports:
- local backup and restore
- optional config encryption
- optional WebDAV upload
- local and remote retention
- password-based restore with optional secret file automation

It does not currently provide:
- built-in WebDAV provisioning
- secret-manager integration
- fully automatic remote download-and-restore flow
- multi-target cloud replication
