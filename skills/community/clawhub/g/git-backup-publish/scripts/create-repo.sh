#!/bin/bash
# Quick repo creation for Gitee
# Usage: ./create-repo.sh <repo-name> [description]

REPO_NAME="${1:-}"
DESCRIPTION="${2:-OpenClaw Agent Backup}"
GITEE_TOKEN="${GITEE_TOKEN:-}"

if [[ -z "$REPO_NAME" ]]; then
    echo "Usage: ./create-repo.sh <repo-name> [description]"
    exit 1
fi

if [[ -z "$GITEE_TOKEN" ]]; then
    echo "Error: GITEE_TOKEN not set"
    exit 1
fi

curl -s -X POST "https://gitee.com/api/v5/user/repos" \
    -H "Content-Type: application/json" \
    -d "{
        \"access_token\": \"$GITEE_TOKEN\",
        \"name\": \"$REPO_NAME\",
        \"description\": \"$DESCRIPTION\",
        \"private\": true,
        \"has_issues\": false,
        \"has_wiki\": false,
        \"auto_init\": true
    }" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Repo: {d.get(\"html_url\", \"ERROR\")}') if 'html_url' in d else print(f'Error: {d}')"