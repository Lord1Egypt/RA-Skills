#!/bin/bash
# auto_commit.sh — Auto git commit workspace changes
# Cron: 0 * * * * (every hour)

WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE" || exit 1

if [ ! -d .git ]; then
    echo "Not a git repo, skipping"
    exit 0
fi

if git diff --quiet && git diff --cached --quiet; then
    exit 0
fi

git add -A
git commit -m "auto: $(date '+%Y-%m-%d %H:%M') hourly commit" --quiet 2>/dev/null || true
