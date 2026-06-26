#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 快照备份脚本（精简版）
#
# 用法: ./snapshot.sh
#
# 功能: 备份记忆系统文件（不包含 session logs 和 daily logs）
# 输出: snapshots/memory-snapshot-YYYY-MM-DD-HHMMSS.tar.gz
#
# 包含:
#   - MEMORY.md
#   - memory/index.json
#   - memory/{user,feedback,project,reference}/ 下的 .md 文件
#   - skills/huo15-memory-evolution/scripts/ 下的脚本
#
# 不包含（太大）:
#   - memory/activity/ （session logs）
#   - memory/YYYY-MM-DD.md （daily logs）
#   - memory/archive/ （已归档）
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"
SNAPSHOT_DIR="$SKILL_DIR/snapshots"
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
OUTPUT_FILE="${SNAPSHOT_DIR}/memory-snapshot-${TIMESTAMP}.tar.gz"

echo "📸 huo15-memory-evolution 快照备份（精简版）"
echo "================================"
echo ""

# 创建快照目录
mkdir -p "$SNAPSHOT_DIR"

# 收集信息
echo "📋 收集当前状态..."
MEMORY_LINES=$(wc -l < "$WORKSPACE_DIR/MEMORY.md" 2>/dev/null || echo "N/A")
SKILL_VERSION=$(grep "version" "$SKILL_DIR/SKILL.md" 2>/dev/null | head -1 || echo "unknown")

cat << EOF > "${SNAPSHOT_DIR}/snapshot-info-${TIMESTAMP}.txt"
# 快照信息
快照时间: $(date -u +%Y-%m-%dT%H:%M:%SZ)
版本: ${SKILL_VERSION}
主机: $(hostname)

# 主 workspace
MEMORY.md 行数: ${MEMORY_LINES}

# 记忆文件统计
user:     $(find "$WORKSPACE_DIR/memory/user" -name "*.md" 2>/dev/null | wc -l | tr -d ' ') 个
feedback: $(find "$WORKSPACE_DIR/memory/feedback" -name "*.md" 2>/dev/null | wc -l | tr -d ' ') 个
project:  $(find "$WORKSPACE_DIR/memory/project" -name "*.md" 2>/dev/null | wc -l | tr -d ' ') 个
reference:$(find "$WORKSPACE_DIR/memory/reference" -name "*.md" 2>/dev/null | wc -l | tr -d ' ') 个
EOF

echo "   ✓ 状态信息已收集"

# 创建 tarball（只包含记忆系统文件，不含 logs）
echo "📦 创建快照压缩包..."

tar czf "$OUTPUT_FILE" \
    -C "$WORKSPACE_DIR" \
        MEMORY.md \
        memory/index.json \
        memory/user/*.md \
        memory/feedback/*.md \
        memory/project/*.md \
        memory/reference/*.md \
    -C "$SKILL_DIR" \
        scripts/ \
    2>/dev/null || {
        echo "   ⚠️ 部分文件打包失败，继续..."
    }

if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "   ✓ 快照已创建: snapshots/memory-snapshot-${TIMESTAMP}.tar.gz"
    echo "   ✓ 大小: ${SIZE}"
else
    echo "   ❌ 快照创建失败"
    exit 1
fi

echo ""
echo "📋 下次回滚: ./rollback.sh ${OUTPUT_FILE}"
