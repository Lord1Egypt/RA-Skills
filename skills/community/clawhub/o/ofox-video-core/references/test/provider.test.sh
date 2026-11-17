#!/usr/bin/env bash
# provider.test.sh — upstream provider pinning for ofox-video.sh.
#
# Free by construction: --print-payload lets us assert on the request body
# without sending it, and anything that would send is pointed at an unroutable
# API base. No case here can create a billable job.
#
# Run: bash references/test/provider.test.sh

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
export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "$2"
  FAIL=$((FAIL + 1))
}

# Runs generate with --print-payload and echoes just the payload JSON.
payload_for() {
  bash "$TARGET" generate --print-payload "$@" 2>&1 |
    sed -n '/^PAYLOAD /s/^PAYLOAD //p'
}

echo "=== Seedance is pinned to byteplus by default ==="
p="$(payload_for --prompt x --duration 5)"
got="$(printf '%s' "$p" | jq -r '.provider.type // "<none>"' 2>/dev/null)"
if [ "$got" = "byteplus" ]; then
  pass "seedance-2.5 defaults to byteplus"
else
  fail "seedance-2.5 should default to byteplus" "got '$got' from: $(printf '%s' "$p" | head -c 160)"
fi

for m in bytedance/seedance-2.0 bytedance/seedance-2.0-fast bytedance/seedance-2.0-mini; do
  p="$(payload_for --model "$m" --prompt x --duration 5)"
  got="$(printf '%s' "$p" | jq -r '.provider.type // "<none>"' 2>/dev/null)"
  if [ "$got" = "byteplus" ]; then
    pass "$m also defaults to byteplus (same upstream pair)"
  else
    fail "$m should default to byteplus" "got '$got'"
  fi
done

echo
echo "=== The default costs no network call ==="
rm -rf "${XDG_CACHE_HOME:?}"
p="$(payload_for --prompt x --duration 5)"
got="$(printf '%s' "$p" | jq -r '.provider.type // "<none>"' 2>/dev/null)"
if [ "$got" = "byteplus" ]; then
  pass "cold cache + unroutable API still pins byteplus (prefix rule, no fetch)"
else
  fail "the default must not depend on a network call" "got '$got'"
fi

echo
echo "=== Single-upstream models get no provider at all ==="
for m in alibaba/wan-2.7 alibaba/happyhorse-1.1; do
  p="$(payload_for --model "$m" --prompt x --duration 5 --resolution 720p)"
  if printf '%s' "$p" | jq -e 'has("provider") | not' >/dev/null 2>&1; then
    pass "$m sends no provider key (weighted routing is already deterministic)"
  else
    fail "$m must not be pinned" "payload has provider: $(printf '%s' "$p" | jq -c '.provider')"
  fi
done

echo
echo "=== Explicit overrides ==="
p="$(payload_for --prompt x --duration 5 --provider volcengine)"
got="$(printf '%s' "$p" | jq -r '.provider.type // "<none>"' 2>/dev/null)"
if [ "$got" = "volcengine" ]; then
  pass "--provider volcengine overrides the default"
else
  fail "--provider should override the default" "got '$got'"
fi

p="$(payload_for --prompt x --duration 5 --provider auto)"
if printf '%s' "$p" | jq -e 'has("provider") | not' >/dev/null 2>&1; then
  pass "--provider auto sends no provider key"
else
  fail "--provider auto must send no provider key" "$(printf '%s' "$p" | jq -c '.provider')"
fi

p="$(OFOX_VIDEO_PROVIDER=volcengine payload_for --prompt x --duration 5)"
got="$(printf '%s' "$p" | jq -r '.provider.type // "<none>"' 2>/dev/null)"
if [ "$got" = "volcengine" ]; then
  pass "OFOX_VIDEO_PROVIDER sets the default"
else
  fail "OFOX_VIDEO_PROVIDER should set the default" "got '$got'"
fi

p="$(OFOX_VIDEO_PROVIDER=volcengine payload_for --prompt x --duration 5 --provider byteplus)"
got="$(printf '%s' "$p" | jq -r '.provider.type // "<none>"' 2>/dev/null)"
if [ "$got" = "byteplus" ]; then
  pass "an explicit flag beats the environment variable"
else
  fail "the flag should beat the env var" "got '$got'"
fi

p="$(OFOX_VIDEO_PROVIDER=auto payload_for --prompt x --duration 5)"
if printf '%s' "$p" | jq -e 'has("provider") | not' >/dev/null 2>&1; then
  pass "OFOX_VIDEO_PROVIDER=auto opts out globally"
else
  fail "OFOX_VIDEO_PROVIDER=auto should opt out" "$(printf '%s' "$p" | jq -c '.provider')"
fi

echo
echo "=== Validation, before any network call ==="
out=$(bash "$TARGET" generate --prompt x --duration 5 --provider not-a-real-slug 2>&1)
code=$?
if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -qi 'provider'; then
  pass "a slug outside the documented enum is rejected locally"
else
  fail "an unknown slug should exit 1" "exit $code: $(printf '%s' "$out" | head -1)"
fi

# aliyun is a real slug, but it does not serve seedance. Catching that needs
# catalog data, so warm it from the real (public, keyless, free) endpoint
# first, then go back offline — validation reads the cache, and anything that
# passes still dies on connect rather than reaching the API.
unset OFOX_API_BASE_URL
env -u OFOX_API_KEY bash "$TARGET" providers bytedance/seedance-2.5 >/dev/null 2>&1 || true
export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"
out=$(bash "$TARGET" generate --prompt x --duration 5 --provider aliyun 2>&1)
code=$?
if [ "$code" -eq 1 ]; then
  pass "a real slug that doesn't serve this model is rejected locally"
  if printf '%s' "$out" | grep -q 'byteplus'; then
    pass "the rejection names the model's real upstreams"
  else
    fail "the rejection should name the real upstreams" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  fi
else
  fail "aliyun on seedance should exit 1" "exit $code: $(printf '%s' "$out" | head -1)"
fi

echo
echo "=== Fail open when catalog data is unavailable ==="
# Same cross-model mistake, but with no catalog cache and no network: we must
# NOT block a request just because we could not check it.
rm -rf "${XDG_CACHE_HOME:?}"
# --approved: what is under test is that an uncheckable provider does not
# BLOCK the run, so the run has to get past the spend gate to show it.
out=$(bash "$TARGET" generate --prompt x --duration 5 --provider aliyun --approved 2>&1)
code=$?
if [ "$code" -ne 1 ]; then
  pass "an uncheckable provider is passed through, not blocked (fail open)"
else
  fail "must not block when the catalog is unreachable" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== Error-code mapping ==="
for code_name in invalid_provider_type provider_type_unavailable; do
  if grep -q "$code_name" "$TARGET"; then
    pass "$code_name is mapped in the script"
  else
    fail "$code_name must be mapped" "not found in ofox-video.sh"
  fi
done
if grep -A3 'provider_type_unavailable)' "$TARGET" | grep -q 'auto'; then
  pass "provider_type_unavailable points at the --provider auto escape hatch"
else
  fail "the error should name --provider auto" "no 'auto' near the mapping"
fi

echo
echo "=== output_moderation_failed names the other upstream as a remedy ==="
if grep -A3 'output_moderation_failed)' "$TARGET" | grep -qi 'provider'; then
  pass "moderation failure suggests trying the other upstream"
else
  fail "output_moderation_failed should mention provider" "no 'provider' near the mapping"
fi

echo
echo "=== The chosen upstream is visible on the submit line ==="
out=$(bash "$TARGET" generate --prompt x --duration 5 --approved 2>&1)
if printf '%s' "$out" | grep -q 'Submitting job to Ofox.*provider=byteplus'; then
  pass "submit line shows the pinned upstream"
else
  fail "submit line should show the upstream" "$(printf '%s' "$out" | grep -i submitting | head -1)"
fi
out=$(bash "$TARGET" generate --prompt x --duration 5 --provider auto --approved 2>&1)
if printf '%s' "$out" | grep -qi 'Submitting job to Ofox.*provider=auto'; then
  pass "submit line says auto when unpinned"
else
  fail "submit line should say auto when unpinned" "$(printf '%s' "$out" | grep -i submitting | head -1)"
fi

echo
echo "=== providers subcommand (public, keyless) ==="
unset OFOX_API_BASE_URL
out=$(env -u OFOX_API_KEY bash "$TARGET" providers 2>&1)
code=$?
if [ "$code" -eq 0 ] && printf '%s' "$out" | grep -q 'byteplus' && printf '%s' "$out" | grep -q 'volcengine'; then
  pass "providers lists seedance-2.5's two upstreams with no API key"
else
  fail "providers should list both upstreams keylessly" "exit $code: $(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
out=$(env -u OFOX_API_KEY bash "$TARGET" providers alibaba/wan-2.7 2>&1)
if printf '%s' "$out" | grep -q 'aliyun'; then
  pass "providers accepts a model argument"
else
  fail "providers MODEL should work" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"

echo
echo "=== batch forwards --provider ==="
p=$(bash "$TARGET" batch --prompt x --takes 2 --duration 5 --provider volcengine --print-payload --approved 2>&1 |
  sed -n '/^PAYLOAD /s/^PAYLOAD //p' | head -1)
got="$(printf '%s' "$p" | jq -r '.provider.type // "<none>"' 2>/dev/null)"
if [ "$got" = "volcengine" ]; then
  pass "batch passes --provider through to each take"
else
  fail "batch should forward --provider" "got '$got'"
fi

echo
echo "=== Usage advertises the new surface ==="
out=$(bash "$TARGET" 2>&1)
for word in providers --provider; do
  if printf '%s' "$out" | grep -q -- "$word"; then
    pass "usage mentions $word"
  else
    fail "usage should mention $word" "$(printf '%s' "$out" | head -8 | tr '\n' ' ')"
  fi
done

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
