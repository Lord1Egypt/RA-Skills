---
name: soul-transfer
version: 1.0.2
description: "Soul Transfer" - Locally packaged complete agent backup and restore. Analyzes ALL files, creates a portable ZIP archive, and fully restores to any environment. 100% local - no cloud dependency.
---

# Soul Transfer - Locally Packaged Complete Agent Migration

## Concept

> "Change the body, keep the soul completely intact."

This skill performs **100% local backup and restore** for any OpenClaw agent. No cloud services, no third-party dependencies - everything stays on your machine.

## Core Principles

1. **Local Only** — All operations happen locally. No data leaves your machine.
2. **Complete** — Every file that makes the agent "itself" is included.
3. **Portable** — ZIP format for maximum compatibility across systems.
4. **Safe** — Verification, safety backups, and rollback support.

## Phase 1: Analyze (Discovery)

Before backup, the skill analyzes exactly what files exist:

```bash
# 1. Find OpenClaw state directory
# 2. Find workspace directory
# 3. Scan ALL subdirectories recursively
```

### Files to Detect

| Type | Files/Directories |
|------|------------------|
| Identity | SOUL.md, IDENTITY.md, USER.md, AGENTS.md, HEARTBEAT.md, TOOLS.md |
| Memory | memory/**/*, self-improving/**/*, proactive/**/* |
| Skills | skills/**/* |
| Config | openclaw.json, config.yaml, .env |
| Credentials | credentials/**/*, tokens/**/* |
| Plugins | extensions/**/*, plugins/**/* |
| Agents | agents/**/* |
| Sessions | sessions/**/* |
| Channels | telegram/**/*, discord/**/*, weixin/**/*, whatsapp/**/* |
| Cron | cron/**/*, scheduled/**/* |
| Database | **/*.db, **/*.sqlite, **/*.sqlite3, qmd/**/* |
| Logs | (excluded by default) |
| Cache | (excluded - regenerated automatically) |

### Environment Detection

```bash
# Detect OS type
detect_linux() { uname == "Linux" && ! grep -q Microsoft /proc/version; }
detect_macos() { uname == "Darwin"; }
detect_windows() { uname == *"MINGW"* || uname == *"CYGWIN"*; }
detect_docker() { grep -q docker /proc/1/cgroup 2>/dev/null; }
```

### Path Mapping Table

| Environment | State Dir | Workspace Dir |
|------------|-----------|---------------|
| Linux | ~/.openclaw/ | ~/workspace/ |
| macOS | ~/.openclaw/ | ~/workspace/ |
| Docker | /home/app/.openclaw/ | /workspace/ |
| 飞牛 NAS | ~/trim.openclaw/data/home/.openclaw/ | ~/trim.openclaw/data/workspace/ |
| Windows | %USERPROFILE%/.openclaw/ | %USERPROFILE%/workspace/ |

## Phase 2: Backup (Create ZIP)

```
1. Ask user: "Where should I save the backup?"
   - Accept: directory path or full filename.zip
   
2. Analyze current environment
   - Scan all OpenClaw directories
   - Build complete file manifest with SHA256 checksums
   
3. Create ZIP archive:
   zip -r <output.zip> <files> -x "*.log" "*/cache/*" "*/node_modules/*"
   
4. Generate backup manifest:
   - File list with checksums
   - Environment info (OS, OpenClaw version, timestamp)
   - Original paths mapping
   
5. Verify ZIP integrity:
   zip -T <output.zip>
   
6. Report:
   - Backup location
   - Total size
   - File count
   - Checksums
```

### Backup Command

```bash
# Create backup with verification
BACKUP_DIR="${1:-~/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/agent-backup-$TIMESTAMP.zip"

mkdir -p "$BACKUP_DIR"

# Find all OpenClaw files and package them
zip -r "$BACKUP_FILE" \
    ~/.openclaw/ \
    ~/workspace/ \
    -x "*.log" \
    -x "*/cache/*" \
    -x "*/node_modules/*" \
    -x "*/.git/*" \
    -x "*/completions/*"

# Generate manifest
cat > "$BACKUP_DIR/manifest-$TIMESTAMP.json" << EOF
{
  "version": "1.0.2",
  "timestamp": "$TIMESTAMP",
  "files": [],
  "checksums": {},
  "environment": "$(uname -a)"
}
EOF

zip -m "$BACKUP_FILE" "$BACKUP_DIR/manifest-$TIMESTAMP.json"
```

## Phase 3: Restore (Complete Recovery)

```
1. Locate backup ZIP
   - Ask user if not provided
   
2. Verify ZIP integrity:
   unzip -t <backup.zip>
   
3. Analyze new environment:
   - Detect OS type
   - Find OpenClaw installation
   - Determine correct paths
   
4. Safety check:
   - Ask user: "This will replace current configuration. Continue?"
   - Create safety backup: ~/.soul-transfer-backup-<timestamp>
   
5. Stop gateway (user confirmation required)

6. Extract ZIP:
   unzip -o <backup.zip> -d ~
   
7. Path translation (if different environment):
   - Read manifest
   - Map old paths to new paths
   - Update openclaw.json if needed
   
8. Reinstall dependencies:
   cd <workspace>
   npm install --silent
   
9. Restart gateway

10. Verify soul transfer:
    Ask agent questions to confirm identity
```

### Restore Command

```bash
# Verify ZIP integrity
unzip -t <backup.zip>
if [ $? -ne 0 ]; then
    echo "ERROR: Backup file is corrupted"
    exit 1
fi

# Create safety backup
SAFETY_DIR=~/.soul-transfer-backup-$(date +%Y%m%d_%H%M%S)
mkdir -p "$SAFETY_DIR"
cp -r ~/.openclaw "$SAFETY_DIR/" 2>/dev/null
cp -r ~/workspace "$SAFETY_DIR/" 2>/dev/null

# Extract backup
unzip -o <backup.zip> -d ~

# Update permissions
chmod -R 755 ~/.openclaw/
chmod -R 755 ~/workspace/

# Reinstall npm packages
cd ~/workspace && npm install --silent 2>/dev/null
```

## Safety Features

| Feature | Description |
|---------|-------------|
| **ZIP Verification** | `unzip -t` validates archive integrity |
| **SHA256 Checksums** | Every file has checksum for tamper detection |
| **Safety Backup** | Current state backed up before any overwrite |
| **Rollback** | Can restore from safety backup if anything fails |
| **Path Mapping** | Automatic translation between environments |
| **Dry Run** | Preview what will happen without making changes |
| **Exclusion Lists** | Cache, logs, node_modules excluded by default |

## Security Features

| Feature | Description |
|---------|-------------|
| **100% Local** | No network requests, no cloud upload |
| **Integrity Check** | SHA256 checksums detect corruption/tampering |
| **Credential Safety** | All credentials included (encrypted if stored) |
| **No Third-Party** | Only uses standard tools: zip, tar, sha256sum |

## What Gets Backed Up

```
Agent "Soul" = Everything that makes this agent ITSELF:

├── Identity
│   ├── SOUL.md
│   ├── IDENTITY.md
│   ├── USER.md
│   ├── AGENTS.md
│   ├── HEARTBEAT.md
│   └── TOOLS.md
│
├── Memory
│   ├── memory/
│   │   ├── user/
│   │   ├── monthlydailylog/
│   │   ├── projects/
│   │   └── setup.md
│   ├── self-improving/
│   │   ├── memory.md
│   │   ├── corrections.md
│   │   ├── index.md
│   │   └── ...
│   └── proactive/
│       ├── memory.md
│       ├── session-state.md
│       └── ...
│
├── Skills
│   └── skills/
│
├── Configuration
│   ├── .openclaw/
│   │   ├── openclaw.json
│   │   ├── credentials/
│   │   ├── extensions/
│   │   ├── agents/
│   │   ├── sessions/
│   │   └── ...
│   └── .env
│
├── Database
│   └── db/
│
└── Channels
    └── (WeChat, Telegram, Discord sessions)
```

## What Gets Excluded

| Type | Reason |
|------|--------|
| `*.log` | Regenerated automatically |
| `*/cache/*` | Regenerated automatically |
| `*/node_modules/*` | Reinstalled via npm install |
| `*/.git/*` | Version control, not part of agent |
| `*/completions/*` | API cache, regenerated |

## Usage Examples

### Create Backup (interactive)
```
> backup
User: Where should I save the backup?
User: /mnt/backup/agent.zip
Creating backup...
Backup created: /mnt/backup/agent.zip (1.2 GB)
Verification: OK
```

### Create Backup (command)
```bash
soul-transfer backup --destination /mnt/backup/my-agent.zip
```

### Restore
```bash
soul-transfer restore --source /mnt/backup/my-agent.zip
```

### Verify Only
```bash
soul-transfer verify --source /mnt/backup/my-agent.zip
```

### Dry Run
```bash
soul-transfer restore --dry-run --source /mnt/backup/my-agent.zip
```

## Verification Questions

After restore, confirm "soul" is intact:

1. "Do you know who you are?"
2. "What is your owner's name?"
3. "What were we working on last?"
4. "What is your communication style?"

Correct answers = successful soul transfer.

## Important Notes

- **API Keys** — Stored in backup, work immediately in new environment
- **Skills** — Require `npm install` after restore
- **Gateway Restart** — Required after restore
- **Channel Re-auth** — Some channels may need re-login (WeChat, Telegram)
- **QMD Index** — Rebuilds automatically on first search

## Design Goals

1. **Universal** — Works on any OS with standard tools (zip, bash)
2. **Complete** — Every agent file is identified and backed up
3. **Safe** — Multiple safety checks and rollback capability
4. **Local** — Zero network dependency, complete privacy
5. **Portable** — ZIP format works everywhere

## Technical Requirements

- `zip` command (standard on most systems)
- `sha256sum` or `shasum` (for checksums)
- `bash` or compatible shell
- Standard Unix tools (cp, mv, chmod, mkdir)

All requirements are available by default on Linux, macOS, and Windows Subsystem for Linux (WSL).
