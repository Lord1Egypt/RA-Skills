#!/bin/bash
# macOS 窗口管理脚本
# 用法：./window_manager.sh [命令] [参数]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 显示帮助
show_help() {
    echo "macOS 窗口管理工具"
    echo ""
    echo "用法：$0 [命令] [参数]"
    echo ""
    echo "命令:"
    echo "  list [APP]         列出应用的所有窗口"
    echo "  close [APP] [N]    关闭应用的第 N 个窗口（默认 1）"
    echo "  minimize [APP]     最小化应用窗口"
    echo "  maximize [APP]     最大化应用窗口"
    echo "  focus [APP] [N]    聚焦到应用的第 N 个窗口"
    echo "  position [APP]     获取窗口位置"
    echo "  move [APP] X Y     移动窗口到指定位置"
    echo "  resize [APP] W H   调整窗口大小"
    echo ""
    echo "示例:"
    echo "  $0 list Safari"
    echo "  $0 close Safari 1"
    echo "  $0 minimize Chrome"
    echo "  $0 position Safari"
}

# 检查自动化权限
check_permission() {
    if ! osascript -e 'tell application "System Events" to name' &>/dev/null; then
        echo -e "${RED}❌ 错误：需要自动化权限${NC}"
        echo ""
        echo "请打开设置："
        echo "  open \"x-apple.systempreferences:com.apple.preference.security?Privacy_Automation\""
        exit 1
    fi
}

# 列出窗口
list_windows() {
    local app="$1"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🪟 $app 的窗口列表：${NC}"
    echo ""
    
    # 使用 AppleScript 获取窗口信息
    osascript -e "
        tell application \"$app\"
            if not (exists window 1) then
                return \"没有打开的窗口\"
            end if
            set windowList to \"\"
            repeat with i from 1 to count of windows
                set win to window i
                set windowList to windowList & i & \". \" & name of win & \" (\" & (class of win) & \")\" & linefeed
            end repeat
            return windowList
        end tell
    " 2>/dev/null || {
        echo -e "${YELLOW}⚠️  无法获取窗口列表（应用可能不支持 AppleScript）${NC}"
        echo "尝试使用备用方案..."
        
        # 备用方案：检查应用是否运行
        if pgrep -x "$app" > /dev/null 2>&1; then
            echo "✅ $app 正在运行"
            echo "⚠️  但无法获取详细窗口信息"
        else
            echo "❌ $app 未运行"
        fi
    }
    
    echo ""
}

# 关闭窗口
close_window() {
    local app="$1"
    local win_num="${2:-1}"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🪟 关闭 $app 的第 $win_num 个窗口...${NC}"
    
    osascript -e "
        tell application \"$app\"
            if exists window $win_num then
                close window $win_num
                return \"✅ 已关闭窗口\"
            else
                return \"❌ 窗口不存在\"
            end if
        end tell
    " 2>/dev/null || {
        echo -e "${YELLOW}⚠️  AppleScript 失败，尝试强制关闭...${NC}"
        if [ "$win_num" -eq 1 ]; then
            osascript -e "tell application \"$app\" to quit" 2>/dev/null && \
                echo -e "${GREEN}✅ 已关闭应用${NC}" || \
                echo -e "${RED}❌ 关闭失败${NC}"
        fi
    }
    
    echo ""
}

# 最小化窗口
minimize_window() {
    local app="$1"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🪟 最小化 $app 窗口...${NC}"
    
    osascript -e "
        tell application \"$app\"
            if exists window 1 then
                set miniaturized of window 1 to true
                return \"✅ 已最小化\"
            else
                return \"❌ 没有窗口\"
            end if
        end tell
    " 2>/dev/null || echo -e "${YELLOW}⚠️  操作失败${NC}"
    
    echo ""
}

# 最大化窗口
maximize_window() {
    local app="$1"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🪟 最大化 $app 窗口...${NC}"
    
    osascript -e "
        tell application \"System Events\"
            tell process \"$app\"
                if exists window 1 then
                    set bounds of window 1 to {0, 0, 1470, 956}
                    return \"✅ 已最大化\"
                else
                    return \"❌ 没有窗口\"
                end if
            end tell
        end tell
    " 2>/dev/null || echo -e "${YELLOW}⚠️  操作失败（可能需要辅助功能权限）${NC}"
    
    echo ""
}

# 聚焦窗口
focus_window() {
    local app="$1"
    local win_num="${2:-1}"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🪟 聚焦到 $app 的第 $win_num 个窗口...${NC}"
    
    osascript -e "
        tell application \"$app\"
            activate
            if exists window $win_num then
                set index of window $win_num to 1
                return \"✅ 已聚焦\"
            else
                return \"❌ 窗口不存在\"
            end if
        end tell
    " 2>/dev/null || echo -e "${YELLOW}⚠️  操作失败${NC}"
    
    echo ""
}

# 获取窗口位置
get_window_position() {
    local app="$1"
    
    if [ -z "$app" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🪟 $app 窗口位置：${NC}"
    echo ""
    
    osascript -e "
        tell application \"System Events\"
            tell process \"$app\"
                if exists window 1 then
                    set winBounds to bounds of window 1
                    return \"位置：{\" & item 1 of winBounds & \", \" & item 2 of winBounds & \"}\" & linefeed & \"大小：{\" & (item 3 of winBounds - item 1 of winBounds) & \"x\" & (item 4 of winBounds - item 2 of winBounds) & \"}\"
                else
                    return \"❌ 没有窗口\"
                end if
            end tell
        end tell
    " 2>/dev/null || echo -e "${YELLOW}⚠️  无法获取位置（需要辅助功能权限）${NC}"
    
    echo ""
}

# 移动窗口
move_window() {
    local app="$1"
    local x="$2"
    local y="$3"
    
    if [ -z "$app" ] || [ -z "$x" ] || [ -z "$y" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称和坐标${NC}"
        echo "用法：$0 move APP X Y"
        exit 1
    fi
    
    echo -e "${BLUE}🪟 移动 $app 窗口到 ($x, $y)...${NC}"
    
    osascript -e "
        tell application \"System Events\"
            tell process \"$app\"
                if exists window 1 then
                    set winBounds to bounds of window 1
                    set width to item 3 of winBounds - item 1 of winBounds
                    set height to item 4 of winBounds - item 2 of winBounds
                    set bounds of window 1 to {$x, $y, $x + width, $y + height}
                    return \"✅ 已移动\"
                else
                    return \"❌ 没有窗口\"
                end if
            end tell
        end tell
    " 2>/dev/null || echo -e "${YELLOW}⚠️  操作失败（需要辅助功能权限）${NC}"
    
    echo ""
}

# 调整窗口大小
resize_window() {
    local app="$1"
    local width="$2"
    local height="$3"
    
    if [ -z "$app" ] || [ -z "$width" ] || [ -z "$height" ]; then
        echo -e "${RED}❌ 错误：请提供应用名称和尺寸${NC}"
        echo "用法：$0 resize APP WIDTH HEIGHT"
        exit 1
    fi
    
    echo -e "${BLUE}🪟 调整 $app 窗口大小为 ${width}x${height}...${NC}"
    
    osascript -e "
        tell application \"System Events\"
            tell process \"$app\"
                if exists window 1 then
                    set winBounds to bounds of window 1
                    set x to item 1 of winBounds
                    set y to item 2 of winBounds
                    set bounds of window 1 to {x, y, x + $width, y + $height}
                    return \"✅ 已调整大小\"
                else
                    return \"❌ 没有窗口\"
                end if
            end tell
        end tell
    " 2>/dev/null || echo -e "${YELLOW}⚠️  操作失败（需要辅助功能权限）${NC}"
    
    echo ""
}

# 主逻辑
main() {
    check_permission
    
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case $1 in
        list)
            list_windows "$2"
            ;;
        close)
            close_window "$2" "$3"
            ;;
        minimize)
            minimize_window "$2"
            ;;
        maximize)
            maximize_window "$2"
            ;;
        focus)
            focus_window "$2" "$3"
            ;;
        position)
            get_window_position "$2"
            ;;
        move)
            move_window "$2" "$3" "$4"
            ;;
        resize)
            resize_window "$2" "$3" "$4"
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
