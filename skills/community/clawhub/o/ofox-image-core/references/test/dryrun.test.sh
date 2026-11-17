#!/usr/bin/env bash
# dryrun.test.sh — pricing an image before spending, and the model chain that
# decides which model gets priced.
#
# Two things are being defended here:
#
#   1. --dry-run really does not send the request. Not "prints a dry-run
#      banner" — actually returns before the POST. The cases below point the
#      API base at an unroutable address, so a leaked request would fail on
#      connect (exit 5) instead of quietly passing.
#   2. The model is resolved to ONE concrete id before the estimate is
#      printed. A quote that names a model the run then swaps out is a user
#      approving a price they were never shown.
#
# Free by construction: no case reaches /v1/images/generations, and the model
# list it does read is public and keyless.
#
# Run: bash references/test/dryrun.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-image.sh"
ANCHORS="$SCRIPT_DIR/../token-anchors.json"
# Captured before the script is sourced as a library further down: sourcing it
# redefines SCRIPT_DIR to wherever the copy lives.
SKILL_MD="$SCRIPT_DIR/../../SKILL.md"

PASS=0
FAIL=0

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export XDG_CACHE_HOME="$WORK/cache"
OUT_DIR="$WORK/out"

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

# Warm the model cache from the real, public list, then make the API base
# unroutable. Validation and pricing still see live data; anything that tries
# to generate dies on connect.
warm() {
  online
  env -u OFOX_API_KEY bash "$TARGET" models >/dev/null 2>&1 || true
  offline
}
warm

echo "=== --dry-run quotes and stops there ==="
# The flags on this call carry two constraints that were not here before, and
# both are the point of a later assertion rather than incidental:
#   --quality low, not standard, because --quality is now checked against the
#     model the request resolves to and MODEL_CHAIN's head (openai/gpt-image-2)
#     does not accept 'standard' — the exact combination that used to pass a
#     dry run and then fail at submission with HTTP 400. That rejection is
#     asserted on its own further down; this call is about the happy path.
#   --size 1024x1024 explicitly, because the estimate is now pair-aware: an
#     omitted size is left to the API, so it cannot be matched to a measured
#     point and takes the upper-bound path by design. Naming the pair
#     gpt-image-2's anchor was measured at is what keeps the 0.0059
#     assertion below testing "priced from its own anchor" rather than
#     "priced from the dearest thing on file".
out=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --prompt "a red apple on a white table" --quality low --size 1024x1024 \
  --out-dir "$OUT_DIR" 2>&1)
code=$?
if [ "$code" -eq 0 ]; then
  pass "--dry-run exits 0 with no OFOX_API_KEY set (pricing precedes signing up)"
else
  fail "--dry-run should exit 0 without a key" "got $code: $(printf '%s' "$out" | tail -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q 'STATUS dry_run'; then
  pass "--dry-run prints STATUS dry_run"
else
  fail "--dry-run must print STATUS dry_run" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
n_est=$(printf '%s\n' "$out" | grep -c 'Estimated cost:')
if [ "$n_est" -eq 1 ]; then
  pass "exactly one 'Estimated cost:' line — never silent, never doubled"
else
  fail "expected exactly one 'Estimated cost:' line" "got $n_est"
fi
# The API base is unroutable, so any leaked request would surface as the
# ambiguous-network exit (5) or a connect error in the output.
if printf '%s' "$out" | grep -qi 'could not reach the Ofox API'; then
  fail "--dry-run reached the generations endpoint" "it must return before the POST"
else
  pass "--dry-run makes no generation request (unroutable base, still exit 0)"
fi
if [ -d "$OUT_DIR" ]; then
  pass "--out-dir is still created and checked under a dry run (free to catch)"
else
  fail "--out-dir should be resolved under a dry run" "$OUT_DIR was not created"
fi

echo
echo "=== The estimate names a real model, resolved before it is printed ==="
model_line=$(printf '%s\n' "$out" | sed -n 's/^MODEL //p')
if [ -n "$model_line" ] && [ "$model_line" != "auto" ]; then
  pass "MODEL is a concrete id, not 'auto' ($model_line)"
else
  fail "MODEL must be the resolved id" "got '$model_line'"
fi
if printf '%s' "$out" | grep -q "openai/gpt-image-2"; then
  pass "the default resolves to the chain's cheapest-per-image available model"
else
  fail "the preferred model should be chosen when it is available" "got '$model_line'"
fi
explicit=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --model google/gemini-3.1-flash-image --prompt x --quality standard \
  --out-dir "$OUT_DIR" 2>&1)
if printf '%s\n' "$explicit" | grep -q '^MODEL google/gemini-3.1-flash-image$'; then
  pass "--model still pins an explicit id (the chain is a priority, not a lock)"
else
  fail "an explicit --model must win over the chain" "$(printf '%s' "$explicit" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== A rough estimate says it is rough; a missing one says why ==="
if printf '%s' "$explicit" | grep -q 'Estimated cost: ROUGH'; then
  pass "a model with a measured token anchor gets a figure labelled ROUGH"
else
  fail "gemini has a measured anchor and should be priced" \
    "$(printf '%s' "$explicit" | grep -i 'estimated cost' | head -1)"
fi
# 1120 output tokens x $0.00006 = 0.0672, the invoice-anchored figure.
if printf '%s' "$explicit" | grep -q '0\.0672'; then
  pass "the rough figure matches the invoice-anchored calculation (~\$0.0672)"
else
  fail "the gemini estimate should be ~0.0672" \
    "$(printf '%s' "$explicit" | grep -i 'estimated cost' | head -1)"
fi
# The chain's preferred model changed from mai-image-2.5-flash to
# gpt-image-2 on 2026-09-04 (see SKILL.md's "The 2026-09-04 reversal" and
# references/pricing.md's decision record for the history). This assertion
# follows that change: the DEFAULT resolve must now be priced from
# gpt-image-2's own measured anchor, not from whichever model used to be
# first. Earlier versions of this assertion checked for mai-flash's 0.0266
# figure for exactly the same reason they now check gpt-image-2's — keep it
# pointed at whichever model MODEL_CHAIN currently prefers.
# 196 output tokens x $0.00003 = 0.0059 (the ROUGH, output-tokens-only
# figure print_estimate prints; the full formula that also adds the
# input-token component is what IMAGE_COST reports on a real run, 0.00595).
if printf '%s' "$out" | grep -q '0\.0059'; then
  pass "the chain's preferred model is priced from its own measured anchor (~\$0.0059)"
else
  fail "gpt-image-2 has a measured anchor and should be priced" \
    "$(printf '%s' "$out" | grep -i 'estimated cost' | head -1)"
fi
# The failure this guards: reusing another model's output-token count for
# the default resolve. gpt-image-2's own count is 196; gemini's is 1120 and
# mai-flash's (the previous default) is 1024 — neither borrowed figure
# should show up here.
if printf '%s' "$out" | grep -Eq '1120|1024 output tokens'; then
  fail "gpt-image-2 borrowed another model's token count" \
    "a borrowed number looks exactly like a measured one"
else
  pass "no anchor is borrowed across models"
fi

echo
echo "=== Fallback down the chain is reported, not silent ==="
# Resolution is exercised against synthetic model lists rather than the live
# one: every skip reason has to be reproducible on demand, and none of them
# is something the real catalog can be asked to produce today. Setting
# MODELS_FILE short-circuits load_models, which is idempotent by design.
LIB="$WORK/lib.sh"
sed -e '/^main "\$@"$/d' -e '/^exit \$?$/d' "$TARGET" >"$LIB"
# shellcheck source=/dev/null
. "$LIB"

# shellcheck disable=SC2034  # read by resolve_model from the sourced script
MODELS_FILE="$WORK/synthetic.json"
jq -nc '{data:[
  {id:"fake/gone",
   supported_endpoints:["/v1/images/generations"],
   pricing:{prompt:"0.0000005", output_image:"0.00002"}},
  {id:"fake/deprecated", is_deprecated:true,
   supported_endpoints:["/v1/images/generations"],
   pricing:{prompt:"0.0000005", output_image:"0.00002"}},
  {id:"fake/videoonly",
   supported_endpoints:["/v1/videos"],
   pricing:{prompt:"0.0000005"}},
  {id:"fake/usable",
   supported_endpoints:["/v1/images/generations"],
   pricing:{prompt:"0.0000005", output_image:"0.00006"}},
  {id:"fake/unpriced",
   supported_endpoints:["/v1/images/generations"],
   pricing:{prompt:"0.0000005"}}]}' >"$MODELS_FILE"

check_fallback() { # <chain> <expected model> <expected reason substring> <desc>
  # shellcheck disable=SC2034  # read by resolve_model from the sourced script
  MODEL_CHAIN="$1"
  resolve_model 2>/dev/null
  if [ "$RESOLVED_MODEL" != "$2" ]; then
    fail "$4" "expected '$2', got '$RESOLVED_MODEL'"
    return
  fi
  case "$MODEL_FALLBACK_REASON" in
    *"$3"*) : ;;
    *)
      fail "$4" "reason should mention '$3', got '$MODEL_FALLBACK_REASON'"
      return
      ;;
  esac
  if [ -z "$MODEL_FALLBACK_FROM" ] || [ -z "$MODEL_PRICE_DELTA" ]; then
    fail "$4" "a fallback must report what was skipped and the price difference"
    return
  fi
  pass "$4"
}

check_fallback "no/such-model fake/usable" "fake/usable" "not in the Ofox model list" \
  "a preferred model missing from the list falls through, and says so"
check_fallback "fake/videoonly fake/usable" "fake/usable" "does not serve /v1/images/generations" \
  "a model that does not do image generation falls through, and says so"
check_fallback "fake/deprecated fake/usable" "fake/usable" "deprecated" \
  "a deprecated preferred model falls through, and says so"

# Both rates known: the delta has to be a real multiple, not "unknown". This
# is the number an approval table needs — "we fell back" without "and it costs
# 3x more" is not enough to approve.
case "$MODEL_PRICE_DELTA" in
  3.00x*) pass "the price gap is quantified when both rates are known ($MODEL_PRICE_DELTA)" ;;
  *) fail "expected a 3.00x price delta" "got '$MODEL_PRICE_DELTA'" ;;
esac

# shellcheck disable=SC2034  # read by resolve_model from the sourced script
MODEL_CHAIN="fake/usable no/such-model"
resolve_model 2>/dev/null
if [ "$RESOLVED_MODEL" = "fake/usable" ] && [ -z "$MODEL_FALLBACK_FROM" ]; then
  pass "no fallback is reported when the preferred model is fine"
else
  fail "a healthy preferred model must not look like a fallback" \
    "model='$RESOLVED_MODEL' from='$MODEL_FALLBACK_FROM'"
fi

# When a rate is missing, the message has to name the side that is actually
# missing it. The first version of this blamed the preferred model in every
# case and added "which is part of why it was skipped" — a causal claim
# resolve_model cannot make, since it never looks at pricing when deciding
# what to skip. A wrong reason in an approval table is worse than no reason.
# shellcheck disable=SC2034  # read by resolve_model from the sourced script
MODEL_CHAIN="fake/deprecated fake/unpriced"
resolve_model 2>/dev/null
case "$MODEL_PRICE_DELTA" in
  *"no published output_image rate for 'fake/unpriced'"*)
    pass "an unpriced *chosen* model is named as the unpriced one, not the preferred"
    ;;
  *) fail "the price delta blamed the wrong model" "got '$MODEL_PRICE_DELTA'" ;;
esac
case "$MODEL_PRICE_DELTA" in
  *"part of why it was skipped"*)
    fail "the price delta still claims a missing rate caused the skip" \
      "resolve_model never looks at pricing when deciding what to skip"
    ;;
  *) pass "no invented causal claim about why the model was skipped" ;;
esac

# Nothing was fallen back TO here, so the fallback lines must stay silent —
# but the reason must still reach the caller, because the model about to be
# quoted is one the script already knows is broken.
# shellcheck disable=SC2034  # read by resolve_model from the sourced script
MODEL_CHAIN="fake/deprecated"
resolve_model 2>/dev/null
if [ -z "$MODEL_FALLBACK_FROM" ] && [ -n "$MODEL_CHAIN_EXHAUSTED" ]; then
  pass "an exhausted chain reports MODEL_CHAIN_EXHAUSTED, not a phantom fallback"
else
  fail "an exhausted chain must surface its reason" \
    "from='$MODEL_FALLBACK_FROM' exhausted='$MODEL_CHAIN_EXHAUSTED'"
fi
# shellcheck disable=SC2034  # read by resolve_model from the sourced script
MODEL_CHAIN="fake/usable"
resolve_model 2>/dev/null
if [ -z "$MODEL_CHAIN_EXHAUSTED" ]; then
  pass "a later healthy resolve clears the exhausted flag (no stale warning)"
else
  fail "MODEL_CHAIN_EXHAUSTED leaked into a healthy resolve" "got '$MODEL_CHAIN_EXHAUSTED'"
fi

echo
echo "=== The anchor file is the single source of the estimate ==="
if jq -e '.anchors | length > 0' "$ANCHORS" >/dev/null 2>&1; then
  pass "token-anchors.json is valid JSON with at least one entry"
else
  fail "token-anchors.json must be valid JSON" "jq could not read $ANCHORS"
fi
if [ "$(jq -r '.anchors["google/gemini-3.1-flash-image"].output_tokens' "$ANCHORS")" = "1120" ]; then
  pass "the measured gemini anchor is the 1120 tokens the invoice was based on"
else
  fail "the gemini anchor drifted from the measured call" \
    "references/pricing.md records 1120 output tokens"
fi
unmeasured=$(jq -r '[.anchors | to_entries[] | select(.value.output_tokens == null) | .key] | join(" ")' "$ANCHORS")
case "$unmeasured" in
  *mai-image-2.5-flash*gpt-image-2* | *gpt-image-2*mai-image-2.5-flash*)
    pass "the two chain models still awaiting a real measurement are marked null, not guessed"
    ;;
  "") pass "every model in the anchor file has been measured" ;;
  *) fail "unexpected set of unmeasured anchors" "got '$unmeasured'" ;;
esac

echo
echo "=== The estimate is priced at the pair the request asks for ==="
# The failure being defended against is a real one, and it cost real money:
# on 2026-09-04 a run at --quality high --size 1792x1024 was quoted from
# gpt-image-2's low / 1024x1024 anchor — approved at ~0.6 cents, billed 15.4.
# The two numbers below are the two ends of that 26x, and which one gets
# printed must follow the flags.
#
# This is also the verbatim reproduction from the bug report: --quality high
# with --target-aspect 16:9 and no --size, where the script itself picks
# 1792x1024 to serve the crop. The quote has to follow the size the script
# chose, not the (absent) flag the caller typed.
repro=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --quality high --prompt t --target-aspect 16:9 --out-dir "$OUT_DIR" 2>&1)
est=$(printf '%s\n' "$repro" | grep 'Estimated cost:' | head -1)
if printf '%s' "$est" | grep -q '0\.1519'; then
  pass "high + 1792x1024 is priced from the 5063-token point (~15.2 cents of output tokens)"
else
  fail "the 1792x1024 repro must quote the high/1792x1024 measurement" "got: $est"
fi
if printf '%s' "$est" | grep -q '0\.0059'; then
  fail "the repro still quotes the low/1024x1024 anchor" \
    "this is the 26x under-quote the pair-aware lookup exists to stop"
else
  pass "the cheap low/1024x1024 anchor is not reused for a high 1792x1024 frame"
fi
if printf '%s' "$est" | grep -q 'at --quality high --size 1792x1024'; then
  pass "the quote carries the pair it was measured at, so the pair reaches the approval table"
else
  fail "the estimate line must name the measured pair" "got: $est"
fi
# An exact pair match is not an upper bound and must not be labelled one —
# the label has to mean something for a reader to act on it.
if printf '%s' "$est" | grep -q 'UPPER BOUND'; then
  fail "an exact pair match was labelled an upper bound" "got: $est"
else
  pass "an exact pair match is quoted plainly, not as a ceiling"
fi

# A pair nobody has measured: 'medium' is accepted by gpt-image-2 and has no
# anchor at any size, so this must fall to the dearest known point and say so.
unknown=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --quality medium --size 1536x1024 --prompt t --out-dir "$OUT_DIR" 2>&1)
uest=$(printf '%s\n' "$unknown" | grep 'Estimated cost:' | head -1)
if printf '%s' "$uest" | grep -q 'UPPER BOUND'; then
  pass "an unmeasured pair is labelled UPPER BOUND rather than quoted as an estimate"
else
  fail "an unmeasured pair must be labelled an upper bound" "got: $uest"
fi
if printf '%s' "$uest" | grep -q '0\.1519'; then
  pass "the upper bound is the dearest measured point (5063 tokens), not the cheapest"
else
  fail "the upper bound must take the dearest measurement" "got: $uest"
fi
if printf '%s' "$uest" | grep -q 'at --quality high --size 1792x1024'; then
  pass "the upper bound names the pair it borrowed from, not the pair requested"
else
  fail "an upper bound must name the pair it came from" "got: $uest"
fi
if printf '%s' "$unknown" | grep -q -- "--quality medium --size 1536x1024"; then
  pass "the note also names the request's own unmeasured pair"
else
  fail "the upper-bound note must say which pair was unmeasured" \
    "$(printf '%s' "$unknown" | grep -i 'upper bound' | tail -1)"
fi
# Nothing between two measured points is ever invented: only 196 and 5063
# exist for this model, so no third token count may appear.
if printf '%s' "$uest" | grep -Eq '\b(19[0-9][0-9]|2[0-9]{3}|3[0-9]{3}|4[0-9]{3}) output tokens'; then
  fail "a token count was interpolated between two measured points" "got: $uest"
else
  pass "no count is interpolated between 196 and 5063"
fi

# --size omitted, and --size auto, are the same situation: the API picks, so
# there is no pair to match and the ceiling is the only honest answer.
for variant in "" "auto"; do
  if [ -z "$variant" ]; then
    label="omitted"
    v=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
      --quality low --prompt t --out-dir "$OUT_DIR" 2>&1)
  else
    label="auto"
    v=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
      --quality low --size auto --prompt t --out-dir "$OUT_DIR" 2>&1)
  fi
  vest=$(printf '%s\n' "$v" | grep 'Estimated cost:' | head -1)
  if printf '%s' "$vest" | grep -q 'UPPER BOUND'; then
    pass "--size $label leaves the size to the API, so the quote is an upper bound"
  else
    fail "--size $label cannot be matched to a measured pair" "got: $vest"
  fi
done
qauto=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --quality auto --size 1024x1024 --prompt t --out-dir "$OUT_DIR" 2>&1)
if printf '%s\n' "$qauto" | grep 'Estimated cost:' | grep -q 'UPPER BOUND'; then
  pass "--quality auto is server-resolved too, so it takes the ceiling as well"
else
  fail "--quality auto must not be matched against a named quality" \
    "$(printf '%s\n' "$qauto" | grep 'Estimated cost:' | head -1)"
fi

# A model with exactly one measurement still gets the pair printed, and is
# still never priced from another model's count.
solo=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --model google/gemini-3.1-flash-image --quality low --size 512x512 \
  --prompt t --out-dir "$OUT_DIR" 2>&1)
sest=$(printf '%s\n' "$solo" | grep 'Estimated cost:' | head -1)
if printf '%s' "$sest" | grep -q '0\.0672' &&
  printf '%s' "$sest" | grep -q 'at --quality low --size 512x512'; then
  pass "gemini's single measured point is matched exactly and names its pair"
else
  fail "gemini at its measured pair should quote 0.0672 and say so" "got: $sest"
fi
if printf '%s' "$sest" | grep -Eq '196|5063'; then
  fail "gemini borrowed gpt-image-2's token count" \
    "a borrowed number looks exactly like a measured one"
else
  pass "pair-awareness did not start borrowing counts across models"
fi

# Still exactly one estimate line on every path — the property the whole
# block above would be worthless without, since an agent cannot relay a line
# it was never told to expect.
for probe in "$repro" "$unknown" "$qauto" "$solo"; do
  n=$(printf '%s\n' "$probe" | grep -c 'Estimated cost:')
  if [ "$n" -ne 1 ]; then
    fail "a pricing path printed $n estimate lines" "exactly one is the contract"
  else
    pass "one 'Estimated cost:' line on this path"
  fi
done

# A ceiling built on ONE measured point is not a ceiling anyone has tested,
# and the line has to admit that. mai-image-2.5-flash has a single point
# (low / 1024x1024); asking it for a big high-quality frame produces a
# "bound" of 2.66 cents that a real bill could plainly exceed, since
# gpt-image-2's own two points are 26x apart.
weak=$(env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --model microsoft/mai-image-2.5-flash --quality high --size 1792x1024 \
  --prompt t --out-dir "$OUT_DIR" 2>&1)
if printf '%s\n' "$weak" | grep 'Estimated cost:' | grep -q 'UPPER BOUND'; then
  pass "a single-point model at an unmeasured pair is still labelled a ceiling"
else
  fail "an unmeasured pair must take the bound path on any model" \
    "$(printf '%s\n' "$weak" | grep 'Estimated cost:' | head -1)"
fi
if printf '%s' "$weak" | grep -q 'Weak ceiling'; then
  pass "and is flagged a WEAK ceiling, because one sample cannot bound a model"
else
  fail "a one-point ceiling must say it is untested" \
    "$(printf '%s' "$weak" | grep -i 'upper bound' | tail -1)"
fi
# Scoped to the quoted FIGURE, not the whole output: the weak-ceiling note
# deliberately cites gpt-image-2's 196-to-5063 spread as the reason one
# sample cannot bound a model, and that citation is the point of the note.
# What must never happen is those counts becoming mai-flash's own number.
wline=$(printf '%s\n' "$weak" | grep 'Estimated cost:' | head -1)
if printf '%s' "$wline" | grep -Eq '196|5063'; then
  fail "mai-flash's ceiling borrowed gpt-image-2's counts" \
    "the 26x spread may be cited as a reason, but not quoted as this model's figure"
else
  pass "the weak ceiling stays on mai-flash's own 1024, borrowing nothing"
fi
if printf '%s' "$wline" | grep -q '1024 output tokens'; then
  pass "and it is mai-flash's own measured 1024 that gets priced"
else
  fail "the weak ceiling must price mai-flash's own point" "got: $wline"
fi
# Two measured points is a real range, so the weak-ceiling caveat must NOT
# fire there — a caveat printed unconditionally is a caveat nobody reads.
if printf '%s' "$unknown" | grep -q 'Weak ceiling'; then
  fail "the weak-ceiling caveat fired on a model with two measured points" \
    "it must distinguish one sample from a measured range"
else
  pass "a model with two measured points gets the ceiling without the weak caveat"
fi
echo
echo "=== Every anchor records the pair it was measured at ==="
# The lookup can only be pair-aware if the data is. An anchor row without a
# quality and a size is exactly the shape that produced the 26x under-quote:
# a number with nothing to check it against.
missing=$(jq -r '
  [ .anchors | to_entries[]
    | .key as $k
    | ([.value] + (.value.additional_measurements // []))[]
    | select(.output_tokens != null)
    | select((.quality == null) or (.size == null))
    | $k ] | unique | join(" ")' "$ANCHORS")
if [ -z "$missing" ]; then
  pass "every measured point carries both a quality and a size"
else
  fail "a measured point has no pair recorded" "models: $missing"
fi
if [ "$(jq -r '[.anchors["openai/gpt-image-2"].additional_measurements[] | select(.quality=="high" and .size=="1792x1024") | .output_tokens] | first' "$ANCHORS")" = "5063" ]; then
  pass "the 5063-token high/1792x1024 measurement is still on file (the ceiling depends on it)"
else
  fail "gpt-image-2's high/1792x1024 measurement went missing" \
    "references/pricing.md records 5063 output tokens, IMAGE_COST 0.154035"
fi
echo
echo "=== SKILL.md's chain table matches the chain the script actually uses ==="
# The chain has one definition (MODEL_CHAIN) and one explanation (the table in
# SKILL.md). The explanation is the part that can quietly stop being true, and
# a doc asserting a priority order the code no longer has is worse than no
# doc. Compare the ids and their order, not the prose around them.
doc_chain=$(sed -n 's/^| [0-9] | `\([^`]*\)`.*/\1/p' "$SKILL_MD" | tr '\n' ' ')
code_chain=$(sed -n 's/^MODEL_CHAIN="\(.*\)"$/\1/p' "$TARGET")
if [ "$(echo "$doc_chain" | xargs)" = "$(echo "$code_chain" | xargs)" ]; then
  pass "the documented chain is the real chain, in the same order"
else
  fail "SKILL.md's chain table has drifted from MODEL_CHAIN" \
    "doc: '$doc_chain' / code: '$code_chain'"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
