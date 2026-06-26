#!/bin/bash
set -euo pipefail

# OpenClaw 恢复最新备份

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"

echo "🐈‍⬛ 恢复最新备份"
echo "备份目录: $BACKUP_ROOT"
echo ""

if [ ! -d "$BACKUP_ROOT" ]; then
    echo "❌ 备份目录不存在"
    exit 1
fi

cd "$BACKUP_ROOT"

LATEST_ENCRYPTED=$(ls -t openclaw_backup_*.tar.gz.enc 2>/dev/null | head -1)
LATEST_PLAIN=$(ls -t openclaw_backup_*.tar.gz 2>/dev/null | grep -v ".enc" | head -1)

if [ -n "$LATEST_ENCRYPTED" ]; then
    echo "发现最新加密备份: $LATEST_ENCRYPTED"
    LATEST="$BACKUP_ROOT/$LATEST_ENCRYPTED"
    SCRIPT="restore_encrypted.sh"
elif [ -n "$LATEST_PLAIN" ]; then
    echo "发现最新备份: $LATEST_PLAIN"
    LATEST="$BACKUP_ROOT/$LATEST_PLAIN"
    SCRIPT="restore.sh"
else
    echo "❌ 未找到备份文件"
    exit 1
fi

echo ""
echo "确认恢复？[y/N]"
read -p "> " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "取消恢复"
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/$SCRIPT" "$LATEST"
