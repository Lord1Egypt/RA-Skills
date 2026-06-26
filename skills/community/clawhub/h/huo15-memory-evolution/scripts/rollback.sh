#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 回滚脚本
#
# 用法: ./rollback.sh <snapshot-tarball>
#
# 示例: ./rollback.sh snapshots/memory-snapshot-2026-04-08-120000.tar.gz
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SNAPSHOT_FILE="$1"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"

if [ -z "$SNAPSHOT_FILE" ]; then
    echo "❌ 用法: ./rollback.sh <snapshot-tarball>"
    echo ""
    echo "可用快照:"
    ls -la "$SKILL_DIR/snapshots/"*.tar.gz 2>/dev/null || echo "  无快照"
    exit 1
fi

if [ ! -f "$SNAPSHOT_FILE" ]; then
    echo "❌ 快照文件不存在: ${SNAPSHOT_FILE}"
    exit 1
fi

echo "🔄 huo15-memory-evolution 回滚"
echo "=============================="
echo "   快照: ${SNAPSHOT_FILE}"
echo ""

# 确认操作
read -p "⚠️  这将覆盖当前的记忆系统。是否继续? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ 回滚已取消"
    exit 0
fi

echo "📦 解压快照..."
TEMP_DIR=$(mktemp -d)
tar xzf "$SNAPSHOT_FILE" -C "$TEMP_DIR"

echo "   ✓ 已解压"

# 备份当前状态
echo "💾 备份当前状态..."
BACKUP_DIR="$SKILL_DIR/pre-rollback-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

cp -r "$WORKSPACE_DIR/MEMORY.md" "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$WORKSPACE_DIR/memory/" "$BACKUP_DIR/" 2>/dev/null || true

echo "   ✓ 当前状态已备份到: $BACKUP_DIR"

# 恢复快照
echo "🔄 恢复快照..."

# 查找解压的 workspace 目录
EXTRACTED_WORKSPACE=$(find "$TEMP_DIR" -name "workspace" -type d 2>/dev/null | head -1)

if [ -n "$EXTRACTED_WORKSPACE" ]; then
    cp -r "$EXTRACTED_WORKSPACE/MEMORY.md" "$WORKSPACE_DIR/" 2>/dev/null || true
    cp -r "$EXTRACTED_WORKSPACE/memory/"* "$WORKSPACE_DIR/memory/" 2>/dev/null || true
fi

# 恢复 openclaw.json
if [ -f "$TEMP_DIR/openclaw.json" ]; then
    cp "$TEMP_DIR/openclaw.json" "$OPENCLAW_DIR/" 2>/dev/null || true
fi

# 清理
rm -rf "$TEMP_DIR"

echo ""
echo "✅ 回滚完成!"
echo ""
echo "📦 备份仍保存在: $BACKUP_DIR"
echo ""
echo "如需确认回滚成功:"
echo "   head -20 $WORKSPACE_DIR/MEMORY.md"
