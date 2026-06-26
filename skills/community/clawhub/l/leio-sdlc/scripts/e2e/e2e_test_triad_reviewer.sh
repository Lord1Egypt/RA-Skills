#!/bin/bash

# Ensure we're in the right directory
cd "$(dirname "$0")/.." || exit 1

echo "Setting up Triad Consistency Test for Reviewer..."

# 2.2.1 Prepare Dummy Files
mkdir -p tests
cat << 'EOF' > tests/dummy_triad_pr.md
# Dummy PR
This is a test PR. Please output an APPROVED status in JSON.
EOF

cat << 'EOF' > tests/dummy_triad.diff
--- a/tests/dummy_script.py
+++ b/tests/dummy_script.py
@@ -1,2 +1,3 @@
 def test_func():
-    return False
+    return True
EOF

# 2.2.2 Environment Configuration
unset SDLC_TEST_MODE

# 2.2.3 Execute Test and Capture Logs
echo "Executing Reviewer spawn script..."
# Pass mandatory --global-dir
python3 scripts/spawn_reviewer.py --pr-file tests/dummy_triad_pr.md --diff-target HEAD --override-diff-file tests/dummy_triad.diff  --workdir "$(pwd)" --global-dir "$(pwd)" > tests/triad_reviewer.log 2>&1

# 2.2.4 Assertions
echo "Running assertions..."
if ! grep -q 'APPROVED' tests/triad_reviewer.log; then
    echo "ERROR: Missing APPROVED status in log."
    cat tests/triad_reviewer.log
    # Cleanup
    rm -f tests/dummy_triad_pr.md tests/dummy_triad.diff tests/triad_reviewer.log
    exit 1
fi

if grep -q -- "--- a/" tests/triad_reviewer.log; then
    echo "ERROR: Output contains raw diff '--- a/'."
    cat tests/triad_reviewer.log
    # Cleanup
    rm -f tests/dummy_triad_pr.md tests/dummy_triad.diff tests/triad_reviewer.log
    exit 1
fi

echo "All assertions passed! Test successful."

# 2.2.5 Cleanup
rm -f tests/dummy_triad_pr.md tests/dummy_triad.diff tests/triad_reviewer.log

exit 0