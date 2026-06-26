#!/bin/bash
#
# 飞书 API 工具函数
#

FEISHU_API_BASE="https://open.feishu.cn/open-apis"

# 获取 tenant access token
get_tenant_token() {
    local app_id=$1
    local app_secret=$2
    
    curl -s -X POST "${FEISHU_API_BASE}/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$app_id\",\"app_secret\":\"$app_secret\"}" | \
        jq -r '.tenant_access_token'
}

# 从 URL 提取文档 token
extract_doc_token() {
    local url=$1
    # 提取 wiki/ 或 docx/ 后的 token
    echo "$url" | sed -E 's/.*\/(wiki|docx)\/([^/?]+).*/\2/'
}

# 获取文档内容
get_doc_content() {
    local token=$1
    local doc_token=$2
    
    curl -s "${FEISHU_API_BASE}/docx/v1/documents/${doc_token}" \
        -H "Authorization: Bearer $token" | \
        jq -r '.data.document.title'
}

# 更新文档（示例函数）
update_document() {
    local token=$1
    local doc_token=$2
    local content=$3
    
    # 实际实现需要调用飞书文档更新 API
    echo "更新文档: $doc_token"
}
