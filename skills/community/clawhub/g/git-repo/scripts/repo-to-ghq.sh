#!/bin/bash
# repo-to-ghq.sh - Move Git repository to ghq directory structure
# Moves entire repo to ~/ghq/host/group/repo/ with regular .git directory
# Supports nested groups (e.g., myorg/devops/repo)
# Handles bare+worktree structure conversion
#
# Options:
#   --no-symlink       Skip symlink creation at original location
#   --remap-origin URL Replace origin remote URL after migration

set -e

NO_SYMLINK=false
REMAP_ORIGIN=""

# Parse flags
while [[ "$1" == --* ]]; do
  case "$1" in
    --no-symlink) NO_SYMLINK=true; shift ;;
    --remap-origin) REMAP_ORIGIN="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Get ghq path from git origin (without .git suffix for working directory)
ghq_path() {
  local origin_url=$(git remote get-url origin 2>/dev/null)
  [[ -z "$origin_url" ]] && return 1

  local host group repo_name

  # Remove user@ from HTTP URLs (e.g., http://user@host/...)
  origin_url=$(echo "$origin_url" | sed -E 's|^(https?://)[^@]*@|\1|')

  # HTTPS/HTTP: https://host/group/repo.git or http://host/group/repo
  if [[ $origin_url =~ ^https?://([^/]+)/(.+)/([^/]+)$ ]]; then
    host=${BASH_REMATCH[1]}
    group=${BASH_REMATCH[2]}
    repo_name=${BASH_REMATCH[3]%.git}
  # SSH: git@host:group/repo.git
  elif [[ $origin_url =~ ^git@([^:]+):(.+)/([^/]+)$ ]]; then
    host=${BASH_REMATCH[1]}
    group=${BASH_REMATCH[2]}
    repo_name=${BASH_REMATCH[3]%.git}
  # SSH with ssh:// prefix: ssh://git@host/group/repo.git
  elif [[ $origin_url =~ ^ssh://(.+)/(.+)/([^/]+)$ ]]; then
    local host_part=${BASH_REMATCH[1]}
    host=${host_part#*@} # Remove user@ if present
    group=${BASH_REMATCH[2]}
    repo_name=${BASH_REMATCH[3]%.git}
  else
    return 1
  fi

  echo "$HOME/ghq/$host/$group/$repo_name"
}

# Resolve path (works for non-existent paths on macOS)
resolve_path() {
  python3 -c "import os, sys; print(os.path.abspath(sys.argv[1]))" "$1"
}

# Convert .git file (worktree or bare+worktree) to regular .git directory
convert_worktree_to_regular() {
  [[ -f .git ]] || return 0

  # Read gitdir from .git file
  local gitdir=$(sed 's/^gitdir: //' .git | xargs)

  # Resolve relative path
  if [[ "$gitdir" != /* ]]; then
    gitdir=$(resolve_path "$gitdir")
  fi

  if [[ ! -d "$gitdir" ]]; then
    echo "Error: Git directory '$gitdir' not found (resolved from .git file)."
    exit 1
  fi

  # Detect type: git worktree (has commondir) vs bare+worktree (no commondir)
  if [[ -f "$gitdir/commondir" ]]; then
    convert_git_worktree "$gitdir"
  else
    convert_bare_worktree "$gitdir"
  fi
}

# Convert a git worktree (.git file → bare.git/worktrees/<name>/) to regular repo
convert_git_worktree() {
  local wt_gitdir="$1"
  echo "Detected git worktree, converting..."

  # Save worktree's HEAD (branch/commit it was on)
  local wt_head=$(cat "$wt_gitdir/HEAD")

  # Resolve bare repo path via commondir
  local commondir_val=$(cat "$wt_gitdir/commondir")
  local bare_repo
  if [[ "$commondir_val" = /* ]]; then
    bare_repo="$commondir_val"
  else
    bare_repo=$(cd "$wt_gitdir" && resolve_path "$commondir_val")
  fi

  if [[ ! -d "$bare_repo" ]]; then
    echo "Error: Bare repo '$bare_repo' not found (from commondir)."
    exit 1
  fi

  # Check if bare repo has other worktrees
  local wt_name=$(basename "$wt_gitdir")
  local other_wt_count=0
  if [[ -d "$bare_repo/worktrees" ]]; then
    local total_wts=$(ls "$bare_repo/worktrees" 2>/dev/null | wc -l | tr -d ' ')
    other_wt_count=$((total_wts - 1))
  fi

  # Remove .git file
  rm .git

  if [[ "$other_wt_count" -gt 0 ]]; then
    # Other worktrees exist - copy bare repo to preserve them
    echo "Bare repo has $other_wt_count other worktree(s), copying..."
    cp -R "$bare_repo" .git
    rm -rf .git/worktrees
  else
    # No other worktrees - move bare repo (clean up worktrees dir)
    rm -rf "$bare_repo/worktrees" 2>/dev/null
    mv "$bare_repo" .git
  fi

  # Configure as regular repo
  git config --bool core.bare false
  git config --unset core.worktree 2>/dev/null || true

  # Restore worktree's HEAD
  echo "$wt_head" > .git/HEAD

  # Rebuild index for the working tree
  git read-tree HEAD
  git checkout-index -a -f 2>/dev/null || true

  # Clean up empty parent directories (only if bare repo was moved)
  if [[ "$other_wt_count" -eq 0 ]]; then
    cleanup_empty_parents "$(dirname "$bare_repo")"
  fi

  echo "Converted from git worktree to regular .git directory."
}

# Convert bare+worktree (.git file → bare.git/) to regular repo
convert_bare_worktree() {
  local gitdir="$1"
  echo "Detected bare+worktree structure, converting..."

  # Capture pre-conversion status
  local pre_status
  pre_status=$(git status --porcelain 2>/dev/null || true)

  # Remove .git file and move bare repo
  rm .git
  mv "$gitdir" .git

  # Configure as regular repo
  git config --bool core.bare false
  git config --unset core.worktree 2>/dev/null || true

  # Verify index integrity
  local post_status
  post_status=$(git status --porcelain 2>/dev/null || true)
  if [[ "$pre_status" != "$post_status" ]]; then
    echo "WARNING: Git status changed after conversion. Rebuilding index..."
    git read-tree HEAD
    echo "Index rebuilt from HEAD."
  fi

  cleanup_empty_parents "$(dirname "$gitdir")"
  echo "Converted to regular .git directory."
}

# Remove empty parent directories up to ~/ghq
cleanup_empty_parents() {
  local parent_dir="$1"
  while [[ "$parent_dir" != "$HOME/ghq" ]] && [[ -d "$parent_dir" ]]; do
    if [[ -z "$(ls -A "$parent_dir" 2>/dev/null)" ]]; then
      rmdir "$parent_dir"
      parent_dir=$(dirname "$parent_dir")
    else
      break
    fi
  done
}

# Main function
main() {
  local src_path="$PWD"

  # Check if current directory is a Git repository
  if [[ ! -d .git ]] && [[ ! -f .git ]]; then
    echo "Error: This is not a Git repository."
    exit 1
  fi

  # Convert bare+worktree to regular if needed
  convert_worktree_to_regular

  local new_ghq_path
  if [[ -z "$1" ]]; then
    new_ghq_path=$(ghq_path)
  else
    # Use python3 os.path.abspath (works for non-existent paths on macOS)
    new_ghq_path=$(python3 -c "import os, sys; print(os.path.abspath(sys.argv[1]))" "$1")
  fi

  if [[ -z "$new_ghq_path" ]]; then
    echo "Usage: repo-to-ghq.sh [--no-symlink] [--remap-origin URL] [target_path]"
    echo "If target_path is not specified, it will be derived from git origin URL."
    exit 1
  fi

  # Check if target path already exists
  if [[ -e "$new_ghq_path" ]]; then
    echo "Error: Target path '$new_ghq_path' already exists."
    exit 1
  fi

  # Create parent directory
  mkdir -p "$(dirname "$new_ghq_path")"

  # Move entire directory to ghq path
  mv "$src_path" "$new_ghq_path"

  echo "Repository moved to '$new_ghq_path'."

  # Remap origin URL if requested
  if [[ -n "$REMAP_ORIGIN" ]]; then
    git -C "$new_ghq_path" remote set-url origin "$REMAP_ORIGIN"
    echo "Origin remapped to '$REMAP_ORIGIN'."
  fi

  # Create symlink at original location (optional)
  if [[ "$NO_SYMLINK" == false ]]; then
    ln -s "$new_ghq_path" "$src_path"
    echo "Symlink created at '$src_path' -> '$new_ghq_path'."
  fi

  # Post-migration index verification
  local verify_status
  verify_status=$(git -C "$new_ghq_path" status --porcelain 2>&1)
  if [[ $? -ne 0 ]]; then
    echo "WARNING: git status failed after migration. Index may be corrupted."
    echo "Attempting index rebuild..."
    git -C "$new_ghq_path" read-tree HEAD
    echo "Index rebuilt."
  fi
}

main "$@"
