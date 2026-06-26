#!/bin/bash
set -euo pipefail

# OpenClaw 备份列表

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"

echo "🐈‍⬛ OpenClaw 备份列表"
echo "位置: $BACKUP_ROOT"
echo ""

if [ ! -d "$BACKUP_ROOT" ]; then
    echo "❌ 备份目录不存在"
    exit 1
fi

cd "$BACKUP_ROOT"

TOTAL_FILES=$(ls -1 openclaw_backup_*.tar.gz* 2>/dev/null | grep -v ".sha256" | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh . | cut -f1)

echo "📦 共 $TOTAL_FILES 个备份文件，总计 $TOTAL_SIZE"
echo ""

ls -lht openclaw_backup_*.tar.gz* 2>/dev/null | grep -v ".sha256" | while read -r line; do
    SIZE=$(echo "$line" | awk '{print $5}')
    DATE=$(echo "$line" | awk '{print $6, $7, $8}')
    FILE=$(echo "$line" | awk '{print $9}')
    
    if [[ "$FILE" == *.enc ]]; then
        ENCRYPTED="🔐 加密"
    else
        ENCRYPTED="📂 未加密"
    fi
    
    if [ -f "$FILE.sha256" ]; then
        CHECKSUM="✓"
    else
        CHECKSUM="✗"
    fi
    
    echo "[$ENCRYPTED] $FILE"
    echo "  大小: $SIZE | 日期: $DATE | 校验: $CHECKSUM"
    echo ""
done

echo "验证备份完整性："
echo "  shasum -c openclaw_backup_XXXX.tar.gz.sha256"
