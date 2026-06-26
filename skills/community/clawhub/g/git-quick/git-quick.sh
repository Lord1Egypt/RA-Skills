#!/usr/bin/env bash
# git-quick — Quick git repo summary
set -euo pipefail

MODE="${1:-}"

# --- Helpers ---
is_git_repo() {
  git rev-parse --is-inside-work-tree >/dev/null 2>&1
}

section() {
  echo ""
  echo "--- $1 ---"
}

if ! is_git_repo; then
  echo "Error: not a git repository." >&2
  exit 1
fi

# --- Branch info ---
if [[ -z "$MODE" || "$MODE" == "--short" ]]; then
  branch=$(git branch --show-current 2>/dev/null || echo "detached")
  remote=$(git config "branch.${branch}.remote" 2>/dev/null || echo "")
  if [[ -n "$remote" ]]; then
    ahead=$(git rev-list --count "${branch}..${remote}/${branch}" 2>/dev/null || echo "0")
    behind=$(git rev-list --count "${remote}/${branch}..${branch}" 2>/dev/null || echo "0")
    if [[ "$ahead" == "0" && "$behind" == "0" ]]; then
      tracking="(up to date with ${remote}/${branch})"
    else
      tracking="(ahead ${ahead}, behind ${behind} vs ${remote}/${branch})"
    fi
  else
    tracking="(no upstream)"
  fi
  echo "=== Git Quick Summary ==="
  echo "Branch: ${branch} ${tracking}"
fi

# --- Status ---
if [[ -z "$MODE" ]]; then
  section "Status"
  git status --short 2>/dev/null || echo "(clean)"
fi

# --- Recent commits ---
if [[ -z "$MODE" || "$MODE" == "--commits" ]]; then
  section "Recent Commits"
  git log --oneline -5 --format="%h %s  (%cr)" 2>/dev/null || echo "(no commits)"
fi

# --- Contributor stats ---
if [[ -z "$MODE" || "$MODE" == "--stats" ]]; then
  section "Top Contributors"
  git shortlog -sn --all 2>/dev/null | head -5 || echo "(no contributors)"
fi

echo ""
