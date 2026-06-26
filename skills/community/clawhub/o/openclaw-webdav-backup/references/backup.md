# Backup notes

## What this skill does
- Creates local backup archives for OpenClaw workspace, extensions, and config
- Can encrypt `openclaw.json` before upload
- Can upload backup sets to a **user-provided** WebDAV endpoint
- Can keep only the latest local/remote backups via `LOCAL_KEEP` and `REMOTE_KEEP`

## What this skill does not do
- It does **not** provide WebDAV storage
- It does **not** manage the user's WebDAV account
- It does **not** store real credentials in tracked files

## Minimum config
Create `.env.backup` with:
- `WEBDAV_URL`
- `WEBDAV_USER`
- `WEBDAV_PASS`

## Encryption password sources
When `--encrypt-config` is used, `BACKUP_ENCRYPT_PASS` can come from:
1. environment variable
2. `.env.backup.secret`
3. interactive password input

This means the secret file and password are **either/or**. Restore depends on the password itself.

## Optional Telegram notifications
Create `.env.backup.notify` if the user wants success/failure notifications for scheduled backups.

Minimum example:
- `BACKUP_NOTIFY=1`
- `BACKUP_NOTIFY_CHANNEL=telegram`
- `BACKUP_NOTIFY_TELEGRAM_CHAT_ID=...`

Optional:
- `BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN=...`

If Telegram bot token is omitted, the notify script will try to read it from `~/.openclaw/openclaw.json`.

Current status:
- Telegram notification is supported
- WeChat notification is not implemented yet

## Common commands
```bash
bash scripts/openclaw-backup.sh
bash scripts/openclaw-backup.sh --upload --dry-run
bash scripts/openclaw-backup.sh --encrypt-config --upload
LOCAL_KEEP=14 REMOTE_KEEP=14 bash scripts/openclaw-backup.sh --encrypt-config --upload
```

## Security notes
- Prefer `--encrypt-config` before remote upload
- Do not commit `.env.backup` or `.env.backup.secret`
- Workspace backup archives exclude `.env.backup` and `.env.backup.secret`
- Save the backup password in a password manager if the user wants cross-machine recovery
