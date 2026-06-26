#!/usr/bin/env bash
# Shared helpers for mfds-cli subcommands.
# Source this from each subcommand: . "$(dirname "$0")/_mfds_common.sh"
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mfds_require_key() {
  if [[ -z "${KEY:-}" ]]; then
    KEY="${MFDS_API_KEY:-}"
  fi
  if [[ -z "$KEY" ]]; then
    echo "mfds-cli: missing API key — set MFDS_API_KEY or pass --key <KEY>" >&2
    echo "  Register at https://www.data.go.kr and copy the *decoded* serviceKey." >&2
    exit 78
  fi
}

# URL-encode a single value using python3 (always available on macOS / Linux).
mfds_urlencode() {
  python3 -c 'import sys, urllib.parse as u; print(u.quote(sys.argv[1], safe=""))' "$1"
}

# Build a query string from KEY=VALUE pairs passed as args. Empty values are skipped.
mfds_qs() {
  local out=""
  while (( "$#" )); do
    local kv="$1"; shift
    local k="${kv%%=*}"
    local v="${kv#*=}"
    [[ -z "$v" ]] && continue
    [[ -n "$out" ]] && out+="&"
    out+="${k}=$(mfds_urlencode "$v")"
  done
  printf '%s' "$out"
}

# Issue an HTTP GET and emit either raw output or normalized JSONL.
# Args: <endpoint-url> <query-string> <record-type> <root-xpath-or-jsonpath>
mfds_request() {
  local url="$1"
  local qs="$2"
  local record_type="${3:-record}"
  local fmt="${FORMAT:-jsonl}"

  local body
  body="$(curl -fsSL --max-time 30 "${url}?${qs}")" || {
    echo "mfds-cli: request failed for $url" >&2
    exit 1
  }

  if [[ "${RAW:-0}" == "1" ]]; then
    printf '%s\n' "$body"
    return
  fi

  case "$fmt" in
    xml)
      printf '%s\n' "$body"
      ;;
    json)
      python3 "$DIR/_normalize.py" --type "$record_type" --output json <<< "$body"
      ;;
    jsonl|*)
      python3 "$DIR/_normalize.py" --type "$record_type" --output jsonl <<< "$body"
      ;;
  esac
}

# Default-arg parser used by every subcommand. Subcommands set the array
# `EXTRA_ARGS` (positional) and look up flags via `$NAME`, `$MAKER`, etc.
# The parser populates: KEY, ROWS, PAGE, FORMAT, RAW, ENDPOINT,
# NAME, MAKER, ITEM_SEQ, INGREDIENT, TYPE_NAME, YEAR, ACTION, BIZRNO,
# TYPE_CODE, CANCEL_NAME, DUR_TYPE,
# QUERY_EFFICACY, QUERY_METHOD, QUERY_WARNING, QUERY_SIDE_EFFECT, QUERY_STORAGE.
mfds_parse_args() {
  KEY=""; ROWS="30"; PAGE="1"; FORMAT="jsonl"; RAW="0"; ENDPOINT=""
  NAME=""; MAKER=""; ITEM_SEQ=""; INGREDIENT=""; TYPE_NAME=""
  YEAR=""; ACTION=""; BIZRNO=""; TYPE_CODE=""; CANCEL_NAME=""
  DUR_TYPE="interaction"
  QUERY_EFFICACY=""; QUERY_METHOD=""; QUERY_WARNING=""; QUERY_SIDE_EFFECT=""; QUERY_STORAGE=""
  EXTRA_ARGS=()

  while (( "$#" )); do
    case "$1" in
      --key)              KEY="$2"; shift 2 ;;
      --rows)             ROWS="$2"; shift 2 ;;
      --page)             PAGE="$2"; shift 2 ;;
      --format)           FORMAT="$2"; shift 2 ;;
      --raw)              RAW="1"; shift ;;
      --endpoint)         ENDPOINT="$2"; shift 2 ;;
      --name)             NAME="$2"; shift 2 ;;
      --maker)            MAKER="$2"; shift 2 ;;
      --item-seq)         ITEM_SEQ="$2"; shift 2 ;;
      --ingredient)       INGREDIENT="$2"; shift 2 ;;
      --type)             DUR_TYPE="$2"; shift 2 ;;
      --type-name)        TYPE_NAME="$2"; shift 2 ;;
      --type-code)        TYPE_CODE="$2"; shift 2 ;;
      --year)             YEAR="$2"; shift 2 ;;
      --action)           ACTION="$2"; shift 2 ;;
      --bizrno)           BIZRNO="$2"; shift 2 ;;
      --cancel-name)      CANCEL_NAME="$2"; shift 2 ;;
      --query-efficacy)   QUERY_EFFICACY="$2"; shift 2 ;;
      --query-method)     QUERY_METHOD="$2"; shift 2 ;;
      --query-warning)    QUERY_WARNING="$2"; shift 2 ;;
      --query-side-effect) QUERY_SIDE_EFFECT="$2"; shift 2 ;;
      --query-storage)    QUERY_STORAGE="$2"; shift 2 ;;
      -h|--help)          HELP=1; shift ;;
      *)                  EXTRA_ARGS+=("$1"); shift ;;
    esac
  done

  export KEY ROWS PAGE FORMAT RAW ENDPOINT
  export NAME MAKER ITEM_SEQ INGREDIENT TYPE_NAME
  export YEAR ACTION BIZRNO TYPE_CODE CANCEL_NAME DUR_TYPE
  export QUERY_EFFICACY QUERY_METHOD QUERY_WARNING QUERY_SIDE_EFFECT QUERY_STORAGE
}
