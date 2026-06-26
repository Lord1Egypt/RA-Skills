#!/bin/bash
# hope-client API 快捷调用脚本
# 用于发起对 Hope Server Max 的 API 请求

# 从环境变量读取配置（OpenClaw skills.entries.hope-client.env）
HOPE_HOST="${HOPE_HOST:-hope05}"
HOPE_PORT="${HOPE_PORT:-8088}"
HOPE_KEY="${HOPE_API_KEY:-hope-openclaw-apikey-2026-0411}"
SSH_PASS="${HOPE_SSH_PASS:-hope}"

# 如果环境变量未设置，提示用户
if [[ -z "$HOPE_API_KEY" ]]; then
    echo "⚠️  HOPE_API_KEY 环境变量未设置，使用默认值"
fi

# 基础调用函数
hope_api() {
    local endpoint="$1"
    local params="${2:-}"
    local method="${3:-GET}"
    local data="${4:-}"
    
    if [[ "$method" == "GET" ]]; then
        sshpass -p "$SSH_PASS" ssh "$HOPE_HOST" \
            "curl -s -H 'X-OpenClaw-Key: $HOPE_KEY' \
             'http://127.0.0.1:$HOPE_PORT${endpoint}?${params}'"
    else
        sshpass -p "$SSH_PASS" ssh "$HOPE_HOST" \
            "curl -s -X $method -H 'X-OpenClaw-Key: $HOPE_KEY' \
             -H 'Content-Type: application/json' \
             'http://127.0.0.1:$HOPE_PORT${endpoint}' \
             -d '${data}'"
    fi
}

# ============== 频道管理 ==============

# 查询频道列表
hope_channel_list() {
    local pageSize="${1:-100}"
    hope_api "/system/channel/list" "pageSize=$pageSize"
}

# 获取所有频道名称
hope_channel_names() {
    hope_api "/system/channel/listAllNames"
}

# 搜索频道名称
hope_channel_search() {
    local name="$1"
    hope_api "/system/channel/searchNames" "channelName=$name"
}

# 获取频道详情
hope_channel_info() {
    local channelId="$1"
    hope_api "/system/channel/$channelId"
}

# 频道统计
hope_channel_stats() {
    hope_api "/system/channel/statistics"
}

# 刷新频道 Cookie
hope_channel_refresh() {
    local channelId="$1"
    hope_api "/system/channel/refresh/$channelId" "" "POST"
}

# ============== 上传实例 ==============

# 查询上传实例列表
hope_upload_list() {
    local params="${1:-pageSize=50}"
    hope_api "/system/instance/list" "$params"
}

# 查询上传实例详情
hope_upload_info() {
    local instanceId="$1"
    hope_api "/system/instance/$instanceId"
}

# 查询上传趋势
hope_upload_trend() {
    local params="${1:-}"
    hope_api "/system/instance/queryTrend" "$params"
}

# 查询失败列表
hope_upload_fail_list() {
    local params="${1:-pageSize=50}"
    hope_api "/system/instance/failList" "$params"
}

# 查询失败日志
hope_upload_fail_log() {
    local engine="$1"
    local path="$2"
    hope_api "/system/instance/queryFailLog" "" "POST" \
        "{\"engineName\":\"$engine\",\"videoPath\":\"$path\"}"
}

# ============== 下载实例 ==============

# 查询下载实例列表
hope_download_list() {
    local params="${1:-pageSize=50}"
    hope_api "/system/downloadInstance/list" "$params"
}

# 查询下载实例详情
hope_download_info() {
    local pkInstanceId="$1"
    hope_api "/system/downloadInstance/$pkInstanceId"
}

# 查询待上传视频列表
hope_pending_list() {
    local limit="${1:-20}"
    local downloadId="${2:-}"
    local params="limit=$limit"
    [[ -n "$downloadId" ]] && params="$params&downloadId=$downloadId"
    hope_api "/system/downloadInstance/pending" "$params"
}

# 统计待上传视频数量
hope_pending_count() {
    local downloadId="${1:-}"
    local params=""
    [[ -n "$downloadId" ]] && params="downloadId=$downloadId"
    hope_api "/system/downloadInstance/pending/count" "$params"
}

# 查询下载趋势
hope_download_trend() {
    local params="${1:-}"
    hope_api "/system/downloadInstance/trend" "$params"
}

# 更新清理状态
hope_download_clean() {
    local pkInstanceIds="$1"
    hope_api "/system/downloadInstance/clean/$pkInstanceIds" "" "PUT"
}

# ============== 账户管理 ==============

# 查询账户列表
hope_account_list() {
    local params="${1:-pageSize=50}"
    hope_api "/system/account/list" "$params"
}

# 获取账户详情
hope_account_info() {
    local accId="$1"
    hope_api "/system/account/$accId"
}

# ============== 引擎管理 ==============

# 查询引擎列表
hope_engine_list() {
    hope_api "/system/engineInfo/list"
}

# 获取所有引擎信息
hope_engine_all() {
    hope_api "/system/engineInfo/listAll"
}

# 获取引擎详情
hope_engine_info() {
    local engineId="$1"
    hope_api "/system/engineInfo/$engineId"
}

# ============== 快捷查询 ==============

# 查询今日上传统计
hope_today_upload() {
    local today=$(date +%Y-%m-%d)
    hope_upload_list "createTime=$today&pageSize=100"
}

# 查询今日下载统计
hope_today_download() {
    local today=$(date +%Y-%m-%d)
    hope_download_list "createTime=$today&pageSize=100"
}

# 查询失败的上传任务
hope_failed_uploads() {
    hope_upload_list "status=1&pageSize=100"
}

# 查询执行中的上传任务
hope_running_uploads() {
    hope_upload_list "status=2&pageSize=100"
}

# 查询排队的上传任务
hope_queued_uploads() {
    hope_upload_list "status=3&pageSize=100"
}

# ============== 帮助 ==============

hope_help() {
    echo "Hope Server Max API Client"
    echo ""
    echo "频道管理:"
    echo "  hope_channel_list [pageSize]      - 查询频道列表"
    echo "  hope_channel_names                - 获取所有频道名称"
    echo "  hope_channel_search <name>        - 搜索频道名称"
    echo "  hope_channel_info <channelId>     - 获取频道详情"
    echo "  hope_channel_stats                - 频道统计"
    echo "  hope_channel_refresh <channelId>  - 刷新频道 Cookie"
    echo ""
    echo "上传实例:"
    echo "  hope_upload_list [params]         - 查询上传列表"
    echo "  hope_upload_info <instanceId>     - 获取上传详情"
    echo "  hope_upload_trend [params]        - 查询上传趋势"
    echo "  hope_upload_fail_list [params]    - 查询失败列表"
    echo ""
    echo "下载实例:"
    echo "  hope_download_list [params]       - 查询下载列表"
    echo "  hope_download_info <pkInstanceId> - 获取下载详情"
    echo "  hope_pending_list [limit]         - 查询待上传视频"
    echo "  hope_pending_count                - 统计待上传数量"
    echo ""
    echo "账户管理:"
    echo "  hope_account_list [params]        - 查询账户列表"
    echo "  hope_account_info <accId>         - 获取账户详情"
    echo ""
    echo "引擎管理:"
    echo "  hope_engine_list                  - 查询引擎列表"
    echo "  hope_engine_all                   - 获取所有引擎"
    echo ""
    echo "快捷查询:"
    echo "  hope_today_upload                 - 今日上传统计"
    echo "  hope_today_download               - 今日下载统计"
    echo "  hope_failed_uploads               - 失败的上传任务"
    echo "  hope_running_uploads              - 执行中的上传任务"
    echo "  hope_queued_uploads               - 排队的上传任务"
}

# 如果直接运行脚本，显示帮助
if [[ $# -eq 0 ]]; then
    hope_help
fi