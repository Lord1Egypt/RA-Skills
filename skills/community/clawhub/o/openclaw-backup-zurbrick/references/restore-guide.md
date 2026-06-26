# Restore Guide

## Overview

Use this guide when moving OpenClaw to a new machine, recovering from disk loss, rolling back to a known-good state, or restoring only selected pieces of the agent.

## Backup set layout

A backup run now creates a timestamped run directory containing:

- `openclaw-backup-YYYY-MM-DD.tar.gz` — operational archive
- `openclaw-secrets-YYYY-MM-DD.tar.gz.age` — optional encrypted secrets archive
- `manifest.json` — checksums, sizes, versions, timestamp, and file inventory

Operational archives are the only files intended for cloud/private GitHub storage by default. Secrets archives stay local unless the operator explicitly decides otherwise.

## Full restore on a new Mac or Linux host

1. Install the base OpenClaw environment first.
   - Confirm the `openclaw` CLI works.
   - Sign in or pair the node if your setup requires it.
2. Install `age` if you plan to restore secrets.
   - macOS: `brew install age`
   - Linux: `apt install age`
3. Copy the backup set onto the new machine.
4. Verify the archive set before restoring:

   ```bash
   bash scripts/verify.sh --manifest /path/to/manifest.json --archive /path/to/openclaw-backup-YYYY-MM-DD.tar.gz [--secrets /path/to/openclaw-secrets-YYYY-MM-DD.tar.gz.age]
   ```

5. Dry-run the restore first:

   ```bash
   bash scripts/restore.sh --manifest /path/to/manifest.json --archive /path/to/openclaw-backup-YYYY-MM-DD.tar.gz --dry-run
   ```

6. Restore it for real:

   ```bash
   bash scripts/restore.sh --manifest /path/to/manifest.json --archive /path/to/openclaw-backup-YYYY-MM-DD.tar.gz
   ```

7. If you also need secrets, provide decryption material:

   ```bash
   bash scripts/restore.sh \
     --manifest /path/to/manifest.json \
     --archive /path/to/openclaw-backup-YYYY-MM-DD.tar.gz \
     --secrets /path/to/openclaw-secrets-YYYY-MM-DD.tar.gz.age \
     --age-identity ~/.config/age/keys.txt
   ```

8. Restart the gateway:

   ```bash
   openclaw gateway restart
   ```

9. Re-test the system.
   - `openclaw gateway status`
   - Run a simple local task
   - Confirm scheduled jobs are present and sane

## Atomic restore behavior

`restore.sh` now restores through a safety workflow:

1. Verify checksums from `manifest.json`
2. Extract to `~/.openclaw/.restore-staging`
3. Confirm critical files exist in staging
4. Move the current installation to `~/.openclaw/.pre-restore-backup-TIMESTAMP`
5. Atomically move staged content into place
6. Run `workspace/scripts/pre-restart-check.sh` if present
7. Roll back automatically if the health check fails
8. Suggest `openclaw gateway restart`

## Partial restore

If only one area is broken, extract the operational archive to a temp directory and copy the specific subtree you need.

### Restore workspace only

```bash
TMP_DIR="$(mktemp -d)"
tar -xzf /path/to/openclaw-backup-YYYY-MM-DD.tar.gz -C "$TMP_DIR"
cp -R "$TMP_DIR/openclaw/workspace/." "$HOME/.openclaw/workspace/"
rm -rf "$TMP_DIR"
```

### Restore config only

```bash
TMP_DIR="$(mktemp -d)"
tar -xzf /path/to/openclaw-backup-YYYY-MM-DD.tar.gz -C "$TMP_DIR"
cp "$TMP_DIR/openclaw/openclaw.json" "$HOME/.openclaw/openclaw.json"
rm -rf "$TMP_DIR"
```

### Restore cron definitions only

```bash
TMP_DIR="$(mktemp -d)"
tar -xzf /path/to/openclaw-backup-YYYY-MM-DD.tar.gz -C "$TMP_DIR"
mkdir -p "$HOME/.openclaw/cron"
cp "$TMP_DIR/openclaw/cron/jobs.json" "$HOME/.openclaw/cron/jobs.json"
rm -rf "$TMP_DIR"
```

## Post-restore checklist

- Verify critical files exist
- Review secrets restoration separately from operational data
- Restart OpenClaw gateway
- Confirm cron jobs still make sense on this host
- Reinstall or reconnect external dependencies not stored in the archive
- Run one real task to prove the agent is alive
