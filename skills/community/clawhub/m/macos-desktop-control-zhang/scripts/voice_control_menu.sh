#!/bin/bash
# macOS 语音控制 - 一键启动
# 整合 Vosk 语音识别 + 自然语言控制

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VOSK_PY="$SCRIPT_DIR/voice_recognition_vosk.py"
DOWNLOAD_PY="$SCRIPT_DIR/download_vosk_model.py"
NATURAL_LANG="$SCRIPT_DIR/natural_language.py"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_menu() {
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     🎤 macOS 语音控制中心              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "请选择操作:"
    echo ""
    echo "  1) 🎤 语音控制（按住说话）"
    echo "  2) 📥 下载语音模型（首次使用）"
    echo "  3) ⌨️  文字输入控制"
    echo "  4) ℹ️  查看帮助"
    echo "  0) 退出"
    echo ""
}

check_model() {
    MODEL_PATH="$HOME/.openclaw/vosk-models/vosk-model-small-zh-cn-0.22"
    if [ ! -d "$MODEL_PATH" ]; then
        return 1
    fi
    return 0
}

voice_control() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🎤 语音控制${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if ! check_model; then
        echo -e "${YELLOW}⚠️  语音模型未下载${NC}"
        echo ""
        echo "请先下载模型："
        echo "  选择菜单 2) 下载语音模型"
        echo ""
        return 1
    fi
    
    # 检查录音工具
    if ! command -v rec &> /dev/null && ! command -v arecord &> /dev/null; then
        echo -e "${YELLOW}⚠️  录音工具未安装${NC}"
        echo ""
        echo "请安装 sox:"
        echo "  brew install sox"
        echo ""
        read -p "是否现在安装？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            brew install sox
        else
            return 1
        fi
    fi
    
    # 运行语音识别
    python3 "$VOSK_PY"
}

text_control() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}⌨️  文字输入控制${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "请输入命令（输入 'quit' 退出）:"
    echo ""
    
    while true; do
        echo -n "> "
        read -r input
        
        if [ "$input" = "quit" ] || [ "$input" = "exit" ] || [ "$input" = "q" ]; then
            echo -e "${GREEN}👋 再见！${NC}"
            break
        fi
        
        if [ -n "$input" ]; then
            python3 "$NATURAL_LANG" "$input"
        fi
        echo ""
    done
}

show_help() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}ℹ️  帮助信息${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "📖 使用说明:"
    echo ""
    echo "1. 首次使用需要下载语音模型（约 50MB）"
    echo "   选择菜单 2) 或运行："
    echo "   python3 scripts/download_vosk_model.py"
    echo ""
    echo "2. 语音控制需要麦克风权限"
    echo "   系统设置 → 隐私与安全性 → 麦克风"
    echo ""
    echo "3. 录音工具 sox（可选）"
    echo "   brew install sox"
    echo ""
    echo "📝 支持命令示例:"
    echo ""
    echo "  截屏类:"
    echo "    - \"帮我截个屏\""
    echo "    - \"截图\""
    echo ""
    echo "  窗口类:"
    echo "    - \"把 Safari 放左边\""
    echo "    - \"Chrome 放右边\""
    echo "    - \"全屏浏览器\""
    echo ""
    echo "  应用类:"
    echo "    - \"打开 Chrome\""
    echo "    - \"关闭 QQ\""
    echo "    - \"切换到 VS Code\""
    echo ""
    echo "  系统类:"
    echo "    - \"显示电脑配置\""
    echo "    - \"看看运行着什么\""
    echo ""
    echo "  自动化:"
    echo "    - \"启动晨会准备\""
    echo "    - \"开启专注模式\""
    echo "    - \"下班清理\""
    echo ""
}

main() {
    while true; do
        show_menu
        echo -n "请选择 [0-4]: "
        read -r choice
        
        case $choice in
            1)
                voice_control
                ;;
            2)
                python3 "$DOWNLOAD_PY"
                ;;
            3)
                text_control
                ;;
            4)
                show_help
                ;;
            0)
                echo -e "${GREEN}👋 再见！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 无效选择${NC}"
                ;;
        esac
        
        echo ""
        echo "按回车继续..."
        read -r
        echo ""
    done
}

main "$@"
