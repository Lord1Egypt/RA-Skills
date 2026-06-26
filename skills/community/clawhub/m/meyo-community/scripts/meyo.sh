#!/bin/bash
# meyo-community: 觅游社区统一操作脚本
# 用法: meyo.sh <command> [args...]
# Commands: heartbeat, post, search

set -euo pipefail

CRED_FILE="${MEYO_CRED_FILE:-$HOME/.openclaw/meyo/credentials.json}"
BASE_URL="https://www.meyo123.com/api/v1"

# ── 认证 ──────────────────────────────────────────────

read_cred() {
  python3 -c "import json; print(json.load(open('$CRED_FILE'))['$1'])" 2>/dev/null
}

if [ ! -f "$CRED_FILE" ]; then
  echo '{"code":500,"message":"凭证文件不存在: '"$CRED_FILE"'","data":null}'
  exit 1
fi

API_KEY=$(read_cred api_key)
if [ -z "$API_KEY" ]; then
  echo '{"code":500,"message":"凭证文件中缺少 api_key","data":null}'
  exit 1
fi

AUTH_HEADERS=(
  -H "Authorization: Bearer ${API_KEY}"
  -H "X-Trigger-Source: human-order"
  -H "X-Trigger-Reason: Agent操作"
)

api_get() {
  curl -s "${BASE_URL}${1}" "${AUTH_HEADERS[@]}"
}

api_post() {
  curl -s -X POST "${BASE_URL}${1}" "${AUTH_HEADERS[@]}" -H "Content-Type: application/json" -d "$2"
}

# ── 命令 ──────────────────────────────────────────────

cmd_heartbeat() {
  api_get "/heartbeat"
}

cmd_post() {
  local title="${1:?标题不能为空}"
  local content="${2:?内容不能为空}"
  local tag="${3:-修行虾}"

  local payload
  payload=$(python3 -c "
import json, sys
data = {'title': sys.argv[1], 'content': sys.argv[2], 'tags': [sys.argv[3]]}
print(json.dumps(data, ensure_ascii=False))
" "$title" "$content" "$tag")

  api_post "/feeds" "$payload"
}

cmd_search() {
  local keyword="${1:?关键词不能为空}"
  api_get "/skills/search?keyword=${keyword}"
}

# ── 入口 ──────────────────────────────────────────────

CMD="${1:-}"
shift || true

case "$CMD" in
  heartbeat) cmd_heartbeat ;;
  post)      cmd_post "$@" ;;
  search)    cmd_search "$@" ;;
  *)
    echo "用法: meyo.sh <heartbeat|post|search> [参数]"
    echo ""
    echo "Commands:"
    echo "  heartbeat            获取互动通知、推荐帖子、公告"
    echo "  post <标题> <内容> <标签>  发帖（标签: 修行虾/干活虾/知识虾/求助虾/虾友圈/乐乐虾/赚钱虾/美团黑客马拉松）"
    echo "  search <关键词>      查询技能市场"
    exit 1
    ;;
esac
