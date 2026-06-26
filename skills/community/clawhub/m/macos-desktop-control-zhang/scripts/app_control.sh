#!/bin/bash
# macOS 应用控制脚本
# 用法：./app_control.sh [open|close|front|list] [应用名]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 显示帮助
show_help() {
    echo "macOS 应用控制工具"
    echo ""
    echo "用法：$0 [命令] [应用名]"
    echo ""
    echo "命令:"
    echo "  open APP       打开应用"
    echo "  close APP      关闭应用"
    echo "  quit APP       退出应用（同 close）"
    echo "  front          获取前端应用"
    echo "  list           列出所有运行的应用"
    echo "  activate APP   激活/切换到应用"
    echo "  info APP       显示应用信息"
    echo ""
    echo "示例:"
    echo "  $0 open Safari          # 打开 Safari"
    echo "  $0 close Safari         # 关闭 Safari"
    echo "  $0 front                # 获取前端应用"
    echo "  $0 list                 # 列出所有应用"
}

# 打开应用
app_open() {
    local app="$1"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    if open -a "$app" 2>/dev/null; then
        echo -e "${GREEN}✅ 已打开应用：$app${NC}"
    else
        echo -e "${RED}❌ 无法打开应用：$app${NC}"
        echo "可能原因：应用不存在或未安装在 Applications 目录"
        exit 1
    fi
}

# 关闭应用
app_close() {
    local app="$1"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    # 尝试 AppleScript
    if osascript -e "tell application \"$app\" to quit" 2>/dev/null; then
        echo -e "${GREEN}✅ 已关闭应用：$app${NC}"
    else
        # 回退到 killall
        if killall "$app" 2>/dev/null; then
            echo -e "${GREEN}✅ 已强制关闭应用：$app${NC}"
        else
            echo -e "${RED}❌ 无法关闭应用：$app${NC}"
            echo "可能原因：应用未运行"
            exit 1
        fi
    fi
}

# 获取前端应用
app_front() {
    local front_app
    front_app=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null)
    
    if [ -n "$front_app" ]; then
        echo -e "${BLUE}📱 前端应用：${GREEN}$front_app${NC}"
        
        # 获取 PID
        local pid
        pid=$(pgrep -x "$front_app" 2>/dev/null | head -1)
        if [ -n "$pid" ]; then
            echo -e "   PID: $pid"
        fi
    else
        echo -e "${RED}❌ 无法获取前端应用${NC}"
        exit 1
    fi
}

# 列出所有运行的应用
app_list() {
    echo -e "${BLUE}📋 正在运行的应用：${NC}"
    echo ""
    
    local apps
    apps=$(osascript -e 'tell application "System Events" to get name of every application process whose background only is false' 2>/dev/null)
    
    if [ -n "$apps" ]; then
        echo "$apps" | tr ',' '\n' | sort -u | while read -r app; do
            app=$(echo "$app" | xargs)  # 去除首尾空格
            if [ -n "$app" ] && [ "$app" != "" ]; then
                local pid
                pid=$(pgrep -x "$app" 2>/dev/null | head -1 || echo "N/A")
                printf "  ${GREEN}%-40s${NC} PID: %s\n" "$app" "$pid"
            fi
        done
    else
        # 回退方案
        echo -e "${YELLOW}⚠️  AppleScript 不可用，使用备用方案...${NC}"
        ps aux | grep -E "Applications/.+\.app" | awk '{print $11}' | sort -u | while read -r app; do
            basename "$app" .app
        done | head -20
    fi
    
    echo ""
}

# 激活/切换到应用
app_activate() {
    local app="$1"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    if osascript -e "tell application \"$app\" to activate" 2>/dev/null; then
        echo -e "${GREEN}✅ 已切换到应用：$app${NC}"
    else
        echo -e "${RED}❌ 无法切换到应用：$app${NC}"
        exit 1
    fi
}

# 应用信息
app_info() {
    local app="$1"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}📱 应用信息：$app${NC}"
    echo ""
    
    # 检查是否运行
    if pgrep -x "$app" > /dev/null 2>&1; then
        echo -e "  ${GREEN}状态：运行中${NC}"
        local pid
        pid=$(pgrep -x "$app" | head -1)
        echo "  PID: $pid"
    else
        echo -e "  ${YELLOW}状态：未运行${NC}"
    fi
    
    # 尝试获取版本信息
    local app_path
    app_path=$(mdfind "kMDItemDisplayName == \"$app\"" | grep "\.app$" | head -1)
    
    if [ -n "$app_path" ]; then
        echo "  路径：$app_path"
        
        # 获取版本
        local version
        version=$(mdls -name kMDItemVersion "$app_path" 2>/dev/null | cut -d= -f2 | xargs)
        if [ -n "$version" ]; then
            echo "  版本：$version"
        fi
    fi
    
    echo ""
}

# 主逻辑
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case $1 in
        open)
            app_open "$2"
            ;;
        close|quit)
            app_close "$2"
            ;;
        front)
            app_front
            ;;
        list)
            app_list
            ;;
        activate)
            app_activate "$2"
            ;;
        info)
            app_info "$2"
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
