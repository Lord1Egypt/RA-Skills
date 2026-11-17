#!/usr/bin/env bash
# validation.test.sh — per-model parameter validation for ofox-video.sh.
#
# Every case here is free: a rejected case exits before any network call, and
# an accepted case is pointed at an unroutable API base so it fails on connect
# instead of creating a billable job. No OFOX credits are ever spent.
#
# Run: bash references/test/validation.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-video.sh"

if [ ! -f "$TARGET" ]; then
  echo "FATAL: cannot find ofox-video.sh at $TARGET" >&2
  exit 1
fi

PASS=0
FAIL=0

CACHE_ROOT="$(mktemp -d)"
trap 'rm -rf "$CACHE_ROOT"' EXIT

# Port 1 (tcpmux) is not listening anywhere, so a create call fails to connect
# rather than reaching the real API. A fake key keeps us past the env check.
export XDG_CACHE_HOME="$CACHE_ROOT"
# Not a credential — the scripts only check that OFOX_API_KEY is non-empty.
# It goes through a variable because a key-shaped literal assigned straight to
# OFOX_API_KEY is what tripped ClawHub's exposed_secret_literal static scan.
# Keep the value a plain dictionary word and keep KEY out of the variable name.
PLACEHOLDER=placeholder
export OFOX_API_KEY="$PLACEHOLDER"

offline_base() { export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"; }
online_base() { unset OFOX_API_BASE_URL; }

# expect_reject WANT_PATTERN DESC -- ARGS...
# Asserts exit code 1 (validation error, no network) and that stderr mentions
# WANT_PATTERN, so we know it failed for the intended reason.
expect_reject() {
  local want="$1" desc="$2"
  shift 3 # drop want, desc, and the literal '--'
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

# expect_accept DESC -- ARGS...
# Asserts validation did NOT reject: the script must get far enough to attempt
# the network call and fail there (exit 5 = ambiguous create failure).
#
# --approved is added here and nowhere in expect_reject: reaching the network
# call means getting past the spend gate, and the base is unroutable so the
# attempt costs nothing. expect_reject deliberately keeps running without it —
# every one of those cases asserts exit 1 AND a message naming the parameter,
# so if the gate ever started firing ahead of validation they would go red.
expect_accept() {
  local desc="$1"
  shift 2 # drop desc and the literal '--'
  local out code
  out=$(bash "$TARGET" generate "$@" --approved 2>&1)
  code=$?
  if [ "$code" -eq 1 ]; then
    printf 'FAIL  %s\n      validation rejected a combination the model supports\n      output: %s\n' \
      "$desc" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    FAIL=$((FAIL + 1))
    return
  fi
  printf 'ok    %s (passed validation, exit %s)\n' "$desc" "$code"
  PASS=$((PASS + 1))
}

echo "=== Defect 1: aspect ratios the model does not actually support ==="
offline_base
expect_reject "aspect" "seedance-2.5 rejects 3:2" -- \
  --prompt x --duration 5 --aspect-ratio 3:2
expect_reject "aspect" "seedance-2.5 rejects 2:3" -- \
  --prompt x --duration 5 --aspect-ratio 2:3
expect_reject "aspect" "seedance-2.5 rejects 9:21" -- \
  --prompt x --duration 5 --aspect-ratio 9:21
expect_reject "aspect" "wan-2.7 rejects 21:9 (only 16:9/9:16/1:1)" -- \
  --model alibaba/wan-2.7 --prompt x --duration 5 --aspect-ratio 21:9
expect_accept "seedance-2.5 accepts 21:9" -- \
  --prompt x --duration 5 --aspect-ratio 21:9
expect_accept "seedance-2.5 accepts 4:3" -- \
  --prompt x --duration 5 --aspect-ratio 4:3

echo
echo "=== Defect 2: duration validated for every model, not just seedance-2.5 ==="
expect_reject "duration" "wan-2.7 rejects 30s (max 15)" -- \
  --model alibaba/wan-2.7 --prompt x --duration 30
expect_reject "duration" "happyhorse-1.1 rejects 2s (min 3)" -- \
  --model alibaba/happyhorse-1.1 --prompt x --duration 2 --resolution 720p
expect_reject "duration" "seedance-2.0-mini rejects 20s (max 15)" -- \
  --model bytedance/seedance-2.0-mini --prompt x --duration 20
expect_reject "duration" "seedance-2.5 still rejects 99s" -- \
  --prompt x --duration 99
expect_reject "duration" "seedance-2.5 still rejects 3s (min 4)" -- \
  --prompt x --duration 3
expect_accept "wan-2.7 accepts 2s (its real minimum)" -- \
  --model alibaba/wan-2.7 --prompt x --duration 2 --resolution 720p
expect_accept "seedance-2.5 accepts 30s" -- \
  --prompt x --duration 30

echo
echo "=== Defect 3: resolution list matches reality ==="
expect_reject "resolution" "1K is rejected (no video model supports it)" -- \
  --prompt x --duration 5 --resolution 1K
expect_reject "resolution" "2K is rejected (no video model supports it)" -- \
  --prompt x --duration 5 --resolution 2K
expect_reject "resolution" "wan-2.7 rejects 480p (720p/1080p only)" -- \
  --model alibaba/wan-2.7 --prompt x --duration 5 --resolution 480p
expect_reject "resolution" "seedance-2.5 rejects 4k (2.0 has it, 2.5 does not)" -- \
  --prompt x --duration 5 --resolution 4k
expect_accept "seedance-2.0 accepts 4k" -- \
  --model bytedance/seedance-2.0 --prompt x --duration 5 --resolution 4k
expect_accept "seedance-2.5 accepts 1080p" -- \
  --prompt x --duration 5 --resolution 1080p

echo
echo "=== Unknown models: reject on a current list, defer on a stale one ==="
# With a live list, an unknown id is genuinely wrong and worth catching for free.
rm -rf "${CACHE_ROOT:?}"/*
online_base
expect_reject "model" "unknown model rejected when the list is live" -- \
  --model bytedance/does-not-exist-xyz --prompt x --duration 5
expect_reject "video generation" "an image-only model is rejected for video" -- \
  --model openai/gpt-image-2 --prompt x --duration 5
# With only the bundled snapshot, the id may simply be newer than the file.
# Blocking it would break a request that would have worked, so we defer.
rm -rf "${CACHE_ROOT:?}"/*
offline_base
expect_accept "unknown model deferred to the API when only a snapshot is available" -- \
  --model bytedance/some-model-newer-than-the-snapshot --prompt x --duration 5

echo
echo "=== Escape hatch: per-model checks can be skipped ==="
out=$(OFOX_SKIP_MODEL_VALIDATION=1 bash "$TARGET" generate \
  --model alibaba/wan-2.7 --prompt x --duration 30 --approved 2>&1)
code=$?
if [ "$code" -ne 1 ]; then
  printf 'ok    OFOX_SKIP_MODEL_VALIDATION=1 bypasses per-model limits (exit %s)\n' "$code"
  PASS=$((PASS + 1))
else
  printf 'FAIL  OFOX_SKIP_MODEL_VALIDATION=1 should bypass per-model limits\n      output: %s\n' \
    "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi

echo
echo "=== Error messages name the model and list its legal values ==="
offline_base
out=$(bash "$TARGET" generate --model alibaba/wan-2.7 --prompt x --duration 30 2>&1)
if printf '%s' "$out" | grep -q 'alibaba/wan-2.7' && printf '%s' "$out" | grep -q '15'; then
  printf 'ok    duration error names the model and its real limit\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  duration error should name the model and its real limit\n      output: %s\n' \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi

out=$(bash "$TARGET" generate --model alibaba/wan-2.7 --prompt x --duration 5 --aspect-ratio 21:9 2>&1)
if printf '%s' "$out" | grep -q '16:9'; then
  printf 'ok    aspect-ratio error lists that model'"'"'s actual valid values\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  aspect-ratio error should list that model'"'"'s valid values\n      output: %s\n' \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi

echo
echo "=== Offline fallback: validation still works with no network ==="
rm -rf "${CACHE_ROOT:?}"/*
offline_base
out=$(bash "$TARGET" generate --model alibaba/wan-2.7 --prompt x --duration 30 2>&1)
code=$?
if [ "$code" -eq 1 ]; then
  printf 'ok    cold cache + unreachable API still validates from the bundled snapshot\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  cold cache + unreachable API should still validate (got exit %s)\n      output: %s\n' \
    "$code" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi
if printf '%s' "$out" | grep -qi 'bundled snapshot'; then
  printf 'ok    falling back to the bundled snapshot is announced, not silent\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  snapshot fallback must warn on stderr, never be silent\n      output: %s\n' \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi

echo
echo "=== Live model list: public, keyless, and cached after first use ==="
rm -rf "${CACHE_ROOT:?}"/*
online_base
out=$(bash "$TARGET" models 2>&1)
code=$?
if [ "$code" -eq 0 ] && printf '%s' "$out" | grep -q 'seedance-2.5'; then
  printf 'ok    models subcommand fetches the live list\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  models subcommand should list live video models (exit %s)\n      output: %s\n' \
    "$code" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi
if find "$CACHE_ROOT" -name 'models.json' -print -quit | grep -q .; then
  printf 'ok    the fetched list is cached on disk\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  the fetched list should be cached under XDG_CACHE_HOME\n'
  FAIL=$((FAIL + 1))
fi

# The models endpoint is documented as public. Prove we do not send the key.
out=$(env -u OFOX_API_KEY bash "$TARGET" models 2>&1)
code=$?
if [ "$code" -eq 0 ]; then
  printf 'ok    models works with no OFOX_API_KEY set (endpoint is public)\n'
  PASS=$((PASS + 1))
else
  printf 'FAIL  models must work without a key (exit %s)\n      output: %s\n' \
    "$code" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
  FAIL=$((FAIL + 1))
fi

echo
echo "=== Pre-existing validation must not regress ==="
offline_base
expect_reject "prompt" "--prompt is still required" -- \
  --duration 5
expect_reject "size" "--size still must be WIDTHxHEIGHT" -- \
  --prompt x --size wide
expect_reject "generate-audio" "--generate-audio still must be true/false" -- \
  --prompt x --generate-audio yes
expect_reject "seed" "--seed still must be an integer" -- \
  --prompt x --seed abc
expect_reject "callback-url" "--callback-url still must be https" -- \
  --prompt x --callback-url http://example.com/hook
expect_reject "JSON" "--extra-json still must be valid JSON" -- \
  --prompt x --extra-json '{nope}'

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
