# Restore notes

## Basic restore
```bash
bash scripts/openclaw-restore.sh --from backups/openclaw/latest
```

## Restore + decrypt config
```bash
bash scripts/openclaw-restore.sh --from backups/openclaw/latest --decrypt-config
```

## Dry-run restore drill
```bash
bash scripts/openclaw-restore.sh --from backups/openclaw/latest --decrypt-config --dry-run
```

## What gets restored
- `workspace.tar.gz` -> `~/.openclaw/workspace/`
- `extensions.tar.gz` -> `~/.openclaw/extensions/`
- `openclaw.json` or decrypted `openclaw.json.enc` -> `~/.openclaw/openclaw.json`

## Decryption rule
For encrypted backups, restore needs the decryption password.
It can be provided through any one of:
1. environment variable `BACKUP_ENCRYPT_PASS`
2. `.env.backup.secret`
3. interactive password input

So `.env.backup.secret` and the password are **either/or**, not both required.

## Post-restore checks
Recommended follow-up:
- `openclaw status`
- `openclaw gateway restart`
- verify Telegram / Weixin / model / plugins.allow / memory

## Troubleshooting
- If decrypt fails, first verify the password, not just the presence of `.env.backup.secret`
- If WebDAV upload had worked before but restore is local-only, remember this script restores from a local backup directory path
- If the user wants cross-machine recovery, make sure they know or have stored the backup password
