#!/usr/bin/env bash
# imagecost.test.sh — the computed dollar cost of an image generation.
#
# The image endpoint returns no cost of its own, and Ofox exposes no billing
# endpoint to look one up (every /v1 and /v2 usage, billing, credits, account
# and balance path answers 404). So the figure is computed here from the
# published rates and the response's own token counts, and the only thing
# that makes it trustworthy is that it was checked against a real invoice.
#
# The anchor case below is that invoice: a call reporting input_tokens=79,
# output_tokens=1120 was billed $0.06723950 on 2026-08-31. It settles a
# question the model page could not — whether image output tokens bill at
# $60/M or $3/M, a 20x difference. If this case ever stops matching, the
# formula has drifted from what is actually charged, and the skill is
# quoting fiction.
#
# Free by construction: rates come from the public, keyless model list (or
# the bundled snapshot when offline), and nothing here submits a request.
#
# Run: bash references/test/imagecost.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-image.sh"

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

LIB="$WORK/lib.sh"
sed -e '/^main "\$@"$/d' -e '/^exit \$?$/d' "$TARGET" > "$LIB"
# shellcheck source=/dev/null
. "$LIB"

# The lib is sourced from a copy in $WORK, so the script's own SCRIPT_DIR — and
# with it MODELS_SNAPSHOT — resolves next to the copy, where nothing exists.
# The effect was invisible with a network: the snapshot rung of the fallback
# ladder was simply unreachable here, and this suite died outright offline
# ("no model list available") while claiming in its own header that it falls
# back to the bundled snapshot. Point both back at the real reference dir.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_SNAPSHOT="$SCRIPT_DIR/../models-snapshot.json"
TOKEN_ANCHORS="$SCRIPT_DIR/../token-anchors.json"

load_models >/dev/null 2>&1 || true
if [ -z "${MODELS_FILE:-}" ]; then
  echo "FAIL  no model list available (live, cache or snapshot) — cannot price anything"
  exit 1
fi
echo "rates from: $MODELS_SOURCE"
echo

GEMINI="google/gemini-3.1-flash-image"

echo "=== The invoice this formula is anchored to ==="
got="$(image_cost_for "$GEMINI" 79 1120)"
if [ "$got" = "0.0672395" ]; then
  pass "in=79 out=1120 -> $got, matching the \$0.06723950 invoice line"
else
  fail "the anchor case no longer matches the real invoice" \
    "want 0.0672395, got '$got' — the charged rate may have changed"
fi

got="$(image_cost_for "$GEMINI" 51 1120)"
if [ "$got" = "0.0672255" ]; then
  pass "in=51 out=1120 -> $got (same batch, same formula)"
else
  fail "second real call priced wrong" "want 0.0672255, got '$got'"
fi


echo
echo "=== Rates are per model, not hardcoded to one ==="
gpt="$(image_cost_for "openai/gpt-image-2" 79 1120 2>/dev/null || true)"
if [ -n "$gpt" ] && [ "$gpt" != "$(image_cost_for "$GEMINI" 79 1120)" ]; then
  pass "a different model prices differently ($gpt vs 0.0672395)"
elif [ -z "$gpt" ]; then
  pass "a model without published rates yields no figure (rather than a guess)"
else
  fail "every model returns the same number" "rates look hardcoded"
fi

echo
echo "=== It refuses rather than guessing ==="
if image_cost_for "no/such-model" 79 1120 >/dev/null 2>&1; then
  fail "an unknown model produced a price" "a made-up cost is worse than none"
else
  pass "an unknown model yields nothing, so the caller says why"
fi
if image_cost_for "$GEMINI" "abc" 1120 >/dev/null 2>&1; then
  fail "non-numeric tokens produced a price" "input was not validated"
else
  pass "non-numeric token counts are refused"
fi
if [ "$(image_cost_for "$GEMINI" 0 0)" = "0" ]; then
  pass "zero tokens cost zero"
else
  fail "zero tokens priced oddly" "$(image_cost_for "$GEMINI" 0 0)"
fi

echo
echo "=== Which model is priced when the response's echo is missing or wrong ==="
# The bug: openai/gpt-image-2 returns no `model` field, the old code defaulted
# it to the literal string "unknown", and pricing "unknown" found no rates —
# so two real, paid calls printed no cost at all. The fallback that fixes it
# must keep two cases apart, because they mean opposite things: a missing echo
# is silence (use what we asked for), a different echo is a contradiction
# (believe it — that is the model the invoice will be for).
GPT="openai/gpt-image-2"
MAI="microsoft/mai-image-2.5-flash"
ERRLOG="$WORK/resolve.err"

# The runs above overwrote MODELS_FILE with synthetic lists in later sections;
# this section needs the real rates, so re-resolve from the live list/snapshot.
MODELS_FILE=""
load_models >/dev/null 2>&1 || true

echoed_body() { jq -nc --arg m "$1" '{model: $m, data: [], usage: {}}'; }

resolve_response_model "$GPT" "$(echoed_body "$GPT")" 2>"$ERRLOG"
if [ "$RESPONSE_MODEL" = "$GPT" ] && [ "$RESPONSE_MODEL_SOURCE" = "response" ]; then
  pass "an echo that agrees is taken from the response, and labelled as such"
else
  fail "an agreeing echo was mishandled" \
    "model='$RESPONSE_MODEL' source='$RESPONSE_MODEL_SOURCE'"
fi
if [ -s "$ERRLOG" ]; then
  fail "the ordinary case warned about something" "$(tr '\n' ' ' <"$ERRLOG")"
else
  pass "the ordinary case says nothing extra"
fi

# Three shapes of "no echo": absent key, explicit null, empty string. All three
# are silence, not contradiction.
for shape in absent explicitly-null empty; do
  case "$shape" in
    absent) body='{"data":[],"usage":{}}' ;;
    explicitly-null) body='{"model":null,"data":[]}' ;;
    empty) body='{"model":"","data":[]}' ;;
  esac
  RESPONSE_MODEL=""
  RESPONSE_MODEL_SOURCE=""
  resolve_response_model "$GPT" "$body" 2>"$ERRLOG"
  if [ "$RESPONSE_MODEL" = "$GPT" ] && [ "$RESPONSE_MODEL_SOURCE" = "request" ]; then
    pass "an $shape 'model' field falls back to the requested id, marked 'request'"
  else
    fail "an $shape 'model' field was mishandled" \
      "model='$RESPONSE_MODEL' source='$RESPONSE_MODEL_SOURCE'"
  fi
  if [ "$RESPONSE_MODEL" = "unknown" ]; then
    fail "the literal string 'unknown' is back" "that is the original bug"
  fi
done
if grep -q "no 'model' field" "$ERRLOG" && grep -q 'not one the API confirmed' "$ERRLOG"; then
  pass "the fallback is disclosed, not silently substituted"
else
  fail "a missing echo must be disclosed" "$(tr '\n' ' ' <"$ERRLOG")"
fi

# The whole point of the fix: a cost comes out the other end.
cost="$(image_cost_for "$RESPONSE_MODEL" 14 196 2>/dev/null || true)"
if [ "$cost" = "0.00595" ]; then
  pass "the requested id prices the call (in=14 out=196 -> \$$cost), where 'unknown' priced nothing"
else
  fail "the fallback id still yields no usable cost" "got '$cost', want 0.00595"
fi

# A different echo must NOT be overwritten with the requested id. Doing that
# would hide an upstream swap, and the swap is exactly what makes a bill fail
# to reconcile.
RESPONSE_MODEL=""
RESPONSE_MODEL_SOURCE=""
resolve_response_model "$GPT" "$(echoed_body "$MAI")" 2>"$ERRLOG"
if [ "$RESPONSE_MODEL" = "$MAI" ] && [ "$RESPONSE_MODEL_SOURCE" = "response" ]; then
  pass "a contradicting echo wins over the requested id"
else
  fail "a contradicting echo was overwritten with the request" \
    "model='$RESPONSE_MODEL' source='$RESPONSE_MODEL_SOURCE' — the swap would be invisible"
fi
if grep -q "upstream ran '$MAI'" "$ERRLOG" && grep -q "$GPT" "$ERRLOG"; then
  pass "the mismatch is reported, naming both the requested and the actual model"
else
  fail "a model swap must be surfaced" "$(tr '\n' ' ' <"$ERRLOG")"
fi
# And it must be priced as the model that ran, not the one that was asked for.
#
# The expectation is DERIVED from the rates the loaded list reports, not typed
# in. It used to be the literal 0.026694, and that broke on 2026-09-15 with no
# code change at all: Ofox moved mai-image-2.5-flash's output_image from
# 0.000026 to 0.0000195 and the suite started failing at HEAD. A hardcoded copy
# of an external API's number is this repo's most-repeated defect, and a test
# is not exempt from it — the number is the vendor's, the invariant is ours.
#
# What is actually under test is the invariant: the figure must follow the
# model that RAN. So compute it here, independently of image_cost_for's own jq,
# and additionally require the two models to disagree — a formula that ignored
# the model id entirely would satisfy the arithmetic but not that.
#
# The one hardcoded figure in this file stays hardcoded on purpose: the
# $0.06723950 invoice line at the top is a fact about a bill that was really
# paid, not a rate that can move under it.
expect_cost_for() { # <model> <input tokens> <output tokens>
  jq -r --arg m "$1" --argjson i "$2" --argjson o "$3" '
    first(.data[] | select(.id == $m or ((.aliases // []) | index($m)) != null))
    | (((.pricing.input // .pricing.prompt) | tonumber) * $i
       + (.pricing.output_image | tonumber) * $o)
    | . * 100000000 | round / 100000000 | tostring' "$MODELS_FILE"
}
swapped="$(image_cost_for "$RESPONSE_MODEL" 14 1024)"
asked="$(image_cost_for "$GPT" 14 1024)"
want_swapped="$(expect_cost_for "$MAI" 14 1024)"
if [ "$swapped" = "$want_swapped" ] && [ "$swapped" != "$asked" ]; then
  pass "the swapped-in model is priced at its own rate (\$$swapped, not \$$asked)"
else
  fail "a swapped model was priced at the requested model's rate" \
    "swapped='$swapped' want='$want_swapped' asked='$asked'"
fi

echo
echo "=== Both spellings of the rate keys are accepted ==="
# /v1/models calls them prompt/completion; /v2/models/catalog calls them
# input/output. The script loads the v1 list, so handling only the catalog
# spelling silently produced no cost at all. Both are exercised against a
# synthetic list rather than by reading the source, so a refactor that keeps
# the behaviour keeps the test passing.
synthetic() { # <input-key> <output-image-value>
  jq -nc --arg ik "$1" --arg oi "$2" \
    '{data:[{id:"fake/model", pricing:{($ik):"0.0000005", output_image:$oi}}]}'
}

for spelling in prompt input; do
  MODELS_FILE="$WORK/models-$spelling.json"
  synthetic "$spelling" "0.00006" > "$MODELS_FILE"
  got="$(image_cost_for "fake/model" 79 1120)"
  if [ "$got" = "0.0672395" ]; then
    pass "a list using '$spelling' for the input rate prices correctly"
  else
    fail "'$spelling' spelling yielded no usable cost" "got '$got'"
  fi
done

# And a list with neither spelling must yield nothing rather than a partial
# figure computed from the output rate alone.
MODELS_FILE="$WORK/models-none.json"
jq -nc '{data:[{id:"fake/model", pricing:{output_image:"0.00006"}}]}' > "$MODELS_FILE"
if image_cost_for "fake/model" 79 1120 >/dev/null 2>&1; then
  fail "priced a model with no input rate" "a partial cost is still a wrong cost"
else
  pass "a missing input rate yields no figure, not a partial one"
fi

echo
echo "-----------------------------------------"
echo "passed: $PASS   failed: $FAIL"
[ "$FAIL" -eq 0 ]
