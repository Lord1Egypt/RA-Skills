#!/usr/bin/env bash
# fetch-platform-data.sh — 多平台运营数据采集脚本
# 依赖：bash, curl, jq, python3
# 配置：从 .env 文件读取 API 密钥

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/../data/raw"
ENV_FILE="${SCRIPT_DIR}/../.env"

# 加载环境变量
if [[ -f "$ENV_FILE" ]]; then
  set -a
  source "$ENV_FILE"
  set +a
else
  echo "[WARN] .env 文件不存在，请先创建并配置 API 密钥"
fi

mkdir -p "$DATA_DIR"

TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d yesterday +%Y-%m-%d)

# ---- 工具函数 ----

log() { echo "[$(date '+%H:%M:%S')] $*"; }
save_data() {
  local platform="$1" date="$2" data="$3"
  echo "$data" > "${DATA_DIR}/${platform}_${date}.json"
  log "已保存 ${platform} 数据 → ${DATA_DIR}/${platform}_${date}.json"
}

# ---- 抖音 ----

fetch_douyin() {
  local account_id="${1:-${DOUYIN_OPEN_ID:-}}"
  local target_date="${2:-$YESTERDAY}"
  log "采集抖音数据 (account: $account_id, date: $target_date)..."

  if [[ -z "${DOUYIN_ACCESS_TOKEN:-}" ]]; then
    echo '{"error":"DOUYIN_ACCESS_TOKEN 未配置","platform":"douyin","date":"'"$target_date"'"}' | save_data douyin "$target_date" "$(cat)"
    return 1
  fi

  local response
  response=$(curl -sf "https://open.douyin.com/data/external/user/fans/data/" \
    -H "access-token: ${DOUYIN_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"open_id\":\"${account_id}\",\"date_type\":1}" \
    --retry 3 --retry-delay 2 || echo '{"error":"API调用失败"}')

  # 标准化字段
  local normalized
  normalized=$(echo "$response" | python3 -c "
import json, sys
raw = json.load(sys.stdin)
data = raw.get('data', {})
print(json.dumps({
  'platform': 'douyin',
  'date': '${target_date}',
  'views': data.get('play_count', 0),
  'likes': data.get('digg_count', 0),
  'comments': data.get('comment_count', 0),
  'shares': data.get('share_count', 0),
  'favorites': data.get('collect_count', 0),
  'new_followers': data.get('new_fans', 0),
  'total_followers': data.get('total_fans', 0),
  'completion_rate': data.get('play_over_rate', 0),
  'raw': raw
}, ensure_ascii=False))
" 2>/dev/null || echo '{"error":"数据解析失败","platform":"douyin","date":"'"$target_date"'"}')

  save_data "douyin" "$target_date" "$normalized"
}

# ---- 小红书 ----

fetch_xiaohongshu() {
  local target_date="${1:-$YESTERDAY}"
  log "采集小红书数据 (date: $target_date)..."

  if [[ -z "${XIAOHONGSHU_COOKIE:-}" ]]; then
    echo '{"error":"XIAOHONGSHU_COOKIE 未配置","platform":"xiaohongshu","date":"'"$target_date"'"}' > "${DATA_DIR}/xiaohongshu_${target_date}.json"
    return 1
  fi

  local response
  response=$(curl -sf "https://creator.xiaohongshu.com/api/galaxy/creator/data/note_stats" \
    -H "Cookie: ${XIAOHONGSHU_COOKIE}" \
    -H "Content-Type: application/json" \
    -d "{\"start_date\":\"${target_date}\",\"end_date\":\"${target_date}\"}" \
    --retry 3 --retry-delay 2 || echo '{"error":"API调用失败"}')

  local normalized
  normalized=$(echo "$response" | python3 -c "
import json, sys
raw = json.load(sys.stdin)
data = raw.get('data', {})
print(json.dumps({
  'platform': 'xiaohongshu',
  'date': '${target_date}',
  'views': data.get('view_count', 0),
  'likes': data.get('liked_count', 0),
  'comments': data.get('comment_count', 0),
  'shares': data.get('share_count', 0),
  'favorites': data.get('collected_count', 0),
  'new_followers': data.get('fans_count_delta', 0),
  'total_followers': data.get('fans_count', 0),
  'raw': raw
}, ensure_ascii=False))
" 2>/dev/null || echo '{"error":"数据解析失败","platform":"xiaohongshu","date":"'"$target_date"'"}')

  save_data "xiaohongshu" "$target_date" "$normalized"
}

# ---- 视频号 ----

fetch_shipinhao() {
  local target_date="${1:-$YESTERDAY}"
  log "采集视频号数据 (date: $target_date)..."

  if [[ -z "${WEIXIN_CORP_ID:-}" ]] || [[ -z "${WEIXIN_CORP_SECRET:-}" ]]; then
    echo '{"error":"WEIXIN_CORP_ID 或 WEIXIN_CORP_SECRET 未配置","platform":"shipinhao","date":"'"$target_date"'"}' > "${DATA_DIR}/shipinhao_${target_date}.json"
    return 1
  fi

  # 获取 access_token
  local token_resp
  token_resp=$(curl -sf "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${WEIXIN_CORP_ID}&corpsecret=${WEIXIN_CORP_SECRET}" || echo '{}')
  local access_token
  access_token=$(echo "$token_resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")

  if [[ -z "$access_token" ]]; then
    echo '{"error":"获取视频号 access_token 失败","platform":"shipinhao","date":"'"$target_date"'"}' > "${DATA_DIR}/shipinhao_${target_date}.json"
    return 1
  fi

  local response
  response=$(curl -sf "https://api.weixin.qq.com/datacube/getweanalysisappiddailysummarytrend?access_token=${access_token}" \
    -H "Content-Type: application/json" \
    -d "{\"begin_date\":\"$(echo $target_date | tr -d -)\",\"end_date\":\"$(echo $target_date | tr -d -)\"}" \
    --retry 3 --retry-delay 2 || echo '{"error":"API调用失败"}')

  save_data "shipinhao" "$target_date" "$response"
}

# ---- 并行采集所有平台 ----

fetch_all() {
  local target_date="${1:-$YESTERDAY}"
  log "并行采集所有平台数据 (date: $target_date)..."

  fetch_douyin "" "$target_date" &
  fetch_xiaohongshu "$target_date" &
  fetch_shipinhao "$target_date" &

  wait
  log "所有平台数据采集完成"
}

# ---- 入口 ----

COMMAND="${1:-help}"
shift || true

case "$COMMAND" in
  fetch)
    PLATFORM="${1:-all}"
    shift || true
    case "$PLATFORM" in
      douyin)      fetch_douyin "$@" ;;
      xiaohongshu) fetch_xiaohongshu "$@" ;;
      shipinhao)   fetch_shipinhao "$@" ;;
      all)         fetch_all "$@" ;;
      *)           echo "未知平台: $PLATFORM"; exit 1 ;;
    esac
    ;;
  help|*)
    echo "用法: $0 fetch <platform|all> [account_id] [date]"
    echo "平台: douyin | xiaohongshu | shipinhao | all"
    echo "示例:"
    echo "  $0 fetch douyin 123456789"
    echo "  $0 fetch all"
    echo "  $0 fetch douyin 123456789 2026-03-31"
    ;;
esac
