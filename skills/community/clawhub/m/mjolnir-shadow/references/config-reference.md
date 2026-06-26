# Configuration Reference

## backup-config.json

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `webdav_url` | string | — | WebDAV base URL (required) |
| `webdav_user` | string | — | WebDAV username (required) |
| `webdav_pass` | string | — | WebDAV password (required) |
| `remote_dir` | string | `openclaw-backups` | Remote folder name |
| `max_backups` | int | `3` | Maximum backups to keep |
| `interval_days` | int | `3` | Days between auto backups |
| `workspace_path` | string | `~/.openclaw/workspace` | Local workspace path |
| `openclaw_dir` | string | `~/.openclaw` | OpenClaw config directory |
| `backup_workspace` | bool | `true` | Include workspace files |
| `backup_config` | bool | `true` | Include OpenClaw config |
| `backup_strategies` | bool | `true` | Include trading strategies |
| `backup_skills` | bool | `true` | Include installed skills |

## Excluded Files (always)

- `.git/` — version control history
- `node_modules/` — npm dependencies (reinstallable)
- `venv/`, `.venv/` — Python virtual environments
- `__pycache__/`, `*.pyc` — Python cache
- `secrets/*.gpg` — encrypted credentials (security)

## WebDAV Compatibility

Tested with:
- ✅ Nextcloud
- ✅ ownCloud
- ✅ Synology WebDAV
- ✅ Apache mod_dav

## Rotation Strategy

The rotation uses a simple FIFO (First In, First Out) approach:

1. List all `backup_*.tar.gz` files in remote directory
2. Sort alphabetically (timestamp in name ensures chronological order)
3. If count >= max_backups, delete oldest (count - max_backups + 1) files
4. Upload new backup

This ensures exactly `max_backups` copies exist after each run.

## Cron Examples

```bash
# Every 3 days at 03:00
0 3 */3 * * Asia/Shanghai

# Daily at 02:00
0 2 * * * Asia/Shanghai

# Weekly on Sunday at 04:00
0 4 * * 0 Asia/Shanghai
```
