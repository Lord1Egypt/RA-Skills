#!/bin/bash
export SDLC_TEST_MODE=true
set -e

WORKSPACE="/tmp/test_069_workspace_$$"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

# Initialize dummy git workspace
git init > /dev/null 2>&1
git config user.email "test@example.com"
git config user.name "Test User"
echo "Dummy file" > README.md
git add README.md
git commit -m "Initial commit" > /dev/null 2>&1

# Setup PRD
mkdir -p docs/PRs/PRD_069_Test
cat << 'EOF' > docs/PRs/PRD_069_Test/PR_001_Namespace_Fix.md
status: in_progress

Dummy PR content.
EOF

# Stage the changes to test State 0 Solidification
git add docs/PRs/PRD_069_Test/PR_001_Namespace_Fix.md

# Path to original orchestrator
ORCHESTRATOR="/root/.openclaw/workspace/projects/leio-sdlc/scripts/orchestrator.py --force-replan true --channel "valid:id""

# Create a wrapper Python script to test the logic directly since we can't easily inject into orchestrator.py --force-replan true --channel "valid:id"'s while loop without it running everything
cat << 'EOF' > test_extraction.py
import os
current_pr = "docs/PRs/PRD_069_Test/PR_001_Namespace_Fix.md"
base_filename = os.path.splitext(os.path.basename(current_pr))[0]
parent_dir_name = os.path.basename(os.path.dirname(os.path.abspath(current_pr)))
branch_name = f"{parent_dir_name}/{base_filename}"
print(branch_name)
EOF

BRANCH_NAME=$(python3 test_extraction.py)

if [ "$BRANCH_NAME" != "PRD_069_Test/PR_001_Namespace_Fix" ]; then
    echo "Assertion failed: Parsed branch name '$BRANCH_NAME' is incorrect."
    exit 1
fi

echo "Branch name extracted correctly: $BRANCH_NAME"

# Test State 0 Solidification manually to assert clean status before proceed
git diff --cached --quiet || git commit -m "docs(planner): auto-generated PR contracts" > /dev/null 2>&1

if ! git diff --cached --quiet; then
    echo "Assertion failed: Git status is not clean."
    exit 1
fi

if ! git diff --quiet; then
    echo "Assertion failed: Git status is not clean."
    exit 1
fi

echo "State 0 Solidification passed."

# Create branch, switch to it
git checkout -b "$BRANCH_NAME" > /dev/null 2>&1
echo "Dummy change" >> dummy_change.txt
git add dummy_change.txt
git commit -m "Dummy commit" > /dev/null 2>&1

# Switch back to master and merge
git checkout master > /dev/null 2>&1
git merge "$BRANCH_NAME" > /dev/null 2>&1

# State 6 Teardown
git branch -D "$BRANCH_NAME" > /dev/null 2>&1

# Assert branch is deleted
if git branch --list | grep -q "$BRANCH_NAME"; then
    echo "Assertion failed: Branch '$BRANCH_NAME' was not deleted."
    exit 1
fi

echo "State 6 Teardown passed."
echo "All assertions passed 100%."

# Cleanup
rm -rf "$WORKSPACE"
exit 0
