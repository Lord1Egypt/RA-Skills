#!/usr/bin/env bash
# create-github-issue.sh — Create a GitHub issue documenting a template update.
#
# Usage:
#   create-github-issue.sh <repo> <title> <body-file>
#
# Environment:
#   GITHUB_TOKEN — GitHub personal access token (required if gh not authed)
#
# Requirements: gh (GitHub CLI) or curl + jq

set -euo pipefail

REPO="${1:?Usage: $0 <owner/repo> <title> <body-file>}"
TITLE="${2:?Usage: $0 <owner/repo> <title> <body-file>}"
BODY_FILE="${3:?Usage: $0 <owner/repo> <title> <body-file>}"

if [[ ! -f "$BODY_FILE" ]]; then
  echo "Error: body file not found: $BODY_FILE" >&2
  exit 1
fi

# Prefer gh CLI if available and authed
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  gh issue create \
    --repo "$REPO" \
    --title "$TITLE" \
    --body-file "$BODY_FILE" \
    --label "documentation" \
    --label "i18n"
else
  # Fallback to API
  : "${GITHUB_TOKEN:?Set GITHUB_TOKEN or authenticate with 'gh auth login'}"
  BODY=$(cat "$BODY_FILE")
  curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" \
      '{title: $t, body: $b, labels: ["documentation", "i18n"]}')" \
    "https://api.github.com/repos/$REPO/issues" | jq -r '.html_url'
fi
