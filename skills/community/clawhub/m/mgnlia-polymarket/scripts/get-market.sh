#!/bin/bash
# Get market details by ID or slug
# Usage: ./get-market.sh MARKET_ID_OR_SLUG

MARKET_ID="$1"

if [ -z "$MARKET_ID" ]; then
  echo "Usage: $0 MARKET_ID_OR_SLUG" >&2
  exit 1
fi

polymarket -o json markets get "$MARKET_ID"
