#!/bin/bash
# MiniMax Token 快速查询 - V9 版本
# 更新日期: 2026-03-12
# 支持两种登录方式：密码登录 + 手机验证码登录

echo "🔍 打开 MiniMax 页面..."

# 打开页面
browser-use --browser real --profile "Default" open "https://platform.minimaxi.com/user-center/payment/coding-plan"
sleep 3

# 检查是否需要登录
PAGE_TEXT=$(browser-use --browser real --profile "Default" eval "document.body.innerText" 2>/dev/null)

if echo "$PAGE_TEXT" | grep -q "开放平台账户登录"; then
    echo "📱 需要登录..."
    
    # 从 memory 获取凭据
    MEMORY_FILE="/home/allen/.openclaw/workspace/memory/minimax-login.txt"
    PHONE=""
    PASSWORD=""
    
    if [ -f "$MEMORY_FILE" ]; then
        PHONE=$(grep "phone=" "$MEMORY_FILE" | cut -d'=' -f2)
        PASSWORD=$(grep "password=" "$MEMORY_FILE" | cut -d'=' -f2-)
    fi
    
    # 如果没有密码，尝试验证码登录
    if [ -z "$PASSWORD" ]; then
        echo "🔐 使用验证码登录..."
        
        # 检查当前是否在验证码登录页面
        STATE=$(browser-use --browser real --profile "Default" state 2>&1)
        if echo "$STATE" | grep -q "手机验证码登录"; then
            # 点击手机验证码登录标签
            PHONE_TAB=$(echo "$STATE" | grep "手机验证码登录" | head -1 | sed 's/.*\[\([0-9]*\)\].*/\1/' | head -1)
            [ -n "$PHONE_TAB" ] && browser-use --browser real --profile "Default" click "$PHONE_TAB" 2>/dev/null
            sleep 1
        fi
        
        # 输入手机号
        if [ -z "$PHONE" ]; then
            echo "⚠️ 请提供手机号："
            read -r PHONE
        fi
        
        STATE=$(browser-use --browser real --profile "Default" state 2>&1)
        PHONE_INPUT=$(echo "$STATE" | grep "register_mail" | head -1 | sed 's/.*\[\([0-9]*\)\].*/\1/' | head -1)
        
        [ -n "$PHONE_INPUT" ] && browser-use --browser real --profile "Default" click "$PHONE_INPUT" 2>/dev/null
        sleep 0.5
        [ -n "$PHONE_INPUT" ] && browser-use --browser real --profile "Default" type "$PHONE"
        echo "📱 手机号: $PHONE"
        
        # 勾选协议
        browser-use --browser real --profile "Default" eval "document.querySelector('#register_protocol')?.click()" 2>/dev/null
        sleep 1
        
        # 点击获取验证码
        STATE=$(browser-use --browser real --profile "Default" state 2>&1)
        SEND_BTN=$(echo "$STATE" | grep -E "获取验证码" | head -1 | sed 's/.*\[\([0-9]*\)\].*/\1/' | head -1)
        [ -n "$SEND_BTN" ] && browser-use --browser real --profile "Default" click "$SEND_BTN" 2>/dev/null
        echo "📱 验证码已发送..."
        
        sleep 3
        
        # 输入验证码
        echo "⚠️ 请提供验证码："
        read -r CODE
        echo "📱 输入验证码: $CODE"
        
        STATE=$(browser-use --browser real --profile "Default" state 2>&1)
        CODE_INPUT=$(echo "$STATE" | grep "register_captcha" | head -1 | sed 's/.*\[\([0-9]*\)\].*/\1/' | head -1)
        [ -n "$CODE_INPUT" ] && browser-use --browser real --profile "Default" click "$CODE_INPUT" 2>/dev/null
        browser-use --browser real --profile "Default" type "$CODE"
        
        # 点击登录
        STATE=$(browser-use --browser real --profile "Default" state 2>&1)
        SUBMIT_BTN=$(echo "$STATE" | grep -E "button.*submit" | head -1 | sed 's/.*\[\([0-9]*\)\].*/\1/' | head -1)
        [ -n "$SUBMIT_BTN" ] && browser-use --browser real --profile "Default" click "$SUBMIT_BTN" 2>/dev/null
        
    else
        # 密码登录方式
        echo "🔐 使用密码登录..."
        
        STATE=$(browser-use --browser real --profile "Default" state 2>&1)
        PHONE_INPUT=$(echo "$STATE" | grep "register_mail" | head -1 | sed 's/.*\[\([0-9]*\)\].*/\1/' | head -1)
        
        [ -n "$PHONE_INPUT" ] && browser-use --browser real --profile "Default" click "$PHONE_INPUT" 2>/dev/null
        sleep 0.5
        [ -n "$PHONE_INPUT" ] && browser-use --browser real --profile "Default" type "$PHONE"
        echo "📱 手机号: $PHONE"
        
        sleep 0.5
        
        STATE=$(browser-use --browser real --profile "Default" state 2>&1)
        PWD_INPUT=$(echo "$STATE" | grep "register_password" | head -1 | sed 's/.*\[\([0-9]*\)\].*/\1/' | head -1)
        
        [ -n "$PWD_INPUT" ] && browser-use --browser real --profile "Default" click "$PWD_INPUT" 2>/dev/null
        sleep 0.5
        [ -n "$PWD_INPUT" ] && browser-use --browser real --profile "Default" type "$PASSWORD"
        echo "📱 密码: ****"
        
        # 勾选协议
        browser-use --browser real --profile "Default" eval "document.querySelector('#register_protocol')?.click()" 2>/dev/null
        sleep 0.5
        
        # 点击登录
        STATE=$(browser-use --browser real --profile "Default" state 2>&1)
        SUBMIT_BTN=$(echo "$STATE" | grep -E "button.*submit" | head -1 | sed 's/.*\[\([0-9]*\)\].*/\1/' | head -1)
        [ -n "$SUBMIT_BTN" ] && browser-use --browser real --profile "Default" click "$SUBMIT_BTN" 2>/dev/null
    fi
    
    # 等待登录
    sleep 4
    
    # 检查登录结果
    PAGE_TEXT=$(browser-use --browser real --profile "Default" eval "document.body.innerText" 2>/dev/null)
    
    if echo "$PAGE_TEXT" | grep -q "请输入正确的手机号或邮箱"; then
        echo "❌ 登录失败：手机号或密码错误"
        rm -f "$MEMORY_FILE"
        exit 1
    fi
    
    if echo "$PAGE_TEXT" | grep -q "开放平台账户登录"; then
        echo "❌ 登录失败，请重试"
        rm -f "$MEMORY_FILE"
        exit 1
    fi
    
    # 登录成功
    echo "✅ 登录成功"
    
    # 如果有密码，保存到 memory
    if [ -n "$PASSWORD" ]; then
        echo "💾 保存凭据到 memory..."
        echo "phone=$PHONE" > "$MEMORY_FILE"
        echo "password=$PASSWORD" >> "$MEMORY_FILE"
        chmod 600 "$MEMORY_FILE"
    fi
fi

# 刷新页面
echo "🔄 刷新页面..."
browser-use --browser real --profile "Default" eval "location.reload()"
sleep 3

# 获取数据
PAGE_TEXT=$(browser-use --browser real --profile "Default" eval "document.body.innerText" 2>/dev/null)

USED=$(echo "$PAGE_TEXT" | grep -oE '[0-9]+% 已使用' | grep -oE '[0-9]+' || echo "0")

# 重置时间 - 修复解析逻辑（顺序很重要）
RESET_MINUTES=""

# 格式1: "X 小时 Y 分钟后重置" (最优先)
if [ -z "$RESET_MINUTES" ]; then
    TEMP=$(echo "$PAGE_TEXT" | grep -oE '[0-9]+ 小时 [0-9]+ 分钟后重置' | head -1)
    if [ -n "$TEMP" ]; then
        HOURS=$(echo "$TEMP" | grep -oE '[0-9]+' | head -1)
        MINS=$(echo "$TEMP" | grep -oE '[0-9]+' | tail -1)
        [ -n "$HOURS" ] && [ -n "$MINS" ] && RESET_MINUTES=$((HOURS * 60 + MINS))
    fi
fi

# 格式2: "X 分钟后重置"
if [ -z "$RESET_MINUTES" ]; then
    TEMP=$(echo "$PAGE_TEXT" | grep -oE '[0-9]+ 分钟后重置' | head -1)
    if [ -n "$TEMP" ]; then
        RESET_MINUTES=$(echo "$TEMP" | grep -oE '[0-9]+' | head -1)
    fi
fi

# 格式3: "X 小时后重置"
if [ -z "$RESET_MINUTES" ]; then
    TEMP=$(echo "$PAGE_TEXT" | grep -oE '[0-9]+ 小时后重置' | head -1)
    if [ -n "$TEMP" ]; then
        HOURS=$(echo "$TEMP" | grep -oE '[0-9]+' | head -1)
        [ -n "$HOURS" ] && RESET_MINUTES=$((HOURS * 60))
    fi
fi

# 如果都没找到，使用默认值
[ -z "$RESET_MINUTES" ] && RESET_MINUTES="0"

TIME_WINDOW=$(echo "$PAGE_TEXT" | grep -oE '[0-9]+:[0-9]+-[0-9]+:[0-9]+' | head -1 || echo "")
TOTAL_PROMPTS=$(echo "$PAGE_TEXT" | grep -oE '[0-9]+ prompts' | grep -oE '[0-9]+' || echo "0")
TOTAL_HOURS=$(echo "$PAGE_TEXT" | grep -oE '[0-9]+ 小时' | grep -oE '[0-9]+' | head -1 || echo "0")

echo ""
echo "📊 MiniMax Token 使用情况："
echo "========================"
echo "已使用: ${USED}%"
echo "重置剩余: ${RESET_MINUTES} 分钟"
echo "可用额度: ${TOTAL_PROMPTS} prompts / ${TOTAL_HOURS} 小时"
[ -n "$TIME_WINDOW" ] && echo "时间窗口: $TIME_WINDOW"
echo "========================"

[ "$USED" -ge 90 ] && echo "⚠️ 警告：Token 使用量已达 ${USED}%！"

browser-use --browser real --profile "Default" screenshot /tmp/minimax-token-query.png 2>/dev/null
echo "📸 截图已保存"
