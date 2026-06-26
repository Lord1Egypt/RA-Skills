#!/bin/bash
# 项目共享系统 — 自动备份
# 每次更新时自动创建快照备份

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
BACKUP_DIR="$WORKSPACE/backups/project_system"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# 备份 JSON
cp "$WORKSPACE/projects_status.json" "$BACKUP_DIR/projects_status_$TIMESTAMP.json"

# 备份 MD
cp "$WORKSPACE/PROJECT_STATUS.md" "$BACKUP_DIR/PROJECT_STATUS_$TIMESTAMP.md"

# 生成快照
bash "$WORKSPACE/scripts/project_snapshot.sh" "$BACKUP_DIR/snapshot_$TIMESTAMP.md" > /dev/null 2>&1

# 保留最近 30 个备份
ls -t "$BACKUP_DIR"/projects_status_*.json | tail -n +31 | xargs rm -f 2>/dev/null
ls -t "$BACKUP_DIR"/PROJECT_STATUS_*.md | tail -n +31 | xargs rm -f 2>/dev/null

echo "✅ 备份完成: $BACKUP_DIR (保留最近30个版本)"
echo "   JSON: projects_status_$TIMESTAMP.json"
echo "   MD:   PROJECT_STATUS_$TIMESTAMP.md"
echo "   快照: snapshot_$TIMESTAMP.md"
