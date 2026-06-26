#!/bin/bash
# Gmail 适配器

require_command gog

# 收取 Gmail 邮件
fetch_gmail() {
    local account="$1"
    local unread_only="$2"
    local query="$3"
    local limit="$4"
    
    local email=$(echo "$account" | jq -r '.email')
    
    # 构建查询参数
    local gog_query=""
    if [ "$unread_only" = "true" ]; then
        gog_query="is:unread"
    fi
    
    if [ -n "$query" ]; then
        if [ -n "$gog_query" ]; then
            gog_query="$gog_query $query"
        else
            gog_query="$query"
        fi
    fi
    
    # 使用 gog 获取邮件
    local gog_cmd="gog gmail messages search"
    
    # 添加查询条件
    if [ -n "$gog_query" ]; then
        gog_cmd="$gog_cmd \"$gog_query\""
    else
        gog_cmd="$gog_cmd \"in:inbox\""
    fi
    
    # 添加其他参数
    gog_cmd="$gog_cmd --max $limit --account $email --json"
    
    local raw_emails=$(eval "$gog_cmd")
    
    # 转换为统一格式
    echo "$raw_emails" | jq --arg account "gmail" '.messages | map({
        id: .id,
        account: $account,
        from: .from,
        to: (.to // ""),
        subject: .subject,
        date: .date,
        unread: (.labels | contains(["UNREAD"])),
        has_attachments: false,
        snippet: (.snippet // "")
    })'
}

# 发送 Gmail 邮件
send_gmail() {
    local account="$1"
    local to="$2"
    local cc="$3"
    local bcc="$4"
    local subject="$5"
    local body="$6"
    local attach="$7"
    local reply_to="$8"
    
    # 构建 gog 命令
    local gog_cmd="gog gmail send --to \"$to\" --subject \"$subject\""
    
    if [ -n "$cc" ]; then
        gog_cmd="$gog_cmd --cc \"$cc\""
    fi
    
    if [ -n "$bcc" ]; then
        gog_cmd="$gog_cmd --bcc \"$bcc\""
    fi
    
    if [ -n "$attach" ]; then
        require_file "$attach"
        gog_cmd="$gog_cmd --attach \"$attach\""
    fi
    
    if [ -n "$reply_to" ]; then
        gog_cmd="$gog_cmd --reply-to \"$reply_to\""
    fi
    
    # 发送邮件（正文通过 stdin）
    gog_cmd="$gog_cmd --body-file -"
    echo "$body" | eval "$gog_cmd"
}
