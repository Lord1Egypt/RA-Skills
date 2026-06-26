#!/bin/bash
#
# test.sh - Run tests for insight-tracker skill
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 Testing insight-tracker skill"
echo "================================"

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

# Test 5: Tag taxonomy exists
echo "Test 5: Check tag taxonomy..."
if [[ -f "$SKILL_DIR/references/tag-taxonomy.md" ]]; then
    echo "  ✅ PASS: tag-taxonomy.md exists"
else
    echo "  ❌ FAIL: tag-taxonomy.md not found"
    exit 1
fi

# Test 6: Scripts are executable
echo "Test 6: Check scripts are executable..."
for script in "$SKILL_DIR/scripts/"*.sh; do
    if [[ -f "$script" ]]; then
        if [[ -x "$script" ]]; then
            echo "  ✅ PASS: $(basename "$script") is executable"
        else
            echo "  ⚠️  WARN: $(basename "$script") is not executable"
        fi
    fi
done

# Test 7: Test add-insight functionality
echo "Test 7: Test add-insight script..."
TEST_DATA_DIR=$(mktemp -d)
if INSIGHT_DATA_DIR="$TEST_DATA_DIR" "$SKILL_DIR/scripts/add-insight.sh" "Test insight for validation" --tags test --priority low --source test >/dev/null 2>&1; then
    echo "  ✅ PASS: add-insight.sh runs successfully"
else
    echo "  ⚠️  WARN: add-insight.sh may have issues (non-critical)"
fi

if INSIGHT_DATA_DIR="$TEST_DATA_DIR" "$SKILL_DIR/scripts/add-insight.sh" '$(touch /tmp/insight-owned)' --tags test --priority low --source test >/dev/null 2>&1; then
    if [[ -f /tmp/insight-owned ]]; then
        echo "  ❌ FAIL: user content was evaluated by the shell"
        rm -f /tmp/insight-owned
        exit 1
    fi
    echo "  ✅ PASS: user content is written literally"
else
    echo "  ❌ FAIL: add-insight.sh rejected literal shell-like content"
    exit 1
fi
rm -rf "$TEST_DATA_DIR"

echo ""
echo "================================"
echo "✅ All critical tests passed!"
