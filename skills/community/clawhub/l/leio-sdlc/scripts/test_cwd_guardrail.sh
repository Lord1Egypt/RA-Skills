#!/bin/bash
export SDLC_TEST_MODE=true
set -e

# test_cwd_guardrail.sh
# Ensures that SDLC scripts correctly enforce working directory boundaries.

PROJECT_ROOT=$(pwd)
TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/bin"
cat << 'INNER_EOF' > "$TEMP_DIR/bin/openclaw"
#!/bin/bash
exit 0
INNER_EOF
chmod +x "$TEMP_DIR/bin/openclaw"
export PATH="$TEMP_DIR/bin:$PATH"
# mock_openclaw added

trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Sandbox: $TEMP_DIR"

# 1. Test Boundary Violation (No .git in workdir but .git in parent)
OUTER_REPO="$TEMP_DIR/outer_repo"
mkdir -p "$OUTER_REPO"
cd "$OUTER_REPO"
git init > /dev/null
git config user.name "Test"
git config user.email "test@example.com"

INNER_DIR="$OUTER_REPO/inner_dir"
mkdir -p "$INNER_DIR"

echo "--- Testing Boundary Violation Detection ---"
cd "$PROJECT_ROOT"
# We expect this to fail with Git Boundary violation error
if python3 scripts/orchestrator.py --force-replan true --enable-exec-from-workspace --enable-exec-from-workspace --workdir "$INNER_DIR" --prd-file "prd.md" --channel "valid:id" --global-dir "$PROJECT_ROOT" 2>&1 | grep -q "Git boundary violation"; then
    echo "✅ Success: Boundary violation detected."
else
    echo "❌ FAILED: Boundary violation NOT detected."
    exit 1
fi

# 2. Test Correct Operation (With .git in workdir)
echo "--- Testing Correct Operation with CWD ---"
cd "$INNER_DIR"
git init > /dev/null
git config user.name "Test"
git config user.email "test@example.com"
touch prd.md
git add prd.md
git commit -m "init" > /dev/null

cd "$PROJECT_ROOT"
# This should now get past the boundary check (though it might fail later due to missing PRs, which is fine for this test)
if python3 scripts/orchestrator.py --force-replan true --enable-exec-from-workspace --enable-exec-from-workspace --workdir "$INNER_DIR" --prd-file "prd.md" --channel "valid:id" --global-dir "$PROJECT_ROOT" 2>&1 | grep -q "Git boundary violation"; then
    echo "❌ FAILED: Boundary violation detected on a valid git repo."
    exit 1
else
    echo "✅ Success: Passed boundary check."
fi

echo "✅ All CWD Guardrail tests passed."
