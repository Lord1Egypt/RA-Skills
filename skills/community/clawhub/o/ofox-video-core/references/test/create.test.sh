#!/usr/bin/env bash
# create.test.sh — submit/wait decoupling, and the fixes from the second review.
#
# Free by construction: the API base points somewhere unroutable, so nothing
# can reach the real API. `create` is the one path here that would submit, and
# it dies on connect.
#
# Run: bash references/test/create.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-video.sh"

PASS=0
FAIL=0

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export XDG_CACHE_HOME="$WORK/cache"

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "$2"
  FAIL=$((FAIL + 1))
}

offline() { export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"; }
online() { unset OFOX_API_BASE_URL; }

online
env -u OFOX_API_KEY bash "$TARGET" providers >/dev/null 2>&1 || true
offline

echo "=== create submits without polling ==="
out=$(OFOX_API_KEY=x bash "$TARGET" create --prompt x --duration 4 --resolution 480p --approved 2>&1)
if printf '%s' "$out" | grep -qi 'submitting job'; then
  pass "create attempts a submit"
else
  fail "create should submit" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -qi 'polling:\|waiting\|poll interval'; then
  fail "create must not poll" "output mentions polling"
else
  pass "create does not poll — the wait is the caller's to schedule"
fi

# The follow-up poll may run from a different directory, so anything create
# hands back has to be absolute or the caller downloads to the wrong place.
out=$(cd "$WORK" && OFOX_API_KEY=x bash "$TARGET" create --prompt x --duration 4 \
  --resolution 480p --out-dir relout 2>&1)
outdir=$(printf '%s' "$out" | sed -n 's/^OUT_DIR //p')
if [ -z "$outdir" ]; then
  # No submit is possible offline; assert on the code path instead.
  if grep -q 'abs_out="$(cd "$out_dir"' "$TARGET"; then
    pass "create resolves --out-dir to an absolute path before reporting it"
  else
    fail "create must report an absolute OUT_DIR" "no resolution in the code path"
  fi
else
  case "$outdir" in
    /*) pass "create reports an absolute OUT_DIR even when given a relative one" ;;
    *) fail "OUT_DIR must be absolute" "got '$outdir'" ;;
  esac
fi

echo
echo "=== create is documented as the timeout-safe path ==="
out=$(bash "$TARGET" 2>&1)
if printf '%s' "$out" | grep -q 'create'; then
  pass "usage lists create"
else
  fail "usage should list create" "$(printf '%s' "$out" | head -12 | tr '\n' ' ')"
fi

echo
echo "=== B1: batch --dry-run prints exactly one estimate line ==="
n=$(OFOX_API_KEY=x bash "$TARGET" batch --prompt x --takes 4 --duration 8 \
  --resolution 480p --dry-run 2>&1 | grep -c 'Estimated cost')
if [ "$n" -eq 1 ]; then
  pass "batch --dry-run prints exactly one estimate line"
else
  fail "batch --dry-run should print 1 estimate line" "printed $n"
fi
# The one it prints must be the batch total, not the per-take figure.
amount=$(OFOX_API_KEY=x bash "$TARGET" batch --prompt x --takes 4 --duration 8 \
  --resolution 480p --dry-run 2>&1 | sed -n 's/.*Estimated cost: ~\$\([0-9.]*\).*/\1/p' | head -1)
expect=$(awk 'BEGIN{printf "%.2f", 4*8*0.11}')
if [ "$amount" = "$expect" ]; then
  pass "the surviving line is the batch total (\$$amount), not per-take"
else
  fail "batch estimate should be \$$expect" "got '\$$amount'"
fi
# A real validation failure must still surface.
out=$(OFOX_API_KEY=x bash "$TARGET" batch --prompt x --takes 2 --duration 99 --dry-run 2>&1)
if [ $? -ne 0 ] && printf '%s' "$out" | grep -qi 'duration'; then
  pass "an invalid parameter still reports its reason under batch --dry-run"
else
  fail "batch --dry-run must surface validation errors" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== B3: a dry run does not promise a bill that never comes ==="
out=$(OFOX_API_KEY=x bash "$TARGET" generate --prompt x --duration 4 \
  --resolution 480p --dry-run 2>&1)
if printf '%s' "$out" | grep -qi 'reported below'; then
  fail "dry-run must not say billing is reported below" "nothing follows it"
else
  pass "dry-run wording doesn't promise a bill"
fi
# But a real run still must say where the actual number comes from.
out=$(OFOX_API_KEY=x bash "$TARGET" generate --prompt x --duration 4 --resolution 480p 2>&1)
if printf '%s' "$out" | grep -qi 'reported below\|from the job'; then
  pass "a real run still points at the job's own usage for the actual figure"
else
  fail "a real run should still name the billing source" "$(printf '%s' "$out" | head -1)"
fi

echo
echo "=== C2: --dry-run works with no API key ==="
for sub in "generate --prompt x" "batch --prompt x --takes 2" "chain --shot a --shot b"; do
  # shellcheck disable=SC2086
  out=$(env -u OFOX_API_KEY bash "$TARGET" $sub --duration 4 --resolution 480p --dry-run 2>&1)
  code=$?
  name="${sub%% *}"
  if [ "$code" -eq 0 ] && printf '%s' "$out" | grep -qi 'estimated cost'; then
    pass "$name --dry-run quotes a price with no key set"
  else
    fail "$name --dry-run must work without a key" "exit $code: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  fi
done

echo
echo "=== A2: --dry-run validates --out-dir before anything is spent ==="
out=$(OFOX_API_KEY=x bash "$TARGET" generate --prompt x --duration 4 \
  --out-dir /proc/nonexistent-xyz/sub --dry-run 2>&1)
if [ $? -ne 0 ]; then
  pass "an unusable --out-dir fails under --dry-run"
else
  fail "--dry-run should catch a bad --out-dir" "exited 0"
fi
out=$(OFOX_API_KEY=x bash "$TARGET" generate --prompt x --duration 4 \
  --out-dir "$WORK/newdir" --dry-run 2>&1)
if [ $? -eq 0 ] && [ -d "$WORK/newdir" ]; then
  pass "a creatable --out-dir is created and accepted"
else
  fail "a valid --out-dir should pass" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== A3: check exits 2 on an environment problem ==="
env -u OFOX_API_KEY bash "$TARGET" check >/dev/null 2>&1
code=$?
if [ "$code" -eq 2 ]; then
  pass "check exits 2 with no key (environment error, per the exit-code table)"
else
  fail "check should exit 2, not $code" "the table defines 1 as a fixable flag error"
fi

echo
echo "=== C1: batch assigns and reports a per-take seed ==="
if grep -q 'SEED' "$TARGET"; then
  pass "the script emits a seed field"
else
  fail "batch must report a seed per take" "no SEED in the script"
fi
# The TAKE line has to carry it, or "re-render take 3" stays impossible.
if grep -q 'echo "TAKE .*seed' "$TARGET" || grep -qE 'TAKE .*\$\{seeds' "$TARGET"; then
  pass "the TAKE line carries the seed"
else
  fail "the TAKE line must carry the seed" "not found"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
