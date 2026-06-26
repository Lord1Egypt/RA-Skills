#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

pass() { printf "[PASS] %s\n" "$1"; }
fail() { printf "[FAIL] %s\n" "$1"; exit 1; }
skip() { printf "[SKIP] %s\n" "$1"; }

HAS_GPU=false
if command -v gpu >/dev/null 2>&1; then HAS_GPU=true; fi

# --- Tests that don't need the gpu binary ---

# 1) Deny semicolon injection
if ./runner.sh gpu status --json \; rm -rf / 2>/dev/null; then
  fail "semicolon injection not blocked"
else
  pass "semicolon injection blocked"
fi

# 2) Deny dollar-sign injection
if SKILL_INPUT='gpu status $(id)' ./runner.sh 2>/dev/null; then
  fail "dollar injection not blocked"
else
  pass "dollar injection blocked"
fi

# --- Tests that need the gpu binary ---

if [[ "$HAS_GPU" != true ]]; then
  skip "gpu binary not on PATH; skipping preflight tests"
  echo "Self-tests completed (some skipped)."
  exit 0
fi

# 3) Preflight dry-run of a safe command (exits 4 = blocked by dry-run)
SKILL_DRY_RUN=true SKILL_REQUIRE_CONFIRM=false ./runner.sh gpu status --json && EXIT=$? || EXIT=$?
if [[ $EXIT -eq 4 ]]; then
  pass "dry-run status (exit 4 = blocked as expected)"
else
  fail "dry-run status: expected exit 4, got $EXIT"
fi

# 4) Doctor dry-run (exits 4 = blocked by dry-run)
OUT=$(./runner.sh gpu doctor --json 2>&1) && EXIT=$? || EXIT=$?
if [[ $EXIT -eq 4 ]]; then
  pass "doctor dry-run (exit 4 = blocked as expected)"
elif [[ $EXIT -eq 0 ]]; then
  pass "doctor ran"
else
  echo "$OUT"
  fail "doctor failed with exit $EXIT"
fi

echo "All self-tests completed."
