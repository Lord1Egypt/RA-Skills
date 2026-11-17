#!/usr/bin/env bash
set -euo pipefail

# github_issue.sh — Create a GitHub issue documenting a template update
#
# Usage:
#   bash github_issue.sh --repo <owner/repo> --title <title> --body-file <path>
#   bash github_issue.sh --repo <owner/repo> --title <title> --body "inline body"
#
# Environment:
#   GITHUB_TOKEN — Personal access token with repo scope
#   (or use `gh auth login` if gh CLI is available)

usage() {
  echo "Usage: $0 --repo <owner/repo> --title <title> (--body-file <path> | --body <text>)" >&2
  exit 1
}

REPO=""
TITLE=""
BODY=""
BODY_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)      REPO="$2"; shift 2 ;;
    --title)     TITLE="$2"; shift 2 ;;
    --body)      BODY="$2"; shift 2 ;;
    --body-file) BODY_FILE="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

[[ -z "$REPO" || -z "$TITLE" ]] && usage

if [[ -n "$BODY_FILE" ]]; then
  [[ -f "$BODY_FILE" ]] || { echo "Body file not found: $BODY_FILE" >&2; exit 1; }
  BODY=$(cat "$BODY_FILE")
fi

[[ -z "$BODY" ]] && { echo "Issue body is required (--body or --body-file)" >&2; usage; }

# Prefer gh CLI if available and authenticated
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  gh issue create --repo "$REPO" --title "$TITLE" --body "$BODY"
  echo "✅ Issue created via gh CLI"
  exit 0
fi

# Fallback: use GitHub REST API with token
: "${GITHUB_TOKEN:?Set GITHUB_TOKEN or install + authenticate gh CLI}"

PAYLOAD=$(jq -n --arg title "$TITLE" --arg body "$BODY" '{title: $title, body: $body}')

HTTP_CODE=$(curl -s -o /tmp/gh_resp.json -w "%{http_code}" \
  -X POST "https://api.github.com/repos/${REPO}/issues" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "$PAYLOAD")

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  ISSUE_URL=$(jq -r '.html_url' /tmp/gh_resp.json)
  echo "✅ Issue created: $ISSUE_URL"
else
  echo "❌ GitHub issue creation failed (HTTP $HTTP_CODE)" >&2
  cat /tmp/gh_resp.json >&2
  exit 1
fi
