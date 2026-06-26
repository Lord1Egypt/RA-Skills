#!/bin/bash
set -e

WORKDIR="/root/.openclaw/workspace/projects/leio-sdlc/tests/sandbox_070"
JOBDIR="$WORKDIR/docs/PRs/dummy_job"
rm -rf "$WORKDIR"
mkdir -p "$JOBDIR"

# Create a mock content file based on the template
CONTENT_FILE="$WORKDIR/mock_content.md"
cat << 'MOCK' > "$CONTENT_FILE"
status: open

# PR-[ID]: Mock PR

## 1. Objective
Mock Obj

## 2. Target Working Set & File Placement
Mock Working Set

## 3. Implementation Scope
Mock Scope

## 4. TDD Blueprint & Acceptance Criteria
Mock TDD
MOCK

# Run create_pr_contract.py
python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/create_pr_contract.py \
    --workdir "$WORKDIR" \
    --job-dir "$JOBDIR" \
    --title "Mock PR" \
    --content-file "$CONTENT_FILE" > /dev/null

# Assert that the created file exists
CREATED_FILE=$(ls "$JOBDIR"/PR_001_Mock_PR.md)
if [ -z "$CREATED_FILE" ]; then
    echo "❌ Error: PR file not created."
    exit 1
fi

# Assert that 'status: open' exists EXACTLY ONCE
STATUS_COUNT=$(grep -c "status: open" "$CREATED_FILE" || true)

if [ "$STATUS_COUNT" -ne 1 ]; then
    echo "❌ Error: 'status: open' should appear exactly once, found $STATUS_COUNT."
    exit 1
fi

echo "✅ Test passed: 'status: open' is not duplicated and template is respected."

# Verify TEMPLATES/PR_Contract.md.template structure
TEMPLATE_FILE="/root/.openclaw/workspace/projects/leio-sdlc/TEMPLATES/PR_Contract.md.template"

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "❌ Error: $TEMPLATE_FILE does not exist."
    exit 1
fi

if ! grep -q "status: open" "$TEMPLATE_FILE"; then
    echo "❌ Error: $TEMPLATE_FILE missing 'status: open'."
    exit 1
fi

if ! grep -q "## 1. Objective" "$TEMPLATE_FILE"; then
    echo "❌ Error: $TEMPLATE_FILE missing '## 1. Objective'."
    exit 1
fi

if ! grep -q "## 2. Target Working Set & File Placement" "$TEMPLATE_FILE"; then
    echo "❌ Error: $TEMPLATE_FILE missing '## 2. Target Working Set & File Placement'."
    exit 1
fi

if ! grep -q "## 3. Implementation Scope" "$TEMPLATE_FILE"; then
    echo "❌ Error: $TEMPLATE_FILE missing '## 3. Implementation Scope'."
    exit 1
fi

if ! grep -q "## 4. TDD Blueprint & Acceptance Criteria" "$TEMPLATE_FILE"; then
    echo "❌ Error: $TEMPLATE_FILE missing '## 4. TDD Blueprint & Acceptance Criteria'."
    exit 1
fi

echo "✅ TEMPLATE structure validated."
