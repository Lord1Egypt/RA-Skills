#!/bin/bash
# ~/.openclaw/scripts/notify.sh
# OpenClaw 告警通知脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
LOG_DIR="$OPENCLAW_HOME/logs"
NOTIFY_CONF="$OPENCLAW_HOME/notify.conf"
UNSENT_ALERTS="$LOG_DIR/unsent_alerts.log"

mkdir -p "$LOG_DIR"

# 加载配置
load_config() {
    if [ -f "$NOTIFY_CONF" ]; then
        source "$NOTIFY_CONF"
    fi
    
    # 环境变量覆盖
    FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-${FEISHU_WEBHOOK:-}}"
    TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN:-}}"
    TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-${TELEGRAM_CHAT_ID:-}}"
    WECHAT_WEBHOOK_URL="${WECHAT_WEBHOOK_URL:-}"
    DINGTALK_WEBHOOK_URL="${DINGTALK_WEBHOOK_URL:-}"
}

# 发送飞书消息
send_feishu() {
    local level="$1"
    local message="$2"
    
    [ -z "$FEISHU_WEBHOOK_URL" ] && return 1
    
    local emoji=""
    case "$level" in
        INFO) emoji="ℹ️" ;;
        WARNING) emoji="⚠️" ;;
        ERROR) emoji="🔴" ;;
        *) emoji="📢" ;;
    esac
    
    local json_payload=$(cat <<EOF
{
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "$emoji OpenClaw 告警 - $level",
                "content": [
                    [
                        {"tag": "text", "text": "级别: $level"},
                        {"tag": "text", "text": "\\n"},
                        {"tag": "text", "text": "时间: $(date '+%Y-%m-%d %H:%M:%S')"},
                        {"tag": "text", "text": "\\n"},
                        {"tag": "text", "text": "内容: $message"}
                    ]
                ]
            }
        }
    }
}
EOF
)
    
    if curl -s -X POST "$FEISHU_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$json_payload" > /dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 飞书发送成功: $message"
        return 0
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 飞书发送失败: $message" >> "$UNSENT_ALERTS"
        return 1
    fi
}

# 发送 Telegram 消息
send_telegram() {
    local level="$1"
    local message="$2"
    
    [ -z "$TELEGRAM_BOT_TOKEN" ] && return 1
    [ -z "$TELEGRAM_CHAT_ID" ] && return 1
    
    local emoji=""
    case "$level" in
        INFO) emoji="ℹ️" ;;
        WARNING) emoji="⚠️" ;;
        ERROR) emoji="🔴" ;;
        *) emoji="📢" ;;
    esac
    
    local text="*$emoji OpenClaw 告警 - $level*

级别: $level
时间: $(date '+%Y-%m-%d %H:%M:%S')

$message"
    
    if curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d "chat_id=$TELEGRAM_CHAT_ID" \
        -d "text=$text" \
        -d "parse_mode=Markdown" > /dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Telegram 发送成功: $message"
        return 0
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Telegram 发送失败: $message" >> "$UNSENT_ALERTS"
        return 1
    fi
}

# 发送企业微信消息
send_wechat() {
    local level="$1"
    local message="$2"
    
    [ -z "$WECHAT_WEBHOOK_URL" ] && return 1
    
    local json_payload=$(cat <<EOF
{
    "msgtype": "text",
    "text": {
        "content": "[$level] OpenClaw 告警\n$(date '+%Y-%m-%d %H:%M:%S')\n$message"
    }
}
EOF
)
    
    if curl -s -X POST "$WECHAT_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$json_payload" > /dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 企业微信发送成功: $message"
        return 0
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 企业微信发送失败: $message" >> "$UNSENT_ALERTS"
        return 1
    fi
}

# 发送钉钉消息
send_dingtalk() {
    local level="$1"
    local message="$2"
    
    [ -z "$DINGTALK_WEBHOOK_URL" ] && return 1
    
    local msg_color=""
    case "$level" in
        INFO) msg_color="info" ;;
        WARNING) msg_color="warning" ;;
        ERROR) msg_color="danger" ;;
        *) msg_color="info" ;;
    esac
    
    local json_payload=$(cat <<EOF
{
    "msgtype": "markdown",
    "markdown": {
        "title": "OpenClaw 告警 - $level",
        "text": "## $level OpenClaw 告警\n\n**级别**: $level\n**时间**: $(date '+%Y-%m-%d %H:%M:%S')\n\n$message"
    }
}
EOF
)
    
    if curl -s -X POST "$DINGTALK_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$json_payload" > /dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 钉钉发送成功: $message"
        return 0
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 钉钉发送失败: $message" >> "$UNSENT_ALERTS"
        return 1
    fi
}

# 主发送函数
send_alert() {
    local level="${1:-INFO}"
    local message="$2"
    
    load_config
    
    local sent=false
    
    # 尝试所有渠道
    send_feishu "$level" "$message" && sent=true
    send_telegram "$level" "$message" && sent=true
    send_wechat "$level" "$message" && sent=true
    send_dingtalk "$level" "$message" && sent=true
    
    # 如果没有配置任何渠道
    if [ -z "$FEISHU_WEBHOOK_URL" ] && \
       [ -z "$TELEGRAM_BOT_TOKEN" ] && \
       [ -z "$WECHAT_WEBHOOK_URL" ] && \
       [ -z "$DINGTALK_WEBHOOK_URL" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] 未配置通知渠道，本地记录: $message" >> "$UNSENT_ALERTS"
        echo "⚠️ 未配置任何通知渠道，告警已写入: $UNSENT_ALERTS"
        exit 1
    fi
    
    if [ "$sent" = true ]; then
        exit 0
    else
        exit 1
    fi
}

# 生成配置模板
generate_config() {
    local config_content=$(cat <<'EOF'
# OpenClaw 告警通知配置
# 复制此文件到 ~/.openclaw/notify.conf 并填入您的配置

# 飞书机器人 Webhook (获取方式: 飞书群设置 -> 智能助手 -> 添加机器人 -> 自定义机器人)
# FEISHU_WEBHOOK_URL="YOUR_FEISHU_WEBHOOK_URL"

# Telegram 机器人 (通过 @BotFather 创建)
# TELEGRAM_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
# TELEGRAM_CHAT_ID="123456789"

# 企业微信机器人 (企业微信群 -> 右键 -> 添加群机器人)
# WECHAT_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# 钉钉机器人 (钉钉群 -> 智能助手 -> 添加机器人 -> 自定义机器人)
# DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxx"

# 取消注释并填入您的配置:
FEISHU_WEBHOOK_URL=""
# TELEGRAM_BOT_TOKEN=""
# TELEGRAM_CHAT_ID=""
# WECHAT_WEBHOOK_URL=""
# DINGTALK_WEBHOOK_URL=""
EOF
)
    
    echo "$config_content" > "$NOTIFY_CONF"
    echo "配置模板已生成: $NOTIFY_CONF"
    echo "请编辑该文件填入您的 webhook 地址"
}

# 主函数
main() {
    local level="INFO"
    local message=""
    
    # 解析参数
    if [ "$#" -eq 0 ]; then
        # 无参数，生成配置
        generate_config
        exit 0
    fi
    
    # 检查是否指定级别
    if [ "$1" = "-l" ] || [ "$1" = "--level" ]; then
        level="$2"
        shift 2
    fi
    
    # 读取消息
    if [ "$#" -gt 0 ]; then
        message="$*"
    elif [ -p /dev/stdin ]; then
        message=$(cat)
    else
        echo "用法: $0 [-l LEVEL] \"消息内容\""
        echo "      echo \"消息\" | $0"
        echo "      $0 --generate-config"
        echo ""
        echo "LEVEL: INFO, WARNING, ERROR (默认: INFO)"
        exit 1
    fi
    
    [ -z "$message" ] && { echo "错误: 消息不能为空"; exit 1; }
    
    send_alert "$level" "$message"
}

main "$@"
