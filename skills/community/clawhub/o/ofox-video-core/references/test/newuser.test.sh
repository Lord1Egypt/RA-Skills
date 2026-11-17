#!/usr/bin/env bash
# newuser.test.sh — what someone with no account and no API key runs into.
#
# Everything here is free: the commands under test are the ones that work
# without a key, which is the whole point of the fixes being verified.
#
# Run: bash references/test/newuser.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-video.sh"
REPO="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

PASS=0
FAIL=0

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
export XDG_CACHE_HOME="$WORK/cache"

# Not a credential — see the note in the sibling tests.
PLACEHOLDER=placeholder

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "$2"
  FAIL=$((FAIL + 1))
}

echo "=== The keyless path actually works (the thing nobody was told) ==="
for cmd in "models" "providers"; do
  out=$(env -u OFOX_API_KEY bash "$TARGET" $cmd 2>&1)
  if [ $? -eq 0 ]; then
    pass "$cmd runs with no API key"
  else
    fail "$cmd must work without a key" "$(printf '%s' "$out" | head -1)"
  fi
done
out=$(env -u OFOX_API_KEY OFOX_API_BASE_URL="http://127.0.0.1:1/v1" \
  bash "$TARGET" generate --prompt x --duration 15 --resolution 720p \
  --out-dir "$WORK/o" --dry-run 2>&1)
if [ $? -eq 0 ] && printf '%s' "$out" | grep -qi 'estimated cost'; then
  pass "generate --dry-run quotes a price with no API key"
else
  fail "the keyless quote must work" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== ...and the docs now say so ==="
CORE="$SCRIPT_DIR/../../SKILL.md"
if grep -qiE 'no (API )?key|without a key|before you sign up|before signing up' "$CORE"; then
  pass "core SKILL.md states the quote path needs no key"
else
  fail "core SKILL.md must say --dry-run needs no key" "no such statement"
fi
README="$REPO/README.md"
if grep -q 'dry-run' "$README"; then
  pass "README mentions the keyless quote"
else
  fail "README must mention it — it is the best first impression here" "0 hits"
fi

echo
echo "=== README tells a person without an account what they're in for ==="
check_readme() {
  if grep -qiE "$2" "$README"; then
    pass "README: $1"
  else
    fail "README should state: $1" "pattern not found"
  fi
}
check_readme "this is a paid API" 'paid|costs money|per second|billed'
check_readme "roughly what a clip costs" '\$[0-9]'
check_readme "where to get a key" 'app\.ofox\.ai'
check_readme "the curl/jq prerequisites" '\bjq\b'

echo
echo "=== README no longer promises dependency resolution it can't do ==="
if grep -qi 'pulls in the one(s)\? it needs' "$README"; then
  fail "README still claims automatic dependency resolution" \
    "skills.sh.json has no dependency field to express it"
else
  pass "the unkeepable dependency promise is gone"
fi

echo
echo "=== models leads with the rate you'd actually pay ==="
out=$(env -u OFOX_API_KEY bash "$TARGET" models 2>&1)
# seedance-2.5 defaults to 720p ($0.24/s). Its headline field says 0.11 (480p).
row=$(printf '%s' "$out" | grep 'bytedance/seedance-2.5' | head -1)
if printf '%s' "$row" | grep -q '0\.24'; then
  pass "seedance-2.5 shows its default-resolution rate (0.24), not the 0.11 headline"
else
  fail "models must not lead with the 480p rate for a 720p default" "row: $row"
fi
header=$(printf '%s' "$out" | grep '^MODEL' | head -1)
if printf '%s' "$header" | grep -qiE '720p|default'; then
  pass "the price column names the resolution it refers to"
else
  fail "the price column must say which resolution it is" "header: $header"
fi

echo
echo "=== check separates 'present' from 'valid' ==="
out=$(OFOX_API_KEY="$PLACEHOLDER" bash "$TARGET" check 2>&1)
if printf '%s' "$out" | grep -qiE 'not.*verif|present.*not.*valid|not been checked'; then
  pass "check says a present key has not been verified"
else
  fail "check must not let 'OK' read as 'my key works'" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
out=$(env -u OFOX_API_KEY bash "$TARGET" check 2>&1)
if printf '%s' "$out" | grep -qi 'dry-run'; then
  pass "a keyless check points at the free quote path instead of dead-ending"
else
  fail "check should tell a keyless user they can still get a quote" \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== Scenario skills cover the keyless path and the missing-core error ==="
for s in seedance-short-drama seedance-ad-creative seedance-product-video seedance-anime-drama; do
  f="$REPO/skills/$s/SKILL.md"
  if grep -qiE 'no (API )?key|without a key|before signing up' "$f"; then
    pass "$s mentions the keyless quote"
  else
    fail "$s should mention it" "no statement"
  fi
  if grep -q 'No such file or directory' "$f"; then
    pass "$s names the missing-core-skill error"
  else
    fail "$s should name that error" "a bare path error tells a non-programmer nothing"
  fi
done

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
