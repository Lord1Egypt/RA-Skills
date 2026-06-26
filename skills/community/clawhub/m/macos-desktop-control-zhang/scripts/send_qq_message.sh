#!/bin/bash
# 使用自然语言控制发送 QQ 消息
# 用法：bash send_qq_message.sh "好友昵称" "消息内容"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QQ_SCRIPT="/Users/zhangchangsha/.openclaw/workspace/scripts/qq-send-simple.sh"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BUDDY_NAME="${1:-}"
MESSAGE="${2:-}"

echo -e "${BLUE}📱 QQ 消息发送${NC}"
echo ""

# 检查参数
if [ -z "$BUDDY_NAME" ] || [ -z "$MESSAGE" ]; then
    echo -e "${RED}❌ 请提供好友昵称和消息内容${NC}"
    echo ""
    echo "用法："
    echo "  bash $0 \"好友昵称\" \"消息内容\""
    echo ""
    echo "示例："
    echo "  bash $0 \"张三\" \"你好，现在几点了？\""
    exit 1
fi

# 检查 QQ 是否运行
if ! pgrep -x "QQ" > /dev/null; then
    echo -e "${RED}❌ QQ 未运行${NC}"
    echo ""
    echo "请先登录 QQ"
    echo ""
    read -p "是否现在打开 QQ？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open -a "QQ"
        echo "等待 QQ 启动..."
        sleep 5
    else
        exit 1
    fi
fi

# 检查 QQ 脚本
if [ ! -f "$QQ_SCRIPT" ]; then
    echo -e "${RED}❌ 找不到 QQ 发送脚本${NC}"
    echo "   $QQ_SCRIPT"
    exit 1
fi

# 发送消息
echo -e "${BLUE}正在发送消息...${NC}"
echo "  好友：$BUDDY_NAME"
echo "  消息：$MESSAGE"
echo ""

# 尝试使用 AppleScript 直接发送
osascript -e "
tell application \"QQ\"
    activate
end tell

delay 1

tell application \"System Events\"
    tell process \"QQ\"
        try
            -- 尝试使用搜索功能
            keystroke \"f\" using {command down}
            delay 0.5
            
            -- 输入好友名称
            set found to false
            
            -- 尝试不同的 UI 结构
            try
                set value of text field 1 of group 1 of scroll area 1 of group 1 of group 1 of group 1 of window 1 to \"$BUDDY_NAME\"
                set found to true
            end try
            
            if not found then
                try
                    set value of text field 1 of window 1 to \"$BUDDY_NAME\"
                    set found to true
                end try
            end if
            
            if found then
                delay 0.5
                key code 36  -- 回车选择
                delay 1
                
                -- 输入消息
                try
                    set value of text area 1 of scroll area 1 of group 1 of group 1 of group 1 of group 1 of window 1 to \"$MESSAGE\"
                end try
                
                delay 0.5
                
                -- 发送
                keystroke return using {command down}
                
                return \"✅ 发送成功\"
            else
                return \"❌ 未找到好友\"
            end if
        on error errMsg
            return \"❌ 错误：\" & errMsg
        end try
    end tell
end tell
" 2>&1

echo ""
echo -e "${YELLOW}💡 提示：${NC}"
echo "  如果自动发送失败，可以手动操作："
echo "  1. 打开 QQ"
echo "  2. 搜索好友：$BUDDY_NAME"
echo "  3. 发送消息：$MESSAGE"
echo ""
