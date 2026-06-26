#!/usr/bin/env bash
set -euo pipefail

PLATFORM="${1:-}"
TARGET_URL="${2:-}"
BASE_URL="${3:-${BIL_CRAWL_URL:-http://127.0.0.1:39002}}"

if [[ -z "$PLATFORM" || -z "$TARGET_URL" ]]; then
  echo "Usage: $0 <bilibili|douyin|youtube|zhihu> <target_url> [base_url]" >&2
  exit 2
fi

case "$PLATFORM" in
  bilibili|douyin|youtube|zhihu) ;;
  *)
    echo "Unsupported platform: $PLATFORM" >&2
    exit 2
    ;;
esac

encoded=$(node -e 'process.stdout.write(encodeURIComponent(process.argv[1]))' "$TARGET_URL")
endpoint="$BASE_URL/start-crawl/$PLATFORM/$encoded"
payload='{"source":"ai"}'

# Best-effort health check
curl -fsS "$BASE_URL/health" >/dev/null 2>&1 || curl -fsS "$BASE_URL/" >/dev/null 2>&1 || {
  echo "Service not reachable at $BASE_URL" >&2
  exit 1
}

curl -fsS -X POST "$endpoint" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  --data "$payload"

echo
