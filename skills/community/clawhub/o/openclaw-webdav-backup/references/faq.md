# FAQ

## Do I need my own WebDAV service?
Yes. This skill does not provide storage. You must supply your own WebDAV URL and credentials.

## Can I use this skill without WebDAV?
Yes. You can run local backups only and skip `--upload`.

## Does restore download directly from WebDAV?
No. The current restore flow restores from a local backup directory path.

## Do I need `.env.backup.secret` to restore?
No. For encrypted backups, restore needs the decryption password. You can provide it via:
1. `BACKUP_ENCRYPT_PASS`
2. `.env.backup.secret`
3. interactive input

## What happens if I forget the backup password?
Encrypted config backups cannot be decrypted.

## What is excluded from the workspace backup?
The workspace archive excludes:
- `.env.backup`
- `.env.backup.secret`

## Does this skill manage my WebDAV account or create credentials for me?
No. It only uses the WebDAV settings the user provides.

## Is this meant for enterprise-grade disaster recovery?
No. This is a lightweight single-instance backup/restore workflow for OpenClaw.
