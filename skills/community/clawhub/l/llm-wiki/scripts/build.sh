#!/bin/bash
# Build the wiki static site and commit changes.
# Usage: bash scripts/build.sh [--push]

set -euo pipefail

WIKI_DIR="${HOME}/wiki"
PUSH=false

[[ "${1:-}" == "--push" ]] && PUSH=true

cd "${WIKI_DIR}"

# Rebuild static site
echo "🔨 Building wiki..."
mkdocs build 2>&1 | grep -E "INFO|ERROR" || true

# Git commit if there are changes
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  
  # Generate commit message from changed files
  CHANGED=$(git diff --cached --name-only | grep "^docs/" | sed 's|docs/||' | head -5)
  if [[ -n "${CHANGED}" ]]; then
    MSG="wiki: update $(echo "${CHANGED}" | tr '\n' ', ' | sed 's/,$//')"
  else
    MSG="wiki: update"
  fi
  
  git commit -m "${MSG}"
  
  if $PUSH && git remote get-url origin &>/dev/null; then
    git push
    echo "✅ Pushed to remote"
  fi
else
  echo "No changes to commit"
fi
