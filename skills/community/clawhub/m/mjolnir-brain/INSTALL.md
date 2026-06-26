# 🧠 Mjolnir Brain — Installation Guide

## Prerequisites

### Required (core memory system)
- [OpenClaw](https://github.com/openclaw/openclaw) installed and running
- That's it! The core memory system is pure Markdown + JSON — no binaries needed.

### Optional (automation scripts)
Only needed if you want to use the scripts in `scripts/`:
- **bash 4+** — all scripts
- **git** — `auto_commit.sh`
- **grep** (with `-P` support) — `memory_search.sh`
- **tar, gzip** — `memory_consolidate.sh` (archiving old logs)
- **curl** — `workspace_backup.sh` (only if WebDAV backup enabled)
- **ssh, scp** — `workspace_backup.sh` (only if SSH backup enabled)

> ⚠️ You can use the full memory system (templates, strategies, Write-Through, heartbeats) without installing any scripts or cron jobs.

## Method 1: OpenClaw Skill (Recommended)

```bash
clawdhub install mjolnir-brain
```

This installs the skill and makes templates available. You still need to copy templates to your workspace:

```bash
# The skill will guide you through setup on first use
```

## Method 2: Manual Installation

### Step 1: Clone

```bash
git clone https://github.com/YOUR_USER/mjolnir-brain.git
cd mjolnir-brain
```

### Step 2: Copy Core Templates (required)

```bash
WORKSPACE="${HOME}/.openclaw/workspace"

# Copy template files — this is the core memory system
cp templates/AGENTS.md "$WORKSPACE/"
cp templates/SOUL.md "$WORKSPACE/"
cp templates/BOOTSTRAP.md "$WORKSPACE/"
cp templates/IDENTITY.md "$WORKSPACE/"
cp templates/USER.md "$WORKSPACE/"
cp templates/MEMORY.md "$WORKSPACE/"
cp templates/HEARTBEAT.md "$WORKSPACE/"

# Copy strategy registry
cp strategies.json "$WORKSPACE/"

# Create memory directory
mkdir -p "$WORKSPACE/memory"

# Create playbooks directory
mkdir -p "$WORKSPACE/playbooks"
cp playbooks/README.md "$WORKSPACE/playbooks/"
cp playbooks/frequency.json "$WORKSPACE/playbooks/"
```

### Step 3: Copy Scripts (optional — review before using!)

> ⚠️ **Audit the scripts before copying.** They will be able to read/write files in your workspace. See [docs/security.md](docs/security.md) for details.

```bash
# Only copy if you want automation features
cp -r scripts "$WORKSPACE/"
chmod +x "$WORKSPACE/scripts/"*.sh
```

### Step 4: Initialize Git

```bash
cd "$WORKSPACE"
git init
git add -A
git commit -m "init: Mjolnir Brain memory system"
```

### Step 5: Set Up Cron Jobs (Optional — OPT-IN)

> **⚠️ 所有 cron 任务均为可选 (OPT-IN)，请在审查脚本后手动启用。** 不启用 cron 不影响核心记忆功能的使用。

```bash
crontab -e
```

Add these lines:

```cron
# Memory consolidation — daily at 04:00
0 4 * * * ~/.openclaw/workspace/scripts/memory_consolidate.sh >> ~/.openclaw/workspace/memory/consolidate.log 2>&1

# Auto git commit — every hour
0 * * * * ~/.openclaw/workspace/scripts/auto_commit.sh

# Workspace backup — daily at 04:00 (configure targets in script first)
# 0 4 * * * ~/.openclaw/workspace/scripts/workspace_backup.sh >> ~/.openclaw/workspace/memory/backup.log 2>&1
```

### Step 6: Configure Backup (Optional — OPT-IN)

Edit `scripts/workspace_backup.sh` and set your backup targets:

```bash
# WebDAV (e.g., Nextcloud)
WEBDAV_URL="http://your-nextcloud/remote.php/webdav/backup/"
WEBDAV_USER="your_user"
WEBDAV_PASS="your_pass"

# SSH remote
SSH_HOST="your-server"
SSH_PATH="/backups/workspace/"
```

### Step 7: Start Using

1. Start an OpenClaw session
2. The agent reads `BOOTSTRAP.md` and guides you through identity setup
3. After setup, `BOOTSTRAP.md` is deleted
4. The memory system runs automatically from here

## Verification

After installation, check that everything is in place:

```bash
cd ~/.openclaw/workspace

# Templates
ls -la AGENTS.md SOUL.md MEMORY.md HEARTBEAT.md BOOTSTRAP.md

# Scripts
ls -la scripts/*.sh

# Strategy registry
cat strategies.json | python3 -m json.tool | head -5

# Memory directory
ls -la memory/

# Cron jobs
crontab -l | grep openclaw
```

## Uninstall

```bash
# Remove scripts (keep your data!)
rm -rf ~/.openclaw/workspace/scripts/memory_consolidate.sh
rm -rf ~/.openclaw/workspace/scripts/memory_search.sh
rm -rf ~/.openclaw/workspace/scripts/strategy_*.sh
rm -rf ~/.openclaw/workspace/scripts/auto_commit.sh
rm -rf ~/.openclaw/workspace/scripts/workspace_backup.sh
rm -rf ~/.openclaw/workspace/scripts/daily_log_init.sh
rm -f ~/.openclaw/workspace/strategies.json

# Remove cron jobs
crontab -l | grep -v openclaw | crontab -

# Your MEMORY.md, AGENTS.md, SOUL.md etc. are YOUR data — keep them!
```
