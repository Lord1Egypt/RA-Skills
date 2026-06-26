# OpenClaw + WebDAV backup and migration plan

## Goal

Use this for lightweight backup and restore of a single OpenClaw instance.

Goals:
- recover after VM deletion, corruption, or migration
- keep backup operations simple
- preserve config, memory, workspace, and extensions
- keep sensitive config encrypted before offsite upload

Core principle:

> Run OpenClaw locally. Use WebDAV only as an offsite backup target.

## What gets backed up

### Must-have
- `~/.openclaw/openclaw.json`
- `~/.openclaw/workspace/`
- `~/.openclaw/extensions/`

### Notes
- `openclaw.json` may contain tokens, API keys, and other secrets
- prefer encrypting config before remote upload
- workspace backups exclude `.env.backup` and `.env.backup.secret`

## What this plan assumes
- the user already has their own WebDAV service
- the user can provide WebDAV URL, username, and password/app token
- this skill does **not** provision WebDAV storage

## Restore model

Recommended restore flow:
1. install OpenClaw and required shell tools
2. restore workspace and extensions from a backup set
3. decrypt and restore `openclaw.json` if needed
4. restart gateway
5. verify channels, model config, plugins, and memory

## Password rule

For encrypted backups, restore depends on the **decryption password itself**.
The password can come from any one of:
1. environment variable `BACKUP_ENCRYPT_PASS`
2. `.env.backup.secret`
3. interactive password input

So `.env.backup.secret` and the password are **either/or**, not both required.

## Suggested validation after restore
- `openclaw status`
- `openclaw gateway restart`
- verify at least one messaging channel works
- verify model access works
- verify `plugins.allow` looks correct
- verify `MEMORY.md` and `memory/` are present

## Retention

Supported via environment variables:
- `LOCAL_KEEP` (default 7)
- `REMOTE_KEEP` (default 7)

Example:
```bash
LOCAL_KEEP=14 REMOTE_KEEP=14 bash scripts/openclaw-backup.sh --encrypt-config --upload
```

## Good fit / bad fit

### Good fit
- single-machine OpenClaw deployment
- simple offsite backup to an existing WebDAV service
- users willing to manage their own encryption password

### Bad fit
- users expecting built-in cloud storage
- multi-target replication
- full secret-manager integration
- one-click remote restore download flow
