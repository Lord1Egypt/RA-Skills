---
name: workspace-backup-manager
description: Manages workspace backups by creating snapshots and enabling restore points for recovery. Use when backing up workspace or restoring from backup.
---

# Workspace Backup Manager

Creates and manages workspace backup snapshots for recovery and versioning.

## Usage

```javascript
const backup = require('./skills/workspace-backup-manager');

// Create a backup
const result = backup.createBackup();

// Create named backup
const result = backup.createBackup({ name: 'before-major-change' });

// List backups
const list = backup.listBackups();
console.log(backup.formatList(list));

// Restore from backup
backup.restoreBackup({ backupName: 'backup-2026-03-26' });

// Cleanup old backups (keep last 10)
backup.cleanupBackups({ keepCount: 10 });
```

## Functions

- `createBackup(options)` - Create a new backup snapshot
- `listBackups(backupDir)` - List all available backups
- `restoreBackup(options)` - Restore workspace from a backup
- `cleanupBackups(options)` - Delete old backups, keeping most recent
- `formatList(result)` - Format backup list for display

## Backup Contents

Backs up:
- Root files: MEMORY.md, SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, TOOLS.md
- Directories: memory/, logs/

## Example Output

```
📦 Available Backups (3)

- backup-2026-03-26T03-12-00
  Created: 2026-03-26T03:12:00Z
  Files: 45 | Size: 128.5 KB

- backup-2026-03-25T18-00-00
  Created: 2026-03-25T18:00:00Z
  Files: 42 | Size: 115.2 KB

Total size: 0.24 MB
```

## CLI Usage

```bash
node -e "require('./skills/workspace-backup-manager').main()"
```

## Storage Location

Backups are stored in:
- `/root/.openclaw/workspace/backups/`
