#!/usr/bin/env bash
# grep_antipatterns.sh
# Quick pre-scan for common UGLIC anti-patterns in a skill / code / doc target.
# This is a *helper* for the U dimension — surfaces likely findings before the
# agent runs the full UGLIC checklist; the agent still has to judge severity
# and cite locations precisely.
#
# Usage:
#   bash scripts/grep_antipatterns.sh <target-dir-or-file>
#   bash scripts/grep_antipatterns.sh .
#   bash scripts/grep_antipatterns.sh ~/.openclaw/workspace/skills/some-skill

set -u

TARGET="${1:-.}"

if [ ! -e "$TARGET" ]; then
  echo "❌ Target not found: $TARGET" >&2
  exit 1
fi

echo "🔍 glic-check anti-pattern pre-scan: $TARGET"
echo "================================================================"

scan() {
  local label="$1"
  local pattern="$2"
  local files="$3"  # file glob/spec for grep -r --include
  echo ""
  echo "── $label ──"
  if [ -d "$TARGET" ]; then
    if [ -n "$files" ]; then
      grep -rEn "$pattern" "$TARGET" --include="$files" 2>/dev/null | head -20 || true
    else
      grep -rEn "$pattern" "$TARGET" 2>/dev/null | head -20 || true
    fi
  else
    grep -En "$pattern" "$TARGET" 2>/dev/null | head -20 || true
  fi
}

# U-Agent: vague directives (Chinese-skill anti-patterns; surface for any locale)
scan "U-Agent: vague Chinese directives (合理判断 / 适当处理 / 酌情考虑 / 按需调整 / 一般情况)" \
  "合理判断|适当处理|酌情考虑|按需调整|一般情况" \
  "*.md"

# U-Agent: vague English directives
scan "U-Agent: vague English directives (handle appropriately / as needed / if necessary)" \
  "handle (appropriately|as appropriate)|as (needed|appropriate)|if necessary|use your judgment" \
  "*.md"

# U-Agent: hard SKILL.md length check (>500 WARN / >800 ERR)
if [ -d "$TARGET" ] && [ -f "$TARGET/SKILL.md" ]; then
  echo ""
  echo "── U-Agent: SKILL.md length budget ──"
  lines=$(wc -l < "$TARGET/SKILL.md")
  if [ "$lines" -gt 800 ]; then
    echo "❌ ERR: SKILL.md = $lines lines (> 800)"
  elif [ "$lines" -gt 500 ]; then
    echo "⚠️ WARN: SKILL.md = $lines lines (> 500)"
  else
    echo "✅ OK: SKILL.md = $lines lines (≤ 500)"
  fi
fi

# G-Skill: frontmatter extra fields
if [ -d "$TARGET" ] && [ -f "$TARGET/SKILL.md" ]; then
  echo ""
  echo "── G-Skill / I-Skill: frontmatter extras (only name + description are safe) ──"
  python3 - <<'PY' "$TARGET/SKILL.md"
import sys, re
p = sys.argv[1]
with open(p) as f: c = f.read()
m = re.match(r'^---\n(.*?)\n---', c, re.DOTALL)
if not m:
    print(f"⚠️ No YAML frontmatter found in {p}")
    sys.exit(0)
try:
    import yaml
    parsed = yaml.safe_load(m.group(1))
    keys = list(parsed.keys()) if isinstance(parsed, dict) else []
    extras = [k for k in keys if k not in ("name", "description")]
    if extras:
        print(f"⚠️ WARN: frontmatter extra fields: {extras} (only name + description recommended)")
    else:
        print(f"✅ OK: frontmatter clean ({keys})")
    desc = parsed.get("description", "") if isinstance(parsed, dict) else ""
    db = len(desc.encode("utf-8"))
    if db > 1024:
        print(f"❌ ERR: description = {db} bytes > 1024 limit")
    elif db > 900:
        print(f"⚠️ WARN: description = {db} bytes (close to 1024 limit)")
except Exception as e:
    print(f"❌ ERR: frontmatter parse failed: {e}")
PY
fi

# I-Skill: build/runtime artifacts that should not be committed
scan "I-Skill: build/runtime artifacts in skill source (should be in .gitignore)" \
  "" \
  "sign.key|.install-source.json|__skill_meta__.json|*.json.md|__pycache__"
echo ""
echo "── I-Skill: artifact files present in $TARGET ──"
if [ -d "$TARGET" ]; then
  found=0
  for art in sign.key .install-source.json __skill_meta__.json __pycache__ .skill-data; do
    if find "$TARGET" -name "$art" 2>/dev/null | grep -q .; then
      find "$TARGET" -name "$art" 2>/dev/null | head -5
      found=1
    fi
  done
  if find "$TARGET" -name "*.json.md" 2>/dev/null | grep -q .; then
    find "$TARGET" -name "*.json.md" 2>/dev/null | head -5
    found=1
  fi
  [ "$found" -eq 0 ] && echo "✅ OK: no obvious build/runtime artifacts found"
fi

# I-Skill: cross-section reference probe (broken section numbers)
echo ""
echo "── I-Skill: cross-section reference candidates (manually verify each) ──"
if [ -d "$TARGET" ]; then
  grep -rEn "Step [0-9]+(\.[0-9]+)*(\.[a-z])?|see (Step|Section) [0-9]" "$TARGET" --include="*.md" 2>/dev/null | head -20 || true
fi

echo ""
echo "================================================================"
echo "✅ pre-scan complete. Now run the full UGLIC checklist for severity + citations."
