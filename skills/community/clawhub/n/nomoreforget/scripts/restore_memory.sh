#!/bin/bash
# No More Forget 记忆恢复脚本

BACKUP_BASE="$HOME/.openclaw/memory-backups"
WORKSPACE_DIR="$HOME/.openclaw/workspace"

echo "🔄 记忆恢复工具"
echo ""

# 检查备份目录
if [ ! -d "$BACKUP_BASE" ]; then
    echo "❌ 未发现备份目录: $BACKUP_BASE"
    echo "   请先运行备份: bash scripts/backup_memory.sh"
    exit 1
fi

# 列出可用备份
echo "可用备份列表："
echo ""

ls -1dt "$BACKUP_BASE"/backup_* 2>/dev/null | head -10 | nl -w2 -s') ' | while read line; do
    backup_path=$(echo "$line" | awk '{print $2}')
    backup_name=$(basename "$backup_path")
    
    if [ -f "$backup_path/backup_info.txt" ]; then
        size=$(grep "总大小" "$backup_path/backup_info.txt" | cut -d: -f2)
    else
        size=$(du -sh "$backup_path" 2>/dev/null | cut -f1)
    fi
    
    echo "$line  [$size]"
done

echo ""
read -p "选择要恢复的备份编号 (1-10, q 退出): " choice

if [ "$choice" = "q" ]; then
    echo "已取消"
    exit 0
fi

# 获取选择的备份路径
SELECTED_BACKUP=$(ls -1dt "$BACKUP_BASE"/backup_* 2>/dev/null | sed -n "${choice}p")

if [ -z "$SELECTED_BACKUP" ]; then
    echo "❌ 无效选择"
    exit 1
fi

echo ""
echo "⚠️  即将从以下备份恢复:"
echo "   $SELECTED_BACKUP"
echo ""
read -p "确认恢复？这将覆盖当前记忆文件 (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 执行恢复
echo ""
echo "正在恢复..."

# 恢复 MEMORY.md
if [ -f "$SELECTED_BACKUP/MEMORY.md" ]; then
    cp "$SELECTED_BACKUP/MEMORY.md" "$WORKSPACE_DIR/"
    echo "✅ 已恢复 MEMORY.md"
fi

# 恢复 memory 目录
if [ -d "$SELECTED_BACKUP/memory" ]; then
    rm -rf "$WORKSPACE_DIR/memory"
    cp -r "$SELECTED_BACKUP/memory" "$WORKSPACE_DIR/"
    echo "✅ 已恢复 memory 目录"
fi

# 恢复其他文件
for file in SOUL.md USER.md AGENTS.md; do
    if [ -f "$SELECTED_BACKUP/$file" ]; then
        cp "$SELECTED_BACKUP/$file" "$WORKSPACE_DIR/"
        echo "✅ 已恢复 $file"
    fi
done

echo ""
echo "✅ 恢复完成！"