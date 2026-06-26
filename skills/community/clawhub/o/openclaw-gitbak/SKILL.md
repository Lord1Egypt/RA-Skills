---
name: openclaw-gitbak
description: Backup/restore OpenClaw config and workspace via git.
---

# OpenClaw Git Backup/Restore

Scripts: `~/.openclaw/skills/openclaw-gitbak/scripts/`
Config: edit `~/.openclaw/skills/openclaw-gitbak/scripts/config.sh`
Format: `BACKUP_ITEMS["key"]="local_path:repo_name:description"`

# Usage
```bash
bash ~/.openclaw/skills/openclaw-gitbak/scripts/restore.sh cfg
bash ~/.openclaw/skills/openclaw-gitbak/scripts/restore.sh workspace
bash ~/.openclaw/skills/openclaw-gitbak/scripts/restore.sh all

bash ~/.openclaw/skills/openclaw-gitbak/scripts/backup.sh cfg
bash ~/.openclaw/skills/openclaw-gitbak/scripts/backup.sh workspace
bash ~/.openclaw/skills/openclaw-gitbak/scripts/backup.sh all

```
