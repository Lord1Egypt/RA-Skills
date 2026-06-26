#!/bin/bash
set -e

echo "Setting up Planner Triad Test..."
mkdir -p tests
cat << 'EOF' > tests/dummy_triad_prd.md
# Dummy PRD for Planner Triad Test
Identifier: PL-999
Please generate a PR document based on this PRD. Make sure to include the identifier PL-999 and markdown headers.
EOF

unset SDLC_TEST_MODE

echo "Running Planner..."
python3 scripts/spawn_planner.py --prd-file tests/dummy_triad_prd.md  --workdir "$(pwd)" > tests/triad_planner.log 2>&1 || true

echo "Asserting Output..."
if grep -q "PL-999" tests/triad_planner.log && grep -q "#" tests/triad_planner.log; then
    echo "Planner Triad Test Passed."
    exit 0
else
    echo "Planner Triad Test Failed."
    cat tests/triad_planner.log
    exit 1
fi
