#!/bin/bash

# MiniMax Token Left Query Script
# 用途：查询 MiniMax Coding Plan 剩余 token 使用量

set -e

SKILL_DIR="/home/allen/.openclaw/workspace/skills/minimax-token-left-query"
COOKIE_FILE="$SKILL_DIR/cookies.txt"

echo "🔍 正在打开 MiniMax 账户管理页面..."

# 使用本地浏览器打开 MiniMax 开发者平台
browser-use -b real --profile "Default" open "https://platform.minimaxi.com/user-center/payment/coding-plan"

# 等待页面加载
sleep 3

# 检查是否需要登录（通过页面内容判断）
echo "📄 检查登录状态..."

# 获取页面内容
PAGE_TEXT=$(browser-use -b real --profile "Default" eval "document.body.innerText")

if echo "$PAGE_TEXT" | grep -q "登录"; then
    echo "⚠️ 需要登录！请提供："
    echo "1. 手机号："
    read -r PHONE
    echo "2. 验证码："
    read -r CODE
    
    # 这里需要用户手动登录，脚本暂停
    echo "📱 请在浏览器中完成登录，完成后按回车继续..."
    read -r
    
    # 再次检查页面
    PAGE_TEXT=$(browser-use -b real --profile "Default" eval "document.body.innerText")
fi

# 提取使用百分比
USED_PERCENT=$(echo "$PAGE_TEXT" | grep -oP '\d+(?=%) 已使用' | grep -oP '\d+' || echo "0")

# 提取重置分钟数
RESET_MINUTES=$(echo "$PAGE_TEXT" | grep -oP '\d+ 分钟后重置' | grep -oP '\d+' || echo "0")

# 提取时间窗口
TIME_WINDOW=$(echo "$PAGE_TEXT" | grep -oP '\d+:\d+-\d+:\d+ UTC' | head -1 || echo "")

# 输出结果
echo ""
echo "📊 MiniMax Token 使用情况："
echo "========================"
echo "已使用: ${USED_PERCENT}%"
echo "重置剩余: ${RESET_MINUTES} 分钟"
if [ -n "$TIME_WINDOW" ]; then
    echo "时间窗口: $TIME_WINDOW"
fi
echo "========================"

# 输出 JSON 格式（方便程序解析）
echo ""
echo "JSON 输出:"
cat <<EOF
{
  "used_percent": $USED_PERCENT,
  "reset_minutes": $RESET_MINUTES,
  "time_window": "$TIME_WINDOW",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

# 如果使用超过 90%，发出警告
if [ "$USED_PERCENT" -ge 90 ]; then
    echo ""
    echo "⚠️ 警告：Token 使用量已达 ${USED_PERCENT}%！即将耗尽，请注意！"
fi
