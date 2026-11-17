#!/usr/bin/env bash
# sync-skill.sh — repo -> installed skill, the only legal direction.
#
# The installed skill is what the agent and the nightly cron load. Editing it
# directly is forbidden (see AGENTS.md Red Lines). This script copies the repo
# into the skill, preserving SKILL.md's YAML frontmatter (the repo omits it).
#
# Usage:
#   scripts/sync-skill.sh            # sync
#   scripts/sync-skill.sh --dry-run  # list what would change
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="${SKILL_DIR:-$HOME/.openclaw/workspace/skills/memory-health}"
SKILL_TRACE="${SKILL_TRACE:-$HOME/.openclaw/workspace/skills/trace-extractor/trace-extractor.py}"
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1

GRN=$'\033[32m'; YLW=$'\033[33m'; RST=$'\033[0m'
say() { echo "${GRN}  →${RST} $*"; }
skip() { echo "${YLW}  =${RST} $* (unchanged)"; }

# Plain files copied verbatim repo -> skill.
FILES=(
  README.md CHANGELOG.md
  auto_archive.py consolidate_advisor.py memory-health.py scoring.py ontology_compact.py
  hybrid-search/hybrid_search.py hybrid-search/compact.py
  hybrid-search/conflict_resolver.py hybrid-search/schema.sql
  hybrid-search/llm_resolution.py
  hybrid-search/test_loopback_guard.py
  hybrid-search/test_model_resolution.py
  hybrid-search/test_extract_atomic.py
  hybrid-search/test_ontology_key_parity.py
  hybrid-search/auto_capture.py hybrid-search/transcript_adapter.py
  docs/SECURITY-AUDIT-NOTES.md
  scripts/release.sh
)

[ -d "$SKILL_DIR" ] || { echo "skill dir not found: $SKILL_DIR"; exit 1; }

echo "sync repo -> skill: $SKILL_DIR"
for f in "${FILES[@]}"; do
  src="$REPO_DIR/$f"; dst="$SKILL_DIR/$f"
  [ -f "$src" ] || { echo "  ! missing in repo: $f"; continue; }
  mkdir -p "$(dirname "$dst")"
  if [ -f "$dst" ] && cmp -s "$src" "$dst"; then skip "$f"; continue; fi
  if [ $DRY -eq 1 ]; then say "would copy $f"; else cp -a "$src" "$dst"; say "$f"; fi
done

# SKILL.md: body from repo, frontmatter preserved from the skill copy.
echo "SKILL.md (frontmatter preserved)"
if [ $DRY -eq 1 ]; then
  say "would rebuild SKILL.md body"
else
  if [ -f "$REPO_DIR/SKILL.md" ] && head -1 "$REPO_DIR/SKILL.md" | grep -q '^---$'; then
    {
      if [ -f "$SKILL_DIR/SKILL.md" ] && head -1 "$SKILL_DIR/SKILL.md" | grep -q '^---$'; then
        sed -n '1,4p' "$SKILL_DIR/SKILL.md"
      else
        sed -n '1,4p' "$REPO_DIR/SKILL.md"
      fi
      cat "$REPO_DIR/SKILL.md" | tail -n +5
    } > "$SKILL_DIR/SKILL.md.tmp"
    mv "$SKILL_DIR/SKILL.md.tmp" "$SKILL_DIR/SKILL.md"
    say "SKILL.md body synced (frontmatter kept)"
  else
    cp -a "$REPO_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
    say "SKILL.md copied (no frontmatter found to preserve)"
  fi
fi

# trace_extractor: the skill copy is the LIVE one. Never overwrite it from the
# repo; report divergence and tell the operator to port forward instead.
echo "trace_extractor.py (single-source check)"
if [ -f "$SKILL_TRACE" ]; then
  if cmp -s "$REPO_DIR/trace_extractor.py" "$SKILL_TRACE"; then
    skip "trace_extractor.py"
  else
    echo "${YLW}  ! trace_extractor.py DIVERGES${RST}"
    echo "    live copy: $SKILL_TRACE"
    echo "    run:  cp '$SKILL_TRACE' '$REPO_DIR/trace_extractor.py'   # port live -> repo"
  fi
fi

echo
if [ $DRY -eq 1 ]; then echo "dry-run: nothing written."; else echo "${GRN}skill synced.${RST} now run: scripts/release.sh check"; fi
