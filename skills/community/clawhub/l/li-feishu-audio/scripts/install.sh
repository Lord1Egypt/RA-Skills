#!/bin/bash
# Li_Feishu_Audio 技能安装脚本
# 用法：./install.sh
# 支持用户自定义目录配置
#
# 安全说明：
# - 不要求 root 权限
# - 所有目录使用用户家目录或技能目录
# - 不修改系统配置

set -e

echo "=== Li_Feishu_Audio 技能安装 ==="

# 获取技能目录
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="${SKILL_DIR}/scripts"

# 加载用户配置的环境变量
if [ -f "${SCRIPTS_DIR}/.env" ]; then
    echo "ℹ️  检测到 .env 配置文件，正在加载..."
    source "${SCRIPTS_DIR}/.env"
fi

# 1. 检查系统依赖
echo ""
echo "1. 检查系统依赖..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：需要 Python 3"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# 检查 uv
if ! command -v uv &> /dev/null; then
    echo "❌ 错误：需要 uv 包管理器"
    echo "   安装：curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
echo "✅ uv: $(uv --version)"

# 检查 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ 错误：需要 ffmpeg"
    echo "   安装：sudo apt install ffmpeg"
    exit 1
fi
echo "✅ ffmpeg: $(ffmpeg -version | head -1)"

# 检查 jq
if ! command -v jq &> /dev/null; then
    echo "❌ 错误：需要 jq"
    echo "   安装：sudo apt install jq"
    exit 1
fi
echo "✅ jq: $(jq --version)"

# 2. 创建虚拟环境（使用技能目录，不需要 root）
echo ""
echo "2. 创建 Python 虚拟环境..."

# 使用用户配置的虚拟环境目录，默认使用技能目录下的 .venv
VENV_DIR="${VENV_DIR:-${SKILL_DIR}/.venv}"

if [ -d "$VENV_DIR" ]; then
    echo "ℹ️  虚拟环境已存在：$VENV_DIR"
else
    uv venv --python 3.11 "$VENV_DIR"
    echo "✅ 虚拟环境已创建：$VENV_DIR"
fi

# 3. 安装 Python 依赖
echo ""
echo "3. 安装 Python 依赖..."

# 使用国内镜像加速下载（hf-mirror.com 是 HuggingFace 中国镜像）
export HF_ENDPOINT=https://hf-mirror.com
echo "ℹ️  使用 HuggingFace 镜像：$HF_ENDPOINT"

uv pip install faster-whisper edge-tts -p "$VENV_DIR"
echo "✅ Python 依赖已安装"

# 4. 下载语音模型（使用用户家目录，不需要 root）
echo ""
echo "4. 下载语音识别模型..."

# 使用用户配置的模型目录，默认使用用户家目录
MODEL_DIR="${FAST_WHISPER_MODEL_DIR:-${HOME}/.fast-whisper-models}"
mkdir -p "$MODEL_DIR"
echo "ℹ️  模型目录：$MODEL_DIR"

# 测试模型是否已下载
"$VENV_DIR/bin/python3" << EOF
from faster_whisper import WhisperModel
try:
    model = WhisperModel("tiny", device="cpu", compute_type="int8", download_root="$MODEL_DIR", local_files_only=True)
    print("✅ 模型已存在：$MODEL_DIR")
except:
    print("⬇️  下载模型中...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8", download_root="$MODEL_DIR")
    print("✅ 模型下载完成：$MODEL_DIR")
EOF

# 5. 创建配置模板
echo ""
echo "5. 创建配置模板..."

if [ ! -f "${SCRIPTS_DIR}/.env" ]; then
    echo "ℹ️  .env 文件不存在，创建模板..."
    cp "${SCRIPTS_DIR}/.env.example" "${SCRIPTS_DIR}/.env"
    echo "✅ 已创建配置文件：${SCRIPTS_DIR}/.env"
    echo "   ⚠️  请编辑 .env 填入实际配置"
else
    echo "ℹ️  .env 文件已存在，跳过创建"
fi

echo "   ⚠️  不要将 .env 提交到版本控制系统！"

# 6. 验证飞书凭证
echo ""
echo "6. 验证飞书凭证配置..."

# 检查环境变量
if [ -n "$FEISHU_APP_ID" ] && [ -n "$FEISHU_APP_SECRET" ]; then
    echo "✅ 飞书凭证已通过环境变量配置"
else
    # 尝试从 openclaw.json 读取（使用用户家目录）
    OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-${HOME}/.openclaw/openclaw.json}"
    if [ -f "$OPENCLAW_CONFIG" ]; then
        FEISHU_CONFIG=$(cat "$OPENCLAW_CONFIG" | jq '.channels.feishu' 2>/dev/null)
        if [ "$FEISHU_CONFIG" != "null" ] && [ "$FEISHU_CONFIG" != "" ]; then
            echo "✅ OpenClaw 飞书配置已存在"
            echo "$FEISHU_CONFIG" | jq .
        else
            echo "⚠️  未找到飞书配置，请手动配置"
            echo "   方法 1: 设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET"
            echo "   方法 2: 编辑 openclaw.json 配置飞书渠道"
        fi
    else
        echo "⚠️  OpenClaw 配置不存在：$OPENCLAW_CONFIG"
        echo "   方法 1: 设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET"
        echo "   方法 2: 创建 openclaw.json 并配置飞书渠道"
    fi
fi

# 7. 配置 TTS
echo ""
echo "7. 配置 TTS..."

if [ -f "$OPENCLAW_CONFIG" ]; then
    TTS_CONFIG=$(cat "$OPENCLAW_CONFIG" | jq '.messages.tts' 2>/dev/null)
    if [ "$TTS_CONFIG" != "null" ] && [ "$TTS_CONFIG" != "" ]; then
        echo "✅ TTS 配置已存在"
        echo "$TTS_CONFIG" | jq .
    else
        echo "⚠️  未找到 TTS 配置"
        echo "   建议在 openclaw.json 中配置："
        echo '   {"messages":{"tts":{"auto":"always","provider":"edge"}}}'
    fi
fi

# 8. 创建日志目录（如果配置）
if [ -n "$LOG_DIR" ]; then
    echo ""
    echo "8. 创建日志目录..."
    mkdir -p "$LOG_DIR"
    echo "✅ 日志目录已创建：$LOG_DIR"
fi

# 完成
echo ""
echo "=== 安装完成 ==="
echo ""
echo "下一步："
echo "1. 配置飞书凭证（二选一）"
echo "   方法 A: 编辑 .env 文件"
echo "     cd ${SCRIPTS_DIR}"
echo "     vi .env  # 填入实际凭证"
echo "     source .env"
echo ""
echo "   方法 B: 配置 openclaw.json"
echo "     编辑您的 openclaw.json 文件"
echo ""
echo "2. 重启 OpenClaw 网关"
echo "     openclaw gateway restart"
echo ""
echo "3. 测试语音交互"
echo "     发送语音消息到飞书"
echo ""
echo "📁 配置信息："
echo "   技能目录：${SKILL_DIR}"
echo "   脚本目录：${SCRIPTS_DIR}"
echo "   虚拟环境：${VENV_DIR}"
echo "   模型目录：${MODEL_DIR}"
echo "   OpenClaw 配置：${OPENCLAW_CONFIG}"
if [ -n "$LOG_DIR" ]; then
    echo "   日志目录：${LOG_DIR}"
fi
echo ""
echo "🔒 安全说明："
echo "   - 不要求 root 权限"
echo "   - 所有目录使用用户家目录或技能目录"
echo "   - 不要将 .env 文件提交到版本控制系统"
echo "   - 建议将 .env 加入 .gitignore"
echo "   - 定期更换凭证，避免长期使用同一凭证"
