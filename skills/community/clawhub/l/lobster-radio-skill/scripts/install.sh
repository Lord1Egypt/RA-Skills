#!/bin/bash
# 龙虾电台Skill一键安装脚本

set -e

echo "🎙️ 龙虾电台Skill安装脚本"
echo "================================"

# 检测操作系统
OS="$(uname -s)"
case "$OS" in
    Darwin*)    OS="macOS" ;;
    Linux*)     OS="Linux" ;;
    CYGWIN*)    OS="Windows" ;;
    MINGW*)     OS="Windows" ;;
    *)          OS="Unknown" ;;
esac

echo "检测到操作系统: $OS"

# 检查OpenClaw是否安装
echo ""
echo "📋 检查OpenClaw安装..."

if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw未安装"
    echo "请先安装OpenClaw: https://docs.openclaw.ai/installation"
    exit 1
fi

echo "✅ OpenClaw已安装"

# 检查Python是否安装
echo ""
echo "📋 检查Python安装..."

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python未安装"
    echo "请先安装Python 3.10+: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python已安装"

# 安装Python依赖
echo ""
echo "📦 安装Python依赖..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$SKILL_DIR"

if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "❌ pip未安装"
    exit 1
fi

echo "✅ Python依赖已安装"

# 检查Qwen3-TTS模型
echo ""
echo "📋 检查Qwen3-TTS模型..."

MODEL_DIR="$SKILL_DIR/models/Qwen3-TTS-12Hz-0.6B-Base"
if [ -d "$MODEL_DIR" ]; then
    echo "✅ Qwen3-TTS模型已存在"
else
    echo "⚠️  Qwen3-TTS模型未下载"
    echo ""
    echo "模型将在首次运行时自动下载，或您可以手动下载："
    echo ""
    echo "方法1: 使用HuggingFace"
    echo "   pip install huggingface_hub"
    echo "   huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base"
    echo ""
    echo "方法2: 使用ModelScope（国内用户推荐）"
    echo "   pip install modelscope"
    echo "   python -c \"from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')\""
    echo ""
    echo "详细说明请查看: QWEN3TTS_GUIDE.md"
fi

# 安装Skill
echo ""
echo "📦 安装龙虾电台Skill..."

# 检查OpenClaw工作区
OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace/skills"
mkdir -p "$OPENCLAW_WORKSPACE"

# 检查是否已安装
if [ -d "$OPENCLAW_WORKSPACE/lobster-radio-skill" ]; then
    echo "⚠️  Skill已存在，正在更新..."
    rm -rf "$OPENCLAW_WORKSPACE/lobster-radio-skill"
fi

# 复制Skill
echo "正在复制Skill文件..."
cp -r "$SKILL_DIR" "$OPENCLAW_WORKSPACE/"

echo "✅ Skill已复制到: $OPENCLAW_WORKSPACE/lobster-radio-skill"

# 配置TTS
echo ""
echo "⚙️  配置TTS..."

cd "$OPENCLAW_WORKSPACE/lobster-radio-skill"

python3 scripts/configure_tts.py --voice xiaoxiao --emotion neutral || true

echo "✅ TTS已配置"

# 重启OpenClaw
echo ""
echo "🔄 重启OpenClaw..."

openclaw gateway restart || openclaw restart || true

echo "✅ OpenClaw已重启"

# 验证安装
echo ""
echo "🔍 验证安装..."

sleep 2

if openclaw skills list 2>/dev/null | grep -q "lobster-radio"; then
    echo "✅ Skill已成功安装并启用"
else
    echo "⚠️  Skill可能未正确安装，请手动检查"
fi

# 完成
echo ""
echo "================================"
echo "🎉 安装完成！"
echo ""
echo "📝 使用方法:"
echo "   在OpenClaw支持的聊天平台中发送:"
echo "   - '生成关于人工智能的电台'"
echo "   - '每天早上8点推送科技新闻'"
echo "   - '配置我的电台音色'"
echo ""
echo "📚 文档:"
echo "   - README: $OPENCLAW_WORKSPACE/lobster-radio-skill/README.md"
echo "   - 快速开始: $OPENCLAW_WORKSPACE/lobster-radio-skill/QUICKSTART.md"
echo "   - 安装指南: $OPENCLAW_WORKSPACE/lobster-radio-skill/INSTALL.md"
echo "   - Qwen3-TTS指南: $OPENCLAW_WORKSPACE/lobster-radio-skill/QWEN3TTS_GUIDE.md"
echo ""
echo "🧪 测试:"
echo "   cd $OPENCLAW_WORKSPACE/lobster-radio-skill"
echo "   python3 tests/verify_all.py"
echo ""
echo "❓ 获取帮助:"
echo "   - GitHub Issues: https://github.com/your-repo/lobster-radio-skill/issues"
echo "   - OpenClaw文档: https://docs.openclaw.ai"
echo ""
