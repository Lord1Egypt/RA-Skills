#!/bin/bash
set -e

# Git Deploy script
# Usage: scripts/deploy.sh "Commit message"

if [ -z "$1" ]; then
    echo "Usage: scripts/deploy.sh \"Commit message\""
    exit 1
fi

# Ensure we're in a git repo
if [ ! -d ".git" ]; then
    echo "Error: Not inside a git repository."
    exit 1
fi

log() { echo "$1"; }

log "Staging changes..."

git add .

# Check if there are changes
if git diff --cached --quiet; then
    log "No changes to commit."
    exit 0
fi

COMMIT_MSG="$1"
log "Committing with message: $COMMIT_MSG"

git commit -m "$COMMIT_MSG"

log "Pushing..."

git push

log "Deployment successful!"
