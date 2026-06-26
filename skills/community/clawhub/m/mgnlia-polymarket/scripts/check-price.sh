#!/bin/bash
# Check midpoint price for a token
# Usage: ./check-price.sh TOKEN_ID

TOKEN_ID="$1"

if [ -z "$TOKEN_ID" ]; then
  echo "Usage: $0 TOKEN_ID" >&2
  exit 1
fi

polymarket -o json clob midpoint "$TOKEN_ID"
