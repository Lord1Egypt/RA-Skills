#!/bin/bash
# OpenClaw Computer Use - 核心脚本
# 提供电脑控制的基础功能

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$HOME/.openclaw/computer-use-config.yml"
LOG_FILE="$HOME/.openclaw/logs/computer-use.log"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 显示帮助
show_help() {
    echo -e "${BLUE}OpenClaw Computer Use${NC}"
    echo "让 OpenClaw 像人类一样使用电脑"
    echo ""
    echo "用法:"
    echo "  computer-screenshot [选项]    截图"
    echo "  computer-mouse [命令]         鼠标控制"
    echo "  computer-keyboard [命令]      键盘控制"
    echo "  computer-app [命令]           应用控制"
    echo "  computer-file [命令]          文件管理"
    echo "  computer-record [选项]        屏幕录制"
    echo "  computer-monitor [命令]       系统监控"
    echo ""
    echo "示例:"
    echo "  computer-screenshot --full"
    echo "  computer-mouse move --x 500 --y 300"
    echo "  computer-app launch --name Chrome"
}

# 截图功能
cmd_screenshot() {
    local mode="full"
    local output=""
    local window=""
    local interval=""
    local count=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --full) mode="full"; shift ;;
            --region) mode="region"; shift ;;
            --window) mode="window"; window="$2"; shift 2 ;;
            --output) output="$2"; shift 2 ;;
            --interval) interval="$2"; shift 2 ;;
            --count) count="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    # 默认输出路径
    if [ -z "$output" ]; then
        mkdir -p ~/Screenshots
        output="~/Screenshots/screenshot_$(date +%Y%m%d_%H%M%S).png"
    fi
    
    echo -e "${YELLOW}📸 截图中...${NC}"
    
    case $mode in
        full)
            if command -v scrot &> /dev/null; then
                scrot "$output"
            elif command -v gnome-screenshot &> /dev/null; then
                gnome-screenshot -f "$output"
            else
                echo -e "${RED}✗ 未找到截图工具，请安装 scrot${NC}"
                exit 1
            fi
            ;;
        region)
            if command -v scrot &> /dev/null; then
                scrot -s "$output"
            else
                echo -e "${RED}✗ 未找到截图工具${NC}"
                exit 1
            fi
            ;;
        window)
            if command -v scrot &> /dev/null; then
                scrot -u "$output"
            else
                echo -e "${RED}✗ 未找到截图工具${NC}"
                exit 1
            fi
            ;;
    esac
    
    echo -e "${GREEN}✓ 截图已保存: $output${NC}"
    log "Screenshot saved: $output"
}

# 鼠标控制
cmd_mouse() {
    local command="$1"
    shift
    
    case $command in
        move)
            local x=""
            local y=""
            while [[ $# -gt 0 ]]; do
                case $1 in
                    --x) x="$2"; shift 2 ;;
                    --y) y="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            
            if command -v xdotool &> /dev/null; then
                xdotool mousemove "$x" "$y"
                echo -e "${GREEN}✓ 鼠标移动到 ($x, $y)${NC}"
            else
                echo -e "${RED}✗ 未安装 xdotool${NC}"
            fi
            ;;
        click)
            if command -v xdotool &> /dev/null; then
                xdotool click 1
                echo -e "${GREEN}✓ 鼠标左键点击${NC}"
            fi
            ;;
        double-click)
            if command -v xdotool &> /dev/null; then
                xdotool click --repeat 2 --delay 100 1
                echo -e "${GREEN}✓ 鼠标双击${NC}"
            fi
            ;;
        right-click)
            if command -v xdotool &> /dev/null; then
                xdotool click 3
                echo -e "${GREEN}✓ 鼠标右键点击${NC}"
            fi
            ;;
        *)
            echo "用法: computer-mouse [move|click|double-click|right-click]"
            ;;
    esac
}

# 键盘控制
cmd_keyboard() {
    local command="$1"
    shift
    
    case $command in
        type)
            local text="$1"
            if command -v xdotool &> /dev/null; then
                xdotool type "$text"
                echo -e "${GREEN}✓ 输入文本: $text${NC}"
            else
                echo -e "${RED}✗ 未安装 xdotool${NC}"
            fi
            ;;
        hotkey)
            if command -v xdotool &> /dev/null; then
                xdotool key "$@"
                echo -e "${GREEN}✓ 快捷键: $@${NC}"
            fi
            ;;
        *)
            echo "用法: computer-keyboard [type|hotkey]"
            ;;
    esac
}

# 应用控制
cmd_app() {
    local command="$1"
    shift
    
    case $command in
        launch)
            local name=""
            while [[ $# -gt 0 ]]; do
                case $1 in
                    --name) name="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            
            if [ -n "$name" ]; then
                $name &
                echo -e "${GREEN}✓ 启动应用: $name${NC}"
                log "Launched app: $name"
            fi
            ;;
        list)
            if command -v wmctrl &> /dev/null; then
                wmctrl -l
            else
                echo -e "${RED}✗ 未安装 wmctrl${NC}"
            fi
            ;;
        *)
            echo "用法: computer-app [launch|list|close|focus]"
            ;;
    esac
}

# 文件管理
cmd_file() {
    local command="$1"
    shift
    
    case $command in
        list)
            local path="${1:-.}"
            ls -la "$path"
            ;;
        search)
            local name=""
            local path="."
            while [[ $# -gt 0 ]]; do
                case $1 in
                    --name) name="$2"; shift 2 ;;
                    --path) path="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            
            if [ -n "$name" ]; then
                find "$path" -name "$name" 2>/dev/null
            fi
            ;;
        *)
            echo "用法: computer-file [list|search|copy|move|delete]"
            ;;
    esac
}

# 系统监控
cmd_monitor() {
    local command="$1"
    
    case $command in
        resources)
            echo -e "${BLUE}系统资源:${NC}"
            echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
            echo "内存: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
            echo "磁盘: $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
            ;;
        processes)
            ps aux --sort=-%cpu | head -11
            ;;
        *)
            echo "用法: computer-monitor [resources|processes|disk|network]"
            ;;
    esac
}

# 主命令分发
case "${1:-}" in
    screenshot)
        shift
        cmd_screenshot "$@"
        ;;
    mouse)
        shift
        cmd_mouse "$@"
        ;;
    keyboard)
        shift
        cmd_keyboard "$@"
        ;;
    app)
        shift
        cmd_app "$@"
        ;;
    file)
        shift
        cmd_file "$@"
        ;;
    monitor)
        shift
        cmd_monitor "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        ;;
esac
