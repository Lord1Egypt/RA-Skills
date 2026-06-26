#!/usr/bin/env bash
# glm-search — Search the web via Zhipu GLM
# Supports two modes:
#   1. cURL mode (preferred) — only requires curl + ZHIPU_API_KEY env var
#   2. MCP mode (advanced) — requires mcporter + setup.sh
#
# Usage: glm-search [options] <query>
#   -q, --query TEXT     Search text (required)
#   -c, --count N        Number of results 1-50 (default: 10)
#   -e, --engine NAME    Engine: pro|sogou|quark|std (default: pro)
#   -r, --recency FILTER noLimit|oneYear|oneMonth|oneWeek|oneDay (default: noLimit)
#   -s, --size SIZE      medium|high (default: medium)
#   -i, --intent         Enable search intent recognition (cURL mode only)
#   -d, --domain DOMAIN  Restrict to specific domain
#   --curl               Force cURL mode (skip mcporter)
#   --mcp                Force MCP mode (skip cURL fallback)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
MCP_CONFIG="${HOME}/.openclaw/config/mcporter/mcporter.json"

# Defaults
QUERY=""
COUNT=10
ENGINE="pro"
RECENCY="noLimit"
CONTENT_SIZE="medium"
INTENT=false
DOMAIN=""
FORCE_MODE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -q|--query) QUERY="$2"; shift 2 ;;
    -c|--count) COUNT="$2"; shift 2 ;;
    -e|--engine) ENGINE="$2"; shift 2 ;;
    -r|--recency) RECENCY="$2"; shift 2 ;;
    -s|--size) CONTENT_SIZE="$2"; shift 2 ;;
    -i|--intent) INTENT=true; shift ;;
    -d|--domain) DOMAIN="$2"; shift 2 ;;
    --curl) FORCE_MODE="curl"; shift ;;
    --mcp) FORCE_MODE="mcp"; shift ;;
    *) QUERY="$1"; shift ;;
  esac
done

if [ -z "$QUERY" ]; then
  echo "Usage: glm-search [options] <query>" >&2
  echo "  -q, --query TEXT   Search text (required)" >&2
  echo "  -c, --count N      Results 1-50 (default: 10)" >&2
  echo "  -e, --engine NAME  pro|sogou|quark|std (default: pro)" >&2
  echo "  -r, --recency F    noLimit|oneYear|oneMonth|oneWeek|oneDay" >&2
  echo "  -s, --size SIZE    medium|high" >&2
  echo "  -i, --intent       Enable intent recognition (cURL mode)" >&2
  echo "  -d, --domain D     Restrict to domain" >&2
  echo "  --curl             Force cURL mode" >&2
  echo "  --mcp              Force MCP mode" >&2
  exit 2
fi

# Engine mapping for MCP tool names
declare -A MCP_ENGINES=(
  [pro]="webSearchPro"
  [sogou]="webSearchSogou"
  [quark]="webSearchQuark"
  [std]="webSearchStd"
)

# Engine mapping for REST API engine names
declare -A REST_ENGINES=(
  [pro]="search_pro"
  [sogou]="search_pro_sogou"
  [quark]="search_pro_quark"
  [std]="search_std"
)

MCP_TOOL="${MCP_ENGINES[$ENGINE]:-webSearchPro}"
REST_ENGINE="${REST_ENGINES[$ENGINE]:-search_pro}"

# Build JSON payload for cURL (safe: all values passed via environment, no variable interpolation in code)
build_payload() {
  export _GLM_QUERY="$QUERY"
  export _GLM_ENGINE="$REST_ENGINE"
  export _GLM_INTENT="$INTENT"
  export _GLM_COUNT="$COUNT"
  export _GLM_RECENCY="$RECENCY"
  export _GLM_SIZE="$CONTENT_SIZE"
  export _GLM_DOMAIN="$DOMAIN"
  python3 << 'PYEOF'
import json, os
payload = {
    "search_query": os.environ["_GLM_QUERY"],
    "search_engine": os.environ["_GLM_ENGINE"],
    "search_intent": os.environ["_GLM_INTENT"].lower() == "true",
    "count": int(os.environ["_GLM_COUNT"]),
    "search_recency_filter": os.environ["_GLM_RECENCY"],
    "content_size": os.environ["_GLM_SIZE"]
}
domain = os.environ.get("_GLM_DOMAIN", "")
if domain:
    payload["search_domain_filter"] = domain
print(json.dumps(payload))
PYEOF
}

# MCP mode via mcporter
search_mcp() {
  if [ ! -f "$MCP_CONFIG" ]; then
    echo "Error: mcporter config not found at $MCP_CONFIG" >&2
    echo "Run setup first: bash ${SKILL_DIR}/scripts/setup.sh" >&2
    return 1
  fi

  if ! command -v mcporter &>/dev/null && ! command -v npx &>/dev/null; then
    echo "Error: mcporter/npx not found." >&2
    echo "Install: npm i -g mcporter" >&2
    return 1
  fi

  local extra_args=()
  [ -n "$DOMAIN" ] && extra_args+=("search_domain_filter=$DOMAIN")

  exec npx -y mcporter --config "$MCP_CONFIG" call "glm-search.${MCP_TOOL}" \
    search_query="$QUERY" \
    count="$COUNT" \
    search_recency_filter="$RECENCY" \
    content_size="$CONTENT_SIZE" \
    "${extra_args[@]+"${extra_args[@]}"}"
}

# cURL mode via REST API
search_curl() {
  if [ -z "${ZHIPU_API_KEY:-}" ]; then
    echo "Error: ZHIPU_API_KEY environment variable not set." >&2
    echo "Set it with: export ZHIPU_API_KEY=\"your-api-key\"" >&2
    return 1
  fi

  local payload
  payload=$(build_payload)

  curl --silent --show-error --request POST \
    --url "https://open.bigmodel.cn/api/paas/v4/web_search" \
    --header "Authorization: Bearer ${ZHIPU_API_KEY}" \
    --header "Content-Type: application/json" \
    --data "$payload"
}

# Auto-select mode: prefer cURL (simpler, no extra deps), fallback to MCP
if [ "$FORCE_MODE" = "mcp" ]; then
  search_mcp
elif [ "$FORCE_MODE" = "curl" ]; then
  search_curl
elif [ -n "${ZHIPU_API_KEY:-}" ] && command -v curl &>/dev/null; then
  search_curl
elif [ -f "$MCP_CONFIG" ]; then
  search_mcp
else
  echo "Error: No usable search backend found." >&2
  echo "Set ZHIPU_API_KEY for cURL mode, or run setup.sh for MCP mode." >&2
  exit 1
fi
