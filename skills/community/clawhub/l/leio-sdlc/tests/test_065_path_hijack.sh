#!/bin/bash
set -e

echo "Running Integration Test: PRD-065 Runtime Path Decoupling"

# Run from the project root
cd "$(dirname "$0")/.."

TEST_DIR="dummy_hijack_workspace"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR/scripts"
mkdir -p "$TEST_DIR/docs/PRs/dummy"

cat << 'INNER_EOF' > "$TEST_DIR/docs/PRs/dummy/PR_001.md"
status: in_progress
INNER_EOF

cat << 'INNER_EOF' > "$TEST_DIR/dummy.md"
# Dummy PRD
INNER_EOF

# Create malicious scripts in the workspace
cat << 'INNER_EOF' > "$TEST_DIR/scripts/spawn_coder.py"
print("[HIJACKED_CODER] Vulnerability exploited!")
INNER_EOF

cat << 'INNER_EOF' > "$TEST_DIR/scripts/spawn_reviewer.py"
print("[HIJACKED_REVIEWER] Vulnerability exploited!")
INNER_EOF

chmod +x "$TEST_DIR/scripts/"*.py

# Initialize git repo so git show-ref works
cd "$TEST_DIR"
git init >/dev/null 2>&1
git config user.email "test@example.com"
git config user.name "Test User"
git commit --allow-empty -m "Initial commit" >/dev/null 2>&1
cd ..

export SDLC_TEST_MODE=true

# Run orchestrator
set +e
OUTPUT=$(python3 scripts/orchestrator.py --force-replan true --enable-exec-from-workspace --channel "valid:id" --workdir "$TEST_DIR" --prd-file "dummy.md" --max-runs 1 2>&1)
set -e

if echo "$OUTPUT" | grep -q "HIJACKED_CODER"; then
    echo "❌ VULNERABILITY DETECTED: Workspace scripts/spawn_coder.py was executed!"
    echo "$OUTPUT"
    exit 1
fi

if echo "$OUTPUT" | grep -q "HIJACKED_REVIEWER"; then
    echo "❌ VULNERABILITY DETECTED: Workspace scripts/spawn_reviewer.py was executed!"
    echo "$OUTPUT"
    exit 1
fi

# Ensure that the orchestrator actually ran spawn_coder correctly.
# In SDLC_TEST_MODE, spawn_coder exits successfully or fails properly, but won't output HIJACKED.
if echo "$OUTPUT" | grep -q "State 3: Spawning Coder for"; then
    echo "✅ Success: Orchestrator ran the real scripts and ignored workspace scripts."
else
    echo "❌ Test failed: Orchestrator did not reach State 3. Output:"
    echo "$OUTPUT"
    exit 1
fi

# Clean up
rm -rf "$TEST_DIR"
exit 0
