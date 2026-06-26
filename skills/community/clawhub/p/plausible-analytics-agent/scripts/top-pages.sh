#!/usr/bin/env bash
# top-pages.sh — Get top pages from Plausible Analytics
# Usage: top-pages.sh --domain "example.com" [--period "30d"] [--limit 10] [--base-url "https://plausible.io"]

set -euo pipefail

DOMAIN="${PLAUSIBLE_SITE_DOMAIN:-}"
API_KEY="${PLAUSIBLE_API_KEY:-}"
BASE_URL="${PLAUSIBLE_BASE_URL:-https://plausible.io}"
PERIOD="30d"
LIMIT="10"

usage() {
  cat <<EOF
Usage: top-pages.sh [options]
Options:
  --domain    Site domain (env: PLAUSIBLE_SITE_DOMAIN)
  --api-key   Plausible API key (env: PLAUSIBLE_API_KEY)
  --period    Time period: 6mo, 12mo, day, 7d, 30d, month (default: 30d)
  --limit     Number of pages to return (default: 10)
  --base-url  Plausible base URL (default: https://plausible.io)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="${2:-}"; shift 2 ;;
    --api-key) API_KEY="${2:-}"; shift 2 ;;
    --period) PERIOD="${2:-}"; shift 2 ;;
    --limit) LIMIT="${2:-}"; shift 2 ;;
    --base-url) BASE_URL="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$DOMAIN" ]]; then
  echo "Error: --domain or PLAUSIBLE_SITE_DOMAIN is required" >&2
  exit 1
fi

if [[ -z "$API_KEY" ]]; then
  echo "Error: --api-key or PLAUSIBLE_API_KEY is required" >&2
  exit 1
fi

PARAMS="site_id=${DOMAIN}&period=${PERIOD}&display=badge&limit=${LIMIT}"

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer ${API_KEY}" \
  "${BASE_URL}/api/v1/stats/breakdown?${PARAMS}&property=event:page")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "Error fetching top pages (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi

echo "$BODY" | jq .
