#!/bin/bash
# Self-update for ocas-sift.
#
# SAFE BY DEFAULT: without --force this does a non-destructive fetch +
# ff-only pull. Local journals/data are never touched; a diverged worktree
# aborts with instructions instead of being clobbered.
#
# --force: destructive sync to the latest pushed state (git reset --hard +
# git clean -fd). Use only when the worktree is knowingly dirty or corrupted;
# this DISCARDS all local modifications. Why it exists: a failed rebase or a
# half-applied edit can leave the repo un-pullable, and the daily cron needs a
# recovery path that does not require hands on the box.
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "Usage: update.sh [--force]"
  echo "  Safe by default: fetch + ff-only pull; aborts on local divergence."
  echo "  --force   Destructive: hard-reset and clean to the latest pushed state"
  echo "            (discards ALL local changes). Recovery path only."
  echo "  --help,-h Show this message and exit."
  exit 0
fi

case "${1:-}" in
  ""|--force) ;;
  *)
    echo "[sift:update] unknown flag: $1 (expected --force or --help)" >&2
    exit 64 ;;
esac

cd "$(dirname "$0")/.." || exit 1

if [ "${1:-}" = "--force" ]; then
  echo "[sift:update] --force: discarding local changes (reset --hard + clean -fd)" >&2
  git reset --hard HEAD 2>/dev/null
  git clean -fd 2>/dev/null
  git pull 2>/dev/null
else
  if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    echo "[sift:update] worktree has uncommitted changes; skipping pull." \
         "Run '$0 --force' to discard them, or commit/stash first." >&2
    exit 3
  fi
  git fetch origin 2>/dev/null || exit 2
  # Abort rather than merge/rebase: divergence means someone edited the skill
  # locally and auto-merging could silently break the running pipeline.
  git pull --ff-only 2>/dev/null || {
    echo "[sift:update] local branch diverged from origin; refusing auto-merge." \
         "Inspect manually or run '$0 --force' to discard local state." >&2
    exit 4
  }
fi
