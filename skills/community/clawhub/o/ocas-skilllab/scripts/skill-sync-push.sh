#!/usr/bin/env bash
# skill-sync-push.sh — commit + push all local skill repos that have changes.
# Idempotent: only touches repos with uncommitted changes OR commits ahead of their
# upstream; skips if secret-scan fails. Sets the the agent identity locally
# (the host global git config defaults to "Koda", a different profile).
# Author: Indigo Karasu. Invoked by cron 'ocas-skilllab-sync' (daily 04:00).
set -u
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "Usage: skill-sync-push.sh [SKILLS_ROOT]"
  echo "Commit + push every local skill repo under SKILLS_ROOT that has uncommitted changes"
  echo "or is ahead of its upstream. Skips repos where the secret-scan gate fails."
  echo "  DRY_RUN=1  -> no-op report (does not commit or push). Default: 0."
  echo "  Default SKILLS_ROOT: ~/.hermes/profiles/indigo/skills"
  exit 0
fi
SKILLS_ROOT="${1:-~/.hermes/profiles/indigo/skills}"
SECRET_SCAN="${SKILLS_ROOT}/ocas-skilllab/scripts/secret-scan.sh"
IDENTITY_NAME="the agent"
IDENTITY_EMAIL="<third-party-or-user-email>"
DRY_RUN="${DRY_RUN:-0}"
LOG=~/.hermes/profiles/indigo/cron/output/skill-sync-push.log
mkdir -p "$(dirname "$LOG")"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
log() { echo "[$(ts)] $*" | tee -a "$LOG"; }

log "=== skill-sync-push start (dry_run=$DRY_RUN) ==="
pushed=0; skipped=0; failed=0; secret_blocked=0

for d in "$SKILLS_ROOT"/*/; do
  [ -d "$d/.git" ] || continue
  git -C "$d" remote get-url origin >/dev/null 2>&1 || { skipped=$((skipped+1)); continue; }
  branch=$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null)
  # uncommitted work to commit?
  n=$(git -C "$d" status --porcelain 2>/dev/null | grep -vE '__pycache__|\.pyc' | wc -l)
  # committed-but-unpushed on the current branch?
  if git -C "$d" rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    ahead=$(git -C "$d" rev-list --count @{u}..HEAD 2>/dev/null || echo 0)
  else
    ahead=1  # no upstream configured -> treat as needing a push
  fi
  [ "$n" -gt 0 ] || [ "${ahead:-0}" -gt 0 ] || { skipped=$((skipped+1)); continue; }
  # secret gate
  if [ -x "$SECRET_SCAN" ]; then
    if ! bash "$SECRET_SCAN" "$d" >/dev/null 2>&1; then
      log "SECRET-BLOCKED: $name (skipping push; investigate manually)"
      secret_blocked=$((secret_blocked+1)); continue
    fi
  fi
  # set local identity (the agent, not the global Koda default)
  git -C "$d" config user.name "$IDENTITY_NAME" 2>/dev/null
  git -C "$d" config user.email "$IDENTITY_EMAIL" 2>/dev/null
  if [ "$DRY_RUN" = "1" ]; then
    log "DRY: would commit+push $name (uncommitted=$n, ahead=$ahead, $branch)"
    skipped=$((skipped+1)); continue
  fi
  if [ "$n" -gt 0 ]; then
    git -C "$d" add -A 2>&1 | head -1
    git -C "$d" reset -q HEAD __pycache__ 2>/dev/null
    git -C "$d" commit -q -m "chore: sync local skill changes ($(date -u +%Y-%m-%d))" 2>&1 | head -1
  fi
  if git -C "$d" rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    out=$(git -C "$d" push 2>&1); rc=$?
  else
    out=$(git -C "$d" push -u origin "$branch" 2>&1); rc=$?
  fi
  if [ $rc -eq 0 ]; then log "PUSHED: $name ($n files, $branch)"; pushed=$((pushed+1));
  else log "FAIL($rc): $name :: $(echo "$out" | head -2 | tr '\n' ' ')"; failed=$((failed+1)); fi
done
log "=== done: pushed=$pushed skipped=$skipped failed=$failed secret_blocked=$secret_blocked ==="