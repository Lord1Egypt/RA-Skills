#!/bin/bash
# music-analysis 技能配置脚本
# 用途：一键配置音乐分析技能的所有依赖

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SKILL_DIR="/Users/huang/.openclaw/workspace/skills/music-analysis"
VENV_DIR="$SKILL_DIR/.venv"
WHISPER_MODEL_DIR="$HOME/.local/share/whisper-cpp"
WHISPER_MODEL="$WHISPER_MODEL_DIR/ggml-large-v3-turbo.bin"

log_info "========== 配置 music-analysis 技能 =========="

# 1. 检查 Python 虚拟环境
if [ -d "$VENV_DIR" ]; then
    log_info "✓ Python 虚拟环境已存在"
else
    log_info "创建 Python 虚拟环境..."
    cd "$SKILL_DIR"
    python3 -m venv .venv
    log_info "✓ 虚拟环境创建完成"
fi

# 2. 安装 Python 依赖
log_info "安装 Python 依赖..."
source "$VENV_DIR/bin/activate"
pip install -q librosa numpy scipy numba scikit-learn soundfile soxr
log_info "✓ Python 依赖安装完成"

# 3. 检查 Whisper 模型
if [ -f "$WHISPER_MODEL" ]; then
    MODEL_SIZE=$(du -h "$WHISPER_MODEL" | cut -f1)
    log_info "✓ Whisper 模型已存在 ($MODEL_SIZE)"
else
    log_warn "Whisper 模型不存在，需要下载 (约 1.5GB)..."
    mkdir -p "$WHISPER_MODEL_DIR"
    curl -L -o "$WHISPER_MODEL" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"
    log_info "✓ Whisper 模型下载完成"
fi

# 4. 检查 FFmpeg
if command -v ffmpeg &> /dev/null; then
    log_info "✓ FFmpeg 已安装 ($(ffmpeg -version | head -1))"
else
    log_error "FFmpeg 未安装，运行：brew install ffmpeg"
    exit 1
fi

# 5. 检查 whisper-cli
if command -v whisper-cli &> /dev/null; then
    log_info "✓ whisper-cli 已安装"
else
    log_error "whisper-cli 未安装，运行：brew install whisper-cpp"
    exit 1
fi

# 6. 测试技能
log_info "测试音乐分析技能..."
TEST_AUDIO="$SKILL_DIR/test_audio.mp3"

# 创建测试音频（静音 5 秒）
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 5 -q:a 0 "$TEST_AUDIO" 2>/dev/null

# 运行分析
if [ -f "$TEST_AUDIO" ]; then
    source "$VENV_DIR/bin/activate"
    python3 "$SKILL_DIR/scripts/analyze_music.py" "$TEST_AUDIO" --json 2>&1 | head -20
    rm -f "$TEST_AUDIO"
    log_info "✓ 技能测试完成"
else
    log_warn "跳过测试（无测试音频）"
fi

# 7. 创建快捷命令
CATALOG="$HOME/.zshrc"
if ! grep -q "music-analysis" "$CATALOG" 2>/dev/null; then
    cat >> "$CATALOG" << 'EOF'

# music-analysis 技能快捷命令
alias music-analyze='cd /Users/huang/.openclaw/workspace/skills/music-analysis && source .venv/bin/activate && python3 scripts/listen.py'
alias music-snapshot='cd /Users/huang/.openclaw/workspace/skills/music-analysis && source .venv/bin/activate && python3 scripts/analyze_music.py'
alias music-temporal='cd /Users/huang/.openclaw/workspace/skills/music-analysis && source .venv/bin/activate && python3 scripts/temporal_listen.py'
EOF
    log_info "✓ 快捷命令已添加到 ~/.zshrc"
    log_warn "请运行 'source ~/.zshrc' 生效"
fi

log_info "========== 配置完成 =========="
echo ""
echo "使用方法:"
echo "  # 完整分析（推荐）"
echo "  music-analyze /path/to/audio.mp3"
echo ""
echo "  # 快照分析（快速）"
echo "  music-snapshot /path/to/audio.mp3"
echo ""
echo "  # 时间线分析"
echo "  music-temporal /path/to/audio.mp3"
