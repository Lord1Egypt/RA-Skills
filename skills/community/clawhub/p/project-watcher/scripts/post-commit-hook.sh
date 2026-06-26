#!/bin/bash
# post-commit hook template
# Place this as .git/hooks/post-commit in any git project

GIT_HASH=$(git rev-parse --short HEAD)
GIT_MSG=$(git log -1 --pretty=%s)
# detached HEAD 时 branch --show-current 返回空，fallback 到 ref name
GIT_BRANCH=$(git branch --show-current 2>/dev/null) || \
             GIT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null) || \
             GIT_BRANCH="(detached)"
GIT_REPO=$(basename "$(git rev-parse --show-toplevel)")
SENDER="ou_303e303666b03ee6300a4944c8d77d16"

SKILL_DIR="/Volumes/File/OpenClaw/workspace/skills/project-watcher/scripts"
CARD_SCRIPT="$SKILL_DIR/send_card.py"

if [ -f "$CARD_SCRIPT" ]; then
    python3 "$CARD_SCRIPT" "$SENDER" "✅ 已提交" "$GIT_REPO" "$GIT_BRANCH" "$GIT_HASH" "$GIT_MSG"
fi
