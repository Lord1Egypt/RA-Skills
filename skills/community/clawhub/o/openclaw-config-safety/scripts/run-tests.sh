#!/usr/bin/env bash
# run-tests.sh — Run config-safety skill tests

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

PASS=0
FAIL=0

for f in test/*.test.js; do
  name=$(basename "$f" .test.js)
  if node "$f" > /tmp/test-$name.out 2>&1; then
    echo "✅ $name"
    PASS=$((PASS+1))
  else
    echo "❌ $name (see /tmp/test-$name.out)"
    FAIL=$((FAIL+1))
    cat /tmp/test-$name.out | grep FAIL | head -5
  fi
done

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
