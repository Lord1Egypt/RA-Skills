#!/bin/bash
# Lota Football 未来24小时比赛特征抓取脚本
# 用于定时任务，获取未来24小时内所有比赛的特征数据
# 保存到 lota_data/matches/$date.json, lota_data/matches/live.json, lota_data/lota_compact_fet/$lota_id.json
# 限制访问频率：1秒2个请求

set -e

VERSION="1.1.0"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${LOTA_DATA_DIR:-$PARENT_DIR/lota_data}"
MATCHES_DIR="$DATA_DIR/matches"
COMPACT_FET_DIR="$DATA_DIR/lota_compact_fet"
METADATA_FILE="$DATA_DIR/fetch_metadata.json"
BASE_URL="${LOTA_API_BASE_URL:-http://deepdata.lota.tv/predictions/api/v2}"
API_KEY="${LOTA_API_KEY}"

# 更新频率配置（秒）
UPDATE_INTERVAL_JINGCAI=1800    # 30分钟
UPDATE_INTERVAL_BEIDAN=3600     # 1小时
UPDATE_INTERVAL_OTHER=5400      # 1.5小时

# 确保目录存在
mkdir -p "$DATA_DIR"
mkdir -p "$MATCHES_DIR"
mkdir -p "$COMPACT_FET_DIR"

show_usage() {
    cat <<EOF
Lota Football 未来24小时比赛特征抓取脚本 v${VERSION}

用法: $0 [选项]

选项:
  --force-update-all   强制更新所有比赛的特征（包括已开始的）
  --dry-run           只显示将要执行的操作，不实际抓取
  --help              显示帮助

环境变量:
  LOTA_API_KEY        API密钥（必需）
  LOTA_API_BASE_URL   API基础URL（可选）
  LOTA_DATA_DIR       数据目录路径（可选，默认在脚本同级目录的lota_data）

频率限制: 每秒最多2个请求（每个请求间隔至少0.5秒）
更新频率配置:
  - 竞彩比赛 (jingcai_number非空): 每30分钟更新
  - 北单比赛 (beidan_number非空): 每1小时更新
  - 其他比赛: 每1.5小时更新

脚本会:
1. 获取今天和明天的比赛列表
2. 保存比赛列表到 matches/YYYY-MM-DD.json
3. 筛选未来24小时未开始的比赛保存到 matches/live.json
4. 为每个未开始的比赛根据类型和上次更新时间获取特征报告并保存到 lota_compact_fet/\${lota_id}.json
   （如果已存在且比赛已开始，则跳过）

EOF
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 错误: $*" >&2
    exit 1
}

# 检查依赖
check_dependencies() {
    command -v curl &>/dev/null || error "curl未安装"
    command -v jq &>/dev/null || error "jq未安装，请安装jq以解析JSON"
    command -v bc &>/dev/null || error "bc未安装，请安装bc以进行数值计算"
    command -v awk &>/dev/null || error "awk未安装"
}

# 加载元数据
load_metadata() {
    if [[ -f "$METADATA_FILE" ]]; then
        cat "$METADATA_FILE"
    else
        echo '{}'
    fi
}

# 保存元数据
save_metadata() {
    local metadata="$1"
    echo "$metadata" | jq '.' > "$METADATA_FILE"
}

# 获取上次更新时间
get_last_update_time() {
    local metadata="$1"
    local lota_id="$2"

    echo "$metadata" | jq -r --arg id "$lota_id" '.[$id] // 0'
}

# 更新元数据中的时间戳
update_metadata_timestamp() {
    local metadata="$1"
    local lota_id="$2"
    local timestamp="$3"

    echo "$metadata" | jq --arg id "$lota_id" --arg ts "$timestamp" '.[$id] = ($ts | tonumber)'
}

# 发送API请求（带频率限制）
last_request_time=0
min_interval=0.5  # 秒

# 获取当前时间戳（秒，浮点）
get_current_timestamp() {
    if command -v python3 &>/dev/null; then
        python3 -c 'import time; print(time.time())'
    elif command -v python &>/dev/null; then
        python -c 'import time; print(time.time())'
    elif command -v perl &>/dev/null; then
        perl -MTime::HiRes -e 'print Time::HiRes::time(), "\n"'
    else
        # 回退到秒级精度
        date +%s
    fi
}

send_request_with_rate_limit() {
    local url="$1"
    local now
    now=$(get_current_timestamp)
    local elapsed
    elapsed=$(awk -v n="$now" -v l="$last_request_time" 'BEGIN { print n - l }')

    if awk -v e="$elapsed" -v m="$min_interval" 'BEGIN { exit (e < m) ? 0 : 1 }'; then
        local sleep_time
        sleep_time=$(awk -v e="$elapsed" -v m="$min_interval" 'BEGIN { print m - e }')
        sleep "$sleep_time"
    fi

    local curl_cmd=(curl -s --connect-timeout 30 --max-time 60)
    [[ -n "$API_KEY" ]] && curl_cmd+=(-H "X-API-Key: $API_KEY")

    local response
    response=$("${curl_cmd[@]}" "$url")
    last_request_time=$(get_current_timestamp)

    echo "$response"
}

# 获取比赛列表
fetch_matches() {
    local start_date="$1"
    local end_date="$2"

    log "获取比赛列表: $start_date 到 $end_date"

    local url="${BASE_URL}/matches/?start_date=${start_date}&end_date=${end_date}"
    local response
    response=$(send_request_with_rate_limit "$url")

    # 检查响应是否有效
    if ! echo "$response" | jq -e . &>/dev/null; then
        error "获取比赛列表失败或返回无效JSON: $response"
    fi

    echo "$response"
}

# 获取特征报告
fetch_compact_fet() {
    local lota_id="$1"

    log "获取特征报告: $lota_id"

    local url="${BASE_URL}/compact-fet/?lota_id=${lota_id}"
    local response
    response=$(send_request_with_rate_limit "$url")

    if ! echo "$response" | jq -e . &>/dev/null; then
        error "获取特征报告失败: $lota_id"
    fi

    echo "$response"
}

# 主函数
main() {
    local force_update_all=false
    local dry_run=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --force-update-all)
                force_update_all=true
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                echo "未知选项: $1" >&2
                show_usage
                exit 1
                ;;
        esac
    done

    if [[ -z "$API_KEY" ]]; then
        error "请设置环境变量 LOTA_API_KEY"
    fi

    check_dependencies

    # 计算日期范围（今天和明天）
    local today
    today=$(date +%Y-%m-%d)
    local tomorrow
    tomorrow=$(date -v+1d +%Y-%m-%d 2>/dev/null || date -d "tomorrow" +%Y-%m-%d)

    log "日期范围: $today 到 $tomorrow"

    # 获取比赛列表
    local matches_json
    matches_json=$(fetch_matches "$today" "$tomorrow")

    if [[ "$dry_run" == "true" ]]; then
        log "干运行模式，不保存数据"
        log "获取到比赛数量: $(echo "$matches_json" | jq '.data.matches | length')"
        echo "$matches_json" | jq .
        exit 0
    fi

    # 按日期保存比赛列表
    log "按日期保存比赛列表..."
    for date in "$today" "$tomorrow"; do
        local date_matches
        date_matches=$(echo "$matches_json" | jq --arg date "$date" '.data.matches | map(select(.match_time | split(" ")[0] == $date))')
        if [[ $(echo "$date_matches" | jq 'length') -gt 0 ]]; then
            echo "$date_matches" | jq '.' > "$MATCHES_DIR/$date.json"
            log "保存 $date 比赛列表: $(echo "$date_matches" | jq 'length') 场比赛"
        fi
    done

    # 筛选未来24小时内未开始的比赛（state == 1 表示未开始）
    local live_matches
    live_matches=$(echo "$matches_json" | jq '.data.matches | map(select(.state == 1))')
    if [[ $(echo "$live_matches" | jq 'length') -gt 0 ]]; then
        echo "$live_matches" | jq '.' > "$MATCHES_DIR/live.json"
        log "保存未来24小时未开始比赛: $(echo "$live_matches" | jq 'length') 场"
    else
        # 如果没有未开始的比赛，保存空数组
        echo '[]' > "$MATCHES_DIR/live.json"
        log "没有未来24小时未开始的比赛"
    fi

    # 处理每场比赛的特征报告
    local total_matches
    total_matches=$(echo "$matches_json" | jq '.data.matches | length')
    log "开始处理 $total_matches 场比赛的特征报告..."

    # 加载元数据
    local metadata
    metadata=$(load_metadata)
    local current_timestamp
    current_timestamp=$(get_current_timestamp)

    local updated_count=0
    local skipped_count=0

    for i in $(seq 0 $((total_matches - 1))); do
        local match
        match=$(echo "$matches_json" | jq ".data.matches[$i]")
        local lota_id
        lota_id=$(echo "$match" | jq -r '.lota_id')
        local state
        state=$(echo "$match" | jq -r '.state')
        local date
        date=$(echo "$match" | jq -r '.match_time | split(" ")[0]')
        local jingcai_number
        jingcai_number=$(echo "$match" | jq -r '.jingcai_number // empty')
        local beidan_number
        beidan_number=$(echo "$match" | jq -r '.beidan_number // empty')

        local compact_fet_file="$COMPACT_FET_DIR/$lota_id.json"

        # 判断是否需要更新
        local need_update=false
        if [[ "$force_update_all" == "true" ]]; then
            need_update=true
            log "强制更新: $lota_id"
        elif [[ ! -f "$compact_fet_file" ]]; then
            need_update=true
            log "特征文件不存在: $lota_id"
        elif [[ "$state" != "1" ]]; then
            # 比赛已开始或结束，不需要更新
            need_update=false
            log "跳过已开始/结束的比赛: $lota_id (状态: $state)"
        else
            # 比赛未开始，根据类型和上次更新时间判断
            local last_update
            last_update=$(get_last_update_time "$metadata" "$lota_id")

            # 确定更新间隔
            local update_interval=$UPDATE_INTERVAL_OTHER
            local match_type="其他"
            if [[ -n "$jingcai_number" ]] && [[ "$jingcai_number" != "null" ]]; then
                update_interval=$UPDATE_INTERVAL_JINGCAI
                match_type="竞彩"
            elif [[ -n "$beidan_number" ]] && [[ "$beidan_number" != "null" ]]; then
                update_interval=$UPDATE_INTERVAL_BEIDAN
                match_type="北单"
            fi

            local time_since_last_update
            time_since_last_update=$(awk -v current="$current_timestamp" -v last="$last_update" 'BEGIN { print current - last }')

            if (( $(echo "$time_since_last_update > $update_interval" | bc -l) )); then
                need_update=true
                log "需要更新: $lota_id (类型: $match_type, 距离上次更新: ${time_since_last_update%.*}秒 > $update_interval秒)"
            else
                need_update=false
                log "跳过更新: $lota_id (类型: $match_type, 距离上次更新: ${time_since_last_update%.*}秒 <= $update_interval秒)"
            fi
        fi

        if [[ "$need_update" == "true" ]]; then
            log "更新特征报告: $lota_id (状态: $state, 日期: $date)"
            local compact_json
            compact_json=$(fetch_compact_fet "$lota_id")
            echo "$compact_json" | jq '.' > "$compact_fet_file"

            # 更新元数据
            metadata=$(update_metadata_timestamp "$metadata" "$lota_id" "$current_timestamp")

            updated_count=$((updated_count + 1))
        else
            skipped_count=$((skipped_count + 1))
        fi
    done

    # 保存元数据
    save_metadata "$metadata"

    log "处理完成: 更新 $updated_count 场, 跳过 $skipped_count 场"
}

main "$@"