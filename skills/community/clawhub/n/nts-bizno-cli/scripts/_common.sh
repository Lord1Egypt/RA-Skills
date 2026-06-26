#!/usr/bin/env bash
# Shared helpers for nts-bizno-cli scripts.
set -euo pipefail

NTS_BASE="${NTS_BASE:-https://api.odcloud.kr/api/nts-businessman/v1}"

require_key() {
  if [[ -z "${NTS_API_KEY:-}" ]]; then
    echo "error: NTS_API_KEY is not set. Get one at https://www.data.go.kr (search '국세청 사업자등록정보 진위확인 및 상태조회 서비스')." >&2
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

# urlencode <string>
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

# Strip dashes/spaces from a business number, e.g. 123-45-67890 -> 1234567890.
strip_bno() {
  printf '%s' "$1" | tr -d -- '- \t'
}

# Verify 사업자등록번호 checksum locally (no API call).
# Returns 0 if checksum is valid, 1 otherwise. Echoes nothing.
# Algorithm (NTS official):
#   weights w = [1,3,7,1,3,7,1,3,5]
#   sum = Σ d[i]*w[i] for i in 0..8  +  floor(d[8]*5 / 10)
#   check = (10 - (sum % 10)) % 10
#   valid iff check == d[9]
checksum_bno() {
  local bno; bno=$(strip_bno "$1")
  if [[ ! "$bno" =~ ^[0-9]{10}$ ]]; then
    return 1
  fi
  local -a w=(1 3 7 1 3 7 1 3 5)
  local sum=0 i d8 d
  for i in 0 1 2 3 4 5 6 7 8; do
    d="${bno:i:1}"
    sum=$(( sum + d * w[i] ))
  done
  d8="${bno:8:1}"
  sum=$(( sum + (d8 * 5) / 10 ))
  local check=$(( (10 - (sum % 10)) % 10 ))
  local last="${bno:9:1}"
  [[ "$check" == "$last" ]]
}

# Format a 10-digit b_no as XXX-XX-XXXXX. Echoes input unchanged on bad length.
format_bno() {
  local bno; bno=$(strip_bno "$1")
  if [[ "$bno" =~ ^[0-9]{10}$ ]]; then
    printf '%s-%s-%s' "${bno:0:3}" "${bno:3:2}" "${bno:5:5}"
  else
    printf '%s' "$1"
  fi
}

# nts_post <endpoint_path> <json_body>
# Posts JSON, surfaces errors, prints raw response on stdout.
nts_post() {
  local path="$1" body_json="$2" body http key_q
  key_q="serviceKey=$(urlencode "$NTS_API_KEY")"
  body=$(mktemp); trap 'rm -f "$body"' RETURN
  http=$(curl -sS -o "$body" -w '%{http_code}' \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -X POST \
    "$NTS_BASE/$path?$key_q" \
    --data "$body_json") || {
    echo "error: curl failed for $path" >&2; exit 3;
  }
  if [[ "$http" != "200" ]]; then
    echo "error: HTTP $http from NTS" >&2
    cat "$body" >&2
    exit 4
  fi
  # NTS odcloud surfaces some errors as XML (<OpenAPI_ServiceResponse>...</OpenAPI_ServiceResponse>).
  if head -c 1 "$body" | grep -q '<'; then
    err=$(grep -oE '<returnReasonCode>[^<]+</returnReasonCode>' "$body" | head -1 | sed -E 's#</?returnReasonCode>##g')
    msg=$(grep -oE '<errMsg>[^<]+</errMsg>' "$body" | head -1 | sed -E 's#</?errMsg>##g')
    auth=$(grep -oE '<returnAuthMsg>[^<]+</returnAuthMsg>' "$body" | head -1 | sed -E 's#</?returnAuthMsg>##g')
    printf '{"err":"%s","errMsg":"%s","authMsg":"%s"}\n' "${err:-unknown}" "${msg:-XML error}" "${auth:-}" >&2
    exit 5
  fi
  cat "$body"
}
