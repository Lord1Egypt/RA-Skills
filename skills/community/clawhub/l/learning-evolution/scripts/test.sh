#!/bin/bash
#
# test.sh - Test learning-evolution functionality
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "Testing learning-evolution"
echo "============================"

# Test 1: Check scripts exist
echo ""
echo "Test 1: Checking script files..."
for script in analyze-usage.sh track-effectiveness.sh suggest-evolutions.sh; do
    if [[ -f "$SCRIPT_DIR/$script" ]]; then
        echo "✅ $script exists"
    else
        echo "❌ $script missing"
        exit 1
    fi
done

# Test 2: Check executability
echo ""
echo "Test 2: Checking executability..."
for script in analyze-usage.sh track-effectiveness.sh suggest-evolutions.sh; do
    if [[ -x "$SCRIPT_DIR/$script" ]]; then
        echo "✅ $script is executable"
    else
        echo "⚠️  $script not executable, fixing..."
        chmod +x "$SCRIPT_DIR/$script"
    fi
done

# Test 3: Test analyze-usage
echo ""
echo "Test 3: Testing analyze-usage..."
"$SCRIPT_DIR/analyze-usage.sh" --skill test-skill --period 30d
if "$SCRIPT_DIR/analyze-usage.sh" --skill ../evil --period 30d >/dev/null 2>&1; then
    echo "❌ analyze-usage accepted path traversal input"
    exit 1
else
    echo "✅ analyze-usage rejects unsafe skill names"
fi

# Test 4: Test track-effectiveness
echo ""
echo "Test 4: Testing track-effectiveness..."
"$SCRIPT_DIR/track-effectiveness.sh" --skill test-skill
if "$SCRIPT_DIR/track-effectiveness.sh" --skill ../evil >/dev/null 2>&1; then
    echo "❌ track-effectiveness accepted path traversal input"
    exit 1
else
    echo "✅ track-effectiveness rejects unsafe skill names"
fi

# Test 5: Test suggest-evolutions
echo ""
echo "Test 5: Testing suggest-evolutions..."
"$SCRIPT_DIR/suggest-evolutions.sh" --skill test-skill
if "$SCRIPT_DIR/suggest-evolutions.sh" --skill ../evil >/dev/null 2>&1; then
    echo "❌ suggest-evolutions accepted path traversal input"
    exit 1
else
    echo "✅ suggest-evolutions rejects unsafe skill names"
fi

echo ""
echo "============================"
echo "Tests complete"
