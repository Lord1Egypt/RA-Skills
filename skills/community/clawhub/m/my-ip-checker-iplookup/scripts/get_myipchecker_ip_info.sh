#!/bin/sh

set -u

BASE_URL="https://myipchecker.ai"
IP=""
TIMEOUT_SECONDS="20"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

usage() {
  cat <<'EOF'
Usage: get_myipchecker_ip_info.sh [--base-url URL] [--ip IPV4] [--timeout SECONDS] [--user-agent VALUE]
EOF
}

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\r//g; :a;N;$!ba;s/\n/\\n/g'
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --base-url)
      if [ "$#" -lt 2 ]; then
        printf 'Missing value for %s\n' "$1" >&2
        exit 2
      fi
      BASE_URL=$2
      shift 2
      ;;
    --ip)
      if [ "$#" -lt 2 ]; then
        printf 'Missing value for %s\n' "$1" >&2
        exit 2
      fi
      IP=$2
      shift 2
      ;;
    --timeout)
      if [ "$#" -lt 2 ]; then
        printf 'Missing value for %s\n' "$1" >&2
        exit 2
      fi
      TIMEOUT_SECONDS=$2
      shift 2
      ;;
    --user-agent)
      if [ "$#" -lt 2 ]; then
        printf 'Missing value for %s\n' "$1" >&2
        exit 2
      fi
      USER_AGENT=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

BASE_URL=${BASE_URL%/}
URL="$BASE_URL/api/ip"

BODY_FILE=$(mktemp)
STATUS_FILE=$(mktemp)
cleanup() {
  rm -f "$BODY_FILE" "$STATUS_FILE"
}
trap cleanup EXIT INT TERM

if ! command -v curl >/dev/null 2>&1; then
  printf '{\n  "transport_error": "missing_curl",\n  "reason": "curl command not found",\n  "url": "%s"\n}\n' "$(json_escape "$URL")"
  exit 1
fi

if [ -n "$IP" ]; then
  HTTP_STATUS=$(curl -sS -L -G \
    -H "Accept: application/json" \
    -H "User-Agent: $USER_AGENT" \
    --connect-timeout "$TIMEOUT_SECONDS" \
    --max-time "$TIMEOUT_SECONDS" \
    --data-urlencode "ip=$IP" \
    -o "$BODY_FILE" \
    -w "%{http_code}" \
    "$URL" 2>"$STATUS_FILE")
else
  HTTP_STATUS=$(curl -sS -L \
    -H "Accept: application/json" \
    -H "User-Agent: $USER_AGENT" \
    --connect-timeout "$TIMEOUT_SECONDS" \
    --max-time "$TIMEOUT_SECONDS" \
    -o "$BODY_FILE" \
    -w "%{http_code}" \
    "$URL" 2>"$STATUS_FILE")
fi
CURL_EXIT=$?

if [ "$CURL_EXIT" -ne 0 ]; then
  REASON=$(cat "$STATUS_FILE")
  printf '{\n  "transport_error": "request_error",\n  "reason": "%s",\n  "url": "%s"\n}\n' "$(json_escape "$REASON")" "$(json_escape "$URL")"
  exit 1
fi

BODY=$(cat "$BODY_FILE")

case "$HTTP_STATUS" in
  2??)
    if [ -z "$BODY" ]; then
      printf '{\n  "transport_error": "invalid_json",\n  "url": "%s",\n  "body": ""\n}\n' "$(json_escape "$URL")"
      exit 1
    fi
    printf '%s\n' "$BODY"
    ;;
  *)
    printf '{\n  "transport_error": "http_error",\n  "status": %s,\n  "reason": "HTTP %s",\n  "url": "%s",\n  "body": "%s"\n}\n' \
      "$HTTP_STATUS" \
      "$HTTP_STATUS" \
      "$(json_escape "$URL")" \
      "$(json_escape "$BODY")"
    exit 1
    ;;
esac
