#!/bin/bash
# one-mail 收取邮件脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# 参数解析
ACCOUNT=""
UNREAD_ONLY=false
QUERY=""
LIMIT=20

while [[ $# -gt 0 ]]; do
    case $1 in
        --account)
            ACCOUNT="$2"
            shift 2
            ;;
        --unread)
            UNREAD_ONLY=true
            shift
            ;;
        --query)
            QUERY="$2"
            shift 2
            ;;
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 加载配置
load_config

# 获取要查询的账户列表
if [ -n "$ACCOUNT" ]; then
    accounts=$(echo "$CONFIG" | jq -c --arg name "$ACCOUNT" '.accounts[] | select(.name == $name)')
    if [ -z "$accounts" ]; then
        echo "❌ 账户不存在: $ACCOUNT" >&2
        exit 1
    fi
else
    accounts=$(echo "$CONFIG" | jq -c '.accounts[]')
fi

# 收取邮件
all_emails="[]"

while IFS= read -r account; do
    account_type=$(echo "$account" | jq -r '.type')
    account_name=$(echo "$account" | jq -r '.name')
    
    log "收取邮件: $account_name ($account_type)"
    
    case $account_type in
        gmail)
            emails=$(source "$SCRIPT_DIR/lib/gmail.sh" && fetch_gmail "$account" "$UNREAD_ONLY" "$QUERY" "$LIMIT")
            ;;
        outlook)
            emails=$(source "$SCRIPT_DIR/lib/outlook.sh" && fetch_outlook "$account" "$UNREAD_ONLY" "$QUERY" "$LIMIT")
            ;;
        163|126)
            emails=$(source "$SCRIPT_DIR/lib/163.sh" && fetch_163 "$account" "$UNREAD_ONLY" "$QUERY" "$LIMIT")
            ;;
        *)
            log "不支持的账户类型: $account_type"
            continue
            ;;
    esac
    
    # 合并结果（跳过空响应）
    if [ -n "$emails" ] && echo "$emails" | jq empty 2>/dev/null; then
        all_emails=$(echo "$all_emails" | jq --argjson new "$emails" '. + $new')
    fi
done < <(echo "$accounts" | jq -c '.')

# 按日期排序
all_emails=$(echo "$all_emails" | jq 'sort_by(.date) | reverse')

# 输出结果
echo "$all_emails" | jq '.'
