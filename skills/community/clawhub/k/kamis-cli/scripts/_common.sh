#!/usr/bin/env bash
# Shared helpers for kamis-cli scripts.
set -euo pipefail

KAMIS_BASE="${KAMIS_BASE:-https://www.kamis.or.kr/service/price/xml.do}"

kamis_creds() {
  local key="${KAMIS_CERT_KEY:-${1:-}}"
  local id="${KAMIS_CERT_ID:-${2:-}}"
  if [[ -z "$key" ]]; then key="TEST"; fi
  if [[ -z "$id" ]]; then id="TEST"; fi
  printf '%s\t%s\n' "$key" "$id"
}

# kamis_call <action> [extra query args ...]
# Reads --key/--id from KAMIS_CERT_KEY/KAMIS_CERT_ID or falls back to TEST.
kamis_call() {
  local action="$1"; shift
  local key="${KAMIS_CERT_KEY:-TEST}"
  local id="${KAMIS_CERT_ID:-TEST}"
  local url="${KAMIS_BASE}?action=${action}&p_cert_key=${key}&p_cert_id=${id}&p_returntype=json"
  for arg in "$@"; do url+="&${arg}"; done
  curl -sS --max-time 30 \
    -H "User-Agent: Mozilla/5.0 (kamis-cli)" \
    -H "Accept: application/json" \
    "$url"
}

require_arg() {
  local name="$1" val="${2:-}"
  if [[ -z "$val" ]]; then
    echo "missing required arg: --${name}" >&2
    exit 2
  fi
}
