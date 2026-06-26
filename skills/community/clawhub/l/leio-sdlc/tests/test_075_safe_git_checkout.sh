#!/usr/bin/env bash
export SDLC_TEST_MODE=true
set -e

# Setup test environment
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"
git init > /dev/null

echo "dummy content" > README.md
git add README.md
git commit -m "initial commit" > /dev/null

# Create a fake PRD and PR
mkdir -p docs/PRDs docs/PRs/dummy_prd
echo "# Dummy PRD" > docs/PRDs/dummy_prd.md
cat << 'PR_EOF' > docs/PRs/dummy_prd/PR_001_dummy.md
status: in_progress
slice_depth: 0

# Dummy PR
PR-001
PR_EOF

git add docs
git commit -m "add prd" > /dev/null

# Simulate a failure by breaking git checkout specifically
# We'll put a broken git script in front of the PATH
mkdir -p fake_bin
cat << 'GIT_EOF' > fake_bin/git
#!/bin/bash
if [[ "$1" == "checkout" ]]; then
    echo "Simulated git checkout failure!" >&2
    exit 1
fi
exec /usr/bin/git "$@"
GIT_EOF
chmod +x fake_bin/git

# Run orchestrator
export PATH="$TEST_DIR/fake_bin:$PATH"

echo "Running orchestrator..."
set +e
/usr/bin/python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/orchestrator.py --force-replan true --enable-exec-from-workspace --channel "valid:id" \
    --prd-file docs/PRDs/dummy_prd.md \
    --workdir "$TEST_DIR" \
    --max-runs 1 > orchestrator.log 2>&1
EXIT_CODE=$?
set -e

cat orchestrator.log

# Assertions
if ! grep -q "Aborting gracefully." orchestrator.log; then
    echo "ERROR: Orchestrator did not catch git checkout failure gracefully."
    exit 1
fi

if ! grep -q "Simulated git checkout failure!" orchestrator.log; then
    echo "ERROR: Did not see the simulated failure in logs."
    exit 1
fi

# Ensure files were not deleted
if [ ! -f "docs/PRDs/dummy_prd.md" ]; then
    echo "ERROR: Orchestrator destructively deleted files."
    exit 1
fi

echo "Test 075 Passed"
rm -rf "$TEST_DIR"
exit 0
