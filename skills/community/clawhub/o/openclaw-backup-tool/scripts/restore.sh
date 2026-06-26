#!/bin/bash
# OpenClaw Restore Script
# 一键还原功能

BACKUP_DIR="$HOME/.openclaw/workspace/backups"

echo "🛡️  OpenClaw 一键还原"
echo "====================="
echo ""

# 列出可用备份（只显示 backup 开头的目录）
echo "📋 可用备份:"
ls -1t "$BACKUP_DIR" | grep "^backup_" | nl

echo ""
read -p "请输入要还原的备份编号 (直接回车=最新): " choice

if [ -z "$choice" ]; then
    LATEST=$(ls -1t "$BACKUP_DIR" | grep "^backup_" | head -1)
    BACKUP_NAME="$LATEST"
else
    BACKUP_NAME=$(ls -1t "$BACKUP_DIR" | grep "^backup_" | sed -n "${choice}p")
fi

if [ -z "$BACKUP_NAME" ] || [ ! -d "$BACKUP_DIR/$BACKUP_NAME" ]; then
    echo "❌ 无效选择，还原取消"
    exit 1
fi

echo ""
echo "⚠️  即将还原: $BACKUP_NAME"
read -p "确认还原? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "❌ 已取消"
    exit 0
fi

# 执行还原
TARGET_DIR="$BACKUP_DIR/$BACKUP_NAME"

# 还原 workspace 文件
for file in IDENTITY.md USER.md MEMORY.md SOUL.md TOOLS.md; do
    if [ -f "$TARGET_DIR/$file" ]; then
        cp "$TARGET_DIR/$file" "$HOME/.openclaw/workspace/"
        echo "✓ 还原: $file"
    fi
done

# 还原 memory 目录
if [ -d "$TARGET_DIR/memory" ]; then
    cp -r "$TARGET_DIR/memory" "$HOME/.openclaw/workspace/"
    echo "✓ 还原: memory/"
fi

if [ -f "$TARGET_DIR/openclaw.json" ]; then
    cp "$TARGET_DIR/openclaw.json" "$HOME/.openclaw/openclaw.json"
    echo "✓ 还原: openclaw.json"
fi

echo ""
echo "✅ 还原完成！"
echo "💡 运行 ocl-restart 或 openclaw gateway restart 使其生效"
