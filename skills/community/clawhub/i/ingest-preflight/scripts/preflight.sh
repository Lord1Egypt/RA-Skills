#!/usr/bin/env bash
# preflight.sh - Validate a ClawHub skill folder BEFORE publishing.
# Usage: preflight.sh <skill-folder> [--slug <slug>]
#
# Exit 0 if the folder is ready for `clawhub publish`, 1 otherwise.
set -euo pipefail

RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; NC=$'\033[0m'
ok=0; fail=0

pass() { echo "${GREEN}[PASS]${NC} $1"; ok=$((ok+1)); }
warn() { echo "${YELLOW}[WARN]${NC} $1"; }
bad()  { echo "${RED}[FAIL]${NC} $1"; fail=$((fail+1)); }

dir="${1:-}"
slug=""
if [[ "${2:-}" == "--slug" && -n "${3:-}" ]]; then slug="$3"; fi

if [[ -z "$dir" || ! -d "$dir" ]]; then
  echo "Usage: $0 <skill-folder> [--slug <slug>]"; exit 2
fi

echo "== preflight: $dir =="

# 1. Required entry file
if [[ -f "$dir/SKILL.md" ]]; then
  pass "SKILL.md exists"
else
  bad "SKILL.md is missing (required by ClawHub)"
fi

# 2. Frontmatter present and parseable
if [[ -f "$dir/SKILL.md" ]]; then
  if head -n1 "$dir/SKILL.md" | grep -q '^---'; then
    pass "frontmatter block starts with ---"
    # extract the frontmatter body (between first and second ---)
    fm=$(awk '/^---$/{c++; if(c==2) exit; if(c==1) next} c==1' "$dir/SKILL.md")
    for key in name description; do
      if echo "$fm" | grep -qE "^${key}:"; then
        pass "frontmatter has '${key}'"
      else
        bad "frontmatter is missing '${key}' (required)"
      fi
    done
  else
    bad "SKILL.md has no frontmatter (must start with ---)"
  fi
fi

# 3. references/ directory (recommended for supporting material)
if [[ -d "$dir/references" ]]; then
  pass "references/ directory present"
else
  warn "references/ directory missing (optional but recommended)"
fi

# 4. No giant binary blobs in the folder
big=$(find "$dir" -type f -size +2M 2>/dev/null | head -n1 || true)
if [[ -z "$big" ]]; then
  pass "no files > 2M (keeps the skill lean)"
else
  warn "large file found: $big (consider moving it out of the skill folder)"
fi

# 5. ClawHub CLI available and authenticated
if command -v clawhub >/dev/null 2>&1; then
  pass "clawhub CLI found"
  if clawhub whoami >/dev/null 2>&1; then
    pass "clawhub identity: $(clawhub whoami 2>/dev/null)"
  else
    bad "clawhub is not authenticated (run: clawhub login)"
  fi
else
  bad "clawhub CLI not found (install the clawhub tool)"
fi

# 6. Slug uniqueness (best-effort, network)
if [[ -n "$slug" ]]; then
  if clawhub inspect "$slug" >/dev/null 2>&1; then
    bad "slug '$slug' already exists on ClawHub (pick a unique one)"
  else
    pass "slug '$slug' appears available"
  fi
else
  warn "no --slug given; cannot check slug uniqueness"
fi

# 7. Dry-run publish (authoritative structural check)
if command -v clawhub >/dev/null 2>&1 && [[ -f "$dir/SKILL.md" ]]; then
  echo "-- running clawhub dry-run --"
  if clawhub publish "$dir" --dry-run --slug "${slug:-preflight-check}" --name "preflight-check" --tags "preflight" >/dev/null 2>&1; then
    pass "clawhub dry-run accepted the folder structure"
  else
    echo "(dry-run output follows)"
    clawhub publish "$dir" --dry-run --slug "${slug:-preflight-check}" --name "preflight-check" --tags "preflight" || true
    bad "clawhub dry-run rejected the folder (see output above)"
  fi
fi

echo "== summary: ${GREEN}${ok} passed${NC}, ${RED}${fail} failed${NC} =="
[[ "$fail" -eq 0 ]]
