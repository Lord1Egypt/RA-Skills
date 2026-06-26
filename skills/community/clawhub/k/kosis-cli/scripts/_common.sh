#!/usr/bin/env bash
# Shared helpers for kosis-cli scripts.
set -euo pipefail

KOSIS_BASE="${KOSIS_BASE:-https://kosis.kr/openapi}"

require_key() {
  if [[ -z "${KOSIS_API_KEY:-}" ]]; then
    echo "error: KOSIS_API_KEY is not set. Get one at https://kosis.kr/openapi/devGuide/devGuide_0102.do" >&2
    exit 2
  fi
}

require_bin() {
  for b in "$@"; do
    if ! command -v "$b" >/dev/null 2>&1; then
      echo "error: required binary '$b' not found in PATH" >&2
      exit 2
    fi
  done
}

# urlencode <string> — emits a URL-encoded copy of $1 on stdout.
urlencode() {
  local s="$1" out="" c i
  for ((i=0; i<${#s}; i++)); do
    c="${s:i:1}"
    case "$c" in
      [a-zA-Z0-9._~-]) out+="$c" ;;
      *) printf -v c '%%%02X' "'$c"; out+="$c" ;;
    esac
  done
  printf '%s' "$out"
}

# kosis_get <endpoint_path> <query_string>
# Fetches the URL, surfaces errors, prints raw response on stdout.
kosis_get() {
  local path="$1" qs="$2" body http
  body=$(mktemp); trap 'rm -f "$body"' RETURN
  http=$(curl -sS -o "$body" -w '%{http_code}' "$KOSIS_BASE/$path?$qs") || {
    echo "error: curl failed for $path" >&2; exit 3;
  }
  if [[ "$http" != "200" ]]; then
    echo "error: HTTP $http from KOSIS" >&2
    cat "$body" >&2
    exit 4
  fi
  # KOSIS surfaces errors in two shapes:
  #   1) JSON  : {"err":"11","errMsg":"…"}
  #   2) XML   : <error><err>11</err><errMsg>…</errMsg></error>  (BigData endpoint)
  if head -c 1 "$body" | grep -q '<'; then
    # XML error response — extract err/errMsg into JSON for stderr clarity, then fail.
    err=$(grep -oE '<err>[^<]+</err>' "$body" | head -1 | sed -E 's#</?err>##g')
    msg=$(grep -oE '<errMsg>[^<]+</errMsg>' "$body" | head -1 | sed -E 's#</?errMsg>##g')
    echo "{\"err\":\"${err:-unknown}\",\"errMsg\":\"${msg:-XML error}\"}" >&2
    exit 5
  fi
  if jq -e 'type=="object" and has("err")' "$body" >/dev/null 2>&1; then
    cat "$body" >&2
    exit 5
  fi
  cat "$body"
}

# emit_jsonl <body_file_or_stdin>
# Accepts a JSON array (KOSIS default) and prints one compact object per line.
emit_jsonl() {
  jq -c '.[]?'
}
