#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Permission smoke test for Propel Review API.

Runs three review-create checks against /v1/reviews:
1) good token + good repo (expects 202)
2) good token + bad repo (expects 404)
3) bad token + good repo (expects 401/403)

Usage:
  ./scripts/smoke_test_permissions.sh [--repo owner/repo] [--base-branch main] [--bad-repo owner/bad] [--api-url https://api.propelcode.ai]

Requirements:
  - PROPEL_API_KEY set
  - jq, curl, git installed
  - non-empty git diff against base branch
EOF
}

for cmd in git curl jq; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

API_URL="${PROPEL_API_BASE_URL:-${PROPEL_API_URL:-https://api.propelcode.ai}}"
BASE_BRANCH=""
REPO_SLUG=""
BAD_REPO=""

require_option_value() {
  local opt="$1"
  local value="${2-}"
  if [[ -z "$value" || "$value" == --* ]]; then
    echo "Missing value for $opt" >&2
    usage >&2
    exit 1
  fi
  printf '%s\n' "$value"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --api-url)
      API_URL="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --base-branch)
      BASE_BRANCH="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --repo)
      REPO_SLUG="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    --bad-repo)
      BAD_REPO="$(require_option_value "$1" "${2-}")"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "${PROPEL_API_KEY:-}" ]]; then
  echo "PROPEL_API_KEY is not set." >&2
  exit 1
fi

if [[ -z "$BASE_BRANCH" ]]; then
  BASE_BRANCH="$(gh pr view --json baseRefName -q '.baseRefName' 2>/dev/null || git remote show origin 2>/dev/null | sed -n '/HEAD branch/s/.*: //p' || true)"
fi

if [[ -z "$REPO_SLUG" ]]; then
  REPO_SLUG="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || git remote get-url origin 2>/dev/null | sed -E 's/\.git$//; s#.*[:/]([^/]+/[^/]+)$#\1#' || true)"
fi

if [[ -z "$BASE_BRANCH" ]]; then
  echo "Error: Could not determine base branch. Please specify with --base-branch." >&2
  exit 1
fi

if [[ -z "$REPO_SLUG" || "$REPO_SLUG" != */* ]]; then
  echo "Error: Could not determine repository slug. Please specify with --repo owner/repo." >&2
  exit 1
fi

if [[ -z "$BAD_REPO" ]]; then
  owner="${REPO_SLUG%%/*}"
  BAD_REPO="${owner}/not-hooked-up-repo"
fi

if ! BASE_COMMIT="$(git merge-base "$BASE_BRANCH" HEAD 2>/dev/null)"; then
  remote_base="origin/$BASE_BRANCH"
  if [[ "$BASE_BRANCH" == origin/* ]]; then
    remote_base="$BASE_BRANCH"
  fi

  if ! BASE_COMMIT="$(git merge-base "$remote_base" HEAD 2>/dev/null)"; then
    echo "Error: Could not compute merge-base for '$BASE_BRANCH' (or '$remote_base') and HEAD." >&2
    exit 1
  fi
fi

DIFF_FILE="$(mktemp)"
trap 'rm -f "$DIFF_FILE"' EXIT
git diff "$BASE_COMMIT" --no-color >"$DIFF_FILE"

if [[ ! -s "$DIFF_FILE" ]]; then
  echo "Diff is empty for base branch '$BASE_BRANCH'. Make a local change first, then re-run." >&2
  exit 1
fi

if [[ "${PROPEL_API_KEY: -1}" == "A" ]]; then
  BAD_TOKEN="${PROPEL_API_KEY%?}B"
else
  BAD_TOKEN="${PROPEL_API_KEY%?}A"
fi

submit_case() {
  local token="$1"
  local repo="$2"
  local body_file
  body_file="$(mktemp)"

  local code
  if ! code="$(
    jq -n --rawfile diff "$DIFF_FILE" --arg repo "$repo" --arg base "$BASE_COMMIT" \
      '{diff:$diff, repository:$repo, base_commit:$base}' \
      | curl -sS -o "$body_file" -w "%{http_code}" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        --data-binary @- \
        "$API_URL/v1/reviews"
  )"; then
    echo "Error: Request failed for repo '$repo' (transport-level failure)." >&2
    rm -f "$body_file"
    return 1
  fi

  printf '%s\n' "$code"
  cat "$body_file"
  rm -f "$body_file"
}

expect_code() {
  local got="$1"
  local expected="$2"
  if [[ "$got" == "$expected" ]]; then
    return 0
  fi
  return 1
}

expect_code_set() {
  local got="$1"
  shift
  for expected in "$@"; do
    if [[ "$got" == "$expected" ]]; then
      return 0
    fi
  done
  return 1
}

echo "Base branch: $BASE_BRANCH"
echo "Base commit: $BASE_COMMIT"
echo "Repo slug: $REPO_SLUG"
echo

overall=0

echo "[Case 1] good token + good repo (expect 202)"
case1_out="$(submit_case "$PROPEL_API_KEY" "$REPO_SLUG")"
case1_code="$(printf '%s\n' "$case1_out" | sed -n '1p')"
case1_body="$(printf '%s\n' "$case1_out" | sed -n '2,$p')"
echo "HTTP: $case1_code"
echo "$case1_body"
if expect_code "$case1_code" "202"; then
  echo "RESULT: PASS"
else
  echo "RESULT: FAIL (expected 202)"
  overall=1
fi
echo

echo "[Case 2] good token + bad repo (expect 404)"
case2_out="$(submit_case "$PROPEL_API_KEY" "$BAD_REPO")"
case2_code="$(printf '%s\n' "$case2_out" | sed -n '1p')"
case2_body="$(printf '%s\n' "$case2_out" | sed -n '2,$p')"
echo "HTTP: $case2_code"
echo "$case2_body"
if expect_code "$case2_code" "404"; then
  echo "RESULT: PASS"
else
  echo "RESULT: FAIL (expected 404)"
  overall=1
fi
echo

echo "[Case 3] bad token + good repo (expect 401 or 403)"
case3_out="$(submit_case "$BAD_TOKEN" "$REPO_SLUG")"
case3_code="$(printf '%s\n' "$case3_out" | sed -n '1p')"
case3_body="$(printf '%s\n' "$case3_out" | sed -n '2,$p')"
echo "HTTP: $case3_code"
echo "$case3_body"
if expect_code_set "$case3_code" "401" "403"; then
  echo "RESULT: PASS"
else
  echo "RESULT: FAIL (expected 401/403)"
  overall=1
fi
echo

if [[ "$overall" -ne 0 ]]; then
  echo "Permission smoke test FAILED." >&2
  exit 1
fi

echo "Permission smoke test PASSED."
