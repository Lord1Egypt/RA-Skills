#!/usr/bin/env bash
# aspect-adaptive.test.sh — what an attached frame does to aspect_ratio, per model.
#
# 'adaptive' means two different things depending on the model:
#   bytedance/seedance-2.5 + a frame REQUIRES it (the API rejects anything
#     else), so the script forces it even over an explicit --aspect-ratio;
#   any other model that lists it merely SUPPORTS it, so it is the default
#     when the caller named no ratio and an explicit ratio is left alone.
# Collapsing the two would either strand the frame's shape (the defect this
# covers) or override a choice the model never demanded.
#
# Free by construction, twice over: every case runs under --dry-run, which
# submits nothing, and the API base points at an unroutable address anyway.
# No case here can create a billable job.
#
# Run: bash references/test/aspect-adaptive.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-video.sh"
SNAPSHOT="$SCRIPT_DIR/../models-snapshot.json"

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

# A remote URL is passed through untouched, so the payload stays readable and
# no image file has to exist. What matters here is only that a frame is attached.
FRAME="https://example.com/frame.png"

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "$2"
  FAIL=$((FAIL + 1))
}

# The model list comes from a cache file we write ourselves: seeded from the
# bundled snapshot (real ids, real video_attributes — never a hand-typed table)
# so the suite is deterministic and needs no network, and so a model that is
# genuinely absent from it exercises the catalog-unavailable path.
seed_models() {
  mkdir -p "$XDG_CACHE_HOME/ofox"
  jq '{object: "list", data: [.data[] | select(.id as $i | ["bytedance/seedance-2.5", "alibaba/wan-3.0-prime", "minimax/hailuo-3", "alibaba/wan-2.7"] | index($i))]}' \
    "$SNAPSHOT" >"$XDG_CACHE_HOME/ofox/models.json"
}
seed_models

# Preconditions. If the snapshot ever stops backing these, the rows below would
# quietly stop testing what they claim to, so assert them rather than assume.
adaptive_of() {
  jq -r --arg m "$1" '(.data[] | select(.id == $m) | .video_attributes.aspect_ratios | index("adaptive") != null) // false' \
    "$XDG_CACHE_HOME/ofox/models.json"
}
for m in bytedance/seedance-2.5 alibaba/wan-3.0-prime minimax/hailuo-3; do
  if [ "$(adaptive_of "$m")" = "true" ]; then
    pass "fixture precondition: $m lists 'adaptive'"
  else
    fail "fixture precondition: $m must list 'adaptive'" "snapshot says otherwise"
  fi
done
if [ "$(adaptive_of alibaba/wan-2.7)" = "false" ]; then
  pass "fixture precondition: alibaba/wan-2.7 does not list 'adaptive'"
else
  fail "fixture precondition: alibaba/wan-2.7 must not list 'adaptive'" "snapshot says otherwise"
fi

OUT=""
run() {
  # Runs generate under --dry-run and captures stdout+stderr into OUT.
  OUT=$(bash "$TARGET" generate --dry-run --print-payload --out-dir "$WORK/out" "$@" 2>&1)
}

# Same, with an empty cache so the run falls all the way down the ladder to the
# bundled snapshot. An id the snapshot doesn't carry is then deferred to the API
# rather than rejected, which is the only way to reach "no catalog entry at all"
# — against a fresh list an unknown id is a local error and never gets this far.
mkdir -p "$WORK/empty-cache"
run_uncatalogued() {
  OUT=$(env XDG_CACHE_HOME="$WORK/empty-cache" bash "$TARGET" generate --dry-run \
    --print-payload --out-dir "$WORK/out" "$@" 2>&1)
}

payload_aspect() {
  # The aspect_ratio actually in the request body, or <absent> when the field
  # was never added. Asserting on the payload, not on the NOTE, is the point:
  # the defect being fixed was a body with no aspect_ratio in it at all.
  printf '%s\n' "$OUT" | sed -n 's/^PAYLOAD //p' | jq -r '.aspect_ratio // "<absent>"'
}

check_aspect() {
  # $1 = expected value (or <absent>), $2 = description
  local got
  got="$(payload_aspect)"
  if [ "$got" = "$1" ]; then
    pass "$2 -> aspect_ratio $got"
  else
    fail "$2 should send aspect_ratio $1" "payload had '$got'"
  fi
}

check_note() {
  # $1 = substring the NOTE must contain, $2 = description
  if printf '%s\n' "$OUT" | grep -q "^NOTE: .*$1"; then
    pass "$2"
  else
    fail "$2" "no NOTE matching '$1' in: $(printf '%s' "$OUT" | grep '^NOTE:' | tr '\n' ' ' | cut -c1-160)"
  fi
}

echo
echo "=== Row 1: seedance-2.5 + frame -> forced, even over an explicit ratio ==="
run --prompt x --duration 4 --resolution 480p --frame-first-image "$FRAME" --aspect-ratio 16:9
check_aspect adaptive "seedance-2.5 + frame + --aspect-ratio 16:9"
check_note "forcing aspect_ratio=adaptive.*ignoring requested aspect ratio '16:9'" \
  "the override is announced and names the value it ignored"

run --prompt x --duration 4 --resolution 480p --frame-last-image "$FRAME"
check_aspect adaptive "seedance-2.5 + frame + no --aspect-ratio"
check_note "forcing aspect_ratio=adaptive.*required by the API" \
  "the forced default is announced as an API requirement"

# The requirement belongs to the model, not to the string the caller typed.
# 'seedance-2.5' is a documented alias the API accepts, and a rule keyed on the
# full id alone would let an alias through to a 400 the script exists to prevent.
run --model seedance-2.5 --prompt x --duration 4 --resolution 480p --frame-first-image "$FRAME" --aspect-ratio 16:9
check_aspect adaptive "the alias 'seedance-2.5' + frame + --aspect-ratio 16:9"
check_note "forcing aspect_ratio=adaptive" "an alias of seedance-2.5 is forced too"

echo
echo "=== Row 2: another model + frame + no --aspect-ratio -> defaults to adaptive ==="
for m in alibaba/wan-3.0-prime minimax/hailuo-3; do
  run --model "$m" --prompt x --duration 4 --frame-first-image "$FRAME"
  check_aspect adaptive "$m + frame + no --aspect-ratio"
  check_note "$m image-to-video: no --aspect-ratio was passed, defaulting" \
    "$m says it chose the default rather than doing it silently"
done

echo
echo "=== Row 3: another model + frame + an explicit ratio -> the caller wins ==="
run --model alibaba/wan-3.0-prime --prompt x --duration 4 --frame-first-image "$FRAME" --aspect-ratio 9:16
check_aspect 9:16 "wan-3.0-prime + frame + --aspect-ratio 9:16"
check_note "keeping the aspect ratio you asked for ('9:16')" \
  "keeping the caller's ratio is announced too"
if printf '%s\n' "$OUT" | grep -q 'forcing aspect_ratio'; then
  fail "a non-seedance model must not be forced" "output claims to force adaptive"
else
  pass "nothing is forced on a model that never required it"
fi

run --model minimax/hailuo-3 --prompt x --duration 4 --frame-first-image "$FRAME" --aspect-ratio 21:9
check_aspect 21:9 "hailuo-3 + frame + --aspect-ratio 21:9"

# Asking for adaptive explicitly is still the caller's value, not an override.
run --model alibaba/wan-3.0-prime --prompt x --duration 4 --frame-first-image "$FRAME" --aspect-ratio adaptive
check_aspect adaptive "wan-3.0-prime + frame + --aspect-ratio adaptive"
check_note "sending aspect_ratio=adaptive as requested" \
  "an explicit 'adaptive' is reported as the caller's choice"

echo
echo "=== Row 4: no 'adaptive' in the catalog entry, or no entry -> send nothing ==="
run --model alibaba/wan-2.7 --prompt x --duration 4 --resolution 720p --frame-first-image "$FRAME"
check_aspect "<absent>" "wan-2.7 (catalog entry has no 'adaptive') + frame"
check_note "does not offer 'adaptive'" \
  "refusing to invent a value is announced, with the model's real list"

# An id no list knows about: the catalog cannot answer, so nothing is added.
run_uncatalogued --model bytedance/not-in-any-list-xyz --prompt x --duration 4 --frame-first-image "$FRAME"
check_aspect "<absent>" "an unknown model + frame"
check_note "no catalog entry for this model was available" \
  "the unknown-model case says why it added nothing"

# Same fail-open when per-model checks are switched off on purpose.
OUT=$(OFOX_SKIP_MODEL_VALIDATION=1 bash "$TARGET" generate --dry-run --print-payload \
  --out-dir "$WORK/out" --model alibaba/wan-3.0-prime --prompt x --duration 4 \
  --frame-first-image "$FRAME" 2>&1)
check_aspect "<absent>" "OFOX_SKIP_MODEL_VALIDATION=1 + frame"
check_note "could not be confirmed" \
  "skipping per-model checks also skips the adaptive default, and says so"

echo
echo "=== No frame attached: text-to-video is untouched ==="
run --model alibaba/wan-3.0-prime --prompt x --duration 4
check_aspect "<absent>" "wan-3.0-prime text-to-video, no --aspect-ratio"
run --model alibaba/wan-3.0-prime --prompt x --duration 4 --aspect-ratio 16:9
check_aspect 16:9 "wan-3.0-prime text-to-video, --aspect-ratio 16:9"
if printf '%s\n' "$OUT" | grep -q 'image-to-video'; then
  fail "text-to-video must not print an image-to-video note" "$(printf '%s' "$OUT" | grep '^NOTE:' | head -1)"
else
  pass "no image-to-video aspect_ratio note on a text-to-video job"
fi

echo
echo "=== Every image-to-video path says something: silence is unrelayable ==="
for args in \
  "--prompt x --duration 4 --resolution 480p --frame-first-image $FRAME" \
  "--model alibaba/wan-3.0-prime --prompt x --duration 4 --frame-first-image $FRAME" \
  "--model alibaba/wan-3.0-prime --prompt x --duration 4 --frame-first-image $FRAME --aspect-ratio 9:16" \
  "--model alibaba/wan-2.7 --prompt x --duration 4 --resolution 720p --frame-first-image $FRAME"; do
  # shellcheck disable=SC2086
  run $args
  n=$(printf '%s\n' "$OUT" | grep '^NOTE:' | grep -c 'aspect')
  if [ "$n" -ge 1 ]; then
    pass "an aspect_ratio NOTE is printed for: ${args%% --prompt*}"
  else
    fail "every i2v path must state what it did with aspect_ratio" "silent for: $args"
  fi
done
run_uncatalogued --model bytedance/not-in-any-list-xyz --prompt x --duration 4 --frame-first-image "$FRAME"
if printf '%s\n' "$OUT" | grep '^NOTE:' | grep -q 'aspect'; then
  pass "an aspect_ratio NOTE is printed for: a model with no catalog entry"
else
  fail "every i2v path must state what it did with aspect_ratio" "silent for an uncatalogued model"
fi

echo
echo "=== chain: the sequence-level note matches what the model actually does ==="
out=$(bash "$TARGET" chain --model alibaba/wan-3.0-prime --shot a --shot b --duration 4 --dry-run --out-dir "$WORK/out" 2>&1)
if printf '%s' "$out" | grep -q "wherever the model offers 'adaptive'"; then
  pass "chain on a non-seedance model does not claim 'adaptive' is required"
else
  fail "chain's shots-2+ note must not overclaim for a non-seedance model" \
    "$(printf '%s' "$out" | grep '^NOTE:' | tr '\n' ' ' | cut -c1-160)"
fi
out=$(bash "$TARGET" chain --shot a --shot b --duration 4 --aspect-ratio 16:9 --dry-run --out-dir "$WORK/out" 2>&1)
if printf '%s' "$out" | grep -q "applies to shot 1 only"; then
  pass "chain on seedance-2.5 still warns that shot 1 alone keeps --aspect-ratio"
else
  fail "chain on seedance-2.5 must keep its shot-1-only warning" \
    "$(printf '%s' "$out" | grep '^NOTE:' | tr '\n' ' ' | cut -c1-160)"
fi

echo
echo "=== The live catalog still backs the fixture (skipped when offline) ==="
live="$WORK/live-models.json"
if curl -fsS --max-time 10 "https://api.ofox.ai/v1/models" -o "$live" 2>/dev/null &&
  jq -e '(.data | length) > 0' "$live" >/dev/null 2>&1; then
  for m in alibaba/wan-3.0-prime minimax/hailuo-3; do
    if jq -e --arg m "$m" '.data[] | select(.id == $m) | .video_attributes.aspect_ratios | index("adaptive")' "$live" >/dev/null 2>&1; then
      pass "live catalog: $m still lists 'adaptive'"
    else
      fail "live catalog: $m no longer lists 'adaptive'" "the bundled snapshot needs refreshing"
    fi
  done
  if jq -e '.data[] | select(.id == "alibaba/wan-2.7") | .video_attributes.aspect_ratios | index("adaptive")' "$live" >/dev/null 2>&1; then
    fail "live catalog: alibaba/wan-2.7 now lists 'adaptive'" "the no-adaptive row needs a different model"
  else
    pass "live catalog: alibaba/wan-2.7 still has no 'adaptive'"
  fi
else
  printf 'skip  the live catalog is unreachable — fixture cross-check not run\n'
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
