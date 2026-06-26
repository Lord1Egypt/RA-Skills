#!/bin/bash
# Test script for Optional Strict Instructions skill

echo "Testing Optional Strict Instructions Skill"
echo "=========================================="

# Test 1: File verification
echo ""
echo "Test 1: File verification"
echo "-------------------------"
touch /tmp/test-file-123.txt
echo "Created test file: /tmp/test-file-123.txt"

# Test 2: Option presentation (simulated)
echo ""
echo "Test 2: Option presentation template"
echo "------------------------------------"
cat << 'EOF'
[Operation: Delete test file]
Found: /tmp/test-file-123.txt (4.0K, user permissions)

Options:
1. sudo rm -f (permanent, needs password)
2. rm (permanent, user permissions)
3. Cancel

Enter choice (1-3):
EOF

# Test 3: Strict execution example
echo ""
echo "Test 3: Strict execution example"
echo "--------------------------------"
cat << 'EOF'
User: "Use sudo to delete test.txt"

Correct workflow:
1. Check test.txt exists ✓
2. Execute: sudo rm test.txt
3. If sudo needs password → Stop and report
4. Wait for password or alternative instruction
5. Do NOT try rm test.txt without permission

Wrong workflow:
1. Check test.txt exists ✓
2. Execute: sudo rm test.txt
3. If sudo fails → Try rm test.txt ❌ (WRONG!)
EOF

# Cleanup
rm -f /tmp/test-file-123.txt
echo ""
echo "Test file cleaned up"
echo ""
echo "Skill test completed successfully!"