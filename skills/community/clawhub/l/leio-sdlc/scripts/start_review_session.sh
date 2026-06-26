#!/usr/bin/env bash
# Starts a code review session for a branch.

BRANCH="$1"

if [ -z "$BRANCH" ]; then
    echo "Usage: $0 <branch>"
    exit 1
fi

if [ -n "$MOCK_GIT_REPLY" ]; then
    BASE_SHA="$MOCK_GIT_REPLY"
else
    BASE_SHA=$(git merge-base origin/master "$BRANCH" 2>/dev/null || echo "")
fi

if [ -z "$BASE_SHA" ]; then
    echo "Error: Could not determine merge-base for branch '$BRANCH'."
    exit 1
fi

echo "Starting code review for branch '$BRANCH' from base SHA: $BASE_SHA"
exit 0