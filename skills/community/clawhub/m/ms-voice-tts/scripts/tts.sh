#!/bin/bash
# edge-tts wrapper for OpenClaw voice messages
# Usage: tts.sh "文本" [voice] [output_path]
#
# 依赖：pipx install edge-tts
#
# Examples:
#   tts.sh "你好世界"
#   tts.sh "你好世界" zh-CN-XiaoxiaoNeural
#   tts.sh "你好世界" zh-CN-YunxiNeural /tmp/custom.opus

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
}

log_warn() {
    echo -e "${YELLOW}WARNING: $1${NC}" >&2
}

log_info() {
    echo -e "${GREEN}INFO: $1${NC}" >&2
}

# 检查 edge-tts 是否安装
if ! command -v edge-tts &>/dev/null; then
    log_error "edge-tts 未安装，请先运行: pipx install edge-tts"
    exit 1
fi

# 检查文本长度
TEXT="${1:?用法: tts.sh \"文本\" [voice] [output_path]}"
TEXT_LENGTH=${#TEXT}

if [ $TEXT_LENGTH -gt 1000 ]; then
    log_warn "文本长度 ($TEXT_LENGTH 字) 超过 1000 字，可能导致生成失败或超时"
    log_warn "建议：长文本请分段生成"
    read -p "是否继续？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
elif [ $TEXT_LENGTH -gt 500 ]; then
    log_warn "文本长度 ($TEXT_LENGTH 字) 超过 500 字，建议分段生成以获得更好质量"
fi

# 设置声音和输出路径
VOICE="${2:-zh-CN-YunxiNeural}"
OUTPUT_DIR="$HOME/.openclaw/media"
OUTPUT="${3:-$OUTPUT_DIR/openclaw_voice_$(date +%s).opus}"

# 确保输出目录存在且可写
if [ ! -d "$OUTPUT_DIR" ]; then
    log_info "创建输出目录: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
fi

if [ ! -w "$OUTPUT_DIR" ]; then
    log_error "输出目录不可写: $OUTPUT_DIR"
    exit 1
fi

# 验证声音名称（可选：提前检查是否有效）
if ! edge-tts --list-voices 2>/dev/null | grep -q "$VOICE"; then
    log_warn "声音 '$VOICE' 可能不存在，使用默认声音: zh-CN-YunxiNeural"
    VOICE="zh-CN-YunxiNeural"
fi

log_info "开始生成语音..."
log_info "  声音: $VOICE"
log_info "  文本: ${TEXT:0:50}${TEXT_LENGTH:50:+...}"
log_info "  输出: $OUTPUT"

# 生成语音（保留错误输出用于调试）
if ! edge-tts \
    --voice "$VOICE" \
    --text "$TEXT" \
    --write-media "$OUTPUT" 2>&1; then
    log_error "语音生成失败"
    log_error "  可能原因："
    log_error "    1. 网络连接问题"
    log_error "    2. 无效的声音名称"
    log_error "    3. 文本包含特殊字符"
    log_error "  可用声音：edge-tts --list-voices | grep 'zh-'"
    exit 1
fi

# 检查生成结果
if [ -f "$OUTPUT" ]; then
    FILE_SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT" 2>/dev/null)
    log_info "语音生成成功 ($FILE_SIZE 字节)"
    echo "$OUTPUT"
else
    log_error "输出文件不存在: $OUTPUT"
    exit 1
fi
