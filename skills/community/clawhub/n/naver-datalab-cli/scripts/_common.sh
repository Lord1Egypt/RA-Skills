#!/usr/bin/env bash
# _common.sh — shared helpers for naver-datalab-cli.
# Source this from each subcommand: `. "$here/_common.sh"`

set -euo pipefail

NAVER_DATALAB_BASE="${NAVER_DATALAB_BASE:-https://openapi.naver.com/v1/datalab}"

require_bin() {
  for b in "$@"; do
    command -v "$b" >/dev/null 2>&1 || { echo "error: $b is required but not installed." >&2; exit 127; }
  done
}

require_keys() {
  if [[ -z "${NAVER_CLIENT_ID:-}" || -z "${NAVER_CLIENT_SECRET:-}" ]]; then
    cat >&2 <<'EOF'
error: NAVER_CLIENT_ID and NAVER_CLIENT_SECRET must be set.
Register an app at https://developers.naver.com/apps/#/register
and enable both 검색어트렌드 + 쇼핑인사이트.
EOF
    exit 78
  fi
}

# valid_date <YYYY-MM-DD> — exit 0 if shape matches; else exit 64.
valid_date() {
  if ! [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "error: date '$1' is not in YYYY-MM-DD format." >&2
    exit 64
  fi
}

# valid_time_unit <date|week|month>
valid_time_unit() {
  case "$1" in
    date|week|month) ;;
    *) echo "error: time-unit must be one of: date, week, month (got '$1')." >&2; exit 64;;
  esac
}

# datalab_post <path> <json-body>
# Posts to https://openapi.naver.com/v1/datalab/<path>, returns body on stdout.
# Non-2xx responses are emitted to stderr and trigger exit 22.
datalab_post() {
  local path="$1"; shift
  local body="$1"; shift

  local out http
  out=$(mktemp)
  http=$(curl -sS -o "$out" -w '%{http_code}' \
    -X POST "${NAVER_DATALAB_BASE}/${path}" \
    -H "X-Naver-Client-Id: ${NAVER_CLIENT_ID}" \
    -H "X-Naver-Client-Secret: ${NAVER_CLIENT_SECRET}" \
    -H "Content-Type: application/json; charset=utf-8" \
    --data "$body" || true)

  if [[ "$http" != 2* ]]; then
    echo "error: NAVER DataLab returned HTTP $http for /${path}" >&2
    sed -e 's/^/  /' "$out" >&2
    rm -f "$out"
    exit 22
  fi

  cat "$out"
  rm -f "$out"
}

# parse_groups <"label:kw1,kw2"...>  -> JSON array of {groupName, keywords[]}
# Returns JSON array on stdout. Each --group flag value is "label:csv".
# Used by search.sh.
parse_groups_to_json() {
  local groups_json="[]"
  for raw in "$@"; do
    [[ -z "$raw" ]] && continue
    local label kws_csv
    label="${raw%%:*}"
    kws_csv="${raw#*:}"
    if [[ "$label" == "$raw" || -z "$kws_csv" ]]; then
      echo "error: group '$raw' must be 'label:keyword1,keyword2,...'" >&2
      exit 64
    fi
    local kws_json
    kws_json=$(printf '%s' "$kws_csv" | jq -Rcn 'inputs | split(",") | map(gsub("^\\s+|\\s+$"; ""))')
    groups_json=$(jq -nc --argjson cur "$groups_json" --arg name "$label" --argjson kws "$kws_json" \
      '$cur + [{groupName:$name, keywords:$kws}]')
  done
  echo "$groups_json"
}

# parse_categories_to_json <"label:50000000"...>  -> JSON array of {name, param[]}
# Used by shop-cat.sh. Param is wrapped to a 1-elem array as the API expects.
parse_categories_to_json() {
  local cats_json="[]"
  for raw in "$@"; do
    [[ -z "$raw" ]] && continue
    local label code
    label="${raw%%:*}"
    code="${raw#*:}"
    if [[ "$label" == "$raw" || -z "$code" ]]; then
      echo "error: category '$raw' must be 'label:code'" >&2
      exit 64
    fi
    cats_json=$(jq -nc --argjson cur "$cats_json" --arg name "$label" --arg code "$code" \
      '$cur + [{name:$name, param:[$code]}]')
  done
  echo "$cats_json"
}

# parse_keywords_to_json <"label:kw1,kw2"...>  -> JSON array of {name, param[]}
# Used by shop-keyword.sh. Same shape as groups but field name is "name" + "param".
parse_keywords_to_json() {
  local kws_json="[]"
  for raw in "$@"; do
    [[ -z "$raw" ]] && continue
    local label kws_csv
    label="${raw%%:*}"
    kws_csv="${raw#*:}"
    if [[ "$label" == "$raw" || -z "$kws_csv" ]]; then
      echo "error: keyword '$raw' must be 'label:kw1,kw2,...'" >&2
      exit 64
    fi
    local arr
    arr=$(printf '%s' "$kws_csv" | jq -Rcn 'inputs | split(",") | map(gsub("^\\s+|\\s+$"; ""))')
    kws_json=$(jq -nc --argjson cur "$kws_json" --arg name "$label" --argjson arr "$arr" \
      '$cur + [{name:$name, param:$arr}]')
  done
  echo "$kws_json"
}

# Add optional demo filters (device/gender/ages) to a request body.
# Usage: add_filters <body-json> <device> <gender> <ages-csv>  (each may be empty)
add_filters() {
  local body="$1" device="${2:-}" gender="${3:-}" ages_csv="${4:-}"
  if [[ -n "$device" ]]; then
    body=$(jq -nc --argjson b "$body" --arg d "$device" '$b + {device:$d}')
  fi
  if [[ -n "$gender" ]]; then
    body=$(jq -nc --argjson b "$body" --arg g "$gender" '$b + {gender:$g}')
  fi
  if [[ -n "$ages_csv" ]]; then
    local arr
    arr=$(printf '%s' "$ages_csv" | jq -Rcn 'inputs | split(",") | map(gsub("^\\s+|\\s+$"; ""))')
    body=$(jq -nc --argjson b "$body" --argjson a "$arr" '$b + {ages:$a}')
  fi
  echo "$body"
}
