#!/usr/bin/env bash
# _common.sh — shared helpers for kto-tourapi-cli.
# Source this from each subcommand: `. "$here/_common.sh"`
#
# Wraps the 한국관광공사 TourAPI 4.0 (KorService2) at apis.data.go.kr/B551011/KorService2.

set -euo pipefail

TOURAPI_BASE="${TOURAPI_BASE:-https://apis.data.go.kr/B551011/KorService2}"
TOURAPI_MOBILE_OS="${TOURAPI_MOBILE_OS:-ETC}"
TOURAPI_MOBILE_APP="${TOURAPI_MOBILE_APP:-kto-tourapi-cli}"

require_bin() {
  for b in "$@"; do
    command -v "$b" >/dev/null 2>&1 || { echo "error: $b is required but not installed." >&2; exit 127; }
  done
}

require_key() {
  if [[ -z "${TOURAPI_SERVICE_KEY:-}" ]]; then
    cat >&2 <<'EOF'
error: TOURAPI_SERVICE_KEY must be set.
Register at https://www.data.go.kr and request approval for:
  "한국관광공사_국문 관광정보 서비스_GW"  (TourAPI 4.0 / KorService2)
Then export the *Decoding* key (raw, not URL-encoded) as TOURAPI_SERVICE_KEY.
EOF
    exit 78
  fi
}

# valid_yyyymmdd <YYYYMMDD>
valid_yyyymmdd() {
  if ! [[ "$1" =~ ^[0-9]{8}$ ]]; then
    echo "error: date '$1' is not in YYYYMMDD format." >&2
    exit 64
  fi
}

# valid_content_type <id>
# Accepts: 12 14 15 25 28 32 38 39 (KorService2 contentTypeId codes).
valid_content_type() {
  case "$1" in
    12|14|15|25|28|32|38|39) ;;
    *) echo "error: contentTypeId '$1' is not one of: 12=관광지 14=문화시설 15=축제공연행사 25=여행코스 28=레포츠 32=숙박 38=쇼핑 39=음식점." >&2; exit 64;;
  esac
}

# tourapi_get <path> <key1=val1> <key2=val2> ...
# - Adds serviceKey, MobileOS, MobileApp, _type=json automatically.
# - URL-encodes values via jq -r @uri.
# - Returns body on stdout. Non-2xx or non-OK resultCode prints to stderr and exits 22.
tourapi_get() {
  local path="$1"; shift
  require_key

  local url="${TOURAPI_BASE}/${path}"
  # Encode service key (some keys contain '+' '/' '=' which must be URL-encoded).
  local enc_key
  enc_key=$(printf '%s' "$TOURAPI_SERVICE_KEY" | jq -Rrn '@uri inputs')
  local qs="serviceKey=${enc_key}&MobileOS=${TOURAPI_MOBILE_OS}&MobileApp=${TOURAPI_MOBILE_APP}&_type=json"

  local kv k v enc_v
  for kv in "$@"; do
    [[ -z "$kv" ]] && continue
    k="${kv%%=*}"
    v="${kv#*=}"
    [[ -z "$v" ]] && continue
    enc_v=$(printf '%s' "$v" | jq -Rrn '@uri inputs')
    qs="${qs}&${k}=${enc_v}"
  done

  local out http
  out=$(mktemp)
  http=$(curl -sS -G -o "$out" -w '%{http_code}' "${url}?${qs}" || true)

  if [[ "$http" != 2* ]]; then
    echo "error: TourAPI returned HTTP $http for /${path}" >&2
    sed -e 's/^/  /' "$out" >&2
    rm -f "$out"
    exit 22
  fi

  # data.go.kr sometimes returns XML with a SERVICE_KEY error even when _type=json.
  # Detect and surface it cleanly.
  if head -c 1 "$out" | grep -q '<'; then
    echo "error: TourAPI returned XML (likely a service-key or quota error) for /${path}" >&2
    sed -e 's/^/  /' "$out" >&2
    rm -f "$out"
    exit 22
  fi

  # Verify the JSON envelope's resultCode == "0000".
  local rc rmsg
  rc=$(jq -r '.response.header.resultCode // "?"' "$out")
  rmsg=$(jq -r '.response.header.resultMsg  // ""'  "$out")
  if [[ "$rc" != "0000" ]]; then
    echo "error: TourAPI resultCode=$rc resultMsg=$rmsg for /${path}" >&2
    rm -f "$out"
    exit 22
  fi

  cat "$out"
  rm -f "$out"
}

# emit_items <body-json>
# Extracts the standard items array (response.body.items.item) as JSONL.
# Handles both list shape (.item is array) and single-item shape (.item is object).
emit_items() {
  jq -c '
    .response.body.items.item as $it
    | if   $it == null then empty
      elif ($it | type) == "array"  then $it[]
      else $it
      end
  '
}
