#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  create_review.sh --diff-file <path> --repo <owner/repo> --base-commit <sha> [options]

Required:
  --diff-file      Path to git diff file
  --repo           Repository slug (owner/repo)
  --base-commit    Base commit SHA

Options:
  --head-commit-sha  Optional HEAD commit SHA for local dedup context
  --branch           Optional branch name for local dedup context
  --output-file    Write raw API response JSON to this file
  --max-attempts   Retry attempts for 5xx responses (default: 3)
  --api-url        Override API base URL (default: https://api.propelcode.ai)
  -h, --help       Show this help

Environment:
  PROPEL_API_KEY     Required bearer token for Propel Review API
  PROPEL_API_BASE_URL  Optional API base URL override (preferred)
  PROPEL_API_URL       Optional legacy API base URL override
EOF
}

DIFF_FILE=""
REPO_SLUG=""
BASE_COMMIT=""
OUTPUT_FILE=""
HEAD_COMMIT_SHA=""
BRANCH_NAME=""
MAX_ATTEMPTS=3
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
    --diff-file)
      DIFF_FILE="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --repo)
      REPO_SLUG="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --base-commit)
      BASE_COMMIT="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --output-file)
      OUTPUT_FILE="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --head-commit-sha)
      HEAD_COMMIT_SHA="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --branch)
      BRANCH_NAME="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --max-attempts)
      MAX_ATTEMPTS="$(require_option_value "$1" "${2-}")"
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

if [[ -z "$DIFF_FILE" || -z "$REPO_SLUG" || -z "$BASE_COMMIT" ]]; then
  echo "Missing required arguments" >&2
  usage >&2
  exit 2
fi

if ! [[ "$MAX_ATTEMPTS" =~ ^[0-9]+$ ]] || [[ "$MAX_ATTEMPTS" -lt 1 ]]; then
  echo "--max-attempts must be a positive integer" >&2
  exit 2
fi

if [[ ! -f "$DIFF_FILE" ]]; then
  echo "Diff file does not exist: $DIFF_FILE" >&2
  exit 1
fi

HEAD_COMMIT_SHA="$(printf '%s' "$HEAD_COMMIT_SHA" | tr '[:upper:]' '[:lower:]')"

DIFF_BYTES="$(wc -c <"$DIFF_FILE" | tr -d '[:space:]')"
echo "repo=$REPO_SLUG base=$BASE_COMMIT diff_bytes=$DIFF_BYTES" >&2

BODY_FILE="$(mktemp)"
CURL_CONFIG_FILE="$(mktemp)"
chmod 600 "$CURL_CONFIG_FILE"
trap 'rm -f "$BODY_FILE" "$CURL_CONFIG_FILE"' EXIT
printf 'header = "Authorization: Bearer %s"\n' "$PROPEL_API_KEY" >"$CURL_CONFIG_FILE"
printf 'header = "Content-Type: application/json"\n' >>"$CURL_CONFIG_FILE"

HTTP_CODE=""
for ((attempt = 1; attempt <= MAX_ATTEMPTS; attempt++)); do
  if ! HTTP_CODE="$(
    jq -n \
      --rawfile diff "$DIFF_FILE" \
      --arg repo "$REPO_SLUG" \
      --arg base "$BASE_COMMIT" \
      --arg head "$HEAD_COMMIT_SHA" \
      --arg branch "$BRANCH_NAME" \
      '({diff:$diff, repository:$repo, base_commit:$base}
        + (if $head != "" then {head_commit_sha:$head} else {} end)
        + (if $branch != "" then {branch:$branch} else {} end))' \
      | curl -sS -o "$BODY_FILE" -w "%{http_code}" \
        --config "$CURL_CONFIG_FILE" \
        --data-binary @- \
        "$API_URL/v1/reviews"
  )"; then
    if [[ "$attempt" -lt "$MAX_ATTEMPTS" ]]; then
      sleep $((attempt * 2))
      continue
    fi
    echo "Review create failed: transport-level request error after bounded retries." >&2
    if [[ -s "$BODY_FILE" ]]; then
      cat "$BODY_FILE" >&2
    fi
    exit 1
  fi

  if [[ "$HTTP_CODE" =~ ^5 ]] && [[ "$attempt" -lt "$MAX_ATTEMPTS" ]]; then
    sleep $((attempt * 2))
    continue
  fi
  break
done

RESPONSE="$(cat "$BODY_FILE")"

case "$HTTP_CODE" in
  202) ;;
  401 | 403)
    echo "Review create failed ($HTTP_CODE): refresh token and confirm scopes reviews:read + reviews:write." >&2
    echo "$RESPONSE" >&2
    exit 1
    ;;
  404)
    echo "Review create failed (404): connect repository in Propel workspace or correct owner/repo slug ($REPO_SLUG)." >&2
    echo "$RESPONSE" >&2
    exit 1
    ;;
  400 | 413)
    echo "Review create failed ($HTTP_CODE): fix request payload (or reduce diff size for 413)." >&2
    echo "$RESPONSE" >&2
    exit 1
    ;;
  5??)
    echo "Review create failed ($HTTP_CODE): transient Propel API error after bounded retries." >&2
    echo "$RESPONSE" >&2
    exit 1
    ;;
  *)
    echo "Review create failed ($HTTP_CODE)." >&2
    echo "$RESPONSE" >&2
    exit 1
    ;;
esac

REVIEW_ID="$(echo "$RESPONSE" | jq -r '.review_id // empty')"
if [[ -z "$REVIEW_ID" ]]; then
  echo "Review create succeeded but review_id is missing." >&2
  echo "$RESPONSE" >&2
  exit 1
fi

if [[ -n "$OUTPUT_FILE" ]]; then
  printf '%s\n' "$RESPONSE" >"$OUTPUT_FILE"
fi

printf '%s\n' "$RESPONSE"
