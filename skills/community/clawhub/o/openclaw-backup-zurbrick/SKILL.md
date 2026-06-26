---
name: openclaw-backup
description: >
 Encrypted backup and restore for OpenClaw agents. Creates two-tier archives:
 cloud-safe operational backups plus optional age-encrypted secrets for local
 recovery. Use when setting up disaster recovery, backing up your agent,
 verifying backup integrity, restoring from backup, or pushing safe archives to GitHub.
---

# OpenClaw Backup

Use this skill for **backup, verify, restore, and disaster-recovery workflows** for an OpenClaw workspace.

## Use when

- setting up backup and restore for an OpenClaw agent or workspace
- creating a cloud-safe operational backup
- creating an encrypted secrets backup for local recovery
- verifying a backup set before trusting it
- dry-running or executing a restore
- pushing an operational backup archive to GitHub

## Do not use when

- the user wants general file sync or generic backup advice unrelated to OpenClaw
- you only need a one-off copy of a few files
- secrets would be pushed or shared without encryption
- the restore target or archive path is unclear

## Default workflow

1. **Identify the job**
   Choose one lane:
   - backup
   - verify
   - restore
   - push operational archive to GitHub
   - schedule / drill / pre-change snapshot

2. **Start with the core path**
   Use the main scripts first:
   - `bash {baseDir}/scripts/backup.sh`
   - `bash {baseDir}/scripts/verify.sh --manifest <path>/manifest.json --archive <path>/backup.tar.gz`
   - `bash {baseDir}/scripts/restore.sh --manifest <path>/manifest.json --archive <path>/backup.tar.gz --dry-run`
   - `bash {baseDir}/scripts/push-to-github.sh --manifest <path>/manifest.json --archive <path>/backup.tar.gz`

3. **Keep the archive model straight**
   Default to **operational-only** backups for cloud storage.
   Secrets are opt-in and must stay encrypted with `age`.

4. **Use dry-run before restore**
   Restore is high-blast-radius. Prefer `--dry-run` before a real restore.

5. **Load references only as needed**
   - `references/restore-guide.md` — full disaster recovery walkthrough
   - `references/what-to-backup.md` — file coverage and rationale
   - `references/retention-policy.md` — retention guidance
   - `references/workflows.md` — weekly verify, monthly drill, pre-change snapshot, CI

## Archive model

| Tier | Contents | Cloud safe? | Encrypted? |
|------|----------|-------------|------------|
| **Operational** | Workspace, redacted config, crons | Yes | No (no secrets) |
| **Secrets** | `.env`, agent auth profiles | No | Required (`age`) |

Default: operational only. Secrets are opt-in via `--include-secrets`.

## Prerequisites

- `age` for secrets encryption
- `gh` for GitHub push (optional)

## Configuration

Set encryption via environment or flags:

```bash
export AGE_RECIPIENT="age1your_public_key"
export AGE_PASSPHRASE_FILE="/path/to/passphrase"

bash {baseDir}/scripts/backup.sh --include-secrets --age-recipient age1...
```

## Safety rules

- Never push secrets unless they are encrypted
- Prefer verify before restore, and dry-run before live restore
- Treat restore as destructive until proven otherwise
- If paths or archive contents are ambiguous, stop and clarify

## References

- `{baseDir}/references/restore-guide.md`
- `{baseDir}/references/what-to-backup.md`
- `{baseDir}/references/retention-policy.md`
- `{baseDir}/references/workflows.md`
