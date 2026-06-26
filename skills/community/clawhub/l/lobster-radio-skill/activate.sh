#!/bin/bash
# 激活虚拟环境脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "🐍 激活Python虚拟环境..."
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "✅ 虚拟环境已激活"
    echo ""
    echo "💡 提示: 现在可以运行Skill脚本了"
    echo "   例如: python scripts/generate_radio.py --topics '人工智能'"
else
    echo "❌ 虚拟环境不存在"
    echo "请先运行: python3 -m venv venv"
fi
