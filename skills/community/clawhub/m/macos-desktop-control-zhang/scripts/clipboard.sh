#!/bin/bash
# macOS 剪贴板脚本
# 用法：./clipboard.sh [get|set] [文字]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 显示帮助
show_help() {
    echo "macOS 剪贴板工具"
    echo ""
    echo "用法：$0 [命令] [参数]"
    echo ""
    echo "命令:"
    echo "  get             读取剪贴板内容"
    echo "  set TEXT        设置剪贴板内容"
    echo "  copy FILE       复制文件到剪贴板"
    echo "  paste           粘贴剪贴板内容到文件"
    echo "  clear           清空剪贴板"
    echo "  history         显示剪贴板历史（需要安装）"
    echo ""
    echo "示例:"
    echo "  $0 get                      # 读取剪贴板"
    echo "  $0 set \"Hello World\"        # 设置剪贴板"
    echo "  $0 copy file.txt            # 复制文件"
    echo "  $0 paste > output.txt       # 粘贴到文件"
}

# 读取剪贴板
clipboard_get() {
    if command -v pbpaste &> /dev/null; then
        pbpaste
    else
        echo -e "${RED}❌ 错误：pbpaste 命令不存在${NC}"
        exit 1
    fi
}

# 设置剪贴板
clipboard_set() {
    local text="$1"
    
    if [ -z "$text" ]; then
        echo -e "${RED}❌ 错误：请提供要复制的文字${NC}"
        echo "用法：$0 set \"要复制的文字\""
        exit 1
    fi
    
    if command -v pbcopy &> /dev/null; then
        echo -n "$text" | pbcopy
        echo -e "${GREEN}✅ 已复制到剪贴板${NC}"
    else
        echo -e "${RED}❌ 错误：pbcopy 命令不存在${NC}"
        exit 1
    fi
}

# 复制文件到剪贴板
clipboard_copy_file() {
    local file="$1"
    
    if [ -z "$file" ]; then
        echo -e "${RED}❌ 错误：请提供文件路径${NC}"
        exit 1
    fi
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ 错误：文件不存在：$file${NC}"
        exit 1
    fi
    
    # 使用 osascript 复制文件
    osascript -e "tell application \"Finder\" to set the clipboard to (POSIX file \"$file\")"
    
    echo -e "${GREEN}✅ 已复制文件到剪贴板：$file${NC}"
}

# 粘贴剪贴板到文件
clipboard_paste() {
    if command -v pbpaste &> /dev/null; then
        pbpaste
    else
        echo -e "${RED}❌ 错误：pbpaste 命令不存在${NC}"
        exit 1
    fi
}

# 清空剪贴板
clipboard_clear() {
    # macOS 没有原生的清空剪贴板命令
    # 使用空字符串覆盖
    echo -n "" | pbcopy
    echo -e "${GREEN}✅ 剪贴板已清空${NC}"
}

# 剪贴板历史（需要额外工具）
clipboard_history() {
    echo -e "${YELLOW}⚠️  剪贴板历史功能需要安装额外工具${NC}"
    echo ""
    echo "推荐工具："
    echo "  - Maccy (免费开源): brew install --cask maccy"
    echo "  - Paste (付费): https://pasteapp.io"
    echo "  - CopyClip (免费): App Store"
    echo ""
}

# 主逻辑
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case $1 in
        get)
            clipboard_get
            ;;
        set)
            if [ -z "${2:-}" ]; then
                echo -e "${RED}❌ 错误：请提供要复制的文字${NC}"
                echo "用法：$0 set \"文字\""
                exit 1
            fi
            clipboard_set "$2"
            ;;
        copy)
            if [ -z "${2:-}" ]; then
                echo -e "${RED}❌ 错误：请提供文件路径${NC}"
                exit 1
            fi
            clipboard_copy_file "$2"
            ;;
        paste)
            clipboard_paste
            ;;
        clear)
            clipboard_clear
            ;;
        history)
            clipboard_history
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 未知命令：$1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
