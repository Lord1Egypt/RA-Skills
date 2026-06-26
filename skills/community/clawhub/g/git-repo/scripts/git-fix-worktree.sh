#!/bin/bash
# git-fix-worktree.sh
# Fix bare repo worktree path in ghq structure
# Usage: git-fix-worktree.sh [repo_path]
# If no path given, fixes all bare repos in ghq root

set -euo pipefail

fix_repo() {
  local bare_repo="$1"
  local config_file="$bare_repo/config"

  [[ ! -f "$config_file" ]] && return 1

  # Check if bare=false and has worktree setting (broken state)
  if grep -q "bare = false" "$config_file" && grep -q "worktree = " "$config_file"; then
    local worktree_path
    worktree_path=$(git config -f "$config_file" core.worktree 2>/dev/null || true)

    if [[ -d "$worktree_path" && -f "$worktree_path/.git" ]]; then
      # Worktree exists but not registered - register it
      local wt_name
      wt_name=$(basename "$worktree_path")
      local wt_dir="$bare_repo/worktrees/$wt_name"

      mkdir -p "$wt_dir"
      echo "$worktree_path/.git" > "$wt_dir/gitdir"
      # Get actual HEAD from worktree, not bare repo
      git -C "$worktree_path" symbolic-ref HEAD 2>/dev/null > "$wt_dir/HEAD" \
        || git -C "$worktree_path" rev-parse HEAD > "$wt_dir/HEAD"
      echo "../.." > "$wt_dir/commondir"

      # Fix worktree's .git file to point to worktrees/ subdirectory
      echo "gitdir: $wt_dir" > "$worktree_path/.git"

      # Rebuild index if missing (preserves uncommitted changes)
      if [[ ! -f "$wt_dir/index" ]]; then
        git -C "$worktree_path" read-tree HEAD 2>/dev/null || true
        echo "  Rebuilt index"
      fi

      # Fix config: remove worktree, set bare=true
      git config -f "$config_file" --unset core.worktree 2>/dev/null || true
      git config -f "$config_file" core.bare true

      echo "Fixed: $bare_repo"
      echo "  Registered worktree: $worktree_path"
      echo "  Updated .git -> $wt_dir"
    else
      # Invalid worktree path - just clean up config
      git config -f "$config_file" --unset core.worktree 2>/dev/null || true
      git config -f "$config_file" core.bare true
      echo "Fixed: $bare_repo"
      echo "  Removed invalid worktree: $worktree_path"
    fi
  fi
}

main() {
  local ghq_root="${GHQ_ROOT:-$(ghq root 2>/dev/null || echo "$HOME/ghq")}"

  if [[ -z "$ghq_root" || ! -d "$ghq_root" ]]; then
    echo "Error: ghq root not found: $ghq_root" >&2
    exit 1
  fi

  if [[ -n "${1:-}" ]]; then
    fix_repo "$1"
  else
    echo "Scanning for broken bare repos in: $ghq_root"
    find "$ghq_root" -name "*.git" -type d | while read -r repo; do
      fix_repo "$repo"
    done
    echo "Done."
  fi
}

main "$@"
