#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage:
  poll_review.sh --review-id <uuid> [options]

Required:
  --review-id      Review ID returned by POST /v1/reviews

Options:
  --output-file    Write final review JSON to this file
  --max-attempts   Baseline polling attempts used to derive the timeout budget (default: ${DEFAULT_MAX_ATTEMPTS})
  --sleep-seconds  Fallback delay between polls in seconds when the API omits poll_after_ms (default: ${DEFAULT_SLEEP_SECONDS})
  --api-url        Override API base URL (default: https://api.propelcode.ai)
  -h, --help       Show this help

Environment:
  PROPEL_API_KEY      Required bearer token for Propel Review API
  PROPEL_API_BASE_URL Optional API base URL override (preferred)
  PROPEL_API_URL      Optional legacy API base URL override
EOF
}

DEFAULT_POLL_TIMEOUT_SECONDS=900
DEFAULT_SLEEP_SECONDS=30
DEFAULT_MAX_ATTEMPTS=$((DEFAULT_POLL_TIMEOUT_SECONDS / DEFAULT_SLEEP_SECONDS))
FINAL_STATUS_REFRESH_WINDOW_SECONDS=1

REVIEW_ID=""
OUTPUT_FILE=""
MAX_ATTEMPTS=$DEFAULT_MAX_ATTEMPTS
SLEEP_SECONDS=$DEFAULT_SLEEP_SECONDS
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

poll_after_ms_to_seconds() {
  local poll_after_ms="$1"
  printf '%s\n' $(((poll_after_ms + 999) / 1000))
}

elapsed_runtime_seconds() {
  if [[ -n "${PROPEL_REVIEW_POLL_ELAPSED_SECONDS_FILE:-}" ]] && [[ -f "${PROPEL_REVIEW_POLL_ELAPSED_SECONDS_FILE}" ]]; then
    cat "${PROPEL_REVIEW_POLL_ELAPSED_SECONDS_FILE}"
    return
  fi
  printf '%s\n' "$SECONDS"
}

remaining_budget_seconds() {
  local elapsed_seconds
  elapsed_seconds="$(elapsed_runtime_seconds)"
  local remaining=$((TOTAL_TIMEOUT_SECONDS - elapsed_seconds))
  if [[ "$remaining" -lt 0 ]]; then
    remaining=0
  fi
  printf '%s\n' "$remaining"
}

clamp_sleep_to_remaining_budget() {
  local requested_sleep_seconds="$1"
  local remaining_seconds
  remaining_seconds="$(remaining_budget_seconds)"
  if [[ "$remaining_seconds" -gt "$FINAL_STATUS_REFRESH_WINDOW_SECONDS" ]]; then
    remaining_seconds=$((remaining_seconds - FINAL_STATUS_REFRESH_WINDOW_SECONDS))
  else
    remaining_seconds=0
  fi
  if [[ "$requested_sleep_seconds" -gt "$remaining_seconds" ]]; then
    printf '%s\n' "$remaining_seconds"
    return
  fi
  printf '%s\n' "$requested_sleep_seconds"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --review-id)
      REVIEW_ID="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --output-file)
      OUTPUT_FILE="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --max-attempts)
      MAX_ATTEMPTS="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --sleep-seconds)
      SLEEP_SECONDS="$(require_option_value "$1" "${2-}")"
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

if [[ -z "$REVIEW_ID" ]]; then
  echo "Missing required argument: --review-id" >&2
  usage >&2
  exit 2
fi

if ! [[ "$MAX_ATTEMPTS" =~ ^[0-9]+$ ]] || [[ "$MAX_ATTEMPTS" -lt 1 ]]; then
  echo "--max-attempts must be a positive integer" >&2
  exit 2
fi

if ! [[ "$SLEEP_SECONDS" =~ ^[0-9]+$ ]] || [[ "$SLEEP_SECONDS" -lt 1 ]]; then
  echo "--sleep-seconds must be a positive integer" >&2
  exit 2
fi

TOTAL_TIMEOUT_SECONDS=$((MAX_ATTEMPTS * SLEEP_SECONDS))
SECONDS=0

BODY_FILE="$(mktemp)"
CURL_CONFIG_FILE="$(mktemp)"
chmod 600 "$CURL_CONFIG_FILE"
trap 'rm -f "$BODY_FILE" "$CURL_CONFIG_FILE"' EXIT
printf 'header = "Authorization: Bearer %s"\n' "$PROPEL_API_KEY" >"$CURL_CONFIG_FILE"

i=0
FINAL_REFRESH_ATTEMPTED=0
while :; do
  i=$((i + 1))
  REQUEST_TIMEOUT_SECONDS="$(remaining_budget_seconds)"
  if [[ "$REQUEST_TIMEOUT_SECONDS" -le 0 ]]; then
    break
  fi
  if ! HTTP_CODE="$(
    curl -sS -o "$BODY_FILE" -w "%{http_code}" \
      --connect-timeout "$REQUEST_TIMEOUT_SECONDS" \
      --max-time "$REQUEST_TIMEOUT_SECONDS" \
      --config "$CURL_CONFIG_FILE" \
      "$API_URL/v1/reviews/$REVIEW_ID"
  )"; then
    RETRY_SLEEP_SECONDS="$(clamp_sleep_to_remaining_budget "$SLEEP_SECONDS")"
    if [[ "$RETRY_SLEEP_SECONDS" -gt 0 ]]; then
      sleep "$RETRY_SLEEP_SECONDS"
      continue
    fi
    if [[ "$(remaining_budget_seconds)" -le 0 ]]; then
      break
    fi
    echo "poll failed: transport-level request error after bounded retries" >&2
    if [[ -s "$BODY_FILE" ]]; then
      cat "$BODY_FILE" >&2
    fi
    exit 1
  fi

  if [[ "$HTTP_CODE" =~ ^5 ]]; then
    RETRY_SLEEP_SECONDS="$(clamp_sleep_to_remaining_budget "$SLEEP_SECONDS")"
    if [[ "$RETRY_SLEEP_SECONDS" -gt 0 ]]; then
      sleep "$RETRY_SLEEP_SECONDS"
      continue
    fi
  fi

  if [[ ! "$HTTP_CODE" =~ ^2 ]]; then
    echo "poll failed ($HTTP_CODE):" >&2
    cat "$BODY_FILE" >&2
    exit 1
  fi

  RESPONSE="$(cat "$BODY_FILE")"
  SANITIZED_RESPONSE="$(printf '%s' "$RESPONSE" | tr -d '\000-\037')"
  # If jq parsing fails, keep polling rather than crashing on transient non-JSON responses.
  REVIEW_STATUS="$(printf '%s' "$SANITIZED_RESPONSE" | jq -r '.status // empty' 2>/dev/null || echo '')"
  NOW="$(date +%H:%M:%S)"
  NEXT_SLEEP_SECONDS="$SLEEP_SECONDS"
  IMMEDIATE_REPOLL_REQUESTED=0
  POLL_AFTER_MS="$(printf '%s' "$SANITIZED_RESPONSE" | jq -r '.poll_after_ms // empty' 2>/dev/null || echo '')"
  if [[ "$POLL_AFTER_MS" =~ ^[0-9]+$ ]]; then
    NEXT_SLEEP_SECONDS="$(poll_after_ms_to_seconds "$POLL_AFTER_MS")"
    if [[ "$POLL_AFTER_MS" -eq 0 ]]; then
      IMMEDIATE_REPOLL_REQUESTED=1
    fi
  fi
  NEXT_SLEEP_SECONDS="$(clamp_sleep_to_remaining_budget "$NEXT_SLEEP_SECONDS")"
  echo "$NOW poll=$i status=${REVIEW_STATUS:-unknown} next_poll_seconds=$NEXT_SLEEP_SECONDS" >&2

  if [[ "$REVIEW_STATUS" == "completed" || "$REVIEW_STATUS" == "failed" ]]; then
    if [[ -n "$OUTPUT_FILE" ]]; then
      printf '%s\n' "$SANITIZED_RESPONSE" >"$OUTPUT_FILE"
    fi
    printf '%s\n' "$SANITIZED_RESPONSE"
    if [[ "$REVIEW_STATUS" == "failed" ]]; then
      exit 2
    fi
    exit 0
  fi

  REMAINING_AFTER_FETCH_SECONDS="$(remaining_budget_seconds)"
  if [[ "$REMAINING_AFTER_FETCH_SECONDS" -le 0 ]]; then
    break
  fi
  if [[ "$REMAINING_AFTER_FETCH_SECONDS" -le "$FINAL_STATUS_REFRESH_WINDOW_SECONDS" ]]; then
    if [[ "$FINAL_REFRESH_ATTEMPTED" -eq 1 ]]; then
      break
    fi
    FINAL_REFRESH_ATTEMPTED=1
    continue
  fi

  if [[ "$IMMEDIATE_REPOLL_REQUESTED" -eq 1 ]]; then
    continue
  fi

  if [[ "$NEXT_SLEEP_SECONDS" -le 0 ]]; then
    if [[ "$FINAL_REFRESH_ATTEMPTED" -eq 1 ]]; then
      break
    fi
    FINAL_REFRESH_ATTEMPTED=1
    continue
  fi
  sleep "$NEXT_SLEEP_SECONDS"
done

echo "timed out after $i polls (~${TOTAL_TIMEOUT_SECONDS} seconds)" >&2
exit 1
