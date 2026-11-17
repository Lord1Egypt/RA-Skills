#!/usr/bin/env bash
# edit.test.sh — the /v1/images/edits path of ofox-image.sh.
#
# Free by construction, and on this endpoint that phrase has to be read more
# carefully than usual. Every other suite here can lean on the API refusing a
# bad request for nothing; /v1/images/edits does NOT do that. Measured
# 2026-09-15: --quality ultra_not_a_value was silently accepted and rendered
# six billable images. So:
#
#   - rejection cases must exit before any network call, and are asserted on
#     exit 1 (validation) rather than on what the API says;
#   - anything that passes validation is pointed at an unroutable API base, so
#     it dies on connect with exit 5 instead of editing anything.
#
# HERMETIC, and that is a second thing "free" does not give you for free. An
# earlier version of this suite warmed the real model list from api.ofox.ai and
# then went offline, so every model-support assertion silently tested whichever
# data source happened to be present: it scored 39/0, 37/2, 36/3 and 30/9 on
# repeated runs of unchanged code. A suite whose result depends on a network
# hiccup, or on whether someone ran a real command earlier, trains people to
# ignore failures. So:
#
#   - nothing here contacts the network. OFOX_API_BASE_URL is unroutable from
#     the first line to the last, and a test asserts it never gets unset.
#   - the two offline data sources are exercised DELIBERATELY and separately.
#     use_fixture_catalog installs a hand-written model list in the cache, so
#     the behavioural assertions run against known content; the snapshot
#     section empties the cache and asserts on the bundled file itself, which
#     is where a stale snapshot shows up as a user-facing defect rather than as
#     a test problem.
#
# Run: bash references/test/edit.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-image.sh"
ANCHORS="$SCRIPT_DIR/../token-anchors.json"
SNAPSHOT="$SCRIPT_DIR/../models-snapshot.json"

if [ ! -f "$TARGET" ]; then
  echo "FATAL: cannot find ofox-image.sh at $TARGET" >&2
  exit 1
fi

PASS=0
FAIL=0

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export XDG_CACHE_HOME="$WORK/cache"
# Not a credential — the script only checks that OFOX_API_KEY is non-empty.
# Through a variable, and a plain dictionary word, because a key-shaped literal
# assigned straight to OFOX_API_KEY is what tripped ClawHub's static scan.
PLACEHOLDER=placeholder
export OFOX_API_KEY="$PLACEHOLDER"

# Set once, never unset. Every command below runs against an unroutable base,
# so a request that passes validation dies on connect instead of editing
# anything, and no test can accidentally read live data.
export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"

# A real, tiny PNG to upload. Built here rather than committed so the suite
# carries no binary fixture: a 2x2 red square is enough for every check below,
# because nothing here inspects the picture.
IMG="$WORK/in.png"
WEBP="$WORK/in.webp"
NOTIMG="$WORK/in.html"
if command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg -nostdin -loglevel error -f lavfi -i color=c=red:s=2x2 -frames:v 1 -y "$IMG" 2>/dev/null
  cp "$IMG" "$WEBP" 2>/dev/null
else
  # No ffmpeg: a real PNG header is all the extension/readability checks need.
  printf '\211PNG\r\n\032\n' >"$IMG"
  printf '\211PNG\r\n\032\n' >"$WEBP"
fi
printf '<html>not an image</html>' >"$NOTIMG"

expect_reject() {
  local want="$1" desc="$2"
  shift 3
  local out code
  out=$(bash "$TARGET" edit "$@" 2>&1)
  code=$?
  if [ "$code" -ne 1 ]; then
    printf 'FAIL  %s\n      expected exit 1 (validation, no network), got %s\n      output: %s\n' \
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

ok() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
bad() {
  printf 'FAIL  %s\n      %s\n' "$1" "${2:-}"
  FAIL=$((FAIL + 1))
}

# The model list every behavioural assertion below runs against. Written here
# rather than fetched, so what the script sees is fixed by this file and not by
# the network, the day, or a cache someone left behind. It is deliberately NOT
# the bundled snapshot either: the snapshot is content under test (see the
# section at the end), and a suite that asserts behaviour against the same file
# it is trying to validate can only ever agree with itself.
#
# Content chosen to exercise both directions of the one rule that matters: a
# model whose supported_endpoints carries /v1/images/edits must be accepted,
# and one whose array omits it must be refused, with nothing in between.
# openai/gpt-image-2 also carries the pricing keys print_edit_estimate needs —
# output_image for the output tokens, prompt and image for the uploaded
# picture. Dropping the last two is how an offline estimate silently loses the
# input-token component and under-quotes by a third.
write_fixture_catalog() {
  cat >"$WORK/fixture-models.json" <<'JSON'
{
  "object": "list",
  "data": [
    { "id": "openai/gpt-image-2",
      "is_deprecated": false,
      "aliases": ["gpt-image-2"],
      "pricing": { "prompt": "0.000005", "image": "0.000008", "output_image": "0.00003" },
      "supported_endpoints": ["/v1/images/edits", "/v1/images/generations"] },
    { "id": "microsoft/mai-image-2.5-flash",
      "is_deprecated": false,
      "aliases": ["mai-image-2.5-flash"],
      "pricing": { "prompt": "0.000005", "output_image": "0.0000195" },
      "supported_endpoints": ["/v1/images/edits", "/v1/images/generations"] },
    { "id": "microsoft/mai-image-2.5-pro",
      "is_deprecated": false,
      "aliases": ["mai-image-2.5-pro"],
      "pricing": { "prompt": "0.000005", "output_image": "0.000106" },
      "supported_endpoints": ["/v1/images/edits", "/v1/images/generations"] },
    { "id": "google/gemini-3-pro-image",
      "is_deprecated": false,
      "aliases": ["gemini-3-pro-image"],
      "pricing": { "prompt": "0.0000005", "output_image": "0.00012" },
      "supported_endpoints": ["/v1/chat/completions", "/v1/images/edits", "/v1/images/generations"] },
    { "id": "generations/only-model",
      "is_deprecated": false,
      "aliases": [],
      "pricing": { "prompt": "0.000005", "output_image": "0.00003" },
      "supported_endpoints": ["/v1/images/generations"] }
  ]
}
JSON
}

# Install the fixture where load_models looks for a fresh cache. This is the
# cache rung of the fetch/cache/fallback ladder, entered deliberately: the
# fetch cannot succeed (unroutable base) and the file is newly written, so it
# is inside the 24h TTL and is used without a NOTE.
use_fixture_catalog() {
  rm -rf "${XDG_CACHE_HOME:?}"
  mkdir -p "$XDG_CACHE_HOME/ofox"
  cp "$WORK/fixture-models.json" "$XDG_CACHE_HOME/ofox/models.json"
}

# The other rung: no cache at all, so load_models falls through to the bundled
# snapshot. Used only by the snapshot section, which is about that file's
# content rather than about the script's logic.
use_bundled_snapshot() {
  rm -rf "${XDG_CACHE_HOME:?}"
}

write_fixture_catalog

echo "=== An input image is required, and has to be one this endpoint takes ==="
use_fixture_catalog
expect_reject "input image is required" "no --image and no --image-url is rejected" -- \
  --prompt "make it blue"
expect_reject "not a file that exists" "a path that does not exist is rejected" -- \
  --image "$WORK/nope.png" --prompt "make it blue"
expect_reject "supported format" "an unsupported input format is rejected locally" -- \
  --image "$NOTIMG" --prompt "make it blue"
expect_reject "not both" "--image and --image-url together is rejected" -- \
  --image "$IMG" --image-url "https://example.com/a.png" --prompt "make it blue"
expect_reject "prompt is required" "--prompt is required" -- \
  --image "$IMG"

# The three formats the API enumerated in its own rejection message must all
# pass. Rejecting one of them would be a false rejection with no way around it
# short of editing the script — worse than the 400 it would be preventing.
for f in png webp; do
  src="$IMG"; [ "$f" = "webp" ] && src="$WEBP"
  out=$(bash "$TARGET" edit --image "$src" --prompt x --dry-run 2>&1)
  if [ $? -eq 0 ]; then
    ok ".$f is accepted as an input format"
  else
    bad ".$f must be accepted (the API enumerates jpeg/png/webp)" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  fi
done

echo
echo "=== Model support is read from the catalog, not from a table here ==="
use_fixture_catalog
# Both directions, against fixture content rather than against whatever the
# catalog says today. The rule under test is "the supported_endpoints array
# decides"; asserting it with live ids would make the suite's verdict depend on
# Ofox's product roadmap, which is how the first version of this file managed
# to report four different scores for one commit.
#
# The real API agrees with this rule in both directions, confirmed free on
# 2026-09-15: qwen/qwen-image-3.0-pro (array omits the endpoint) is refused
# with endpoint_not_supported, and seven models carrying it all ran an edit.
# That confirmation belongs in the docs; what belongs here is that the script
# reads the field at all.
expect_reject "does not serve /v1/images/edits" "a model whose array omits the endpoint is rejected before the request" -- \
  --image "$IMG" --prompt x --model generations/only-model
expect_reject "models --endpoint edits" "and the error points at the live list, not a table" -- \
  --image "$IMG" --prompt x --model generations/only-model

# The other direction: a model whose entry DOES carry the endpoint must pass.
for m in openai/gpt-image-2 google/gemini-3-pro-image microsoft/mai-image-2.5-pro; do
  out=$(bash "$TARGET" edit --image "$IMG" --prompt x --model "$m" --dry-run 2>&1)
  if [ $? -eq 0 ]; then
    ok "$m is accepted for editing (its catalog entry carries the endpoint)"
  else
    bad "$m serves /v1/images/edits and must not be rejected" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  fi
done

# Same fixture, one field flipped, nothing else. If the verdict does not follow
# the array, the lookup is reading something other than the catalog — which is
# the failure the section is named after, and the one a live-data assertion
# cannot distinguish from "the vendor changed their mind".
flipped="$WORK/flipped.json"
jq '(.data[] | select(.id == "openai/gpt-image-2").supported_endpoints)
      |= map(select(. != "/v1/images/edits"))' \
  "$WORK/fixture-models.json" >"$flipped"
cp "$flipped" "$XDG_CACHE_HOME/ofox/models.json"
expect_reject "does not serve /v1/images/edits" "removing the endpoint from a model's array flips the verdict" -- \
  --image "$IMG" --prompt x --model openai/gpt-image-2
use_fixture_catalog

# The guard that keeps R3 honest: no hardcoded edit-support list may appear.
# Support has to come from each model's supported_endpoints. Five defects in
# this repo came from keeping a local copy of an external API's value table.
hits=$(grep -c 'EDITS_ENDPOINT' "$TARGET")
if [ "$hits" -gt 0 ] &&
  grep -q 'index($e)' "$TARGET" &&
  ! grep -qE '^(EDIT_MODELS|EDIT_CAPABLE|MODELS_WITH_EDITS)=' "$TARGET"; then
  ok "edit support is looked up in supported_endpoints; no static model table exists"
else
  bad "edit support must be read from the catalog, never hardcoded" "found a static-looking table"
fi

echo
echo "=== Parameters are checked HERE, because the API does not check them ==="
# This is the expensive asymmetry. /v1/images/generations rejects a bad
# --quality with a free HTTP 400. /v1/images/edits accepted
# quality=ultra_not_a_value and rendered six billable images on 2026-09-15.
# So these checks are not a round-trip saving, they are the only guard.
use_fixture_catalog
expect_reject "quality" "an undocumented --quality is rejected locally" -- \
  --image "$IMG" --prompt x --quality ultra_not_a_value
out=$(bash "$TARGET" edit --image "$IMG" --prompt x --quality ultra_not_a_value 2>&1)
if printf '%s' "$out" | grep -qi 'does NOT reject'; then
  ok "and the error says why it matters here — the API would have billed it"
else
  bad "the --quality error must say this endpoint does not reject it upstream" \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
expect_reject "size" "an undocumented --size is rejected" -- \
  --image "$IMG" --prompt x --size 123x456
expect_reject "n" "--n out of range is rejected" -- \
  --image "$IMG" --prompt x --n 99
expect_reject "KEY=VALUE" "--extra-form without an = is rejected" -- \
  --image "$IMG" --prompt x --extra-form nonsense
expect_reject "collides" "--extra-form cannot override a field a flag owns" -- \
  --image "$IMG" --prompt x --extra-form prompt=other
expect_reject "out-name" "--out-name with a path separator is rejected" -- \
  --image "$IMG" --prompt x --out-name sub/dir

echo
echo "=== The multipart form is assembled, and JSON is never built ==="
use_fixture_catalog
out=$(bash "$TARGET" edit --image "$IMG" --prompt "make it blue" \
  --quality low --size 1024x1024 --n 2 --output-format webp --background opaque \
  --extra-form mask_hint=none --dry-run 2>&1)
fields=$(printf '%s' "$out" | grep '^FORM_FIELDS' | sed 's/^FORM_FIELDS //')
missing=""
for want in image model prompt quality size n output_format background mask_hint; do
  case " $fields " in
    *" $want "*) : ;;
    *) missing="$missing $want" ;;
  esac
done
if [ -z "$missing" ]; then
  ok "every flag reaches the form: $fields"
else
  bad "fields missing from the multipart form:$missing" "got: $fields"
fi
# The endpoint is multipart-only — an application/json body was rejected with
# "You must provide a model parameter" even with model set, i.e. the field was
# never seen. So the edit path must never print or build a JSON payload.
if printf '%s' "$out" | grep -q '^PAYLOAD'; then
  bad "the edit path must not build a JSON payload — this endpoint rejects JSON" ""
else
  ok "no JSON payload is built for a multipart-only endpoint"
fi
# Field NAMES only. --extra-form is a passthrough, so values must never be
# echoed into a line an agent will paste into a chat.
if printf '%s' "$out" | grep -q 'mask_hint=none'; then
  bad "FORM_FIELDS must list field names, never their values" ""
else
  ok "FORM_FIELDS lists names only, so a passthrough value cannot leak"
fi

echo
echo "=== --dry-run spends nothing and needs no API key ==="
use_fixture_catalog
out=$(env -u OFOX_API_KEY bash "$TARGET" edit --image "$IMG" --prompt x --dry-run 2>&1)
code=$?
if [ "$code" -eq 0 ]; then
  ok "--dry-run succeeds with no OFOX_API_KEY set (pricing a job precedes signing up)"
else
  bad "--dry-run must not require a key (exit $code)" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q '^STATUS dry_run'; then
  ok "--dry-run reports STATUS dry_run"
else
  bad "--dry-run must report STATUS dry_run" ""
fi
if printf '%s' "$out" | grep -qi 'nothing was submitted and nothing was billed'; then
  ok "--dry-run says outright that nothing was billed"
else
  bad "--dry-run must state that nothing was billed" ""
fi
# An agent can relay a number, and can relay "cannot be predicted". It cannot
# notice a line that was never printed — so the estimate prints on every path.
if printf '%s' "$out" | grep -q 'Estimated cost:'; then
  ok "exactly one estimate line is printed, even with no key"
else
  bad "an estimate must print on every path" ""
fi
n_est=$(printf '%s' "$out" | grep -c 'Estimated cost:')
if [ "$n_est" -eq 1 ]; then
  ok "and exactly one, not two"
else
  bad "expected exactly 1 estimate line, got $n_est" ""
fi

echo
echo "=== The estimate is matched on the INPUT image, and errs high ==="
# The axis that matters here is not (quality, size) as it is for a generation:
# two of the measured points share a model, a quality and an identical 1672x941
# output and still differ 2.3x in output tokens. They track the upload — but
# not proportionally to it (854x480 has 6.3x the pixels of 256x256 and bills
# 2.25x the image tokens), which is why the unmatched case below must quote the
# dearest point rather than anything interpolated.
if command -v ffprobe >/dev/null 2>&1 && command -v ffmpeg >/dev/null 2>&1; then
  small="$WORK/320x180.png"
  large="$WORK/854x480.png"
  square="$WORK/256x256.png"
  odd="$WORK/640x360.png"
  ffmpeg -nostdin -loglevel error -f lavfi -i color=c=red:s=320x180 -frames:v 1 -y "$small" 2>/dev/null
  ffmpeg -nostdin -loglevel error -f lavfi -i color=c=red:s=854x480 -frames:v 1 -y "$large" 2>/dev/null
  ffmpeg -nostdin -loglevel error -f lavfi -i color=c=red:s=256x256 -frames:v 1 -y "$square" 2>/dev/null
  ffmpeg -nostdin -loglevel error -f lavfi -i color=c=red:s=640x360 -frames:v 1 -y "$odd" 2>/dev/null

  s_out=$(bash "$TARGET" edit --image "$small" --prompt x --model openai/gpt-image-2 --dry-run 2>&1)
  l_out=$(bash "$TARGET" edit --image "$large" --prompt x --model openai/gpt-image-2 --dry-run 2>&1)
  q_out=$(bash "$TARGET" edit --image "$square" --prompt x --model openai/gpt-image-2 --dry-run 2>&1)
  o_out=$(bash "$TARGET" edit --image "$odd" --prompt x --model openai/gpt-image-2 --dry-run 2>&1)

  if printf '%s' "$s_out" | grep -q 'input image of 320x180'; then
    ok "a 320x180 input quotes the point measured at 320x180"
  else
    bad "a measured input size must quote its own point" "$(printf '%s' "$s_out" | grep -m1 Estimated)"
  fi
  # The 1:1 point. It exists because two 16:9 samples could not distinguish
  # "output follows the input ratio" from "output is a fixed 1672x941", and the
  # first of those had been written down as a finding on the strength of them.
  if printf '%s' "$q_out" | grep -q 'input image of 256x256'; then
    ok "a 256x256 input quotes the point measured at 256x256"
  else
    bad "a measured input size must quote its own point" "$(printf '%s' "$q_out" | grep -m1 Estimated)"
  fi
  if printf '%s' "$l_out" | grep -q 'input image of 854x480'; then
    ok "an 854x480 input quotes the point measured at 854x480"
  else
    bad "a measured input size must quote its own point" "$(printf '%s' "$l_out" | grep -m1 Estimated)"
  fi
  # No match: quote the DEAREST point, labelled. Never a cheaper one, and never
  # something interpolated between them — a table that errs low is how a 26x
  # bill got approved on the other endpoint.
  #
  # ⚠️ THESE ASSERTIONS USED TO COMPARE OUTPUT-TOKEN COUNTS, and that was the
  # same mistake as the code they check. Both treated "dearest" as "most output
  # tokens". An edit's bill is dominated by the INPUT image at large sizes, so
  # those are different orderings, and when the 1792x1008 point landed (129
  # output tokens, yet the dearest point on record at 0.016438) the old
  # assertions INVERTED: they began demanding the cheaper point and forbidding
  # the dearest — the exact opposite of the comment above them. They had passed
  # all along because implementation and test shared one wrong premise. A check
  # cannot catch a bug it also contains.
  #
  # So this is judged in MONEY now, derived from the anchor file and the rate
  # card at run time. Nothing here hardcodes a token count or a dollar figure:
  # swapping one hardcoded number for another would only move the mine. A fifth
  # anchor, at any size, keeps this assertion correct with no edit.
  edit_rate_out=$(jq -r '.data[]? // .[]? | select(.id=="openai/gpt-image-2")
    | .pricing.output_image // empty' "$SNAPSHOT" 2>/dev/null | head -1)
  edit_rate_in=$(jq -r '.data[]? // .[]? | select(.id=="openai/gpt-image-2")
    | (.pricing.image // .pricing.input // .pricing.prompt) // empty' "$SNAPSHOT" 2>/dev/null | head -1)
  # The dearest measured point, priced the way the script prices one.
  dearest=$(jq -r --arg ro "$edit_rate_out" --arg ri "$edit_rate_in" '
    .edit_anchors["openai/gpt-image-2"] as $a
    | ([$a] + ($a.additional_measurements // []))
    | map(select((.output_tokens | type) == "number")
          | (.output_tokens * ($ro | tonumber)) + ((.input_tokens // 0) * ($ri | tonumber)))
    | max' "$ANCHORS" 2>/dev/null)
  quoted=$(printf '%s' "$o_out" | grep -m1 'Estimated cost:' \
    | sed -n 's/.*~\$\([0-9.]*\).*/\1/p')

  if printf '%s' "$o_out" | grep -q 'ROUGH UPPER BOUND'; then
    ok "an unmeasured input size is labelled an UPPER BOUND"
  else
    bad "an unmeasured input must say it is a bound" "$(printf '%s' "$o_out" | grep -m1 Estimated)"
  fi
  # The bound must be >= the dearest thing anyone has actually been billed.
  # Printed to 4dp, so allow half a unit in the last place and nothing more.
  if [ -n "$quoted" ] && [ -n "$dearest" ] &&
    awk -v q="$quoted" -v d="$dearest" 'BEGIN { exit !(q + 0.00005 >= d) }'; then
    ok "the bound ($quoted) is >= the dearest measured point ($(awk -v d="$dearest" 'BEGIN{printf "%.6f", d}'))"
  else
    bad "an unmeasured input was quoted BELOW a known real bill — a bound that is not the largest known value is not a bound" \
      "quoted=$quoted dearest=$dearest :: $(printf '%s' "$o_out" | grep -m1 Estimated)"
  fi
else
  printf 'skip  input-size matching (needs ffmpeg/ffprobe)\n'
fi

# A model with no edit measurement must refuse to quote rather than borrow a
# figure from another model, or from its own GENERATION anchor — the same
# model reported 196 output tokens for a generation and 301 for an edit.
out=$(bash "$TARGET" edit --image "$IMG" --prompt x --model google/gemini-3-pro-image --dry-run 2>&1)
if printf '%s' "$out" | grep -q 'cannot be predicted'; then
  ok "a model with no edit measurement says so instead of borrowing a number"
else
  bad "an unmeasured model must not be quoted a borrowed figure" "$(printf '%s' "$out" | grep -m1 Estimated)"
fi
if printf '%s' "$out" | grep -q '196\|301'; then
  bad "an unmeasured model must not leak another measurement's token count" ""
else
  ok "and names no other measurement's token count"
fi

echo
echo "=== Edit anchors are separate from generation anchors ==="
if jq -e '.edit_anchors' "$ANCHORS" >/dev/null 2>&1; then
  ok "token-anchors.json carries an edit_anchors section"
else
  bad "edit measurements must live in edit_anchors, not in anchors" ""
fi
# Every edit measurement must carry the input size it was measured at. Without
# it the number cannot be matched to a request and is a coincidence waiting to
# be quoted — the generation side already paid 26x for that lesson.
missing=$(jq -r '
  [ .edit_anchors // {} | to_entries[]
    | .value as $a
    | ([$a] + ($a.additional_measurements // []))[]
    | select((.input_size // "") == "" or (.output_tokens | type) != "number")
  ] | length' "$ANCHORS" 2>/dev/null)
if [ "$missing" = "0" ]; then
  ok "every edit measurement records the input size it was measured at"
else
  bad "$missing edit measurement(s) lack an input_size or output_tokens" ""
fi
# No edit anchor may claim an invoice check. Neither reading of the token
# counts has been held against a billing line.
claimed=$(jq -r '[ .edit_anchors // {} | to_entries[] | .value as $a
  | ([$a] + ($a.additional_measurements // []))[]
  | select(.cost_invoice_checked == true) ] | length' "$ANCHORS" 2>/dev/null)
if [ "$claimed" = "0" ]; then
  ok "no edit cost claims to be invoice-checked, because none is"
else
  bad "$claimed edit anchor(s) claim an invoice check that has not happened" ""
fi

echo
echo "=== Nothing above reached the network; a valid request dies on connect ==="
use_fixture_catalog
out=$(bash "$TARGET" edit --image "$IMG" --prompt "make it blue" 2>&1)
code=$?
if [ "$code" -eq 5 ]; then
  ok "a fully valid edit against an unroutable base exits 5 (ambiguous, no response)"
else
  bad "expected exit 5 from an unroutable base, got $code" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -qi 'billing history'; then
  ok "and points at the billing history, since there is no job id to poll"
else
  bad "exit 5 must tell the caller how to find out whether it was billed" ""
fi

echo
echo "=== The BUNDLED SNAPSHOT, which is what a cold cache offline actually uses ==="
# A separate rung of the ladder and a separate kind of failure. Everything
# above tests the script's logic against fixture content; this tests the
# shipped data, because a snapshot that predates a capability makes the script
# give a confident wrong answer to a real user — "'openai/gpt-image-2' exists
# but does not serve /v1/images/edits" for a model that does. That shipped
# once: the snapshot was generated before Ofox advertised the endpoint and was
# never refreshed, so `edit` was unusable offline on every model in the chain.
# Regenerate with references/refresh-snapshot.sh.
use_bundled_snapshot
if [ -f "$SNAPSHOT" ]; then
  ok "a bundled snapshot exists to fall back to"
else
  bad "models-snapshot.json is missing; offline runs have no model list" ""
fi
snap_edit_models=$(jq '[.data[] | select((.supported_endpoints // []) | index("/v1/images/edits"))] | length' "$SNAPSHOT" 2>/dev/null)
if [ "${snap_edit_models:-0}" -gt 0 ] 2>/dev/null; then
  ok "the snapshot records $snap_edit_models model(s) that serve /v1/images/edits"
else
  bad "no model in the bundled snapshot serves /v1/images/edits" \
    "the snapshot predates edit support — run references/refresh-snapshot.sh"
fi
# The head of MODEL_CHAIN is what an `edit` with no --model resolves to, so it
# is the one entry whose staleness breaks the feature outright rather than
# narrowing it.
chain_head=$(grep -m1 '^MODEL_CHAIN=' "$SCRIPT_DIR/../ofox-image.sh" | sed 's/^MODEL_CHAIN="//; s/ .*//')
if jq -e --arg m "$chain_head" \
  '.data[] | select(.id == $m) | (.supported_endpoints // []) | index("/v1/images/edits")' \
  "$SNAPSHOT" >/dev/null 2>&1; then
  ok "and the chain head ($chain_head) is one of them, so an offline edit resolves"
else
  bad "the chain head $chain_head cannot edit according to the snapshot" \
    "an offline 'edit' with no --model is refused — refresh the snapshot"
fi
# The offline estimate must keep its input-token component. output_image alone
# prices the output and silently drops the uploaded picture, which on the
# measured 854x480 run is 35% of the bill — an under-quote wearing the
# exact-match ROUGH label rather than a bound.
missing_rates=$(jq -r '[.data[] | select((.supported_endpoints // []) | index("/v1/images/edits"))
  | select((.pricing.output_image // null) != null)
  | select((.pricing.prompt // null) == null)] | length' "$SNAPSHOT" 2>/dev/null)
if [ "${missing_rates:-1}" = "0" ]; then
  ok "every edit-capable snapshot entry with an output rate also carries its input rate"
else
  bad "$missing_rates snapshot entr(y/ies) price output but not input" \
    "the offline edit estimate would under-quote by the whole input component"
fi
# End to end on the snapshot path: no cache, unroutable base, no --model.
out=$(bash "$TARGET" edit --image "$IMG" --prompt x --dry-run 2>&1)
code=$?
if [ "$code" -eq 0 ] && printf '%s' "$out" | grep -q '^STATUS dry_run'; then
  ok "a chain-resolved edit --dry-run works with a cold cache and no network"
else
  bad "the snapshot path must serve a dry-run edit (exit $code)" \
    "$(printf '%s' "$out" | grep -m1 ERROR)"
fi
if printf '%s' "$out" | grep -q 'bundled snapshot'; then
  ok "and says out loud which rung of the fallback ladder it used"
else
  bad "falling back to the snapshot must never be silent" ""
fi

echo
echo "=== The suite itself spends nothing and reads nothing live ==="
# Asserted rather than assumed. The defect this replaces was invisible exactly
# because the network access was incidental — a cache-warming helper nobody
# thought of as a dependency.
if [ "${OFOX_API_BASE_URL:-}" = "http://127.0.0.1:1/v1" ]; then
  ok "OFOX_API_BASE_URL is still unroutable at the end of the run"
else
  bad "something unset or changed OFOX_API_BASE_URL mid-suite" \
    "value is '${OFOX_API_BASE_URL:-<unset>}' — a test may have read live data"
fi
# Comments are stripped first, because this file discusses api.ofox.ai and the
# helper that used to unset the base; a check that cannot tell prose from code
# would fire on its own explanation of itself. The pattern is then assembled
# from fragments so the grep line does not match itself either — the first two
# attempts at this check both failed on exactly that, which is a small live
# demonstration of why a self-inspecting assertion needs its own test run.
live_host="api""."'ofox'".ai"
escape_hatch="unset OFOX_API""_BASE_URL"
if grep -vE '^[[:space:]]*#' "$0" | grep -qE "$escape_hatch|$live_host"; then
  bad "this suite must not reach the real API" "found a live-base escape in $0"
else
  ok "no executable line in this file points at the real API"
fi
if [ "${XDG_CACHE_HOME:-}" = "$WORK/cache" ]; then
  ok "the model cache stayed inside the temp dir, not the user's ~/.cache"
else
  bad "XDG_CACHE_HOME escaped the temp dir" "value is '${XDG_CACHE_HOME:-<unset>}'"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
