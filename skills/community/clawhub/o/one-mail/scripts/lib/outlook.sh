#!/bin/bash
# Outlook 适配器

require_command curl
require_command jq

# 获取访问令牌
get_outlook_token() {
    local account="$1"
    
    local client_id=$(echo "$account" | jq -r '.client_id')
    local creds=$(get_credentials "outlook")
    local client_secret=$(echo "$creds" | jq -r '.client_secret')
    local refresh_token=$(echo "$creds" | jq -r '.refresh_token')
    
    # 使用 refresh token 获取新的 access token
    local token_response=$(curl -s -X POST \
        "https://login.microsoftonline.com/common/oauth2/v2.0/token" \
        -d "client_id=$client_id" \
        -d "client_secret=$client_secret" \
        -d "refresh_token=$refresh_token" \
        -d "grant_type=refresh_token" \
        -d "scope=Mail.ReadWrite Mail.Send")
    
    local access_token=$(echo "$token_response" | jq -r '.access_token')
    local new_refresh_token=$(echo "$token_response" | jq -r '.refresh_token')
    
    if [ "$access_token" = "null" ]; then
        echo "❌ 获取 Outlook access token 失败" >&2
        echo "$token_response" >&2
        exit 1
    fi
    
    # 更新 refresh token（如果有新的）
    if [ "$new_refresh_token" != "null" ]; then
        local new_creds=$(echo "$creds" | jq --arg token "$new_refresh_token" '.refresh_token = $token')
        save_credentials "outlook" "" "$new_creds"
    fi
    
    echo "$access_token"
}

# 收取 Outlook 邮件
fetch_outlook() {
    local account="$1"
    local unread_only="$2"
    local query="$3"
    local limit="$4"
    
    local access_token=$(get_outlook_token "$account")
    
    # 构建 API URL，只选择需要的字段
    local api_url='https://graph.microsoft.com/v1.0/me/messages?$select=id,subject,from,toRecipients,receivedDateTime,isRead,hasAttachments,bodyPreview&$top='"$limit"'&$orderby=receivedDateTime%20desc'
    
    # 添加过滤条件
    local filter=""
    if [ "$unread_only" = "true" ]; then
        filter="isRead eq false"
    fi
    
    if [ -n "$query" ]; then
        if [ -n "$filter" ]; then
            filter="$filter and contains(subject,'$query')"
        else
            filter="contains(subject,'$query')"
        fi
    fi
    
    if [ -n "$filter" ]; then
        # URL 编码 filter 中的空格
        local encoded_filter=$(echo "$filter" | sed 's/ /%20/g')
        api_url="$api_url"'&$filter='"$encoded_filter"
    fi
    
    # 获取邮件
    local raw_emails=$(curl -s -H "Authorization: Bearer $access_token" "$api_url")
    
    # 检查响应是否有效
    if [ -z "$raw_emails" ] || ! echo "$raw_emails" | jq -e '.value' >/dev/null 2>&1; then
        echo "[]"
        return
    fi
    
    # 转换为统一格式
    echo "$raw_emails" | jq --arg account "outlook" '.value | map({
        id: .id,
        account: $account,
        from: .from.emailAddress.address,
        to: (.toRecipients[0].emailAddress.address // ""),
        subject: .subject,
        date: .receivedDateTime,
        unread: (.isRead | not),
        has_attachments: .hasAttachments,
        snippet: .bodyPreview
    })'
}

# 发送 Outlook 邮件
send_outlook() {
    local account="$1"
    local to="$2"
    local cc="$3"
    local bcc="$4"
    local subject="$5"
    local body="$6"
    local attach="$7"
    local reply_to="$8"
    
    local access_token=$(get_outlook_token "$account")
    
    # 构建邮件 JSON
    local message=$(jq -n \
        --arg subject "$subject" \
        --arg body "$body" \
        --arg to "$to" \
        '{
            subject: $subject,
            body: {
                contentType: "Text",
                content: $body
            },
            toRecipients: [
                {
                    emailAddress: {
                        address: $to
                    }
                }
            ]
        }')
    
    # 添加 CC
    if [ -n "$cc" ]; then
        message=$(echo "$message" | jq --arg cc "$cc" \
            '.ccRecipients = [{emailAddress: {address: $cc}}]')
    fi
    
    # 添加 BCC
    if [ -n "$bcc" ]; then
        message=$(echo "$message" | jq --arg bcc "$bcc" \
            '.bccRecipients = [{emailAddress: {address: $bcc}}]')
    fi
    
    # 处理附件
    if [ -n "$attach" ]; then
        # 检查文件是否存在
        if [ ! -f "$attach" ]; then
            echo "❌ 附件文件不存在: $attach" >&2
            exit 1
        fi
        
        # 获取文件名和大小
        local filename=$(basename "$attach")
        local filesize=$(stat -f%z "$attach" 2>/dev/null || stat -c%s "$attach" 2>/dev/null)
        
        # 检查文件大小（Graph API 限制：小于 3MB 可以直接附加，大于 3MB 需要上传会话）
        local max_inline_size=$((3 * 1024 * 1024))  # 3MB
        
        if [ "$filesize" -lt "$max_inline_size" ]; then
            # 小文件：直接 base64 编码并附加到邮件
            local base64_content=$(base64 -i "$attach" | tr -d '\n')
            
            message=$(echo "$message" | jq \
                --arg name "$filename" \
                --arg content "$base64_content" \
                '.attachments = [{
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": $name,
                    "contentBytes": $content
                }]')
            
            log "📎 添加附件: $filename ($(numfmt --to=iec-i --suffix=B $filesize 2>/dev/null || echo ${filesize}B))"
        else
            # 大文件：需要使用上传会话（暂不支持）
            echo "⚠️  附件过大 ($(numfmt --to=iec-i --suffix=B $filesize 2>/dev/null || echo ${filesize}B))，Outlook 直接附加限制为 3MB" >&2
            echo "提示：大文件请使用 OneDrive 分享链接" >&2
            exit 1
        fi
    fi
    
    # 发送邮件（需要包裹在 message 字段中）
    local payload=$(jq -n --argjson msg "$message" '{message: $msg}')
    local response=$(curl -s -X POST \
        "https://graph.microsoft.com/v1.0/me/sendMail" \
        -H "Authorization: Bearer $access_token" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    # 检查错误
    local error=$(echo "$response" | jq -r '.error.message // empty')
    if [ -n "$error" ]; then
        echo "❌ 发送失败: $error" >&2
        echo "$response" | jq '.' >&2
        exit 1
    fi
}
