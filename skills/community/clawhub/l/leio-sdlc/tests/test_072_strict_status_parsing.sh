#!/bin/bash
set -e

DIR="/tmp/test_072_workspace_$$"
mkdir -p "$DIR/docs/PRs/mock_072"

cat << 'FILEEOF' > "$DIR/docs/PRs/mock_072/PR_001_Mock.md"
status: completed

# PR-001
This PR fixes the `status: open` bug.
The previous system falsely detected the text "status: open" in this sentence!
FILEEOF

echo "Running Assertion 1..."
cd "$DIR"
OUTPUT=$(python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/get_next_pr.py --workdir . --job-dir docs/PRs/mock_072)

if echo "$OUTPUT" | grep -q "QUEUE_EMPTY"; then
    echo "Assertion 1 passed."
else
    echo "Assertion 1 failed. Output was: $OUTPUT"
    exit 1
fi

echo "Running Assertion 2..."
python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/update_pr_status.py --pr-file "$DIR/docs/PRs/mock_072/PR_001_Mock.md" --status in_progress

HEAD_LINE=$(head -n 1 "$DIR/docs/PRs/mock_072/PR_001_Mock.md")
if [ "$HEAD_LINE" != "status: in_progress" ]; then
    echo "Assertion 2 failed. First line is: $HEAD_LINE"
    exit 1
fi

BODY_LINE=$(grep "This PR fixes the \`status: open\` bug." "$DIR/docs/PRs/mock_072/PR_001_Mock.md")
if [ -z "$BODY_LINE" ]; then
    echo "Assertion 2 failed. Body 'status: open' was modified."
    exit 1
fi

echo "Assertion 2 passed."
rm -rf "$DIR"
exit 0
