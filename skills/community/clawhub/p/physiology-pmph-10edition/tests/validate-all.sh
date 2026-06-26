#!/bin/bash
# validate-all.sh - Validate skill collection integrity
# 验证技能集合完整性

cd "$(dirname "$0")/.."
errors=0
warnings=0

echo "=== Physiology-PMPH-10edition Validation ==="
echo ""

# Check all folders have SKILL.md
echo "--- Checking SKILL.md presence ---"
folders=0
for item in */; do
  folder="${item%/}"
  if [ -d "$folder" ] && [ "$folder" != "config" ] && [ "$folder" != "scripts" ] && [ "$folder" != "tests" ] && [ "$folder" != "assets" ]; then
    folders=$((folders + 1))
    if [ ! -f "${folder}/SKILL.md" ]; then
      echo "  ERROR: $folder/SKILL.md missing"
      errors=$((errors + 1))
    fi
  fi
done
echo "  Total skill folders: $folders"
echo ""

# Check folder naming (kebab-case English only)
echo "--- Checking folder naming ---"
for item in */; do
  folder="${item%/}"
  if [ -d "$folder" ] && [ "$folder" != "config" ] && [ "$folder" != "scripts" ] && [ "$folder" != "tests" ] && [ "$folder" != "assets" ]; then
    if echo "$folder" | grep -qP '[\x80-\xFF]'; then
      echo "  ERROR: $folder contains non-ASCII characters"
      errors=$((errors + 1))
    fi
  fi
done
echo ""

# Check frontmatter validity
echo "--- Checking SKILL.md frontmatter ---"
for item in */; do
  folder="${item%/}"
  if [ -d "$folder" ] && [ -f "${folder}/SKILL.md" ]; then
    first=$(head -1 "${folder}/SKILL.md")
    if [ "$first" != "---" ]; then
      echo "  WARNING: $folder/SKILL.md missing frontmatter (starts with '$first')"
      warnings=$((warnings + 1))
    fi
    has_name=$(grep "^name:" "${folder}/SKILL.md" 2>/dev/null | head -1)
    if [ -z "$has_name" ]; then
      echo "  WARNING: $folder/SKILL.md missing 'name:' in frontmatter"
      warnings=$((warnings + 1))
    fi
  fi
done
echo ""

echo "=== Results ==="
echo "  Errors:   $errors"
echo "  Warnings: $warnings"
if [ $errors -eq 0 ]; then
  echo "  STATUS: PASS"
else
  echo "  STATUS: FAIL"
fi
