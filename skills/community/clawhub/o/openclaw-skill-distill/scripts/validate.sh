#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage: validate.sh <skill-directory>

Pre-publish validation for a skill directory. Checks:
  - SKILL.md exists with valid frontmatter (name + description)
  - Directory structure is compliant
  - No hardcoded paths or secrets (via scan.sh)
  - No .git or node_modules directories
  - No oversized files (>1MB)

Output: PASS or FAIL with details.
EOF
  exit 1
}

[[ $# -lt 1 ]] && usage
SKILL_DIR="$1"
[[ ! -d "$SKILL_DIR" ]] && echo "ERROR: '$SKILL_DIR' is not a directory" && exit 1

ERRORS=0

fail() {
  echo "FAIL: $1"
  ERRORS=$((ERRORS + 1))
}

pass() {
  echo "  OK: $1"
}

echo "=== Validating skill: $SKILL_DIR ==="
echo ""

# 1. SKILL.md exists
SKILL_MD="$SKILL_DIR/SKILL.md"
if [[ ! -f "$SKILL_MD" ]]; then
  fail "SKILL.md not found"
else
  pass "SKILL.md exists"

  # Check frontmatter
  if ! head -1 "$SKILL_MD" | grep -q '^---'; then
    fail "SKILL.md missing frontmatter (no opening ---)"
  else
    FRONTMATTER=$(awk 'NR==1{next} /^---$/{exit} {print}' "$SKILL_MD")

    if echo "$FRONTMATTER" | grep -q '^name:'; then
      pass "SKILL.md has 'name' field"
    else
      fail "SKILL.md frontmatter missing 'name'"
    fi

    if echo "$FRONTMATTER" | grep -q '^description:'; then
      pass "SKILL.md has 'description' field"
    else
      fail "SKILL.md frontmatter missing 'description'"
    fi
    # Check frontmatter fields are English-only (no CJK characters)
    NAME_VAL=$(echo "$FRONTMATTER" | grep '^name:' | sed 's/^name:[[:space:]]*//')
    DESC_VAL=$(echo "$FRONTMATTER" | grep '^description:' | sed 's/^description:[[:space:]]*//')
    if echo "${NAME_VAL}${DESC_VAL}" | grep -Pq '[\x{4e00}-\x{9fff}]'; then
      fail "SKILL.md frontmatter contains Chinese characters. Use English only for ClawHub publishing."
    else
      pass "SKILL.md frontmatter is English-only"
    fi
  fi
fi

# 2. No .git directory
if [[ -d "$SKILL_DIR/.git" ]]; then
  fail ".git directory found — must be removed before publish"
else
  pass "No .git directory"
fi

# 3. No node_modules
if [[ -d "$SKILL_DIR/node_modules" ]]; then
  fail "node_modules directory found — must be removed before publish"
else
  pass "No node_modules directory"
fi

# 4. Directory structure compliance (known dirs only)
while IFS= read -r dir; do
  dirname=$(basename "$dir")
  case "$dirname" in
    scripts|references|assets|templates|examples) ;;
    .*) ;; # hidden dirs already checked
    *) fail "Non-standard directory: $dir (allowed: scripts/ references/ assets/ templates/ examples/)" ;;
  esac
done < <(find "$SKILL_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)

# 5. File size check (<1MB each)
while IFS= read -r bigfile; do
  size=$(stat -c%s "$bigfile" 2>/dev/null || echo 0)
  if [[ "$size" -gt 1048576 ]]; then
    fail "Oversized file (>1MB): $bigfile ($(( size / 1024 ))KB)"
  fi
done < <(find "$SKILL_DIR" -type f -not -path '*/.git/*' 2>/dev/null)

# 6. No hardcoded paths / secrets (via scan.sh)
echo ""
echo "--- Running scan.sh ---"
if bash "$SCRIPT_DIR/scan.sh" "$SKILL_DIR" >/dev/null 2>&1; then
  pass "No local traces found (scan.sh clean)"
else
  fail "scan.sh found local traces — run scan.sh manually for details"
fi

# Result
echo ""
echo "========================"
if [[ "$ERRORS" -eq 0 ]]; then
  echo "RESULT: PASS"
  exit 0
else
  echo "RESULT: FAIL ($ERRORS issues)"
  exit 1
fi
