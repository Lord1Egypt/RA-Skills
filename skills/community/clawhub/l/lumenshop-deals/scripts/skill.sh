#!/usr/bin/env bash
# LumenShop Deal Finder — search discounted Shopify products via the LumenShop API
# Usage: ./skill.sh [OPTIONS]
#
# Options:
#   --query      Direct search query, e.g. "skirt" or "blue jacket"
#   --category   shoes|clothes|bags|all  (default: all; ignored if --query set)
#   --price-max  Maximum price in USD, e.g. 50  (optional)
#   --price-min  Minimum price in USD, e.g. 10  (optional)
#   --limit      Max results to show (default: 20, max: 200)
#   --api-url    API base URL (default: https://lumenshop.vercel.app)
#   --api-key    Bearer token (default: dev-key — works out of the box)
#   --json       Output raw JSON instead of table

set -euo pipefail

# ── Defaults ─────────────────────────────────────────────────────────────────
QUERY=""
CATEGORY="all"
PRICE_MAX=""
PRICE_MIN=""
LIMIT=20
API_URL="${LUMENSHOP_API_URL:-https://lumenshop.vercel.app}"
API_KEY="${LUMENSHOP_API_KEY:-dev-key}"

# ── Arg parsing ───────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --query)     QUERY="$2";     shift 2 ;;
    --category)  CATEGORY="$2";  shift 2 ;;
    --price-max) PRICE_MAX="$2"; shift 2 ;;
    --price-min) PRICE_MIN="$2"; shift 2 ;;
    --limit)     LIMIT="$2";     shift 2 ;;
    --api-url)   API_URL="$2";   shift 2 ;;
    --api-key)   API_KEY="$2";   shift 2 ;;
    -h|--help)
      sed -n '2,13p' "$0" | sed 's/^# \?//'
      exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# ── Resolve query from category if --query not given ─────────────────────────
if [[ -z "$QUERY" ]]; then
  case "$CATEGORY" in
    shoes)   QUERY="shoe sneaker boot sandal" ;;
    clothes) QUERY="shirt jacket dress hoodie pants skirt" ;;
    bags)    QUERY="bag backpack purse tote" ;;
    all)     QUERY="shoe shirt bag jacket dress sneaker skirt" ;;
    *)
      echo "Unknown category: $CATEGORY. Use: shoes, clothes, bags, all" >&2
      exit 1 ;;
  esac
fi

# ── Build optional filters JSON fragment ─────────────────────────────────────
FILTERS="{"
SEP=""
if [[ -n "$PRICE_MIN" ]]; then
  FILTERS+="${SEP}\"price_min\": ${PRICE_MIN}"
  SEP=", "
fi
if [[ -n "$PRICE_MAX" ]]; then
  FILTERS+="${SEP}\"price_max\": ${PRICE_MAX}"
fi
FILTERS+="}"

# ── Single API call ───────────────────────────────────────────────────────────
BODY="{\"query\": \"${QUERY}\", \"limit\": ${LIMIT}, \"filters\": ${FILTERS}}"

RESPONSE=$(curl -sS -X POST "${API_URL}/api/search" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY") || {
  echo "Error: failed to reach ${API_URL}/api/search" >&2
  exit 1
}

if [[ -z "$RESPONSE" ]]; then
  echo "Error: empty response from API" >&2
  exit 1
fi

echo "$RESPONSE"
