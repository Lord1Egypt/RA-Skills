#!/bin/bash
# OpenClaw 自动备份脚本
# 每15分钟执行，备份整个openclaw目录（排除大文件）

BACKUP_DIR="/home/acrdik/.openclaw/backups"
OPENCLAW_DIR="/home/acrdik/.openclaw"
MAX_BACKUPS=96  # 保留24小时（15分钟×96）

mkdir -p "$BACKUP_DIR"

# 生成时间戳
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/openclaw_${TIMESTAMP}.tar.gz"

# 排除目录
EXCLUDE_DIRS=(
  "--exclude=${OPENCLAW_DIR}/node_modules"
  "--exclude=${OPENCLAW_DIR}/.cache"
  "--exclude=${OPENCLAW_DIR}/agents/*/node_modules"
  "--exclude=${OPENCLAW_DIR}/workspace/skills/*/node_modules"
  "--exclude=${OPENCLAW_DIR}/backups"
  "--exclude=${OPENCLAW_DIR}/*/logs"
  "--exclude=${OPENCLAW_DIR}/*/*.log"
  "--exclude=${OPENCLAW_DIR}/media"
  "--exclude=${OPENCLAW_DIR}/*/media"
)

echo "[$(date)] 开始备份 OpenClaw..."

tar -czf "$BACKUP_FILE" "${EXCLUDE_DIRS[@]}" "$OPENCLAW_DIR" 2>/dev/null

if [ -f "$BACKUP_FILE" ]; then
  SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
  echo "[$(date)] ✅ 备份完成: openclaw_${TIMESTAMP}.tar.gz (${SIZE})"
  
  # 记录元数据
  echo "$(date +%Y-%m-%d\ %H:%M:%S)|${TIMESTAMP}|${SIZE}" >> "${BACKUP_DIR}/backup_log.txt"
  
  # 清理旧备份（只保留MAX_BACKUPS个）
  cd "$BACKUP_DIR" || exit
  ls -t openclaw_*.tar.gz 2>/dev/null | tail -n +$((MAX_BACKUPS+1)) | xargs rm -f 2>/dev/null
  echo "[$(date)] 🧹 旧备份已清理，保留最近${MAX_BACKUPS}个"
else
  echo "[$(date)] ❌ 备份失败"
  exit 1
fi
