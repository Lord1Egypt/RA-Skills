#!/bin/bash
# macOS 语音控制 - 整合 moss-tts ASR + 自然语言控制
# 用法：./voice_command.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOSI_ASR="/Users/zhangchangsha/.openclaw/workspace/skills/moss-tts-family-chatbot/scripts/mosi_asr.sh"
NATURAL_LANG="$SCRIPT_DIR/natural_language.py"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🎤 macOS 语音控制${NC}"
echo ""

# 检查依赖
check_dependencies() {
    if [ ! -f "$MOSI_ASR" ]; then
        echo -e "${RED}❌ 找不到 moss-tts ASR 脚本${NC}"
        echo "   请确保已安装 moss-tts-family-chatbot skill"
        exit 1
    fi
    
    if [ -z "${MOSI_TTS_API_KEY:-}" ]; then
        echo -e "${YELLOW}⚠️  MOSI_TTS_API_KEY 未设置${NC}"
        echo "   语音识别需要 API Key"
        echo ""
        echo "   请设置："
        echo "   export MOSI_TTS_API_KEY=\"your-api-key\""
        echo ""
        exit 1
    fi
}

# 录音函数（使用 macOS 自带工具）
record_audio() {
    local output_file="$1"
    local duration="${2:-5}"
    
    echo -e "${YELLOW}🎤 正在录音...（${duration}秒）${NC}"
    echo "   请说话..."
    echo ""
    
    # 使用 arecord 或 rec 录音
    if command -v arecord &> /dev/null; then
        arecord -d "$duration" -f cd "$output_file" 2>/dev/null
    elif command -v rec &> /dev/null; then
        rec -d "$duration" "$output_file" 2>/dev/null
    else
        echo -e "${RED}❌ 找不到录音工具${NC}"
        echo ""
        echo "请安装："
        echo "  brew install sox  # 提供 rec 命令"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 录音完成${NC}"
    echo "   文件：$output_file"
}

# 语音识别
recognize_speech() {
    local audio_file="$1"
    
    echo ""
    echo -e "${BLUE}🧠 正在识别语音...${NC}"
    
    local text
    text=$(bash "$MOSI_ASR" --file "$audio_file" --language zh 2>/dev/null)
    
    if [ -n "$text" ]; then
        echo -e "${GREEN}✅ 识别结果：${NC}\"$text\""
        echo ""
        echo "$text"
    else
        echo -e "${RED}❌ 识别失败${NC}"
        exit 1
    fi
}

# 主流程
main() {
    check_dependencies
    
    # 临时文件
    local temp_audio="/tmp/voice_command_$$.wav"
    trap "rm -f $temp_audio" EXIT
    
    # 1. 录音
    record_audio "$temp_audio" 5
    
    # 2. 识别
    local recognized_text
    recognized_text=$(recognize_speech "$temp_audio")
    
    # 3. 执行自然语言命令
    echo ""
    echo -e "${BLUE}🚀 执行命令...${NC}"
    python3 "$NATURAL_LANG" "$recognized_text"
}

main "$@"
