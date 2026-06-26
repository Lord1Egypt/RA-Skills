#!/bin/bash
# macOS 语音控制（使用系统自带语音识别）
# 需要 macOS 10.15+ 和中文语音识别包

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🎤 macOS 语音控制${NC}"
echo ""

# 检查语音识别是否启用
check_dictation() {
    local enabled=$(defaults read com.apple.speech recognitionenabled 2>/dev/null || echo "0")
    if [ "$enabled" != "1" ]; then
        echo -e "${RED}❌ 语音识别未启用${NC}"
        echo ""
        echo "请启用语音识别："
        echo "1. 打开「系统设置」→「键盘」→「听写」"
        echo "2. 启用「听写」"
        echo "3. 选择语言：中文（普通话）"
        echo ""
        open "x-apple.systempreferences:com.apple.preference.keyboard?Dictation"
        exit 1
    fi
    echo -e "${GREEN}✅ 语音识别已启用${NC}"
}

# 录音并识别
record_and_recognize() {
    echo -e "${YELLOW}🎤 请说话...（5 秒）${NC}"
    echo ""
    
    # 使用 say 命令的听写功能（简化版）
    # 实际应该用 Speech Recognition framework
    
    echo -e "${YELLOW}⚠️  当前 macOS 听写功能限制：${NC}"
    echo "   macOS 自带听写主要用于文本输入，不直接支持命令识别"
    echo ""
    echo -e "${BLUE}💡 替代方案：${NC}"
    echo "   1. 使用 Siri 快捷指令"
    echo "   2. 使用第三方 STT 服务（百度/讯飞）"
    echo "   3. 继续使用文字输入（推荐）"
    echo ""
}

# 主逻辑
main() {
    check_dictation
    record_and_recognize
}

main "$@"
