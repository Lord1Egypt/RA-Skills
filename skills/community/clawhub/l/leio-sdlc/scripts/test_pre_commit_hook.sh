#!/bin/bash
set -e

echo "=== Testing Pre-Commit Hook Integration ==="

# 1. Setup Sandbox
SANDBOX_DIR=$(mktemp -d)
cd "$SANDBOX_DIR"
git init > /dev/null
git config user.name "Test"
git config user.email "test@example.com"
touch .sdlc_guardrail
git add .sdlc_guardrail
git commit -m "init" > /dev/null
cp -r /root/.openclaw/workspace/projects/leio-sdlc/.sdlc_hooks .

# 2. Configure hooksPath
git config core.hooksPath .sdlc_hooks

# 3. Test: Raw commit on master should fail
echo "Test 1: Expecting rejection for raw commit on master..."
set +e
git commit --allow-empty -m "direct commit" > commit.log 2>&1
EXIT_CODE=$?
set -e
if [ $EXIT_CODE -eq 0 ]; then
    echo "❌ FAILED: Direct commit on master was not blocked."
    exit 1
fi
if ! grep -q "GIT COMMIT REJECTED" commit.log; then
    echo "❌ FAILED: Rejection message not found."
    exit 1
fi
if ! grep -q "python3 ~/.openclaw/skills/leio-sdlc/scripts/commit_state.py" commit.log; then
    echo "❌ FAILED: Missing commit_state.py instruction in pre-commit hook output."
    exit 1
fi
echo "✅ PASSED: Raw commit rejected as expected."

# 4. Test: Override flag should succeed
echo "Test 2: Expecting success with override flag..."
git -c sdlc.override=true commit --allow-empty -m "override commit"
echo "✅ PASSED: Override flag works as expected."

# 5. Test: Runtime flag should succeed
echo "Test 3: Expecting success with runtime flag..."
git -c sdlc.runtime=1 commit --allow-empty -m "runtime commit"
echo "✅ PASSED: Runtime flag works as expected."

# 6. Test: Commit on feature branch should succeed
echo "Test 4: Expecting success on feature branch..."
git checkout -b feature/test > /dev/null
git commit --allow-empty -m "feature commit"
echo "✅ PASSED: Commit on feature branch allowed."

# 7. Test: No guardrail file should succeed
echo "Test 5: Expecting success without .sdlc_guardrail..."
git checkout master > /dev/null
rm .sdlc_guardrail
git commit --allow-empty -m "no guardrail commit"
echo "✅ PASSED: Commit without guardrail allowed."


rm -rf "$SANDBOX_DIR"
echo "✅ All pre-commit hook tests passed."
