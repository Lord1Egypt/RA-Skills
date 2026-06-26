# OpenClaw Backup Restore

**Never lose your agent's memory or config.** Backup, restore, and daily GitHub sync for OpenClaw workspace state.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18-brightgreen)](https://nodejs.org/)

---

## What is OpenClaw Backup Restore?

OpenClaw Backup Restore protects your OpenClaw agent's personality, configuration, and memory by creating timestamped snapshots of critical workspace files:

- `SOUL.md` — agent personality and mission
- `USER.md` — user profile and preferences
- `AGENTS.md` — agent instructions and workflows
- `IDENTITY.md` — agent identity configuration
- `TOOLS.md` — local tool configuration
- `HEARTBEAT.md` — periodic task configuration
- `BOOTSTRAP.md` — initialization instructions
- `~/.openclaw/openclaw.json` — OpenClaw config file (sanitized by default, real config optional)

**Problem:** Accidental deletion or bad configuration changes can destroy your agent's personality. Manual git setup is complex. No built-in OpenClaw backup exists.

**Solution:** One-command backup/restore with validation, rollback, version history, automatic `git add` / `commit` / `push`, built-in daily backup to GitHub, and optional real `openclaw.json` config backup for true off-machine recovery.

---

## Quick Start

### Installation

```bash
cd ~/.openclaw/workspace-YOUR-AGENT
git clone https://github.com/X-RayLuan/openclaw-backup-restore.git
cd openclaw-backup-restore
chmod +x scripts/*.mjs
```

### Create Your First Backup

```bash
# Default: backup workspace files + sanitized openclaw.json
node scripts/backup.mjs

# Include the real ~/.openclaw/openclaw.json config file in the backup
node scripts/backup.mjs --raw-openclaw-config
```

Output:
```
🔍 Starting SOUL backup...
✅ Backed up: SOUL.md (2194 bytes)
✅ Backed up: USER.md (343 bytes)
✅ Backed up: AGENTS.md (747 bytes)
📦 Backup complete!
   Location: backups/2026-03-05T00-51-30
   Files backed up: 6
```

### List Backups

```bash
node scripts/list.mjs
```

### Restore from Backup

```bash
# Preview what will change (dry run)
node scripts/restore.mjs --dry-run

# Restore latest backup
node scripts/restore.mjs

# Restore specific backup
node scripts/restore.mjs --timestamp 2026-03-05T00-51-30
```

### Validate Backup Integrity

```bash
node scripts/validate.mjs
```

---

## Features

✅ **One-click backup** — Create timestamped snapshots in seconds  
✅ **Instant restore** — Roll back to any previous state  
✅ **Automatic validation** — SHA-256 checksums detect corruption  
✅ **Version history** — Track agent evolution with named backups  
✅ **Pre-restore safety** — Every restore creates automatic rollback point  
✅ **Single-file restore** — Restore only specific files (e.g., `SOUL.md`)  
✅ **Zero dependencies** — Uses only Node.js built-ins (crypto, fs, path)
✅ **OpenClaw config backup** — Backs up `~/.openclaw/openclaw.json` in sanitized mode by default, or real mode with `--raw-openclaw-config`
✅ **Auto git sync** — Built-in `git add` / `git commit` / `git push` flow via `backup-and-push.mjs`
✅ **Daily GitHub backup** — Ready-to-use daily remote backup pattern included

---

## Usage Examples

### Named Backups for Milestones

```bash
# Before major refactor
node scripts/backup.mjs --name "pre-migration" --desc "Before switching to new SOUL format"

# Restore named backup
node scripts/restore.mjs --name "pre-migration"
```

### Single File Restore

```bash
# Restore only SOUL.md
node scripts/restore.mjs --file SOUL.md
```

### Config File Backup Modes

```bash
# Default mode: backup a sanitized copy of ~/.openclaw/openclaw.json
node scripts/backup.mjs

# Real backup mode: include the actual config file for full recovery
node scripts/backup.mjs --raw-openclaw-config
```

Use real config mode only with a private backup repo.

### Rollback After Bad Restore

```bash
# Every restore creates pre-restore-TIMESTAMP backup
node scripts/list.mjs | grep pre-restore

# Rollback
node scripts/restore.mjs --timestamp pre-restore-2026-03-05T01-20-00
```

---

## Documentation

- **[SKILL.md](SKILL.md)** — Full user documentation
- **[RUNBOOK.md](RUNBOOK.md)** — Operations manual and recovery scenarios
- **[FEATURE_DEFINITION.md](FEATURE_DEFINITION.md)** — Commercial positioning and roadmap

---

## Recovery Scenarios

### Scenario 1: Accidental File Deletion

```bash
node scripts/restore.mjs --file SOUL.md
```

### Scenario 2: Bad Configuration Change

```bash
# Find previous backup
node scripts/list.mjs

# Restore it
node scripts/restore.mjs --timestamp <previous-backup>
```

### Scenario 3: Complete Workspace Corruption

```bash
# Validate backups
node scripts/validate.mjs

# Restore from last good backup
node scripts/restore.mjs --timestamp <last-good>
```

---

## Backup Structure

By default, real backups are stored **outside the skill repo** to keep skill code and backup data separated:

```text
~/.openclaw/backups/openclaw-backup-restore-clawlite/
```

And the Git-tracked daily backup mirror lives separately at:

```text
~/.openclaw/backup-repos/openclaw-backup-restore-clawlite/
```

Structure:

```
~/.openclaw/backups/openclaw-backup-restore-clawlite/
├── 2026-03-05T00-51-30/
│   ├── manifest.json          # Backup metadata
│   ├── SOUL.md
│   ├── USER.md
│   ├── AGENTS.md
│   ├── IDENTITY.md
│   ├── TOOLS.md
│   ├── HEARTBEAT.md
│   ├── BOOTSTRAP.md
│   └── openclaw.json or openclaw.sanitized.json
├── 2026-03-05T01-15-42/
│   └── ...
└── named/
    ├── pre-migration/
    │   └── ...
    └── stable-v1/
        └── ...
```

Each backup includes a `manifest.json` with:
- Timestamp and description
- File sizes and SHA-256 hashes
- Workspace path and OpenClaw version

---

## Automation

### Daily Backup (Cron)

```bash
# Add to crontab: crontab -e
0 2 * * * cd ~/.openclaw/workspace-YOUR-AGENT/openclaw-backup-restore && /usr/local/bin/node scripts/backup-and-push.mjs --remote origin --message "backup: daily-$(date +\%Y-\%m-\%d)"
```

### Daily Backup (GitHub Actions)

A ready-to-use workflow is included at:

```text
.github/workflows/daily-backup.yml
```

It runs once per day and uses the same built-in backup + git sync script.

### Pre-Deployment Hook

```bash
# Before deploying changes
cd ~/.openclaw/workspace-YOUR-AGENT/soul-backup
node scripts/backup.mjs --name "pre-deploy-$(git rev-parse --short HEAD)"
```

---

## Requirements

- Node.js 18+
- OpenClaw workspace with SOUL files
- No external npm packages required

---

## Roadmap

**v1.0 (Current):**
- Local backups with validation
- Manual backup/restore
- 30-day retention

**v2.0 (Planned):**
- Cloud sync (Dropbox, S3)
- Automatic daily backups
- Encrypted backups
- Web UI

**v3.0 (Future):**
- Team backup sharing
- Role-based access control
- Audit logs

---

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Support

- **Issues:** [GitHub Issues](https://github.com/X-RayLuan/soul-backup-skill/issues)
- **Repository:** [X-RayLuan/soul-backup-skill](https://github.com/X-RayLuan/soul-backup-skill)
- **ClawHub:** [openclaw-workspace-backup-restore](https://clawhub.ai/skills/openclaw-workspace-backup-restore)

---

## Credits

Built for the OpenClaw community.

Inspired by the need for production-grade reliability in AI agent deployments.

---

## Related Projects

- [OpenClaw](https://github.com/openclaw/openclaw) — The AI agent framework
- [ClawHub](https://clawhub.com) — OpenClaw skill marketplace
- [ClawLite](https://clawlite.ai) — Commercial OpenClaw distribution

---

**Made with ❤️ for the OpenClaw community**
