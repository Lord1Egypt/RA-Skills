---
name: healthy-backup
version: 1.3.0
description: Health-gated backup for OpenClaw rigs. Audits first — only backs up if healthy. Three tiers, 5-backup retention, optional rclone sync. Sensitive config values scrubbed before staging. Linux/cron native.
metadata: {"openclaw":{"emoji":"🩺","requires":{"bins":["tar","gpg","jq","rsync"]}}}
---

# Healthy Backup
Version: 1.3.0

**A health-first backup skill for OpenClaw.**

Before touching a single file, `healthy-backup` audits your rig. If anything critical is broken, it aborts with a clear report. No silent snapshots of a broken state.

---

## How it works

1. **Health audit** — checks required binaries, config integrity, key directories, disk space, encryption readiness, secrets file permissions, and optional rclone remote
2. **Hard block** — any failing check aborts the backup immediately with a full report
3. **Stage** — collects files for your chosen tier; secret-bearing paths are always excluded (see Secrets policy)
4. **Compress → Encrypt (AES256 GPG) → Save**
5. **Prune** — keeps the last N healthy backups; older archives are deleted
6. **Sync** (optional) — pushes to your configured rclone remote

Run with `--dry-run` to execute the full audit and see exactly what would be staged — without writing anything.

---

## Secrets policy (enforced in code)

### openclaw.json — scrubbed before staging

`openclaw.json` is **never copied verbatim**. Before staging, the script uses `jq walk()` to replace the *value* of any field whose name contains `password`, `token`, `secret`, or `key` with `"<redacted>"`. Config structure and all non-sensitive values are preserved. The live file on disk is never modified.

> **Recommendation:** store your backup password in `~/.openclaw/credentials/backup.key` (chmod 600) rather than inline in `openclaw.json`. The health audit will warn if an inline password is detected.

### rsync exclusions — always applied, no config override

The following paths are hard-excluded from rsync at every tier:

```
~/.openclaw/shared/secrets/
~/.openclaw/credentials/
**/*.key  **/*.pem  **/*.env  **/*.secret  **/.env
```

### Secrets manifest

At all tiers the script reads `openclaw-secrets.env` to extract variable *names* only — values are never written. The resulting `secrets-manifest.txt` lists what environment variables your rig expects, useful for rebuilding on a new machine.

### GPG passphrase

Written to a `chmod 600` temp file and passed to GPG via `--passphrase-file` — never on the CLI, never visible in `ps`. Deleted via `trap EXIT` on success or failure.

---

## What this script reads

This section lists every file and system call the script makes, so there are no surprises:

| What | Why | Sensitive? |
|------|-----|-----------|
| `~/.openclaw/openclaw.json` | Load config + stage (scrubbed copy) | Sensitive fields redacted before staging |
| `~/.openclaw/shared/secrets/openclaw-secrets.env` | Extract variable *names* for manifest | Values never written; file never copied |
| `~/.openclaw/credentials/backup.key` | Load encryption password | Read into memory only; file excluded from rsync |
| `~/.openclaw/` (migratable+) | rsync to staging | Secrets paths hard-excluded |
| Workspace + skills dirs (full tier) | rsync to staging | Secrets paths hard-excluded |
| `command -v <bin>` | Check required binaries exist | No |
| `df -m $HOME` | Check available disk space | No |
| `ollama list` (audit + opt-in manifest) | Check models loaded / list for DEPENDENCIES.md | Model names only |
| `npm list -g` (opt-in, default off) | List global packages for DEPENDENCIES.md | Can reveal installed tooling |
| `crontab -l` (opt-in, default off) | List cron jobs for DEPENDENCIES.md | VAR=values redacted before writing |
| `rclone listremotes` (if uploadMode=rclone) | Verify configured remote exists | No |
| `rclone sync` (if uploadMode=rclone) | Upload encrypted archives | Transfers only `*.gpg` files |

No network calls are made by the script itself beyond `rclone` when explicitly configured.

---

| Tier | What's included |
|------|----------------|
| `minimal` | `openclaw.json` + secrets manifest (key names only) |
| `migratable` | Everything in minimal + `~/.openclaw` (secrets excluded) + `DEPENDENCIES.md` |
| `full` | Everything in migratable + workspace + skills (secrets excluded in all) |

Default tier: `migratable`

### DEPENDENCIES.md

Generated for `migratable` and `full` tiers. By default, only binary versions and OS info are collected. Sensitive system state (crontab, npm globals) requires explicit opt-in:

| Config key | Default | What it collects |
|------------|---------|-----------------|
| `collectOllama` | `true` | Installed Ollama model names |
| `collectNpm` | `false` | `npm list -g --depth=0` output |
| `collectCrontab` | `false` | Crontab — values after `=` are redacted before staging |

Even when `collectCrontab` is enabled, any `VAR=VALUE` patterns in cron lines are replaced with `VAR=<REDACTED>` before the file is written.

---

## Setup

### 1. Run the setup wizard

```bash
chmod +x setup.sh healthy-backup.sh verify-backup.sh
bash setup.sh
```

The wizard will ask about tier, backup location, retention, cloud sync, and optional collectors. It writes config to `~/.openclaw/config/healthy-backup/hb-config.json`, creates your encryption key file if needed, runs a dry-run automatically, and optionally installs the cron job — all in one flow.

To reconfigure at any time, just run `bash setup.sh` again.

### 2. System dependencies

```bash
sudo apt install tar gpg jq rsync        # Debian/Ubuntu
sudo dnf install tar gpg jq rsync        # Fedora/RHEL
```

For rclone (only required when `uploadMode = rclone`):

```bash
# Preferred — package manager:
sudo apt install rclone    # Debian/Ubuntu
sudo dnf install rclone    # Fedora/RHEL

# Alternative — official binary. Download and inspect BEFORE running:
curl -fsSL https://rclone.org/install.sh -o rclone-install.sh
cat rclone-install.sh        # review it first
sudo bash rclone-install.sh
# Do NOT pipe curl directly to bash without reviewing the script.
```

These are OS-level binaries, listed in skill metadata for dependency checking only — not as npm packages.

### 2. Encryption password (choose one — in priority order)

```bash
# Recommended: key file with strict permissions
mkdir -p ~/.openclaw/credentials
echo "your-strong-password" > ~/.openclaw/credentials/backup.key
chmod 600 ~/.openclaw/credentials/backup.key

# Or: environment variable
export BACKUP_PASSWORD="your-strong-password"

# Or: inline in skill config (least preferred — see config section)
```

The health audit checks that `backup.key` has permissions `600` and will hard-fail if it does not.

### 3. Install the script

```bash
# Place wherever you keep scripts:
chmod +x /path/to/healthy-backup.sh

# Recommended: test run before scheduling — audits rig and shows what would be staged:
/path/to/healthy-backup.sh --dry-run
```

### 4. Schedule with cron (Linux)

```bash
crontab -e
```

Example — daily at 03:00:

```
0 3 * * * /path/to/healthy-backup.sh >> ~/.openclaw/logs/healthy-backup.log 2>&1
```

---

## Configuration

All config lives in `~/.openclaw/openclaw.json` under `skills.entries["healthy-backup"].config`.

```json
{
  "skills": {
    "entries": {
      "healthy-backup": {
        "config": {
          "backupTier":       "migratable",
          "backupRoot":       "~/openclaw-backups",
          "uploadMode":       "local-only",
          "remoteDest":       "gdrive:openclaw-backups",
          "maxBackups":       5,
          "minDiskMb":        500,
          "collectOllama":    true,
          "collectNpm":       false,
          "collectCrontab":   false
        }
      }
    }
  }
}
```

> **Do not add a `password` field here.** Although the script scrubs it from the backup copy, the value would still exist in your live `openclaw.json` on disk. Use `~/.openclaw/credentials/backup.key` (chmod 600) instead — it is excluded from staging entirely.
```

### Full configuration reference

| Key | Env var | Default | Description |
|-----|---------|---------|-------------|
| `backupTier` | `BACKUP_TIER` | `migratable` | `minimal` / `migratable` / `full` |
| `backupRoot` | `BACKUP_ROOT` | `~/openclaw-backups` | Local backup storage directory |
| `uploadMode` | `UPLOAD_MODE` | `local-only` | `local-only` or `rclone` |
| `remoteDest` | `REMOTE_DEST` | _(none)_ | rclone destination e.g. `gdrive:backups` |
| `maxBackups` | `MAX_BACKUPS` | `5` | Healthy backups to retain |
| `minDiskMb` | `MIN_DISK_MB` | `500` | Minimum free disk (MB) required |
| `skillsDir` | `SKILLS_DIR` | `~/.openclaw/skills` | Skills directory |
| `collectOllama` | `COLLECT_OLLAMA` | `true` | Include Ollama model list in DEPENDENCIES.md |
| `collectNpm` | `COLLECT_NPM` | `false` | Include npm globals in DEPENDENCIES.md (opt-in) |
| `collectCrontab` | `COLLECT_CRONTAB` | `false` | Include sanitised crontab in DEPENDENCIES.md (opt-in) |
| `password` | `BACKUP_PASSWORD` | _(none)_ | ⚠ Discouraged — prefer key file; if set, value is scrubbed from backup copy but remains in live config |

**Priority:** Config file → Env var → Auto-detect

---

## Health checks

| Check | Behaviour |
|-------|-----------|
| Required binaries (`tar`, `gpg`, `jq`, `rsync`) | Hard fail |
| `rclone` present (if `uploadMode = rclone`) | Hard fail |
| `openclaw.json` is valid JSON | Hard fail |
| Key directories exist (OpenClaw dir, workspace) | Hard fail |
| Free disk ≥ `minDiskMb` | Hard fail |
| Encryption password available | Hard fail |
| `backup.key` permissions = 600 (if file exists) | Hard fail |
| Secrets file permissions = 600 (if file exists) | Hard fail |
| rclone remote reachable (if `uploadMode = rclone`) | Hard fail |
| Skills dir present | Warn only |
| Ollama models loaded | Warn only |
| No agents in config | Warn only |

---

## Archive contents

```
config/openclaw.json            ← always present
config/secrets-manifest.txt     ← key names only, no values (migratable+)
openclaw/                       ← ~/.openclaw minus secrets paths (migratable+)
workspace/                      ← workspace minus secrets paths (full only)
skills/                         ← skills minus secrets paths (full only)
DEPENDENCIES.md                 ← system snapshot (migratable+, opt-in fields)
HEALTH_REPORT.txt               ← full audit log from backup time
```

---

## Verifying the script

After downloading, verify the script has not been modified:

```bash
sha256sum healthy-backup.sh
```

Compare the output against the checksum published in the skill's release or provided by the author. The script also prints its own SHA256 on every successful run so you can confirm the installed version matches what ran.

---

## Restore

```bash
gpg --batch --passphrase-file /path/to/backup.key \
    --decrypt healthy-backup-YYYYMMDD-HHMMSS-migratable.tgz.gpg \
  | tar -xzf - -C /restore/target
```

---

## Security checklist

- [ ] `backup.key` exists and has `chmod 600`
- [ ] `openclaw-secrets.env` has `chmod 600`
- [ ] Backup root directory is not world-readable
- [ ] If using rclone cloud sync: prefer `rclone crypt` remote for an additional encryption layer
- [ ] Tested decryption of at least one archive before relying on backups
- [ ] `collectCrontab` and `collectNpm` left `false` unless you specifically need them

---

## Credits

Inspired by and building on:
- **simple-backup** by VACInc — GPG + rclone pattern, config resolution hierarchy
- **claw-backup** by vidarbrekke — tier thinking, dependency manifests, restore notes

---

## License

MIT

---

## Release checksums (v1.3.0)

Verify your downloaded files match these SHA256 hashes before running:

```
a8e0f8e922c05755a43a8bb156a327984d9fbc50a620ce08e172a48d72f79a39  healthy-backup.sh
ae0bda0195e408aee84f441a39494995f8cd1eb5578eba07d0870810d6ad1433  verify-backup.sh
185fa27b052ed1c9d294f4d40a7700a501683906b0d6d2e75ab059532decbd4f  setup.sh
```

```bash
sha256sum healthy-backup.sh verify-backup.sh setup.sh
```
