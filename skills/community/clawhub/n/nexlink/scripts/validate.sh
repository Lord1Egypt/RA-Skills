#!/bin/bash
# NexLink Validation Script
# Run this after any changes to verify functionality

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/nexlink.py"

echo "=========================================="
echo "NexLink Validation Script"
echo "=========================================="
echo ""

# Check if CLI exists
if [ ! -f "$CLI" ]; then
    echo "❌ ERROR: CLI not found at $CLI"
    exit 1
fi

echo "✅ CLI found: $CLI"
echo ""

# ==========================================
# Exchange Module Tests
# ==========================================
echo "--- Testing Exchange Module ---"

# Test mail commands
echo ""
echo "Testing: mail connect"
python3 "$CLI" mail connect
if [ $? -eq 0 ]; then
    echo "✅ mail connect: OK"
else
    echo "❌ mail connect: FAILED"
    exit 1
fi

echo ""
echo "Testing: mail read --limit 1"
python3 "$CLI" mail read --limit 1
if [ $? -eq 0 ]; then
    echo "✅ mail read: OK"
else
    echo "❌ mail read: FAILED"
    exit 1
fi

echo ""
echo "Testing: calendar today"
python3 "$CLI" cal today
if [ $? -eq 0 ]; then
    echo "✅ cal today: OK"
else
    echo "❌ cal today: FAILED"
    exit 1
fi

echo ""
echo "Testing: tasks list"
python3 "$CLI" tasks list
if [ $? -eq 0 ]; then
    echo "✅ tasks list: OK"
else
    echo "❌ tasks list: FAILED"
    exit 1
fi

# ==========================================
# Nextcloud Module Tests
# ==========================================
echo ""
echo "--- Testing Nextcloud Module ---"

echo ""
echo "Testing: files list /"
python3 "$CLI" files list /
if [ $? -eq 0 ]; then
    echo "✅ files list: OK"
else
    echo "❌ files list: FAILED"
    exit 1
fi

echo ""
echo "Testing: files info (root check)"
python3 "$CLI" files info /
if [ $? -eq 0 ]; then
    echo "✅ files info: OK"
else
    echo "⚠️  files info: Not critical (may fail on root)"
fi

# ==========================================
# Summary
# ==========================================
echo ""
echo "=========================================="
echo "✅ All validation tests passed!"
echo "=========================================="
echo ""
echo "Validated commands:"
echo "  - mail connect"
echo "  - mail read --limit 1"
echo "  - cal today"
echo "  - tasks list"
echo "  - files list /"
echo ""