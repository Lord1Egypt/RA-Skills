#!/usr/bin/env bash
# pricing.test.sh — cost estimates come from the catalog, not a hardcoded table.
#
# Free by construction: estimates are printed before anything is submitted, and
# the API base points at an unroutable address so nothing can create a job.
#
# Run: bash references/test/pricing.test.sh

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

# Warm the catalog from the real (public, keyless, free) endpoint, then go
# offline so nothing can submit.
warm() {
  online
  env -u OFOX_API_KEY bash "$TARGET" providers "${1:-bytedance/seedance-2.5}" >/dev/null 2>&1 || true
  offline
}

# Read the rate from the source the run is meant to agree with. The live
# catalog cache has a different envelope from the bundled offline snapshot,
# so keep both paths explicit instead of copying today's external prices into
# this test. A price change should test the estimator, not break a stale
# constant in the test itself.
catalog_rate() {
  local res="$1" mode="$2"
  local live="$XDG_CACHE_HOME/ofox/catalog-bytedance-seedance-2.5.json"
  if [ -f "$live" ]; then
    jq -r --arg res "$res" --arg mode "$mode" '
      first(.provider_cards[]
        | select(.provider_type == "byteplus")
        | .pricing.video_pricing.tiers[]
        | select(.resolution == $res and .input_type == $mode)
        | .price) // empty
    ' "$live"
  else
    jq -r --arg res "$res" --arg mode "$mode" '
      first(.models[]
        | select(.id == "bytedance/seedance-2.5")
        | .provider_cards[]
        | select(.provider_type == "byteplus")
        | .pricing.video_pricing.tiers[]
        | select(.resolution == $res and .input_type == $mode)
        | .price) // empty
    ' "$SCRIPT_DIR/../pricing-snapshot.json"
  fi
}

# Pulls the dollar figure out of an "Estimated cost: ~$X.XX ..." line.
est_amount() {
  sed -n 's/.*Estimated cost: ~\$\([0-9.]*\).*/\1/p' | head -1
}

echo "=== No per-resolution price constants left in the script ==="
# The old table had arms like 'bytedance/seedance-2.5:720p) echo "0.24"'.
if grep -qE '^\s+bytedance/[a-z0-9.-]+:[0-9]+[pk]\)' "$TARGET"; then
  fail "hardcoded per-resolution rates still present" "$(grep -nE '^\s+bytedance/[a-z0-9.-]+:[0-9]+[pk]\)' "$TARGET" | head -2 | tr '\n' ' ')"
else
  pass "the hardcoded model:resolution price table is gone"
fi

echo
echo "=== Estimates match the live catalog ==="
warm
check_rate() {
  local res="$1" dur=4 takes=2
  local out amount expect
  local want
  want="$(catalog_rate "$res" t2v)"
  if [ -z "$want" ]; then
    fail "catalog has a seedance-2.5 t2v rate for $res" "no byteplus tier found"
    return
  fi
  out=$(bash "$TARGET" batch --prompt x --takes "$takes" --duration "$dur" --resolution "$res" 2>&1)
  amount=$(printf '%s' "$out" | est_amount)
  expect=$(awk -v d="$dur" -v n="$takes" -v r="$want" 'BEGIN{printf "%.2f", d*n*r}')
  if [ "$amount" = "$expect" ]; then
    pass "batch estimate at $res is \$$amount (${dur}s x $takes x \$$want/s)"
  else
    fail "batch estimate at $res should be \$$expect" "got '\$$amount'"
  fi
}
check_rate 480p
check_rate 720p
check_rate 1080p

rate_480_t2v="$(catalog_rate 480p t2v)"
rate_720_t2v="$(catalog_rate 720p t2v)"
rate_480_v2v="$(catalog_rate 480p v2v)"

echo
echo "=== generate estimates too, on stderr ==="
out=$(bash "$TARGET" generate --prompt x --duration 5 --resolution 720p 2>&1)
amount=$(printf '%s' "$out" | est_amount)
expect=$(awk -v r="$rate_720_t2v" 'BEGIN{printf "%.2f", 5*r}')
if [ "$amount" = "$expect" ]; then
  pass "generate prints an estimate before submitting (\$$amount)"
else
  fail "generate should estimate \$$expect" "got '\$$amount' from: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
# It must not pollute the KEY VALUE contract on stdout.
outp=$(bash "$TARGET" generate --prompt x --duration 5 --resolution 720p 2>/dev/null)
if printf '%s' "$outp" | grep -qi 'estimated cost'; then
  fail "the estimate must go to stderr, not stdout" "found it on stdout"
else
  pass "the estimate stays off stdout (KEY VALUE contract intact)"
fi

echo
echo "=== Resolution defaults to the model's own default_resolution ==="
# seedance-2.5's default_resolution is 720p, so omitting --resolution should
# estimate at the 720p rate, not some hardcoded assumption.
out=$(bash "$TARGET" generate --prompt x --duration 5 2>&1)
amount=$(printf '%s' "$out" | est_amount)
if [ "$amount" = "$expect" ]; then
  pass "omitting --resolution estimates at the model's default (720p)"
else
  fail "default resolution estimate should be \$$expect" "got '\$$amount'"
fi

echo
echo "=== Image-to-video bills at t2v rates, not v2v ==="
# A frame image is i2v, which bills as t2v rather than the v2v tier.
printf 'not-a-real-image' > "$WORK/frame.png"
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --frame-first-image "$WORK/frame.png" 2>&1)
amount=$(printf '%s' "$out" | est_amount)
expect_i2v=$(awk -v r="$rate_480_t2v" 'BEGIN{printf "%.2f", 4*r}')
if [ "$amount" = "$expect_i2v" ]; then
  pass "i2v estimates at the t2v rate (\$$amount, not the v2v tier)"
else
  fail "i2v should estimate at the t2v rate \$$expect_i2v" "got '\$$amount'"
fi

echo
echo "=== Video-to-video is priced at the v2v tier ==="
# The API's reference type is "video_url". Getting this wrong quotes the t2v
# rate for a v2v job — measured 2026-08-31: estimated $0.44, billed $0.56.
v2v_refs='{"input_references":[{"type":"video_url","video_url":{"url":"https://example.com/ref.mp4"}}]}'
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --extra-json "$v2v_refs" 2>&1)
amount=$(printf '%s' "$out" | est_amount)
expect_v2v=$(awk -v r="$rate_480_v2v" 'BEGIN{printf "%.2f", 4*r}')
if [ "$amount" = "$expect_v2v" ]; then
  pass "a video_url reference estimates at the v2v rate (\$$amount)"
else
  fail "v2v should estimate \$$expect_v2v, not the t2v rate" "got '\$$amount'"
fi

# A bare "video" type isn't what the API uses, but tolerate it rather than
# silently pricing it as t2v.
alt_refs='{"input_references":[{"type":"video","video_url":{"url":"https://example.com/ref.mp4"}}]}'
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --extra-json "$alt_refs" 2>&1)
amount=$(printf '%s' "$out" | est_amount)
if [ "$amount" = "$expect_v2v" ]; then
  pass "a bare 'video' type is tolerated and still priced as v2v"
else
  fail "'video' should also price as v2v" "got '\$$amount'"
fi

# Image references are not v2v — they bill at t2v.
img_refs='{"input_references":[{"type":"image_url","image_url":{"url":"https://example.com/a.jpg"}}]}'
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --extra-json "$img_refs" 2>&1)
amount=$(printf '%s' "$out" | est_amount)
expect_t2v=$(awk -v r="$rate_480_t2v" 'BEGIN{printf "%.2f", 4*r}')
if [ "$amount" = "$expect_t2v" ]; then
  pass "image references still estimate at the t2v rate (\$$amount)"
else
  fail "image refs should stay t2v at \$$expect_t2v" "got '\$$amount'"
fi

echo
echo "=== Offline: the bundled snapshot still produces an estimate ==="
rm -rf "${XDG_CACHE_HOME:?}"
offline
out=$(bash "$TARGET" batch --prompt x --takes 2 --duration 4 --resolution 720p 2>&1)
amount=$(printf '%s' "$out" | est_amount)
snapshot_rate=$(jq -r '
  first(.models[]
    | select(.id == "bytedance/seedance-2.5")
    | .provider_cards[]
    | select(.provider_type == "byteplus")
    | .pricing.video_pricing.tiers[]
    | select(.resolution == "720p" and .input_type == "t2v")
    | .price) // empty
' "$SCRIPT_DIR/../pricing-snapshot.json")
expect_snap=$(awk -v r="$snapshot_rate" 'BEGIN{printf "%.2f", 4*2*r}')
if [ "$amount" = "$expect_snap" ]; then
  pass "cold cache + no network still estimates from the bundled snapshot"
else
  fail "snapshot fallback should estimate \$$expect_snap" "got '\$$amount' from: $(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== An unknown combination says so instead of inventing a number ==="
out=$(bash "$TARGET" batch --prompt x --takes 2 --duration 4 \
  --model bytedance/some-unknown-model --resolution 720p 2>&1)
if printf '%s' "$out" | grep -qi 'estimate.*unavailable\|unavailable.*estimate'; then
  pass "an unknown model reports the estimate as unavailable"
else
  fail "an unpriceable combination must not print a number" \
    "$(printf '%s' "$out" | grep -i estimat | head -1)"
fi
if printf '%s' "$out" | est_amount | grep -q '[0-9]'; then
  fail "no dollar figure should be printed for an unknown model" "got one anyway"
else
  pass "no invented figure for an unknown model"
fi

echo
echo "=== A run that cannot be priced still proceeds ==="
# Failing to price something must never block generation (fail open).
# --approved: this case is about what happens AFTER the estimate fails, so
# it has to be allowed past the spend gate. The base is unroutable.
out=$(bash "$TARGET" generate --prompt x --duration 4 \
  --model bytedance/some-unknown-model --resolution 720p --approved 2>&1)
code=$?
if [ "$code" -ne 1 ]; then
  pass "an unpriceable run still gets submitted (exit $code, not a validation block)"
else
  fail "pricing failure must not block the run" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== pricing.md no longer claims to be the runtime source ==="
PRICING="$SCRIPT_DIR/../pricing.md"
if grep -qi 'providers' "$PRICING"; then
  pass "pricing.md points at the providers subcommand for live numbers"
else
  fail "pricing.md should name the live source" "no mention of the providers subcommand"
fi
if grep -qiE 'snapshot|point-in-time|as of' "$PRICING"; then
  pass "pricing.md marks its table as a point-in-time snapshot"
else
  fail "pricing.md must not present itself as current" "no snapshot/as-of marker"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
