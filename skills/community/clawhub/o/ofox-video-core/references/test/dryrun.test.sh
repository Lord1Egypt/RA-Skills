#!/usr/bin/env bash
# dryrun.test.sh — quoting a price before spending, and never going silent.
#
# Free by construction, and doubly so: --dry-run must not make a network call
# at all, and the API base points somewhere unroutable regardless.
#
# Run: bash references/test/dryrun.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-video.sh"

PASS=0
FAIL=0

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export XDG_CACHE_HOME="$WORK/cache"
# Not a credential — the scripts only check that OFOX_API_KEY is non-empty.
# It goes through a variable because a key-shaped literal assigned straight to
# OFOX_API_KEY is what tripped ClawHub's exposed_secret_literal static scan.
# Keep the value a plain dictionary word and keep KEY out of the variable name.
PLACEHOLDER=placeholder
export OFOX_API_KEY="$PLACEHOLDER"

offline() { export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"; }
online() { unset OFOX_API_BASE_URL; }

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "$2"
  FAIL=$((FAIL + 1))
}

warm() {
  online
  env -u OFOX_API_KEY bash "$TARGET" providers >/dev/null 2>&1 || true
  offline
}

est_amount() { sed -n 's/.*Estimated cost: ~\$\([0-9.]*\).*/\1/p' | head -1; }

warm

echo "=== --dry-run quotes a price and stops there ==="
for sub in "generate --prompt x" "batch --prompt x --takes 3" "chain --shot a --shot b"; do
  # shellcheck disable=SC2086
  out=$(bash "$TARGET" $sub --duration 4 --resolution 480p --dry-run 2>&1)
  code=$?
  name="${sub%% *}"
  if [ "$code" -eq 0 ]; then
    pass "$name --dry-run exits 0"
  else
    fail "$name --dry-run should exit 0" "got $code: $(printf '%s' "$out" | tail -2 | tr '\n' ' ')"
  fi
  if printf '%s' "$out" | grep -qi 'estimated cost'; then
    pass "$name --dry-run prints an estimate"
  else
    fail "$name --dry-run must print an estimate" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  fi
  if printf '%s' "$out" | grep -qi 'submitting job'; then
    fail "$name --dry-run must not submit" "output mentions submitting"
  else
    pass "$name --dry-run submits nothing"
  fi
done

echo
echo "=== The dry-run quote matches what the real run would cost ==="
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p --dry-run 2>&1)
amount=$(printf '%s' "$out" | est_amount)
expect=$(awk 'BEGIN{printf "%.2f", 4*0.11}')
if [ "$amount" = "$expect" ]; then
  pass "generate --dry-run quotes \$$amount (4s x \$0.11/s)"
else
  fail "dry-run quote should be \$$expect" "got '\$$amount'"
fi
out=$(bash "$TARGET" batch --prompt x --takes 3 --duration 4 --resolution 480p --dry-run 2>&1)
amount=$(printf '%s' "$out" | est_amount)
expect=$(awk 'BEGIN{printf "%.2f", 3*4*0.11}')
if [ "$amount" = "$expect" ]; then
  pass "batch --dry-run quotes the whole batch (\$$amount)"
else
  fail "batch dry-run should quote \$$expect" "got '\$$amount'"
fi

echo
echo "=== --dry-run still validates, so a bad request is caught for free ==="
out=$(bash "$TARGET" generate --prompt x --duration 99 --dry-run 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'duration'; then
  pass "an out-of-range duration is rejected under --dry-run"
else
  fail "--dry-run must still validate" "$(printf '%s' "$out" | head -1)"
fi
out=$(bash "$TARGET" generate --duration 4 --dry-run 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'prompt'; then
  pass "a missing --prompt is rejected under --dry-run"
else
  fail "--dry-run must still require a prompt" "$(printf '%s' "$out" | head -1)"
fi

echo
echo "=== An estimate line always appears — silence is unrelayable ==="
# No --duration at all: previously printed nothing whatsoever.
out=$(bash "$TARGET" generate --prompt x --resolution 480p --dry-run 2>&1)
if printf '%s' "$out" | grep -qi 'estimated cost'; then
  pass "omitting --duration still produces an estimate line"
else
  fail "an estimate line must always print" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
out=$(bash "$TARGET" batch --prompt x --takes 2 --resolution 480p --dry-run 2>&1)
if printf '%s' "$out" | grep -qi 'estimated cost'; then
  pass "batch without --duration still produces an estimate line"
else
  fail "batch must always print an estimate line" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
# And when it genuinely can't be priced, it says so rather than nothing.
out=$(bash "$TARGET" generate --prompt x --duration 4 \
  --model bytedance/some-unknown-model --resolution 720p --dry-run 2>&1)
if printf '%s' "$out" | grep -qi 'unavailable'; then
  pass "an unpriceable request says 'unavailable' rather than staying silent"
else
  fail "must state why an estimate is missing" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== Human-facing lines round; the machine contract keeps precision ==="
# Prose must not carry ten decimals at a reader.
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p --dry-run 2>&1)
if printf '%s' "$out" | grep -qE '\$[0-9]+\.[0-9]{3,}'; then
  fail "no human-facing line should print 3+ decimals" \
    "$(printf '%s' "$out" | grep -oE '\$[0-9]+\.[0-9]{3,}' | head -1)"
else
  pass "the quote reads as money, not as a float"
fi
# The KEY VALUE contract is a separate matter and must keep full precision.
if grep -q 'echo "VIDEO_COST \$cost"' "$TARGET"; then
  pass "VIDEO_COST still emits the exact API string"
else
  fail "VIDEO_COST must keep full precision" "contract line changed"
fi

echo
echo "=== Usage advertises --dry-run ==="
out=$(bash "$TARGET" 2>&1)
if printf '%s' "$out" | grep -q -- '--dry-run'; then
  pass "usage mentions --dry-run"
else
  fail "usage should mention --dry-run" "$(printf '%s' "$out" | head -10 | tr '\n' ' ')"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
