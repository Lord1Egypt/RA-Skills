#!/bin/bash
# No More Forget 记忆备份脚本

BACKUP_BASE="$HOME/.openclaw/memory-backups"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_BASE/backup_$TIMESTAMP"

echo "💾 记忆备份工具"
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份 MEMORY.md
if [ -f "$WORKSPACE_DIR/MEMORY.md" ]; then
    cp "$WORKSPACE_DIR/MEMORY.md" "$BACKUP_DIR/"
    echo "✅ 已备份 MEMORY.md"
fi

# 备份 memory 目录
if [ -d "$WORKSPACE_DIR/memory" ]; then
    cp -r "$WORKSPACE_DIR/memory" "$BACKUP_DIR/"
    echo "✅ 已备份 memory 目录"
fi

# 备份其他关键文件
for file in SOUL.md USER.md AGENTS.md; do
    if [ -f "$WORKSPACE_DIR/$file" ]; then
        cp "$WORKSPACE_DIR/$file" "$BACKUP_DIR/"
        echo "✅ 已备份 $file"
    fi
done

# 创建备份信息
cat > "$BACKUP_DIR/backup_info.txt" << EOF
备份时间: $(date '+%Y-%m-%d %H:%M:%S')
备份路径: $BACKUP_DIR
文件数量: $(find "$BACKUP_DIR" -type f | wc -l)
总大小: $(du -sh "$BACKUP_DIR" | cut -f1)
EOF

# 清理旧备份（保留最近 10 个）
BACKUP_COUNT=$(ls -1d "$BACKUP_BASE"/backup_* 2>/dev/null | wc -l)
if [ $BACKUP_COUNT -gt 10 ]; then
    echo ""
    echo "🧹 清理旧备份..."
    ls -1dt "$BACKUP_BASE"/backup_* | tail -n +11 | xargs rm -rf
    echo "   已保留最近 10 个备份"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "✅ 备份完成！"
echo "   路径: $BACKUP_DIR"
echo "   大小: $(du -sh "$BACKUP_DIR" | cut -f1)"
echo "═══════════════════════════════════════════════════════"