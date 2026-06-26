# Auto Backup for OpenClaw

Automatic backup for OpenClaw configuration files.

[中文版本](README_CN.md)

---

## ✨ Features

- 📦 **Manual Backup** - Backup anytime
- ⏰ **Scheduled Backup** - Auto backup at 2 AM daily
- 📚 **Version Management** - View all backup versions
- 🔄 **One-Click Restore** - Restore to any version
- 🧹 **Auto Cleanup** - Keep last N backups

---

## 🚀 Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/williamwg2025/openclaw-auto-backup.git auto-backup
chmod +x auto-backup/scripts/*.py
```

---

## 📖 Usage

### Backup

```bash
# Manual backup
python3 auto-backup/scripts/backup.py

# With note
python3 auto-backup/scripts/backup.py --note "After config update"
```

### List Backups

```bash
python3 auto-backup/scripts/list.py
```

### Restore

```bash
# Restore to specific version
python3 auto-backup/scripts/restore.py --version backup-20260310-195545

# Restore to previous version
python3 auto-backup/scripts/restore.py --offset -1
```

### Cleanup

```bash
# Keep last 10 backups
python3 auto-backup/scripts/cleanup.py --keep 10

# Delete backups older than 30 days
python3 auto-backup/scripts/cleanup.py --older-than 30d
```

---

## ⏰ Scheduled Task

Configured to auto backup daily at 2 AM.

View cron jobs:
```bash
openclaw cron list
```

---

## 📋 Configuration

Backup config:
`~/.openclaw/workspace/skills/auto-backup/config/backup-config.json`

Backup location:
`~/.openclaw/backups/`

---

## 🛠️ Scripts

| Script | Function |
|--------|----------|
| `backup.py` | Backup configs |
| `list.py` | List backups |
| `restore.py` | Restore configs |
| `cleanup.py` | Cleanup old backups |

---

## 📄 License

MIT-0

---

**Author:** @williamwg2025  
**Version:** 1.0.0
