#!/bin/bash
set -e

echo "Running test_076_unit_git_commit.sh..."

TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

cd "$TEST_DIR"
git init
git config user.email "test@openclaw.ai"
git config user.name "TDD Tester"
echo "init" > README.md
git add README.md
git commit -m "initial commit"

echo "dirty code hallucinated by coder" > ghost_file.py

cat << 'EOF' > run_test.py
import sys
sys.path.append("/root/.openclaw/workspace/projects/leio-sdlc/scripts")
try:
    from orchestrator import force_commit_untracked_changes
    force_commit_untracked_changes(".")
except ImportError as e:
    print(f"Failed to import: {e}")
    sys.exit(1)
EOF

python3 run_test.py

STATUS=$(git status --porcelain)
if [ -n "$STATUS" ]; then
    echo "FAIL: Working tree is not clean. Force commit failed."
    git status
    exit 1
fi

LAST_COMMIT_MSG=$(git log -1 --pretty=%B)
if [[ "$LAST_COMMIT_MSG" != *"chore(auto): force commit uncommitted changes before review"* ]]; then
    echo "FAIL: Commit message missing or incorrect."
    echo "Got: $LAST_COMMIT_MSG"
    exit 1
fi

python3 run_test.py
echo "PASS: Successfully executed force_commit_untracked_changes."

exit 0
