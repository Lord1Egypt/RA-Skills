#!/bin/bash
set -e

# Test Setup:
# 1. Initialize a dummy Git workspace (/tmp/test_071_workspace_$$).
WORKSPACE="/tmp/test_071_workspace_$$"
mkdir -p "$WORKSPACE"

# Ensure cleanup on exit
trap 'rm -rf "$WORKSPACE"' EXIT

# Absolute path to spawn_reviewer.py and PR file
SPAWN_SCRIPT=$(realpath "/root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_reviewer.py")
DUMMY_PR="$WORKSPACE/PR_002_dummy.md"
touch "$DUMMY_PR"

cd "$WORKSPACE"
git init > /dev/null

# Set git user
git config user.name "Test Bot"
git config user.email "test@example.com"

# 2. Create and commit a base file to master with the message "Base commit on master".
echo "base file content" > base_file.txt
git add base_file.txt
git commit -m "Base commit on master" > /dev/null

# Force branch name to master if it defaulted to main
git branch -m master || true

# 3. Checkout a new branch feature/intra_branch_test.
git checkout -b feature/intra_branch_test > /dev/null 2>&1

# 4. Create and commit a dummy file with the message "Feature commit A: buggy test".
echo "buggy test" > feature_file.txt
git add feature_file.txt
git commit -m "Feature commit A: buggy test" > /dev/null

# 5. Modify the file and commit with the message "Feature commit B: fix buggy test".
echo "fix buggy test" > feature_file.txt
git add feature_file.txt
git commit -m "Feature commit B: fix buggy test" > /dev/null

# 6. Run the Reviewer script
# To prevent actually calling out to openclaw in tests, let's set the environment variable.
export SDLC_TEST_MODE=true

python3 "$SPAWN_SCRIPT" --pr-file "$DUMMY_PR" --diff-target master --workdir "$WORKSPACE" --global-dir "$WORKSPACE"

# Assertions:
# 1. Read the generated recent_history.diff.
DIFF_FILE="$WORKSPACE/recent_history.diff"

if [ ! -f "$DIFF_FILE" ]; then
    echo "Error: $DIFF_FILE not generated."
    exit 1
fi

# 2. Assert Pass: The file MUST contain the string "Base commit on master".
if ! grep -q "Base commit on master" "$DIFF_FILE"; then
    echo "Assertion Failed: 'Base commit on master' not found in $DIFF_FILE"
    exit 1
fi

# 3. Assert Fail: The file MUST NOT contain the strings "Feature commit A" or "Feature commit B".
if grep -q "Feature commit A" "$DIFF_FILE"; then
    echo "Assertion Failed: 'Feature commit A' leaked into $DIFF_FILE"
    exit 1
fi

if grep -q "Feature commit B" "$DIFF_FILE"; then
    echo "Assertion Failed: 'Feature commit B' leaked into $DIFF_FILE"
    exit 1
fi

echo "Test passed: Reviewer history scope is correctly locked to the base branch."
exit 0
