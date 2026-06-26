#!/usr/bin/env bash
set -euo pipefail

VAULT_ROOT="${NOTES_VAULT_ROOT:-/root/obsidian-vault}"
BRANCH="${NOTES_GIT_BRANCH:-}"

cd "$VAULT_ROOT"

if [[ ! -d .git ]]; then
  echo "Vault is not a git repository: $VAULT_ROOT" >&2
  exit 1
fi

git fetch --all --prune

if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
  git add -A
  if ! git diff --cached --quiet; then
    git commit -m "notes update $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  fi
fi

CURRENT_BRANCH="${BRANCH:-$(git branch --show-current)}"
if [[ -z "$CURRENT_BRANCH" ]]; then
  echo "Unable to determine git branch." >&2
  exit 1
fi

git pull --rebase --autostash origin "$CURRENT_BRANCH"
git push origin "$CURRENT_BRANCH"
