#!/usr/bin/env bash
# release.sh — OpenClaw Memory Toolkit release gate.
#
# Turns "verify before confirming" into a mechanism: it refuses to tag until the
# repo, the installed skill and the documented invariants agree.
#
# Pipeline it enforces:  local repo  ->  skill  ->  GitHub  ->  (ClawHub, manual)
#
# Usage:
#   scripts/release.sh check                 # verify only, no mutation
#   scripts/release.sh release vX.Y.Z "msg"  # check, tag, push tag
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="${SKILL_DIR:-$HOME/.openclaw/workspace/skills/memory-health}"
SKILL_TRACE="${SKILL_TRACE:-$HOME/.openclaw/workspace/skills/trace-extractor/trace-extractor.py}"

RED=$'\033[31m'; GRN=$'\033[32m'; YLW=$'\033[33m'; RST=$'\033[0m'
ok()   { echo "${GRN}  OK${RST}  $*"; }
bad()  { echo "${RED}  ✗  $*${RST}"; FAILED=1; }
warn() { echo "${YLW}  !  $*${RST}"; }
FAILED=0

cd "$REPO_DIR"

SYNC_FILES=(
  SKILL.md README.md CHANGELOG.md
  auto_archive.py consolidate_advisor.py memory-health.py scoring.py ontology_compact.py
  hybrid-search/hybrid_search.py hybrid-search/compact.py
  hybrid-search/conflict_resolver.py hybrid-search/schema.sql
  hybrid-search/test_loopback_guard.py hybrid-search/test_model_resolution.py
  hybrid-search/test_meta_gate.py hybrid-search/test_extract_atomic.py
  hybrid-search/test_ontology_key_parity.py hybrid-search/test_orphan_link.py
  docs/SECURITY-AUDIT-NOTES.md
  hybrid-search/auto_capture.py hybrid-search/transcript_adapter.py
)

echo "== 1. repo <-> skill sync =="
for f in "${SYNC_FILES[@]}"; do
  r="$REPO_DIR/$f"; s="$SKILL_DIR/$f"
  [ -f "$r" ] || { bad "missing in repo: $f"; continue; }
  [ -f "$s" ] || { bad "missing in skill: $f"; continue; }
  if cmp -s "$r" "$s"; then
    ok "$f"
  elif [ "$f" = "SKILL.md" ]; then
    if diff -q <(tail -n +5 "$s") <(cat "$r") >/dev/null 2>&1; then
      ok "$f (body matches; skill frontmatter preserved)"
    else
      bad "$f body differs repo<->skill"
    fi
  else
    bad "$f differs repo<->skill"
  fi
done

echo "== 2. single source: trace_extractor =="
if [ -f "$SKILL_TRACE" ]; then
  if cmp -s "$REPO_DIR/trace_extractor.py" "$SKILL_TRACE"; then
    ok "trace_extractor.py repo == skill copy (identical)"
  else
    warn "trace_extractor.py differs from $SKILL_TRACE"
    warn "  the skill copy is the live one (cron uses it); port it into the repo"
  fi
else
  warn "trace-extractor skill copy not found at $SKILL_TRACE"
fi

echo "== 3. version markers agree =="
V_CHANGELOG="$(grep -m1 '^## v' CHANGELOG.md | sed -E 's/^## (v[0-9.]+).*/\1/')"
V_SKILL="$(grep -o 'current release v[0-9]\+\.[0-9]\+\.[0-9]\+' SKILL.md | head -1 | grep -o 'v[0-9]\+\.[0-9]\+\.[0-9]\+' || true)"
[ -z "$V_SKILL" ] && V_SKILL="$(grep -o 'v[0-9]\+\.[0-9]\+\.[0-9]\+' SKILL.md | head -1 || true)"
[ -n "$V_CHANGELOG" ] && ok "CHANGELOG latest: $V_CHANGELOG" || bad "no version in CHANGELOG.md"
if [ -n "$V_SKILL" ]; then
  if [ "$V_SKILL" = "$V_CHANGELOG" ]; then ok "SKILL.md marker matches: $V_SKILL"
  else warn "SKILL.md marker ($V_SKILL) != CHANGELOG ($V_CHANGELOG)"; fi
else
  warn "no explicit version marker in SKILL.md"
fi

echo "== 4. documented invariants present =="
grep -q "ALLOWED_OLLAMA_HOSTS" hybrid-search/hybrid_search.py && ok "loopback allowlist present" || bad "loopback allowlist missing"
grep -q "get_safe_ollama_url" hybrid-search/conflict_resolver.py && ok "conflict_resolver guards URLs" || bad "conflict_resolver guard missing"
# llm_resolution.py is the shared, loopback-by-design resolver (v4.0): its single
# OLLAMA_URL read is the documented source of the safety-net endpoint. It is not
# an unguarded script-level read; the whole module exists to police that URL.
grep -q "OLLAMA_LOCAL_URL" hybrid-search/llm_resolution.py && ok "llm_resolution: loopback resolver present" || warn "llm_resolution.py missing"
UNG_VIOL=0
while IFS= read -r line; do
  code="${line%%#*}"   # strip trailing comment before matching
  case "$code" in
    *get_safe_ollama_url*) continue ;;
    *llm_resolution.py*) continue ;;
  esac
  if printf '%s' "$code" | grep -Eq 'os\.environ.*"(OLLAMA_URL|OLLAMA_GEN_URL|OLLAMA_EMBED_URL)"'; then
    bad "unguarded OLLAMA_* URL read: $line"; UNG_VIOL=1
  fi
done < <(grep -rn --include=*.py -E 'os\.environ.*"(OLLAMA_URL|OLLAMA_GEN_URL|OLLAMA_EMBED_URL)"' . | grep -v "__pycache__" || true)
[ "$UNG_VIOL" -eq 0 ] && ok "no unguarded OLLAMA_* URL read"

echo "== 4c. SKILL.md frontmatter present =="
if head -1 "$REPO_DIR/SKILL.md" | grep -q '^---$'; then
  grep -q '^name:' "$REPO_DIR/SKILL.md" && ok "frontmatter: name present" || bad "frontmatter: missing 'name:'"
  grep -q '^description:' "$REPO_DIR/SKILL.md" && ok "frontmatter: description present" || bad "frontmatter: missing 'description:'"
else
  bad "SKILL.md frontmatter missing (must start with ---)"
fi

echo "== 5. python syntax =="
# Interpreter for syntax + test steps. Must have sqlite_vec: hybrid_search imports
# it at module level, so a bare `python3` makes test_loopback_guard fail with a
# misleading 'sqlite-vec is not installed' error (seen 2026-10-06). Prefer the
# skill venv — the interpreter the toolkit actually runs under — then the old
# scratch venv, then whatever python3 we have.
PYBIN="${SKILL_DIR:-$HOME/.openclaw/workspace/skills/memory-health}/.venv/bin/python"
[ -x "$PYBIN" ] || PYBIN="/tmp/v22-vec/bin/python"
[ -x "$PYBIN" ] || PYBIN="python3"
if ! "$PYBIN" -c 'import sqlite_vec' >/dev/null 2>&1; then
  warn "$PYBIN lacks sqlite_vec — guard tests may fail spuriously"
fi
for f in "$REPO_DIR"/*.py "$REPO_DIR"/hybrid-search/*.py; do
  "$PYBIN" -c "import ast,sys; ast.parse(open('$f').read())" 2>/dev/null \
    && ok "$(basename "$f")" || bad "syntax: $(basename "$f")"
done

echo "== 6. loopback guard test =="
"$PYBIN" hybrid-search/test_loopback_guard.py >/dev/null 2>&1 \
  && ok "test_loopback_guard.py passes" || bad "test_loopback_guard.py FAILED"

"$PYBIN" hybrid-search/test_model_resolution.py >/dev/null 2>&1 \
  && ok "test_model_resolution.py passes" || bad "test_model_resolution.py FAILED"

"$PYBIN" hybrid-search/test_meta_gate.py >/dev/null 2>&1 \
  && ok "test_meta_gate.py passes" || bad "test_meta_gate.py FAILED"

"$PYBIN" hybrid-search/test_extract_atomic.py >/dev/null 2>&1 \
  && ok "test_extract_atomic.py passes" || bad "test_extract_atomic.py FAILED"

"$PYBIN" hybrid-search/test_ontology_key_parity.py >/dev/null 2>&1 \
  && ok "test_ontology_key_parity.py passes" || bad "test_ontology_key_parity.py FAILED"

"$PYBIN" hybrid-search/test_orphan_link.py >/dev/null 2>&1 \
  && ok "test_orphan_link.py passes" || bad "test_orphan_link.py FAILED"

echo "== 7. git hygiene =="
if [ -n "$(git status --porcelain)" ]; then
  warn "working tree not clean (commit before release):"; git status --short
else
  ok "working tree clean"
fi

echo
if [ "${1:-check}" = "release" ]; then
  VERSION="${2:-}"; MSG="${3:-}"
  if [ $FAILED -ne 0 ]; then echo "${RED}Release aborted: checks failed.${RST}"; exit 1; fi
  [ -n "$VERSION" ] || { echo "usage: release.sh release vX.Y.Z \"msg\""; exit 2; }
  if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null; then
    echo "${RED}tag $VERSION already exists${RST}"; exit 1
  fi
  git tag -a "$VERSION" -m "${MSG:-$VERSION}"
  git push origin "$VERSION"
  # `git push origin <tag>` pushes ONLY the tag. Without this, main stays
  # behind the released commit and a fresh clone misses the release — exactly
  # the v3.3.0 mishap. Push the current branch too, and skip silently if it is
  # already level with its upstream.
  BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  if git rev-parse -q --verify "refs/remotes/origin/$BRANCH" >/dev/null; then
    if [ "$(git rev-parse "$BRANCH")" != "$(git rev-parse "origin/$BRANCH")" ]; then
      git push origin "$BRANCH" && echo "${GRN}pushed branch $BRANCH${RST}"
    else
      echo "branch $BRANCH already up to date with origin"
    fi
  else
    git push -u origin "$BRANCH" && echo "${GRN}pushed new branch $BRANCH${RST}"
  fi
  echo "${GRN}tagged and pushed $VERSION${RST}"
  echo "next: GitHub release, then ClawHub (manual, Stéphane)."
else
  if [ $FAILED -ne 0 ]; then echo "${RED}CHECK FAILED${RST}"; exit 1; fi
  echo "${GRN}All checks passed — safe to release.${RST}"
fi
