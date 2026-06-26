#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PASS=0
FAIL=0
SKIP=0

pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }
skip() { echo "  SKIP: $1"; SKIP=$((SKIP + 1)); }

expect_error() {
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then
    fail "$desc (expected error, got success)"
  else
    pass "$desc"
  fi
}

echo "=== Phase 1: Argument validation (offline) ==="

expect_error "create-request: missing all args" \
  bash "$SCRIPT_DIR/create-request.sh"

expect_error "create-request: missing --type and --name" \
  bash "$SCRIPT_DIR/create-request.sh" --contact "test@test.com"

expect_error "create-request: invalid --type" \
  bash "$SCRIPT_DIR/create-request.sh" --contact "test@test.com" --type "invalid" --name "Test"

expect_error "get-request: missing --id" \
  bash "$SCRIPT_DIR/get-request.sh"

expect_error "find-requests: missing all args" \
  bash "$SCRIPT_DIR/find-requests.sh"

expect_error "get-credential: missing --id" \
  bash "$SCRIPT_DIR/get-credential.sh"

expect_error "get-mandate: missing --id" \
  bash "$SCRIPT_DIR/get-mandate.sh"

expect_error "get-mandate-vc: missing --id" \
  bash "$SCRIPT_DIR/get-mandate-vc.sh"

expect_error "resolve-did: missing --did" \
  bash "$SCRIPT_DIR/resolve-did.sh"

expect_error "get-user: missing all args" \
  bash "$SCRIPT_DIR/get-user.sh"

expect_error "cancel-request: missing --id" \
  bash "$SCRIPT_DIR/cancel-request.sh"

expect_error "resend-otp: missing --id" \
  bash "$SCRIPT_DIR/resend-otp.sh"

expect_error "create-request: FORM type blocked" \
  bash "$SCRIPT_DIR/create-request.sh" --contact "test@test.com" --type "form" --name "Test"

echo ""
echo "=== Phase 2: API integration tests ==="

if [[ -z "${VIA_API_KEY:-}" || -z "${VIA_SIGNATURE_SECRET:-}" ]]; then
  echo "  VIA_API_KEY or VIA_SIGNATURE_SECRET not set — skipping API tests"
  SKIP=$((SKIP + 5))
else
  source "$SCRIPT_DIR/sign-request.sh"

  # Test: get-user with a known contact
  echo "  Testing get-user..."
  RESULT=$(bash "$SCRIPT_DIR/get-user.sh" --contact "test@humanos.id" 2>&1) || true
  if echo "$RESULT" | jq -e . >/dev/null 2>&1; then
    pass "get-user returns valid JSON"
  else
    fail "get-user did not return valid JSON"
  fi

  # Test: create-request with consent
  echo "  Testing create-request (consent)..."
  RESULT=$(bash "$SCRIPT_DIR/create-request.sh" \
    --contact "test@humanos.id" \
    --type "consent" \
    --name "Test Consent" \
    --data '[{"label":"text","type":"string","value":"Test consent text","hidden":false}]' 2>&1) || true
  if echo "$RESULT" | jq -e '.requestId // .id // .error' >/dev/null 2>&1; then
    pass "create-request returns valid JSON"
  else
    fail "create-request did not return valid JSON"
  fi

  # Test: find-requests
  echo "  Testing find-requests..."
  RESULT=$(bash "$SCRIPT_DIR/find-requests.sh" --contact "test@humanos.id" 2>&1) || true
  if echo "$RESULT" | jq -e . >/dev/null 2>&1; then
    pass "find-requests returns valid JSON"
  else
    fail "find-requests did not return valid JSON"
  fi

  # Test: create-request with json
  echo "  Testing create-request (json)..."
  RESULT=$(bash "$SCRIPT_DIR/create-request.sh" \
    --contact "test@humanos.id" \
    --type "json" \
    --name "Test JSON" \
    --data '[{"label":"amount","type":"number","value":100,"hidden":false}]' 2>&1) || true
  if echo "$RESULT" | jq -e '.requestId // .id // .error' >/dev/null 2>&1; then
    pass "create-request (json) returns valid JSON"
  else
    fail "create-request (json) did not return valid JSON"
  fi

  echo "  NOTE: get-request, get-credential, get-mandate, resolve-did, cancel-request, resend-otp"
  echo "        require valid IDs from previous operations — skipped in automated tests."
  SKIP=$((SKIP + 1))
fi

echo ""
echo "=== Results ==="
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
echo "  Skipped: $SKIP"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
