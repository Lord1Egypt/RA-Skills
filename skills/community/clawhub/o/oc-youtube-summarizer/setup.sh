#!/bin/bash
# Setup script for YouTube Summarizer skill

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SKILL_DIR/venv"

echo "🔧 Setting up YouTube Summarizer skill..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Check/install yt-dlp
if ! command -v yt-dlp &> /dev/null; then
    echo "📦 Installing yt-dlp..."
    if command -v brew &> /dev/null; then
        brew install yt-dlp
    else
        echo "❌ Homebrew not found. Please install yt-dlp manually:"
        echo "   brew install yt-dlp"
        exit 1
    fi
else
    echo "✅ yt-dlp found"
fi

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate and install dependencies
echo "📦 Installing Python dependencies..."
source "$VENV_DIR/bin/activate"
pip install --quiet youtube-transcript-api requests innertube faster-whisper

echo ""

# Check ffmpeg (required for Bilibili)
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found. Required for Bilibili video processing."
    echo "   Install: sudo apt install ffmpeg (Linux) / brew install ffmpeg (macOS)"
else
    echo "✅ ffmpeg found"
fi

echo ""
echo "✅ 依赖安装完成！"
echo ""

# ─────────────────────────────────────────────
# 模式引导配置
# ─────────────────────────────────────────────
CONFIG_DIR="$SKILL_DIR/config"
CONFIG_FILE="$CONFIG_DIR/settings.json"
mkdir -p "$CONFIG_DIR"

configure_mode() {
    echo "📋 选择默认图文模式 (Select default output mode):"
    echo ""
    echo "  1) text-only    - 纯文字，不抽帧（最快）"
    echo "  2) auto-insert  - 自动选帧插入文档（推荐平衡）"
    echo "  3) ai-review    - AI 智能选图（默认，最佳效果，多消耗 ~5-8k token）"
    echo ""
    printf "请选择 [1/2/3] (默认 3): "
    read -r MODE_CHOICE

    case "$MODE_CHOICE" in
        1) DEFAULT_MODE="text-only" ;;
        2) DEFAULT_MODE="auto-insert" ;;
        *) DEFAULT_MODE="ai-review" ;;
    esac

    # Read existing config if present, else use defaults
    MAX_FRAMES=15
    FRAME_INTERVAL=30
    FRAME_TIME_OFFSET=5
    WHISPER_MODEL="small"

    if [ -f "$CONFIG_FILE" ]; then
        # Try to preserve existing values
        existing_max=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('max_frames',15))" 2>/dev/null)
        existing_fi=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('frame_interval',30))" 2>/dev/null)
        existing_fto=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('frame_time_offset',5))" 2>/dev/null)
        existing_wm=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('whisper_model','small'))" 2>/dev/null)
        [ -n "$existing_max" ] && MAX_FRAMES="$existing_max"
        [ -n "$existing_fi" ] && FRAME_INTERVAL="$existing_fi"
        [ -n "$existing_fto" ] && FRAME_TIME_OFFSET="$existing_fto"
        [ -n "$existing_wm" ] && WHISPER_MODEL="$existing_wm"
    fi

    cat > "$CONFIG_FILE" << JSONEOF
{
  "default_mode": "$DEFAULT_MODE",
  "max_frames": $MAX_FRAMES,
  "frame_interval": $FRAME_INTERVAL,
  "frame_time_offset": $FRAME_TIME_OFFSET,
  "whisper_model": "$WHISPER_MODEL"
}
JSONEOF

    echo ""
    echo "✅ 已设置默认模式：$DEFAULT_MODE"
    echo "   配置已写入 $CONFIG_FILE"
}

configure_mode

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  youtube-summarizer --url 'https://youtube.com/watch?v=VIDEO_ID'"
echo "  youtube-summarizer --url 'https://www.bilibili.com/video/BV1xxxxx'"
echo "  youtube-summarizer --channel 'UC_x5XG1OV2P6uZZ5FSM9Ttw' --hours 24"
echo "  youtube-summarizer --config channels.json --daily --output /tmp/youtube_summary.json"
echo ""
echo "图文模式（可重新配置）:"
echo "  youtube-summarizer --setup"
echo ""
echo "Add to PATH:"
echo "  export PATH=\"\$PATH:$HOME/.openclaw/skills/youtube-summarizer\""
