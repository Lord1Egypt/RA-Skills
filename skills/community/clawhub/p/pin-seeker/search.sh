#!/usr/bin/env sh
# Search Pin Seeker tee times. Usage:
#   ./search.sh "Saturday morning near San Francisco for 2" [IANA_timezone]
set -eu

BASE="${PINSEEKER_URL:-https://pinseeker.xyz}"
QUERY="${1:-}"
TZ="${2:-}"

if [ -z "$QUERY" ]; then
  echo "usage: search.sh \"Saturday morning near San Francisco for 2\" [IANA_timezone]" >&2
  exit 1
fi

if [ -n "$TZ" ]; then
  curl -fsS -G "$BASE/api/agent/search" \
    --data-urlencode "query=$QUERY" \
    --data-urlencode "timezone=$TZ"
else
  curl -fsS -G "$BASE/api/agent/search" \
    --data-urlencode "query=$QUERY"
fi

echo
