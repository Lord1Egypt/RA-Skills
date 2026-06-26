#!/bin/bash
# macOS 窗口吸附/平铺脚本
# 用法：./window_snap.sh [命令] [参数]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 屏幕尺寸（可自动检测）
SCREEN_WIDTH=1470
SCREEN_HEIGHT=956

show_help() {
    echo "macOS 窗口吸附/平铺工具"
    echo ""
    echo "用法：$0 [命令] [应用名]"
    echo ""
    echo "命令:"
    echo "  left APP      左半屏"
    echo "  right APP     右半屏"
    echo "  top APP       上半屏"
    echo "  bottom APP    下半屏"
    echo "  corner APP N  四分之一屏（1-4）"
    echo "  center APP    居中"
    echo "  full APP      全屏"
    echo "  grid APP      显示网格布局"
    echo ""
    echo "示例:"
    echo "  $0 left Safari"
    echo "  $0 right Chrome"
    echo "  $0 corner VSCode 1"
}

# 检查权限
check_permission() {
    if ! osascript -e 'tell application "System Events" to name' &>/dev/null; then
        echo -e "${RED}❌ 需要辅助功能权限${NC}"
        open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
        exit 1
    fi
}

# 获取应用窗口位置
get_window_bounds() {
    local app="$1"
    osascript -e "
        tell application \"System Events\"
            tell process \"$app\"
                if exists window 1 then
                    set bounds to bounds of window 1
                    return bounds
                else
                    return \"\"
                end if
            end tell
        end tell
    " 2>/dev/null
}

# 设置窗口位置
set_window_bounds() {
    local app="$1"
    local x="$2"
    local y="$3"
    local width="$4"
    local height="$5"
    
    osascript -e "
        tell application \"System Events\"
            tell process \"$app\"
                if exists window 1 then
                    set bounds of window 1 to {$x, $y, $x + $width, $y + $height}
                    return true
                else
                    return false
                end if
            end tell
        end tell
    " 2>/dev/null
}

# 左半屏
snap_left() {
    local app="$1"
    echo -e "${BLUE}🪟 将 $app 吸附到左半屏...${NC}"
    
    local half_width=$((SCREEN_WIDTH / 2))
    if set_window_bounds "$app" 0 0 $half_width $SCREEN_HEIGHT; then
        echo -e "${GREEN}✅ 已吸附到左半屏${NC}"
    else
        echo -e "${RED}❌ 失败${NC}"
    fi
}

# 右半屏
snap_right() {
    local app="$1"
    echo -e "${BLUE}🪟 将 $app 吸附到右半屏...${NC}"
    
    local half_width=$((SCREEN_WIDTH / 2))
    if set_window_bounds "$app" $half_width 0 $half_width $SCREEN_HEIGHT; then
        echo -e "${GREEN}✅ 已吸附到右半屏${NC}"
    else
        echo -e "${RED}❌ 失败${NC}"
    fi
}

# 上半屏
snap_top() {
    local app="$1"
    echo -e "${BLUE}🪟 将 $app 吸附到上半屏...${NC}"
    
    local half_height=$((SCREEN_HEIGHT / 2))
    if set_window_bounds "$app" 0 0 $SCREEN_WIDTH $half_height; then
        echo -e "${GREEN}✅ 已吸附到上半屏${NC}"
    else
        echo -e "${RED}❌ 失败${NC}"
    fi
}

# 下半屏
snap_bottom() {
    local app="$1"
    echo -e "${BLUE}🪟 将 $app 吸附到下半屏...${NC}"
    
    local half_height=$((SCREEN_HEIGHT / 2))
    if set_window_bounds "$app" 0 $half_height $SCREEN_WIDTH $half_height; then
        echo -e "${GREEN}✅ 已吸附到下半屏${NC}"
    else
        echo -e "${RED}❌ 失败${NC}"
    fi
}

# 四分之一屏
snap_corner() {
    local app="$1"
    local corner="$2"
    
    local half_width=$((SCREEN_WIDTH / 2))
    local half_height=$((SCREEN_HEIGHT / 2))
    
    local x=0 y=0
    
    case $corner in
        1) x=0; y=0; echo -e "${BLUE}🪟 左上角...${NC}" ;;
        2) x=$half_width; y=0; echo -e "${BLUE}🪟 右上角...${NC}" ;;
        3) x=0; y=$half_height; echo -e "${BLUE}🪟 左下角...${NC}" ;;
        4) x=$half_width; y=$half_height; echo -e "${BLUE}🪟 右下角...${NC}" ;;
        *) echo -e "${RED}❌ 无效的角落（1-4）${NC}"; return 1 ;;
    esac
    
    if set_window_bounds "$app" $x $y $half_width $half_height; then
        echo -e "${GREEN}✅ 已吸附到${corner}号角落${NC}"
    else
        echo -e "${RED}❌ 失败${NC}"
    fi
}

# 居中
snap_center() {
    local app="$1"
    echo -e "${BLUE}🪟 将 $app 窗口居中...${NC}"
    
    # 使用 70% 屏幕尺寸
    local width=$((SCREEN_WIDTH * 70 / 100))
    local height=$((SCREEN_HEIGHT * 70 / 100))
    local x=$(( (SCREEN_WIDTH - width) / 2 ))
    local y=$(( (SCREEN_HEIGHT - height) / 2 ))
    
    if set_window_bounds "$app" $x $y $width $height; then
        echo -e "${GREEN}✅ 已居中${NC}"
    else
        echo -e "${RED}❌ 失败${NC}"
    fi
}

# 全屏
snap_full() {
    local app="$1"
    echo -e "${BLUE}🪟 将 $app 全屏...${NC}"
    
    if set_window_bounds "$app" 0 0 $SCREEN_WIDTH $SCREEN_HEIGHT; then
        echo -e "${GREEN}✅ 已全屏${NC}"
    else
        echo -e "${RED}❌ 失败${NC}"
    fi
}

# 显示网格
show_grid() {
    echo -e "${BLUE}📐 屏幕网格布局：${NC}"
    echo ""
    echo "┌──────────────┬──────────────┐"
    echo "│   左上 (1)   │   右上 (2)   │"
    echo "│  1/4 屏幕    │  1/4 屏幕    │"
    echo "├──────────────┼──────────────┤"
    echo "│   左下 (3)   │   右下 (4)   │"
    echo "│  1/4 屏幕    │  1/4 屏幕    │"
    echo "└──────────────┴──────────────┘"
    echo ""
    echo "┌─────────────────────────────┐"
    echo "│        左半屏 (left)        │"
    echo "│         50% 宽度            │"
    echo "└─────────────────────────────┘"
    echo ""
    echo "┌─────────────────────────────┐"
    echo "│       右半屏 (right)        │"
    echo "│         50% 宽度            │"
    echo "└─────────────────────────────┘"
    echo ""
    echo "屏幕尺寸：${SCREEN_WIDTH}x${SCREEN_HEIGHT}"
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
        left)
            snap_left "$2"
            ;;
        right)
            snap_right "$2"
            ;;
        top)
            snap_top "$2"
            ;;
        bottom)
            snap_bottom "$2"
            ;;
        corner)
            snap_corner "$2" "${3:-1}"
            ;;
        center)
            snap_center "$2"
            ;;
        full)
            snap_full "$2"
            ;;
        grid)
            show_grid
            ;;
        -h|--help)
            show_help
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
