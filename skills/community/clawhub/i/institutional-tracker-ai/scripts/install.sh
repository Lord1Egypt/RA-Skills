#!/bin/bash
# institutional-tracker-ai 安装脚本
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${1:-$HOME/institutional_tracker}"

echo "🦉 AI链条机构建仓探测算法 - 安装"
echo "=================================="
echo "  Skill目录: $SKILL_DIR"
echo "  安装目录: $TARGET_DIR"
echo ""

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3.10+，请先安装 Python"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "  ✅ Python $PY_VERSION"

# 2. 创建目标目录
mkdir -p "$TARGET_DIR/data/daily_scores"
mkdir -p "$TARGET_DIR/data/state_history"
mkdir -p "$TARGET_DIR/reports"
echo "  ✅ 目录创建完成"

# 3. 复制脚本
cp "$SKILL_DIR/scripts/"*.py "$TARGET_DIR/"
echo "  ✅ 脚本复制完成"

# 4. 提示配置
echo ""
echo "=================================="
echo "📋 TODO: 完成以下配置"
echo "=================================="
echo ""
echo "  1. 编辑 $TARGET_DIR/config.py"
echo "     - 填入 TUSHARE_TOKEN"
echo "     - 填入 TUSHARE_API_URL"
echo ""
echo "  2. 运行一次测试:"
echo "     cd $TARGET_DIR && python3 main.py"
echo ""
echo "  3. (可选) 设置每日自动化:"
echo "     在 WorkBuddy 中创建自动化任务"
echo "     时间: 每个交易日 16:35"
echo "     命令: cd $TARGET_DIR && python3 main.py"
echo ""
echo "✅ 安装完成!"
