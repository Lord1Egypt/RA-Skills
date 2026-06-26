#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://genius.corp.kuaishou.com"
COOKIE=""
YEAR="2026"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url) BASE_URL="$2"; shift 2 ;;
    --cookie) COOKIE="$2"; shift 2 ;;
    --year) YEAR="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$COOKIE" ]]; then
  echo "ERROR: --cookie is required, e.g. --cookie 'accessproxy_session=xxx'"
  exit 1
fi

function hit_get() {
  local path="$1"
  echo "\n>>> GET $path"
  curl -sS -i \
    -H "Cookie: $COOKIE" \
    "$BASE_URL$path" | head -c 800
  echo
}

function hit_post() {
  local path="$1"
  local body="$2"
  echo "\n>>> POST $path"
  curl -sS -i \
    -H "Cookie: $COOKIE" \
    -H "Content-Type: application/json" \
    -X POST \
    -d "$body" \
    "$BASE_URL$path" | head -c 800
  echo
}

hit_get "/budget-portal/api/authority/user"
hit_get "/budget-portal/api/authority/org/tree"
hit_get "/budget-portal/api/horse-race-lamp/query?tabCode=management-yearly%2Factual"
hit_get "/budget-portal/api/description/act-latest-update-date"
hit_get "/budget-portal/api/annual-actual/versions?year=${YEAR}"

# Placeholder payloads: adjust from live capture when needed.
hit_post "/budget-portal/api/actual-ledger/detail" '{"year":'"$YEAR"',"periodType":"MONTH"}'
hit_post "/budget-portal/api/actual-ledger/products" '{"year":'"$YEAR"',"periodType":"MONTH"}'

echo "\nDone. If POST returns validation error, capture real request body from browser Network and retry."