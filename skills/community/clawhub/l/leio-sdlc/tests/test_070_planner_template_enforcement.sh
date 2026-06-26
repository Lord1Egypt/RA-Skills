#!/bin/bash
set -e

# Setup mock PRD
MOCK_PRD="tests/mock_prd_070.md"
echo "# Mock PRD for Template Test" > "$MOCK_PRD"

# Run planner in test mode
export SDLC_TEST_MODE=true
OUT_DIR="docs/PRs/mock_prd_070"
rm -rf "$OUT_DIR"
python3 scripts/spawn_planner.py --workdir . --prd-file "$MOCK_PRD" --out-dir "$OUT_DIR"

# Verify outputs
for pr_file in "$OUT_DIR"/*.md; do
    if [ ! -f "$pr_file" ]; then
        echo "FAIL: No PR files generated."
        exit 1
    fi

    # Check status: open
    if ! head -n 1 "$pr_file" | grep -q "^status: open$"; then
        echo "FAIL: PR file $pr_file does not start with 'status: open'"
        exit 1
    fi

    # Check multiple status: open (duplicates)
    STATUS_COUNT=$(grep -c "^status: open" "$pr_file" || true)
    if [ "$STATUS_COUNT" -gt 1 ]; then
        echo "FAIL: PR file $pr_file contains duplicate 'status: open'"
        exit 1
    fi

    # Check headers
    if ! grep -q "## 1. Objective" "$pr_file"; then
        echo "FAIL: PR file $pr_file is missing '## 1. Objective'"
        exit 1
    fi

    if ! grep -q "## 2. Target Working Set & File Placement" "$pr_file"; then
        echo "FAIL: PR file $pr_file is missing '## 2. Target Working Set & File Placement'"
        exit 1
    fi

    if ! grep -q "## 3. Implementation Scope" "$pr_file"; then
        echo "FAIL: PR file $pr_file is missing '## 3. Implementation Scope'"
        exit 1
    fi

    if ! grep -q "## 4. TDD Blueprint & Acceptance Criteria" "$pr_file"; then
        echo "FAIL: PR file $pr_file is missing '## 4. TDD Blueprint & Acceptance Criteria'"
        exit 1
    fi
done

echo "PASS: test_070_planner_template_enforcement.sh"
