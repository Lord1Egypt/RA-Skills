#!/usr/bin/env bash
# validation.test.sh — model and parameter validation for ofox-image.sh.
#
# Free by construction: rejected cases exit before any network call, and
# accepted cases are pointed at an unroutable API base so they fail on connect
# instead of generating a billable image.
#
# Run: bash references/test/validation.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-image.sh"

if [ ! -f "$TARGET" ]; then
  echo "FATAL: cannot find ofox-image.sh at $TARGET" >&2
  exit 1
fi

PASS=0
FAIL=0

CACHE_ROOT="$(mktemp -d)"
trap 'rm -rf "$CACHE_ROOT"' EXIT

export XDG_CACHE_HOME="$CACHE_ROOT"
# Not a credential — the scripts only check that OFOX_API_KEY is non-empty.
# It goes through a variable because a key-shaped literal assigned straight to
# OFOX_API_KEY is what tripped ClawHub's exposed_secret_literal static scan.
# Keep the value a plain dictionary word and keep KEY out of the variable name.
PLACEHOLDER=placeholder
export OFOX_API_KEY="$PLACEHOLDER"

offline_base() { export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"; }
online_base() { unset OFOX_API_BASE_URL; }

expect_reject() {
  local want="$1" desc="$2"
  shift 3
  local out code
  out=$(bash "$TARGET" generate "$@" 2>&1)
  code=$?
  if [ "$code" -ne 1 ]; then
    printf 'FAIL  %s\n      expected exit 1 (validation), got %s\n      output: %s\n' \
      "$desc" "$code" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    FAIL=$((FAIL + 1))
    return
  fi
  if ! printf '%s' "$out" | grep -qi -- "$want"; then
    printf 'FAIL  %s\n      exit 1 as expected, but message did not mention %s\n      output: %s\n' \
      "$desc" "$want" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    FAIL=$((FAIL + 1))
    return
  fi
  printf 'ok    %s\n' "$desc"
  PASS=$((PASS + 1))
}

expect_accept() {
  local desc="$1"
  shift 2
  local out code
  out=$(bash "$TARGET" generate "$@" 2>&1)
  code=$?
  if [ "$code" -eq 1 ]; then
    printf 'FAIL  %s\n      validation rejected a model/combination the API supports\n      output: %s\n' \
      "$desc" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    FAIL=$((FAIL + 1))
    return
  fi
  printf 'ok    %s (passed validation, exit %s)\n' "$desc" "$code"
  PASS=$((PASS + 1))
}

# Warm the model cache from the real endpoint (public, keyless, free), then
# point the API base somewhere unroutable. Validation still sees a live model
# list, but a request that passes it dies on connect instead of reaching the
# real generations endpoint. Without this split, every accept case below would
# fire a real request at api.ofox.ai.
warm_cache_then_go_offline() {
  rm -rf "${CACHE_ROOT:?}"/*
  online_base
  env -u OFOX_API_KEY bash "$TARGET" models >/dev/null 2>&1 || true
  offline_base
}

echo "=== Models the API supports are no longer rejected locally ==="
warm_cache_then_go_offline
expect_accept "openai/gpt-image-2 (was hardcoded)" -- \
  --model openai/gpt-image-2 --prompt x --quality high
expect_accept "openai/gpt-image-1.5 (was rejected)" -- \
  --model openai/gpt-image-1.5 --prompt x --quality high
expect_accept "google/gemini-3-pro-image (was rejected)" -- \
  --model google/gemini-3-pro-image --prompt x --quality high
expect_accept "volcengine/doubao-seedream-5.0-pro (was rejected)" -- \
  --model volcengine/doubao-seedream-5.0-pro --prompt x --quality high
expect_accept "microsoft/mai-image-2.5 (was rejected)" -- \
  --model microsoft/mai-image-2.5 --prompt x --quality high

echo
echo "=== --model is optional now, and resolves to one concrete id ==="
# It used to be required, refused a default, and rejected the call outright.
# The default is the priority chain; what makes that acceptable rather than
# "silently picking a price" is that the resolved id and its price go in
# front of the user before every spend (--dry-run + the approval gate).
warm_cache_then_go_offline
expect_accept "omitting --model resolves the chain instead of failing" -- \
  --prompt x --quality high
expect_accept "--model auto is the same as omitting it" -- \
  --model auto --prompt x --quality high

echo
echo "=== Wrong-endpoint and unknown models are still caught ==="
# These reject before any network call, so a live base is safe here.
online_base
expect_reject "image generation" "a video model is rejected for image generation" -- \
  --model bytedance/seedance-2.5 --prompt x --quality high
expect_reject "model" "an unknown model id is rejected when the list is live" -- \
  --model openai/does-not-exist-xyz --prompt x --quality high

echo
echo "=== Offline: unknown ids defer to the API, known ones still validate ==="
rm -rf "${CACHE_ROOT:?}"/*
offline_base
expect_accept "unknown model deferred when only a snapshot is available" -- \
  --model openai/model-newer-than-the-snapshot --prompt x --quality high
out=$(bash "$TARGET" generate --model openai/gpt-image-2 --prompt x --quality high 2>&1)
# Match only the snapshot notice — 'could not reach' would also match the
# connect failure that follows it, which would pass this test for free.
if printf '%s' "$out" | grep -qi 'bundled snapshot'; then
  printf 'ok    falling back to the bundled snapshot is announced, not silent\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  snapshot fallback must warn on stderr\n      output: %s\n' \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi

echo
echo "=== models subcommand ==="
rm -rf "${CACHE_ROOT:?}"/*
online_base
out=$(env -u OFOX_API_KEY bash "$TARGET" models 2>&1)
code=$?
if [ "$code" -eq 0 ] && printf '%s' "$out" | grep -q 'gpt-image-2'; then
  printf 'ok    models lists image models with no API key (endpoint is public)\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  models should list image models without a key (exit %s)\n      output: %s\n' \
    "$code" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi
if printf '%s' "$out" | grep -q 'seedance-2.5'; then
  printf 'FAIL  models must not list video models\n'
  FAIL=$((FAIL + 1))
else
  printf 'ok    models lists only image models\n'
  PASS=$((PASS + 1))
fi

echo
echo "=== Parameters the API does not describe stay hardcoded and enforced ==="
offline_base
expect_reject "prompt" "--prompt is still required" -- \
  --model openai/gpt-image-2 --quality high
expect_reject "quality" "--quality is still required" -- \
  --model openai/gpt-image-2 --prompt x
expect_reject "quality" "an undocumented --quality is still rejected" -- \
  --model openai/gpt-image-2 --prompt x --quality ultra
expect_reject "size" "an undocumented --size is still rejected" -- \
  --model openai/gpt-image-2 --prompt x --quality high --size 123x456
expect_reject "n" "--n out of range is still rejected" -- \
  --model openai/gpt-image-2 --prompt x --quality high --n 99
expect_reject "n" "--n is still rejected for the model that cannot take it" -- \
  --model google/gemini-3.1-flash-image --prompt x --quality high --n 1

echo
echo "=== --quality is checked against the model, not just the union ==="
# The union (auto low medium high standard hd) says a value exists somewhere
# in this API. It does not say it exists on the model that will serve the
# request — and 'standard' is the value where those two differ. It passed
# validation, passed --dry-run, and then died at submission with
#   Invalid value: 'standard'. Supported values are: 'low', 'medium',
#   'high', and 'auto'
# the day MODEL_CHAIN's head became openai/gpt-image-2 (2026-09-04). Five
# copy-pasteable commands in two other skills shipped broken that way.
warm_cache_then_go_offline
expect_reject "standard" "--quality standard is rejected for the model that refused it upstream" -- \
  --model openai/gpt-image-2 --prompt x --quality standard
expect_reject "hd" "--quality hd is rejected too — the same enumeration excludes it" -- \
  --model openai/gpt-image-2 --prompt x --quality hd

# The four values the API's own message listed must all still work, or this
# check has replaced a 400 with something worse: a false rejection, which
# costs nothing to the API and blocks the caller completely.
for q in auto low medium high; do
  expect_accept "--quality $q is accepted by gpt-image-2 (its own enumeration)" -- \
    --model openai/gpt-image-2 --prompt x --quality "$q"
done

# The rejection must be reachable without --model, because that is how it
# actually happened — nobody typed 'openai/gpt-image-2'; the chain did.
expect_reject "standard" "the chain-resolved model rejects it too, with no --model passed" -- \
  --prompt x --quality standard
out=$(bash "$TARGET" generate --prompt x --quality standard 2>&1)
if printf '%s' "$out" | grep -q 'openai/gpt-image-2'; then
  printf 'ok    the error names the model the request resolved to\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  an error about an unpassed model must name it\n      output: %s\n' \
    "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi
if printf '%s' "$out" | grep -qi 'no --model was passed'; then
  printf 'ok    and says where that model came from, so it connects to something the user typed\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  the error must say the model came from the chain, not from the caller\n      output: %s\n' \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi
if printf '%s' "$out" | grep -qi -- '--model'; then
  printf 'ok    and offers pinning a different --model as one of the fixes\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  the error must name pinning --model as a fix\n      output: %s\n' \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi

# The other half of the rule: where a model's accepted set has never been
# enumerated, an absence of evidence stays permissive. mai-image-2.5-flash
# took 'standard' on nine real runs; narrowing it on the strength of that
# would invent a whitelist and reject calls that work.
expect_accept "--quality standard still works on the model that accepts it, when pinned" -- \
  --model microsoft/mai-image-2.5-flash --prompt x --quality standard
expect_accept "an unenumerated model keeps the full union (no invented whitelist)" -- \
  --model google/gemini-3.1-flash-image --prompt x --quality standard
expect_accept "--quality hd survives on an unenumerated model as well" -- \
  --model microsoft/mai-image-2.5 --prompt x --quality hd

# And a value outside the union is still caught first, by the union check,
# so the per-model check never has to speak for values nothing accepts.
expect_reject "not a documented value" "a value outside the union is still caught by the union check" -- \
  --model microsoft/mai-image-2.5-flash --prompt x --quality ultra

# check must not have grown a dependency on knowing the model.
out=$(bash "$TARGET" check 2>&1)
code=$?
if [ "$code" -eq 0 ]; then
  printf 'ok    check still passes with no model in hand\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  check must not need a model to validate the environment (exit %s)\n      output: %s\n' \
    "$code" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi

# The table is first-hand only, and that is a property worth pinning: one row
# today, and any row added later has to come with an enumeration.
enumerated=$(sed -n '/^model_qualities() {/,/^}/p' "$TARGET" | sed -n 's/^ *\([a-z0-9./|-]*\)) echo .*/\1/p' | tr '\n' ' ')
if [ "$(echo "$enumerated" | xargs)" = "openai/gpt-image-2" ]; then
  printf 'ok    exactly one model has a first-hand quality enumeration\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  model_qualities() gained a row — was it sourced from the API, or guessed?\n      rows: %s\n' \
    "$enumerated"
  FAIL=$((FAIL + 1))
fi
echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
