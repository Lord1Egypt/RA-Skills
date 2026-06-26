#!/bin/bash
# macOS 截屏脚本
# 用法：./screenshot.sh [选项]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认输出目录
OUTPUT_DIR="$HOME/Desktop/OpenClaw-Screenshots"

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

# 生成文件名
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$OUTPUT_DIR/screenshot_${TIMESTAMP}.png"

# 显示帮助
show_help() {
    echo "macOS 截屏工具"
    echo ""
    echo "用法：$0 [选项]"
    echo ""
    echo "选项:"
    echo "  -f, --full       全屏截图（默认）"
    echo "  -s, --select     选择区域截图"
    echo "  -w, --window     窗口截图"
    echo "  -d, --delay N    延迟 N 秒截图"
    echo "  -o, --output FILE 输出文件路径"
    echo "  -h, --help       显示帮助"
    echo ""
    echo "示例:"
    echo "  $0                    # 全屏截图"
    echo "  $0 -s                 # 选择区域截图"
    echo "  $0 -d 5               # 延迟 5 秒截图"
    echo "  $0 -o ~/Desktop/test.png"
}

# 检查屏幕录制权限
check_permission() {
    if ! command -v screencapture &> /dev/null; then
        echo -e "${RED}❌ 错误：screencapture 命令不存在${NC}"
        echo ""
        echo "💡 提示：这是 macOS 系统命令，应该存在。请检查系统是否完整。"
        exit 1
    fi
    
    # 尝试截屏测试
    local test_file="/tmp/screencapture_test_$$.png"
    if ! screencapture -x "$test_file" 2>/dev/null; then
        echo -e "${RED}❌ 错误：截屏失败${NC}"
        echo ""
        echo "🔐 可能原因：屏幕录制权限未授予"
        echo ""
        echo "✅ 解决方案："
        echo "1. 打开「系统设置」→「隐私与安全性」→「屏幕录制」"
        echo "2. 勾选「终端」或你的终端应用（如 VS Code）"
        echo "3. 重启终端应用（完全退出后重新打开）"
        echo ""
        echo "🚀 快速打开设置："
        echo "  open \"x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture\""
        echo ""
        rm -f "$test_file"
        exit 1
    fi
    rm -f "$test_file"
}

# 全屏截图
capture_full() {
    local delay=${1:-0}
    
    if [ "$delay" -gt 0 ]; then
        echo -e "${YELLOW}📸 将在 ${delay} 秒后截屏...${NC}"
        sleep "$delay"
    fi
    
    screencapture -x "$OUTPUT_FILE"
    
    if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
        echo -e "${GREEN}✅ 截屏成功！${NC}"
        echo "保存位置：$OUTPUT_FILE"
        echo "文件大小：$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')"
        
        # 尝试打开文件
        if command -v open &> /dev/null; then
            open -R "$OUTPUT_FILE" 2>/dev/null || true
        fi
    else
        echo -e "${RED}❌ 截屏失败${NC}"
        exit 1
    fi
}

# 选择区域截图
capture_select() {
    local delay=${1:-0}
    local select_file="/tmp/screencapture_select_$$.png"
    
    if [ "$delay" -gt 0 ]; then
        echo -e "${YELLOW}📸 将在 ${delay} 秒后选择区域...${NC}"
        sleep "$delay"
    fi
    
    echo -e "${YELLOW}📸 请在屏幕上拖动选择区域...${NC}"
    screencapture -i -x "$select_file"
    
    if [ -f "$select_file" ] && [ -s "$select_file" ]; then
        mv "$select_file" "$OUTPUT_FILE"
        echo -e "${GREEN}✅ 截屏成功！${NC}"
        echo "保存位置：$OUTPUT_FILE"
        echo "文件大小：$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')"
        open -R "$OUTPUT_FILE" 2>/dev/null || true
    else
        rm -f "$select_file"
        echo -e "${RED}❌ 截屏取消或失败${NC}"
        exit 1
    fi
}

# 窗口截图
capture_window() {
    local delay=${1:-0}
    
    if [ "$delay" -gt 0 ]; then
        echo -e "${YELLOW}📸 将在 ${delay} 秒后截屏...${NC}"
        sleep "$delay"
    fi
    
    echo -e "${YELLOW}📸 点击要截取的窗口...${NC}"
    screencapture -W -x "$OUTPUT_FILE"
    
    if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
        echo -e "${GREEN}✅ 截屏成功！${NC}"
        echo "保存位置：$OUTPUT_FILE"
        open -R "$OUTPUT_FILE" 2>/dev/null || true
    else
        echo -e "${RED}❌ 截屏取消或失败${NC}"
        exit 1
    fi
}

# 主逻辑
main() {
    # 检查权限
    check_permission
    
    # 默认模式
    local mode="full"
    local delay=0
    local custom_output=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--full)
                mode="full"
                shift
                ;;
            -s|--select)
                mode="select"
                shift
                ;;
            -w|--window)
                mode="window"
                shift
                ;;
            -d|--delay)
                delay="$2"
                shift 2
                ;;
            -o|--output)
                custom_output="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 未知选项：$1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 自定义输出路径
    if [ -n "$custom_output" ]; then
        OUTPUT_FILE="$custom_output"
        # 确保目录存在
        mkdir -p "$(dirname "$OUTPUT_FILE")"
    fi
    
    # 执行截图
    case $mode in
        full)
            capture_full "$delay"
            ;;
        select)
            capture_select "$delay"
            ;;
        window)
            capture_window "$delay"
            ;;
    esac
}

# 运行主函数
main "$@"
