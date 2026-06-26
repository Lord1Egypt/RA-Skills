#!/bin/bash
# Test script for Mac Clamshell Mode skill

echo "🧪 Testing Mac Clamshell Mode Skill"
echo "=================================="

# Test 1: Check compatibility
echo "Test 1: Compatibility Check"
./check-compatibility.sh
echo ""

# Test 2: Show help
echo "Test 2: Help Display"
./help.sh
echo ""

# Test 3: Configuration (dry run)
echo "Test 3: Configuration Preview"
./configure-clamshell.sh --dry-run
echo ""

echo "✅ All tests completed!"