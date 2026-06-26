#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  post_comment_feedback.sh --review-id <uuid> --comment-id <id> --incorporated <true|false> [options]

Required:
  --review-id       Review ID
  --comment-id      Review comment ID
  --incorporated    true or false

Options:
  --notes           Optional short note describing the decision
  --output-file     Write API response JSON to this file
  --api-url         Override API base URL (default: https://api.propelcode.ai)
  -h, --help        Show this help

Environment:
  PROPEL_API_KEY      Required bearer token for Propel Review API
  PROPEL_API_BASE_URL Optional API base URL override (preferred)
  PROPEL_API_URL      Optional legacy API base URL override
EOF
}

REVIEW_ID=""
COMMENT_ID=""
INCORPORATED=""
NOTES=""
OUTPUT_FILE=""
API_URL="${PROPEL_API_BASE_URL:-${PROPEL_API_URL:-https://api.propelcode.ai}}"

require_option_value() {
  local opt="$1"
  local value="${2-}"
  if [[ -z "$value" || "$value" == --* ]]; then
    echo "Missing value for $opt" >&2
    usage >&2
    exit 2
  fi
  printf '%s\n' "$value"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --review-id)
      REVIEW_ID="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --comment-id)
      COMMENT_ID="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --incorporated)
      INCORPORATED="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --notes)
      NOTES="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --output-file)
      OUTPUT_FILE="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --api-url)
      API_URL="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "${PROPEL_API_KEY:-}" ]]; then
  echo "PROPEL_API_KEY is not set" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required" >&2
  exit 1
fi

if [[ -z "$REVIEW_ID" || -z "$COMMENT_ID" || -z "$INCORPORATED" ]]; then
  echo "Missing required arguments" >&2
  usage >&2
  exit 2
fi

if [[ "$INCORPORATED" != "true" && "$INCORPORATED" != "false" ]]; then
  echo "--incorporated must be true or false" >&2
  exit 2
fi

PAYLOAD="$(
  jq -n \
    --arg comment_id "$COMMENT_ID" \
    --arg notes "$NOTES" \
    --argjson incorporated "$INCORPORATED" \
    'if $notes == "" then
       {comment_id:$comment_id, incorporated:$incorporated}
     else
       {comment_id:$comment_id, incorporated:$incorporated, notes:$notes}
     end'
)"

BODY_FILE="$(mktemp)"
CURL_CONFIG_FILE="$(mktemp)"
chmod 600 "$CURL_CONFIG_FILE"
trap 'rm -f "$BODY_FILE" "$CURL_CONFIG_FILE"' EXIT
printf 'header = "Authorization: Bearer %s"\n' "$PROPEL_API_KEY" >"$CURL_CONFIG_FILE"
printf 'header = "Content-Type: application/json"\n' >>"$CURL_CONFIG_FILE"

if ! HTTP_CODE="$(
  curl -sS -o "$BODY_FILE" -w "%{http_code}" \
    --config "$CURL_CONFIG_FILE" \
    -X POST "$API_URL/v1/reviews/$REVIEW_ID/comments/feedback" \
    --data-binary "$PAYLOAD"
)"; then
  echo "Feedback post failed: transport-level request error." >&2
  if [[ -s "$BODY_FILE" ]]; then
    cat "$BODY_FILE" >&2
  fi
  exit 1
fi

RESPONSE="$(cat "$BODY_FILE")"

if [[ ! "$HTTP_CODE" =~ ^2 ]]; then
  echo "Feedback post failed ($HTTP_CODE)" >&2
  echo "$RESPONSE" >&2
  exit 1
fi

if [[ -n "$OUTPUT_FILE" ]]; then
  printf '%s\n' "$RESPONSE" >"$OUTPUT_FILE"
fi

printf '%s\n' "$RESPONSE"
