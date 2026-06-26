#!/bin/bash
# install.sh — openclaw-health-audit 一键安装入口
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "╔══════════════════════════════════════════════════════╗"
echo "║      openclaw-health-audit 安装向导 v1.0.0          ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Skill 目录: $SKILL_DIR"
echo ""

# 检查 Python 版本
if ! python3 --version &>/dev/null; then
    echo "❌ 未找到 python3，请安装 Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION 已就绪"

# 运行向导
python3 "$SKILL_DIR/scripts/audit_wizard.py"
