#!/bin/bash
set -e

# Setup test environment
export SDLC_TEST_MODE="true"
WORKDIR="/root/.openclaw/workspace/projects/leio-sdlc"
cd "$WORKDIR"

# Create a dummy PR contract
cat << 'PR' > tests/dummy_pr.md
# PR_001
Dummy PR content.
PR

# Run the reviewer with a custom out-file
python3 scripts/spawn_reviewer.py \
    --pr-file tests/dummy_pr.md \
    --diff-target HEAD \
    --workdir "$WORKDIR" \
    --out-file "custom_report.md"

# Check if the out-file was created by the mock
if [ ! -f "custom_report.md" ]; then
    echo "Error: custom_report.md was not created!"
    exit 1
fi

# Check if the prompt instructed the LLM to write to the custom path
if ! grep -q "exactly '$WORKDIR/custom_report.md'" tests/tool_calls.log; then
    echo "Error: Prompt did not instruct LLM to write to custom_report.md!"
    cat tests/tool_calls.log
    exit 1
fi

echo "Test passed!"
# Clean up
rm -f custom_report.md tests/dummy_pr.md current_review.diff recent_history.diff
