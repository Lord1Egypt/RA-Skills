#!/usr/bin/env bash
# Worktree bootstrap — link/copy/generate resources a fresh git worktree needs.
#
# Triggered by:
#   - .claude/settings.json SessionStart hook (auto on Claude Code session)
#   - manual: bash scripts/setup-worktree.sh
#   - .claude/settings.json WorktreeCreate hook (Claude Code `--worktree`)
#
# Customise: edit the "resource declarations" section near the bottom.

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve main repo (works from any worktree; no hard-coded paths).
# ---------------------------------------------------------------------------
MAIN_REPO=$(cd "$(git rev-parse --git-common-dir)/.." && pwd)
CURRENT_DIR=$(pwd)

if [ "$MAIN_REPO" = "$CURRENT_DIR" ]; then
  echo "Already in main repo, nothing to bootstrap."
  exit 0
fi

echo "Main repo:  $MAIN_REPO"
echo "Worktree:   $CURRENT_DIR"
echo ""

# ---------------------------------------------------------------------------
# Helpers — idempotent + dead-symlink-safe.
# ---------------------------------------------------------------------------

# Symlink $MAIN_REPO/<rel> → $CURRENT_DIR/<rel>.
# Skips if main lacks it (no dead links). Skips if already linked.
# Removes existing real file/dir before linking (the worktree had a stub).
link_resource() {
  local rel=$1
  local target="$MAIN_REPO/$rel"
  local dest="$CURRENT_DIR/$rel"

  if [ ! -e "$target" ]; then
    echo "  skip   $rel  (not in main)"
    return
  fi
  if [ -L "$dest" ]; then
    echo "  skip   $rel  (already symlinked)"
    return
  fi
  if [ -e "$dest" ]; then
    rm -rf "$dest"
    echo "  replace $rel  -> $target"
  else
    echo "  link    $rel  -> $target"
  fi
  mkdir -p "$(dirname "$dest")"
  ln -s "$target" "$dest"
}

# Copy $MAIN_REPO/<rel> → $CURRENT_DIR/<rel> (never overwrite existing).
# Skips if main lacks it.
copy_resource() {
  local rel=$1
  local src="$MAIN_REPO/$rel"
  local dest="$CURRENT_DIR/$rel"

  if [ ! -e "$src" ]; then
    echo "  skip   $rel  (not in main)"
    return
  fi
  if [ -e "$dest" ]; then
    echo "  skip   $rel  (already exists)"
    return
  fi
  mkdir -p "$(dirname "$dest")"
  cp -R "$src" "$dest"
  echo "  copy    $rel  <- $src"
}

# Loop a glob under main and link each match (relative path preserved).
# Use for "all workspace node_modules" without enumerating each.
link_glob() {
  local pattern=$1
  local matched=0
  for abs in $MAIN_REPO/$pattern; do
    [ -e "$abs" ] || continue
    matched=1
    local rel="${abs#$MAIN_REPO/}"
    link_resource "$rel"
  done
  [ $matched -eq 0 ] && echo "  skip   $pattern  (no matches in main)"
  return 0
}

# Stable per-branch port: hash branch name → port in [3100, 9999].
# Usage:  PORT=$(hash_port "$(git -C "$CURRENT_DIR" branch --show-current)")
# For multiple ports on same branch, salt the input: hash_port "${BRANCH}-api"
hash_port() {
  local input=$1
  local hash
  hash=$(printf '%s' "$input" | shasum -a 1 | tr -d -c '0-9' | head -c 5)
  echo $(( (10#${hash:-0} % 6900) + 3100 ))
}

# Sanitised branch name suitable for COMPOSE_PROJECT_NAME, container names, etc.
# Keeps [a-zA-Z0-9-], replaces everything else with '-'.
clean_branch_name() {
  local raw=${1:-$(git -C "$CURRENT_DIR" branch --show-current)}
  printf '%s' "$raw" | tr '/' '-' | tr -d -c 'a-zA-Z0-9-'
}

# Idempotent KEY=value upsert into a dotenv-style file.
# Usage: upsert_env "$CURRENT_DIR/.env.local" DEV_PORT 4837
# Re-running with same value is a no-op; new value overwrites old in place.
upsert_env() {
  local file=$1 key=$2 val=$3
  mkdir -p "$(dirname "$file")"
  touch "$file"
  if grep -qE "^${key}=" "$file"; then
    # macOS sed needs '' after -i; use a portable workaround with a temp file
    local tmp; tmp=$(mktemp)
    awk -v k="$key" -v v="$val" 'BEGIN{FS=OFS="="} $1==k{$2=v; print; next} {print}' "$file" > "$tmp"
    mv "$tmp" "$file"
  else
    printf '%s=%s\n' "$key" "$val" >> "$file"
  fi
}

# ---------------------------------------------------------------------------
# Resource declarations — EDIT THIS BLOCK FOR YOUR REPO.
# ---------------------------------------------------------------------------

# Share — root hoisted deps + every workspace's local node_modules.
# (Critical for monorepos: bundlers resolve from apps/*/, not root.)
link_resource "node_modules"
link_glob    "apps/*/node_modules"
link_glob    "packages/*/node_modules"

# Share — local DB / state shared across worktrees so agents see same data.
link_resource "apps/api/.wrangler/state"

# Copy — secrets / per-worktree config (skips silently if main lacks it).
copy_resource "apps/api/.dev.vars"
# copy_resource ".env"
# copy_resource ".env.local"

# Generate — per-worktree port + container project name (uncomment as needed).
# BRANCH=$(git -C "$CURRENT_DIR" branch --show-current)
# DEV_PORT=$(hash_port "$BRANCH")
# API_PORT=$(hash_port "${BRANCH}-api")
# DB_PORT=$(hash_port "${BRANCH}-db")     # docker-compose host port for postgres etc
# upsert_env "$CURRENT_DIR/.env.local" DEV_PORT "$DEV_PORT"
# upsert_env "$CURRENT_DIR/.env.local" API_PORT "$API_PORT"
# upsert_env "$CURRENT_DIR/.env.local" POSTGRES_HOST_PORT "$DB_PORT"
# upsert_env "$CURRENT_DIR/.env.local" COMPOSE_PROJECT_NAME "$(clean_branch_name "$BRANCH")"
# echo "  generate .env.local  DEV_PORT=$DEV_PORT API_PORT=$API_PORT DB_PORT=$DB_PORT"

echo ""
echo "Bootstrap complete."
