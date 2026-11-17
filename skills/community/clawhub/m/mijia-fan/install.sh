#!/bin/bash
# mijia-fan Skill 安装脚本
# 用法：bash install.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📦 mijia-fan Skill 安装中..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3，请先安装"
    exit 1
fi

# 检查 pip
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ 需要 pip，请先安装"
    exit 1
fi

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活并安装依赖
echo "📥 安装依赖..."
source .venv/bin/activate
pip install --upgrade pip --quiet
pip install mijiaAPI --quiet

# 复制 mijiaAPI token（如果主 skill 存在）
if [ -f "$HOME/.qclaw/skills/mijia/.mijia_token" ]; then
    cp "$HOME/.qclaw/skills/mijia/.mijia_token" . 2>/dev/null || true
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📖 使用方法："
echo "  cd $SCRIPT_DIR"
echo "  source .venv/bin/activate"
echo "  export MIJIA_FAN_DID=\"<你的风扇 DID>\""
echo "  python scripts/fan_cli.py on"
echo ""
echo "💡 不知道 DID？运行：python scripts/fan_cli.py list"
