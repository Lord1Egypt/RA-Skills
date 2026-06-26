#!/bin/bash
#===============================================================================
# Plan Mode 初始化脚本
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE="$HOME/.openclaw/workspace"

echo "========================================"
echo "Plan Mode 初始化"
echo "========================================"
echo ""

# 创建日志目录
echo "[1/4] 创建日志目录..."
mkdir -p "$WORKSPACE/memory/activity"
echo "   [OK] $WORKSPACE/memory/activity/"

# 创建日志文件
echo "[2/4] 创建日志文件..."
if [ ! -f "$WORKSPACE/memory/activity/plan-mode-log.md" ]; then
    cat > "$WORKSPACE/memory/activity/plan-mode-log.md" << 'EOF'
# Plan Mode 操作日志

## 日志格式
`## 时间 | 操作 | 命令 | 结果`

EOF
    echo "   [OK] plan-mode-log.md"
else
    echo "   [SKIP] 已存在"
fi

# 设置权限
echo "[3/4] 设置脚本权限..."
chmod +x "$SCRIPT_DIR/plan-mode.sh"
echo "   [OK] plan-mode.sh"

# 创建 HEARTBEAT 集成
echo "[4/4] 创建 HEARTBEAT 集成..."
mkdir -p "$WORKSPACE/memory/activity"

# 检查是否已有 HEARTBEAT.md
if [ -f "$WORKSPACE/HEARTBEAT.md" ]; then
    # 追加 Plan Mode 检查
    if ! grep -q "Plan Mode" "$WORKSPACE/HEARTBEAT.md"; then
        echo "" >> "$WORKSPACE/HEARTBEAT.md"
        echo '## ⚠️ Plan Mode 检查' >> "$WORKSPACE/HEARTBEAT.md"
        echo '检测到危险操作时暂停，等待用户确认后再执行' >> "$WORKSPACE/HEARTBEAT.md"
        echo "   [OK] 已集成到 HEARTBEAT.md"
    else
        echo "   [SKIP] HEARTBEAT.md 已包含 Plan Mode"
    fi
else
    # 创建新的 HEARTBEAT.md
    cat > "$WORKSPACE/HEARTBEAT.md" << 'EOF'
# HEARTBEAT.md

## ⚠️ Plan Mode 检查
检测到危险操作时暂停，等待用户确认后再执行。
EOF
    echo "   [OK] HEARTBEAT.md 已创建"
fi

echo ""
echo "========================================"
echo "✅ Plan Mode 初始化完成!"
echo "========================================"
echo ""
echo "下一步:"
echo "  1. 运行 ./plan-mode.sh status 查看状态"
echo "  2. 运行 ./plan-mode.sh enable 开启严格模式"
echo "  3. 查看 $WORKSPACE/memory/activity/plan-mode-log.md"
