#!/bin/bash
#
# test.sh - Run tests for knowledge-distillation skill
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 Testing knowledge-distillation skill"
echo "======================================="

# Test 1: SKILL.md exists
echo "Test 1: Check SKILL.md exists..."
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    echo "  ✅ PASS: SKILL.md exists"
else
    echo "  ❌ FAIL: SKILL.md not found"
    exit 1
fi

# Test 2: YAML frontmatter
echo "Test 2: Check YAML frontmatter..."
if grep -q "^---$" "$SKILL_DIR/SKILL.md"; then
    echo "  ✅ PASS: YAML frontmatter present"
else
    echo "  ❌ FAIL: Missing YAML frontmatter"
    exit 1
fi

# Test 3: Required fields
echo "Test 3: Check required fields..."
for field in "name:" "description:"; do
    if grep -q "^$field" "$SKILL_DIR/SKILL.md"; then
        echo "  ✅ PASS: Found $field"
    else
        echo "  ❌ FAIL: Missing $field"
        exit 1
    fi
done

# Test 4: References directory
echo "Test 4: Check references directory..."
if [[ -d "$SKILL_DIR/references" ]]; then
    echo "  ✅ PASS: references/ directory exists"
else
    echo "  ❌ FAIL: references/ directory not found"
    exit 1
fi

# Test 5: Output templates exist
echo "Test 5: Check output templates..."
if [[ -f "$SKILL_DIR/references/output-templates.md" ]]; then
    echo "  ✅ PASS: output-templates.md exists"
else
    echo "  ❌ FAIL: output-templates.md not found"
    exit 1
fi

# Test 6: Shell syntax
echo "Test 6: Check shell syntax..."
for script in "$SKILL_DIR/scripts/"*.sh; do
    bash -n "$script"
    echo "  ✅ PASS: $(basename "$script") syntax is valid"
done

# Test 7: No machine-specific absolute paths in package files
echo "Test 7: Check for machine-specific paths..."
LOCAL_HOME="$(cd ~ && pwd)"
HARDCODED_MATCHES="$(
    find "$SKILL_DIR" -type f \( -name '*.md' -o -name '*.sh' -o -name '*.json' \) \
        -not -path "$SKILL_DIR/.clawhub/*" \
        -exec grep -H "$LOCAL_HOME" {} + || true
)"
if [[ -n "$HARDCODED_MATCHES" ]]; then
    echo "  ❌ FAIL: Found hardcoded local paths"
    echo "$HARDCODED_MATCHES"
    exit 1
else
    echo "  ✅ PASS: No machine-specific local paths"
fi

# Test 8: distill.sh creates a dated draft in the requested output directory
echo "Test 8: Run distill.sh smoke test..."
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT
mkdir -p "$TMP_ROOT/memory"
printf '# Memory\n\n- Repeated signal worth reviewing.\n' > "$TMP_ROOT/memory/MEMORY.md"
KNOWLEDGE_DISTILLATION_MEMORY_DIR="$TMP_ROOT/memory" \
KNOWLEDGE_DISTILLATION_OUTPUT_DIR="$TMP_ROOT/out" \
    bash "$SKILL_DIR/scripts/distill.sh" > "$TMP_ROOT/run.log"

if find "$TMP_ROOT/out" -type f -name 'knowledge-distillation-*.md' | grep -q .; then
    echo "  ✅ PASS: distill.sh created a dated Markdown draft"
else
    echo "  ❌ FAIL: distill.sh did not create a dated Markdown draft"
    cat "$TMP_ROOT/run.log"
    exit 1
fi

echo ""
echo "======================================="
echo "✅ All tests passed!"
