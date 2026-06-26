# 🔐 OpenClaw Backup

**Encrypted backup and restore for OpenClaw agents.**

`openclaw-backup` creates two-tier archives for disaster recovery:
- **operational backups** that are safe to store in the cloud
- **encrypted secrets backups** for local recovery only

It is built for the real failure modes:
- dead disks
- bad config edits
- broken gateway restarts
- lost cron definitions
- corrupted local state

## What it does

### 1. Backup
Create a backup set with:
- operational archive
- optional encrypted secrets archive
- manifest with checksums and metadata

### 2. Verify
Validate that a backup set is structurally sound before trusting it.

### 3. Restore
Use staged restore with dry-run support and rollback protection.

### 4. Push operational archive to GitHub
Keep the cloud-safe backup separate from secrets.

## Quick start

```bash
# Operational backup only
bash scripts/backup.sh

# Include encrypted secrets
bash scripts/backup.sh --include-secrets --age-recipient age1your_public_key

# Verify a backup set
bash scripts/verify.sh --manifest path/to/manifest.json --archive path/to/backup.tar.gz

# Dry-run restore
bash scripts/restore.sh --manifest path/to/manifest.json --archive path/to/backup.tar.gz --dry-run
```

## Archive model

| Tier | Contents | Cloud safe? | Encrypted? |
|------|----------|-------------|------------|
| **Operational** | Workspace, redacted config, crons | Yes | No |
| **Secrets** | `.env`, auth profiles | No | Required (`age`) |

Default: operational only.
Secrets are opt-in.

## Safety model

- secrets never go to cloud storage unencrypted
- verify before restore
- prefer dry-run before live restore
- restore uses staging and preserves the previous state
- manifest checksums are validated before restore

## Common workflows

The runtime skill stays lean. For deeper operations, use the references:

- `references/restore-guide.md` — detailed recovery walkthrough
- `references/what-to-backup.md` — what belongs in the archive and why
- `references/retention-policy.md` — retention rules
- `references/workflows.md` — weekly verify, monthly drill, pre-change snapshot, CI

## Included scripts

- `scripts/backup.sh`
- `scripts/verify.sh`
- `scripts/restore.sh`
- `scripts/push-to-github.sh`
- `scripts/schedule.sh`
- `scripts/weekly-verify.sh`
- `scripts/monthly-drill.sh`
- `scripts/pre-change-snapshot.sh`

## Requirements

- `age` for encrypted secrets backups
- `gh` for GitHub push (optional)

## License

MIT
