#!/usr/bin/env bash
set -e

echo "Running Micro-Slicing Act Test..."

SANDBOX="$(pwd)/tests/planner_sandbox_$$"
trap 'cd / && [[ -n "$SANDBOX" ]] && rm -rf "$SANDBOX"' EXIT
mkdir -p "$SANDBOX/prs"
rm -f "$SANDBOX"/prs/*.md || true

cat << 'EOF' > "$SANDBOX/dummy_complex_prd.md"
# Complex Feature: Full Stack Login System
This is a complex feature that REQUIRES multiple PRs.
1. Database Schema for Users
2. Core Authentication Logic (Python)
3. API Endpoints (Flask)
4. UI Integration (React)
Please generate a sequential, dependency-ordered chain of Micro-PRs.
EOF

# Run Planner
SDLC_TEST_MODE=true python3 scripts/spawn_planner.py --prd-file "$SANDBOX/dummy_complex_prd.md" --out-dir "$SANDBOX/prs" --workdir "$(pwd)" --global-dir "$(pwd)"

# Assertions
PR_COUNT=$(ls -1q "$SANDBOX/prs/"*.md 2>/dev/null | wc -l)

if [ "$PR_COUNT" -le 1 ]; then
    echo "❌ Micro-Slicing failed: Planner generated only $PR_COUNT PR(s)."
    exit 1
fi

echo "✅ Planner generated $PR_COUNT PRs."

# Verify "status: open" and alphabetical prefixes
PREV_NAME=""
for file in "$SANDBOX/prs/"*.md; do
    filename=$(basename "$file")
    
    # Check status: open
    if ! grep -q "status: open" "$file"; then
        echo "❌ Micro-Slicing failed: '$filename' is missing 'status: open'."
        exit 1
    fi
    
    # Check simple alphabetical order implicitly based on ls
    if [[ "$PREV_NAME" != "" && "$filename" < "$PREV_NAME" ]]; then
         echo "❌ Micro-Slicing failed: '$filename' is not sorted after '$PREV_NAME'."
         exit 1
    fi
    PREV_NAME="$filename"
done

echo "✅ All PRs contain 'status: open' and are correctly sorted."
exit 0
