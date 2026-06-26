#!/bin/bash
# one-mail 公共函数库

CONFIG_DIR="$HOME/.onemail"
CONFIG_FILE="$CONFIG_DIR/config.json"
CREDS_FILE="$CONFIG_DIR/credentials.json"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

# 加载配置
load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "❌ 配置文件不存在，请先运行: bash scripts/setup.sh" >&2
        exit 1
    fi
    
    CONFIG=$(cat "$CONFIG_FILE")
    export CONFIG
    
    if [ ! -f "$CREDS_FILE" ]; then
        echo "❌ 凭证文件不存在" >&2
        exit 1
    fi
    
    CREDS=$(cat "$CREDS_FILE")
    export CREDS
}

# 获取账户凭证
get_credentials() {
    local account_type="$1"
    local email="$2"
    
    if [ -n "$email" ]; then
        echo "$CREDS" | jq -r --arg type "$account_type" --arg email "$email" '.[$type][$email]'
    else
        echo "$CREDS" | jq -r --arg type "$account_type" '.[$type]'
    fi
}

# 保存凭证
save_credentials() {
    local account_type="$1"
    local email="$2"
    local data="$3"
    
    if [ -n "$email" ]; then
        CREDS=$(echo "$CREDS" | jq --arg type "$account_type" --arg email "$email" --argjson data "$data" \
            '.[$type][$email] = $data')
    else
        CREDS=$(echo "$CREDS" | jq --arg type "$account_type" --argjson data "$data" \
            '.[$type] = $data')
    fi
    
    echo "$CREDS" > "$CREDS_FILE"
    chmod 600 "$CREDS_FILE"
}

# 格式化邮件为统一 JSON 格式
format_email() {
    local id="$1"
    local account="$2"
    local from="$3"
    local to="$4"
    local subject="$5"
    local date="$6"
    local unread="$7"
    local has_attachments="$8"
    local snippet="$9"
    
    jq -n \
        --arg id "$id" \
        --arg account "$account" \
        --arg from "$from" \
        --arg to "$to" \
        --arg subject "$subject" \
        --arg date "$date" \
        --argjson unread "$unread" \
        --argjson has_attachments "$has_attachments" \
        --arg snippet "$snippet" \
        '{
            id: $id,
            account: $account,
            from: $from,
            to: $to,
            subject: $subject,
            date: $date,
            unread: $unread,
            has_attachments: $has_attachments,
            snippet: $snippet
        }'
}

# Base64 编码（URL 安全）
base64_encode() {
    echo -n "$1" | base64 | tr '+/' '-_' | tr -d '='
}

# Base64 解码
base64_decode() {
    local len=$((${#1} % 4))
    local result="$1"
    if [ $len -eq 2 ]; then result="$1"'=='; fi
    if [ $len -eq 3 ]; then result="$1"'='; fi
    echo "$result" | tr '_-' '/+' | base64 -d
}

# 检查命令是否存在
require_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ 缺少命令: $1" >&2
        exit 1
    fi
}

# 检查文件是否存在
require_file() {
    if [ ! -f "$1" ]; then
        echo "❌ 文件不存在: $1" >&2
        exit 1
    fi
}
