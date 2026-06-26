#!/bin/bash
# OpenClaw Backup Script
# 自动备份关键配置文件

BACKUP_DIR="$HOME/.openclaw/workspace/backups"
DATE=$(date +%Y-%m-%d_%H%M%S)
BACKUP_NAME="backup_$DATE"

# 需要备份的关键文件
FILES=(
    "$HOME/.openclaw/workspace/IDENTITY.md"
    "$HOME/.openclaw/workspace/USER.md"
    "$HOME/.openclaw/workspace/MEMORY.md"
    "$HOME/.openclaw/workspace/SOUL.md"
    "$HOME/.openclaw/workspace/TOOLS.md"
    "$HOME/.openclaw/openclaw.json"
    "$HOME/.openclaw/workspace/memory/"
)

mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

echo "🛡️  OpenClaw 备份中..."
echo "====================="

for file in "${FILES[@]}"; do
    if [ -e "$file" ]; then
        cp -r "$file" "$BACKUP_DIR/$BACKUP_NAME/"
        echo "✓ 备份: $file"
    fi
done

echo ""
echo "✅ 备份完成: $BACKUP_NAME"
echo "📁 位置: $BACKUP_DIR/$BACKUP_NAME"
