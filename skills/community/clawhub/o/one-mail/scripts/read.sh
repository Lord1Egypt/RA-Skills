#!/bin/bash
# one-mail 邮件阅读脚本
# 用法: bash scripts/read.sh --id <message_id> --account <account_name>
#       bash scripts/read.sh --account outlook --latest
#       bash scripts/read.sh --account gmail --query "MacBook"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# 解析参数
MSG_ID=""
ACCOUNT=""
QUERY=""
LATEST=false
FORMAT="text"  # text | json | html

while [[ $# -gt 0 ]]; do
    case $1 in
        --id) MSG_ID="$2"; shift 2 ;;
        --account) ACCOUNT="$2"; shift 2 ;;
        --query) QUERY="$2"; shift 2 ;;
        --latest) LATEST=true; shift ;;
        --format) FORMAT="$2"; shift 2 ;;
        --json) FORMAT="json"; shift ;;
        --html) FORMAT="html"; shift ;;
        *) echo "未知参数: $1" >&2; exit 1 ;;
    esac
done

load_config

# 确定账户
if [ -z "$ACCOUNT" ]; then
    # 默认使用第一个账户
    ACCOUNT=$(echo "$CONFIG" | jq -r '.accounts[0].name')
fi

account=$(echo "$CONFIG" | jq -c --arg name "$ACCOUNT" '.accounts[] | select(.name == $name)')
if [ -z "$account" ]; then
    echo "❌ 账户不存在: $ACCOUNT" >&2
    exit 1
fi

account_type=$(echo "$account" | jq -r '.type')

# ============================================================
# Gmail 阅读
# ============================================================
read_gmail() {
    local msg_id="$1"
    local query="$2"

    # 如果没有 ID，用搜索找到第一封
    if [ -z "$msg_id" ]; then
        if [ -n "$query" ]; then
            msg_id=$(gog gmail messages search "$query" --limit 1 --json 2>/dev/null | jq -r '.messages[0].id // empty')
        elif [ "$LATEST" = true ]; then
            msg_id=$(gog gmail messages search "is:unread" --limit 1 --json 2>/dev/null | jq -r '.messages[0].id // empty')
        fi
    fi

    if [ -z "$msg_id" ]; then
        echo "❌ 未找到邮件" >&2
        exit 1
    fi

    # 获取完整邮件
    local raw=$(gog gmail get "$msg_id" --json 2>/dev/null)

    if [ "$FORMAT" = "json" ]; then
        echo "$raw"
    elif [ "$FORMAT" = "html" ]; then
        echo "$raw" | jq -r '.body // ""'
    else
        # 提取元信息
        local subject=$(echo "$raw" | jq -r '.headers.subject // ""')
        local from=$(echo "$raw" | jq -r '.headers.from // ""')
        local date=$(echo "$raw" | jq -r '.headers.date // ""')
        local body=$(echo "$raw" | jq -r '.body // ""')

        echo "From: $from"
        echo "Subject: $subject"
        echo "Date: $date"
        echo "---"

        if echo "$body" | grep -q '<html\|<div\|<p\|<table'; then
            echo "$body" | python3 "$SCRIPT_DIR/lib/html2text.py"
        else
            echo "$body"
        fi
    fi
}

# ============================================================
# Outlook 阅读
# ============================================================
read_outlook() {
    local msg_id="$1"
    local query="$2"

    source "$SCRIPT_DIR/lib/outlook.sh"
    local access_token=$(get_outlook_token "$account" 2>/dev/null)

    if [ -z "$access_token" ] || [ "$access_token" = "null" ]; then
        echo "❌ Outlook 认证失败" >&2
        exit 1
    fi

    # 如果没有 ID，用搜索找到第一封
    if [ -z "$msg_id" ]; then
        local search_url='https://graph.microsoft.com/v1.0/me/messages?$select=id&$top=1&$orderby=receivedDateTime%20desc'
        if [ -n "$query" ]; then
            local encoded_filter=$(python3 -c "import urllib.parse; print(urllib.parse.quote(\"contains(subject,'$query')\"))")
            search_url="${search_url}&\$filter=${encoded_filter}"
            # 如果 filter 搜索失败，尝试 $search
            msg_id=$(curl -s -H "Authorization: Bearer $access_token" "$search_url" | jq -r '.value[0].id // empty')
            if [ -z "$msg_id" ]; then
                local search_url2="https://graph.microsoft.com/v1.0/me/messages?\$search=%22$(python3 -c "import urllib.parse; print(urllib.parse.quote('$query'))")%22&\$select=id&\$top=1"
                msg_id=$(curl -s -H "Authorization: Bearer $access_token" "$search_url2" | jq -r '.value[0].id // empty')
            fi
        elif [ "$LATEST" = true ]; then
            search_url="${search_url}&\$filter=isRead%20eq%20false"
            msg_id=$(curl -s -H "Authorization: Bearer $access_token" "$search_url" | jq -r '.value[0].id // empty')
        fi
    fi

    if [ -z "$msg_id" ]; then
        echo "❌ 未找到邮件" >&2
        exit 1
    fi

    # 获取完整邮件
    local mail_url="https://graph.microsoft.com/v1.0/me/messages/${msg_id}?\$select=id,subject,from,toRecipients,receivedDateTime,body,hasAttachments"
    local raw=$(curl -s -H "Authorization: Bearer $access_token" "$mail_url")

    if [ "$FORMAT" = "json" ]; then
        echo "$raw" | jq '{
            id: .id,
            subject: .subject,
            from: .from.emailAddress.address,
            to: (.toRecipients // [] | map(.emailAddress.address) | join(", ")),
            date: .receivedDateTime,
            has_attachments: .hasAttachments,
            body_type: .body.contentType,
            body: .body.content
        }'
    elif [ "$FORMAT" = "html" ]; then
        echo "$raw" | jq -r '.body.content // ""'
    else
        # 提取元信息
        local subject=$(echo "$raw" | jq -r '.subject // ""')
        local from=$(echo "$raw" | jq -r '.from.emailAddress.address // ""')
        local date=$(echo "$raw" | jq -r '.receivedDateTime // ""')
        local body_type=$(echo "$raw" | jq -r '.body.contentType // ""')
        local body=$(echo "$raw" | jq -r '.body.content // ""')

        echo "From: $from"
        echo "Subject: $subject"
        echo "Date: $date"
        echo "---"

        if [ "$body_type" = "html" ]; then
            echo "$body" | python3 "$SCRIPT_DIR/lib/html2text.py"
        else
            echo "$body"
        fi
    fi
}

# ============================================================
# 163 阅读
# ============================================================
read_163() {
    local msg_id="$1"
    echo "❌ 163 邮箱暂不支持单封阅读，请使用 fetch.sh" >&2
    exit 1
}

# ============================================================
# 主逻辑
# ============================================================
case $account_type in
    gmail)
        read_gmail "$MSG_ID" "$QUERY"
        ;;
    outlook)
        read_outlook "$MSG_ID" "$QUERY"
        ;;
    163|126)
        read_163 "$MSG_ID"
        ;;
    *)
        echo "❌ 不支持的账户类型: $account_type" >&2
        exit 1
        ;;
esac
