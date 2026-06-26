#!/bin/bash
# L76 Core Architecture - Validation Script
# Validates skill structure and content before publishing

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME=$(basename "$SKILL_DIR")

echo "🔍 Validating skill: $SKILL_NAME"
echo ""

# Check required files
REQUIRED_FILES=("SKILL.md")
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$SKILL_DIR/$file" ]; then
    echo "❌ Missing required file: $file"
    exit 1
  fi
  echo "✅ Found: $file"
done

# Check optional files (warn if missing)
OPTIONAL_FILES=("index.js" "references/examples.md")
for file in "${OPTIONAL_FILES[@]}"; do
  if [ ! -f "$SKILL_DIR/$file" ]; then
    echo "⚠️  Missing optional file: $file"
  else
    echo "✅ Found: $file"
  fi
done

# Validate SKILL.md frontmatter
echo ""
echo "📋 Validating SKILL.md frontmatter..."

if ! grep -q "^---$" "$SKILL_DIR/SKILL.md"; then
  echo "❌ SKILL.md missing YAML frontmatter delimiter (---)"
  exit 1
fi

if ! grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
  echo "❌ SKILL.md missing 'name:' field"
  exit 1
fi

if ! grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
  echo "❌ SKILL.md missing 'description:' field"
  exit 1
fi

echo "✅ Frontmatter valid"

# Check for placeholder text
echo ""
echo "🔍 Checking for placeholder text..."

if grep -q "{placeholder}" "$SKILL_DIR/SKILL.md"; then
  echo "❌ Found placeholder text: {placeholder}"
  exit 1
fi

if grep -q "TODO" "$SKILL_DIR/SKILL.md"; then
  echo "⚠️  Found TODO markers in SKILL.md"
fi

echo "✅ No critical placeholders found"

# Validate JavaScript (if index.js exists)
if [ -f "$SKILL_DIR/index.js" ]; then
  echo ""
  echo "🟨 Validating JavaScript..."
  
  if command -v node &> /dev/null; then
    if node --check "$SKILL_DIR/index.js" 2>/dev/null; then
      echo "✅ JavaScript syntax valid"
    else
      echo "❌ JavaScript syntax errors detected"
      exit 1
    fi
  else
    echo "⚠️  Node.js not available, skipping JS validation"
  fi
fi

# Check file sizes
echo ""
echo "📏 Checking file sizes..."

MAX_SIZE=1048576  # 1MB
for file in "$SKILL_DIR"/*; do
  if [ -f "$file" ]; then
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    if [ "$size" -gt "$MAX_SIZE" ]; then
      echo "⚠️  Large file: $(basename "$file") ($(numfmt --to=iec $size))"
    fi
  fi
done

echo "✅ File sizes acceptable"

# Summary
echo ""
echo "================================"
echo "✅ Validation complete!"
echo "================================"
echo ""
echo "Skill is ready for:"
echo "  - Testing with: node index.js"
echo "  - Publishing with: clawhub publish ./$SKILL_NAME"
echo ""
