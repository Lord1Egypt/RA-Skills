#!/bin/bash
# one-mail 发送邮件脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# 参数解析
ACCOUNT=""
TO=""
CC=""
BCC=""
SUBJECT=""
BODY=""
ATTACH=""
REPLY_TO=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --account)
            ACCOUNT="$2"
            shift 2
            ;;
        --to)
            TO="$2"
            shift 2
            ;;
        --cc)
            CC="$2"
            shift 2
            ;;
        --bcc)
            BCC="$2"
            shift 2
            ;;
        --subject)
            SUBJECT="$2"
            shift 2
            ;;
        --body)
            BODY="$2"
            shift 2
            ;;
        --attach)
            ATTACH="$2"
            shift 2
            ;;
        --reply-to)
            REPLY_TO="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 验证必需参数
if [ -z "$TO" ]; then
    echo "❌ 缺少收件人 (--to)" >&2
    exit 1
fi

if [ -z "$SUBJECT" ]; then
    echo "❌ 缺少主题 (--subject)" >&2
    exit 1
fi

if [ -z "$BODY" ]; then
    echo "❌ 缺少正文 (--body)" >&2
    exit 1
fi

# 加载配置
load_config

# 确定使用的账户
if [ -z "$ACCOUNT" ]; then
    ACCOUNT=$(echo "$CONFIG" | jq -r '.default_account')
    if [ "$ACCOUNT" = "null" ]; then
        echo "❌ 未设置默认账户，请使用 --account 指定" >&2
        exit 1
    fi
    log "使用默认账户: $ACCOUNT"
fi

# 获取账户信息
account=$(echo "$CONFIG" | jq -r --arg email "$ACCOUNT" '.accounts[] | select(.email == $email)')
if [ -z "$account" ]; then
    echo "❌ 账户不存在: $ACCOUNT" >&2
    exit 1
fi

account_type=$(echo "$account" | jq -r '.type')
account_name=$(echo "$account" | jq -r '.name')

log "发送邮件: $account_name ($account_type)"
log "收件人: $TO"
log "主题: $SUBJECT"

# 发送邮件
case $account_type in
    gmail)
        source "$SCRIPT_DIR/lib/gmail.sh"
        send_gmail "$account" "$TO" "$CC" "$BCC" "$SUBJECT" "$BODY" "$ATTACH" "$REPLY_TO"
        ;;
    outlook)
        source "$SCRIPT_DIR/lib/outlook.sh"
        send_outlook "$account" "$TO" "$CC" "$BCC" "$SUBJECT" "$BODY" "$ATTACH" "$REPLY_TO"
        ;;
    163|126)
        source "$SCRIPT_DIR/lib/163.sh"
        send_163 "$account" "$TO" "$CC" "$BCC" "$SUBJECT" "$BODY" "$ATTACH" "$REPLY_TO"
        ;;
    *)
        echo "❌ 不支持的账户类型: $account_type" >&2
        exit 1
        ;;
esac

echo "✅ 邮件已发送"
