# Architecture

PaperMC AI Operations - System Architecture

## Overview

This skill provides a controlled interface for AI agents to manage PaperMC Minecraft servers safely.

## Design Principles

1. **Safety First**: All operations go through approved scripts
2. **Backup-First**: Mandatory backups before risky operations
3. **Audit Trail**: All actions logged and traceable
4. **No Direct Commands**: System commands mediated through Python layer

## Components

### Control Layer (Python Scripts)

| Script | Purpose |
|--------|---------|
| `manage_server.py` | Service lifecycle, logs, backups |
| `plugin_manager.py` | Plugin operations |
| `update_paper.py` | PaperMC jar updates |

### System Layer

- systemd service (paper-mc.service)
- Journald logging
- File system operations

### Data Layer

- World data (world/, world_nether/, world_the_end/)
- Plugin data (plugins/)
- Backups (backup/, plugin_backup/, jar_backup/)

## Workflow Examples

### Backup Workflow
```
Agent → manage_server.py backup → backup.sh → tar.gz archive
```

### Plugin Update
```
Agent → plugin_manager.py backup → plugin_manager.py install-url → restart
```

### PaperMC Update
```
Agent → update_paper.py backup-jar → update_paper.py update-from-url → restart
```

## Security

- No secrets in repository
- Configuration via environment variables
- Backup retention policies
- Controlled access to system resources
