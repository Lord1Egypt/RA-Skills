#!/usr/bin/env bash
# manto-geo shell client - publish to Manto (https://manto.xin) with curl only.
#
# Usage:
#   ./manto.sh register you@example.com
#   ./manto.sh publish "external-id" "title" "content" ["url"]
#   ./manto.sh account
#   ./manto.sh search "query" [limit]
#   ./manto.sh delete <content_id>
#
# The API key is read from $MANTO_API_KEY, else ~/.config/manto/api_key.
# Override the endpoint with $MANTO_BASE_URL (defaults to https://manto.xin).

set -euo pipefail

BASE_URL="${MANTO_BASE_URL:-https://manto.xin}"
KEY_FILE="${HOME}/.config/manto/api_key"

# Prints the key on stdout; returns non-zero when unavailable.
#
# IMPORTANT: never call this as $(key) inside another command substitution.
# `exit` inside $( ) only kills the subshell and the script keeps running with an
# empty key. Always assign in the parent shell and test the status:
#     K=$(key) || { echo "..." >&2; exit 2; }
key() {
  if [ -n "${MANTO_API_KEY:-}" ]; then printf '%s' "$MANTO_API_KEY"; return 0; fi
  if [ -f "$KEY_FILE" ]; then tr -d '[:space:]' < "$KEY_FILE"; return 0; fi
  return 1
}

die_no_key() {
  echo "error: no API key. Set MANTO_API_KEY or run: $0 register <email>" >&2
  echo "       (the key is shown only once, at account creation)" >&2
  exit 2
}

json_str() {  # escape a value for embedding in a JSON string
  printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])' \
    2>/dev/null || printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

case "${1:-}" in
  register)
    [ $# -ge 2 ] || { echo "usage: $0 register <email>" >&2; exit 64; }
    resp=$(curl -fsS -X POST "$BASE_URL/v1/accounts" \
             -H 'content-type: application/json' \
             -d "{\"email\": $(printf '"%s"' "$2")}")
    printf '%s\n' "$resp"
    api_key=$(printf '%s' "$resp" | sed -n 's/.*"api_key"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
    if [ -n "$api_key" ]; then
      mkdir -p "$(dirname "$KEY_FILE")"
      (umask 077; printf '%s\n' "$api_key" > "$KEY_FILE")
      echo "api_key saved to $KEY_FILE (mode 600). It is never shown again."
    fi
    ;;

  publish)
    [ $# -ge 4 ] || { echo "usage: $0 publish <external_id> <title> <content> [url]" >&2; exit 64; }
    body=$(cat <<EOF
{"external_id": "$(json_str "$2")", "title": "$(json_str "$3")", "content": "$(json_str "$4")"$(if [ $# -ge 5 ]; then printf ', "url": "%s"' "$(json_str "$5")"; fi)}
EOF
)
    K=$(key) || die_no_key
    curl -fsS -X POST "$BASE_URL/v1/content" \
      -H 'content-type: application/json' \
      -H "authorization: Bearer $K" \
      -d "$body"
    echo
    ;;

  account)
    K=$(key) || die_no_key
    curl -fsS "$BASE_URL/v1/account" -H "authorization: Bearer $K"
    echo
    ;;

  search)
    [ $# -ge 2 ] || { echo "usage: $0 search <query> [limit]" >&2; exit 64; }
    curl -fsS --get "$BASE_URL/v1/search" \
      --data-urlencode "query=$2" --data-urlencode "limit=${3:-10}"
    echo
    ;;

  delete)
    [ $# -ge 2 ] || { echo "usage: $0 delete <content_id>" >&2; exit 64; }
    K=$(key) || die_no_key
    curl -fsS -X DELETE "$BASE_URL/v1/content/$2" -H "authorization: Bearer $K"
    echo
    ;;

  *)
    sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
    exit 64
    ;;
esac
