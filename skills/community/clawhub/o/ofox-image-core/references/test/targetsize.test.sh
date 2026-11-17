#!/usr/bin/env bash
# targetsize.test.sh — --target-aspect / --target-size: the ratio the caller
# actually needs, guaranteed against the written file.
#
# What is being defended here, and why any of it is worth a test:
#
#   1. 16:9 and 9:16 are NOT in this API's size enum and cannot be requested.
#      1792x1024 is 1.7500 and 1024x1792 is 0.5714; the real ratios are
#      1.7778 and 0.5625. So a 16:9 frame is always a crop, and the crop has
#      to be computed from the FILE — on microsoft/mai-image-2.5-flash the
#      request, the response's echo and the file measured three different
#      numbers on three separate runs.
#   2. The two hand-crops on record must fall out of the code, not out of an
#      agent doing arithmetic: 1344x768 -> 1344x756 and 1792x1024 -> 1792x1008.
#      Three agents in a row re-derived that by hand before this existed.
#   3. A target that cannot be met must fail loudly. These frames get attached
#      to bytedance/seedance-2.5 jobs, which force aspect_ratio: adaptive, so
#      a wrong-ratio frame becomes a wrong-ratio PAID video. A silently
#      almost-right image is the expensive outcome, not the safe one.
#   4. An explicit --size is respected, never silently replaced. It is warned
#      about when it cannot cover the target, and that is all.
#
# Free by construction: the selection and crop logic is exercised as sourced
# functions on ffmpeg-synthesized local images, and every integration case
# runs --dry-run against an unroutable API base, so a leaked request would
# surface as a connect failure rather than a billable image.
#
# Run: bash references/test/targetsize.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-image.sh"
SKILL_MD="$SCRIPT_DIR/../../SKILL.md"

if [ ! -f "$TARGET" ]; then
  echo "FATAL: cannot find ofox-image.sh at $TARGET" >&2
  exit 1
fi

PASS=0
FAIL=0

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export XDG_CACHE_HOME="$WORK/cache"
OUT_DIR="$WORK/out"

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "$2"
  FAIL=$((FAIL + 1))
}

# Warm the model cache from the real, public, keyless list, then make the API
# base unroutable: validation and pricing still see live data, anything that
# tries to generate dies on connect.
unset OFOX_API_BASE_URL
env -u OFOX_API_KEY bash "$TARGET" models >/dev/null 2>&1 || true
export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"

gen() { env -u OFOX_API_KEY bash "$TARGET" generate "$@" 2>&1; }

# ---------------------------------------------------------------------------
# unit: the geometry, sourced straight out of the script
# ---------------------------------------------------------------------------

LIB="$WORK/lib.sh"
sed -e '/^main "\$@"$/d' -e '/^exit \$?$/d' "$TARGET" >"$LIB"
# shellcheck source=/dev/null
. "$LIB"

echo "=== The size enum cannot express 16:9 or 9:16 — the premise, asserted ==="
# If this ever stops being true the whole flag is unnecessary, so assert it
# rather than trusting the comment above.
reachable=""
for cand in $VALID_SIZES; do
  [ "$cand" = "auto" ] && continue
  cw="${cand%x*}"
  ch="${cand#*x}"
  # exact 16:9 or 9:16 means 9*w == 16*h or 16*w == 9*h
  if [ $((9 * cw)) -eq $((16 * ch)) ] || [ $((16 * cw)) -eq $((9 * ch)) ]; then
    reachable="$reachable $cand"
  fi
done
if [ -z "$reachable" ]; then
  pass "no entry in VALID_SIZES is exactly 16:9 or 9:16 (so a crop is mandatory, not a fallback)"
else
  fail "VALID_SIZES now contains an exact 16:9/9:16 entry — revisit whether the crop is still needed" \
    "reachable:$reachable"
fi

echo
echo "=== Crop dimensions are exact multiples of the reduced ratio ==="
check_crop() { # <mw> <mh> <tw> <th> <expected "W H"> <desc>
  local got
  got="$(crop_dims_for "$1" "$2" "$3" "$4")" || got="FAILED"
  if [ "$got" = "$5" ]; then
    pass "$6"
  else
    fail "$6" "expected '$5', got '$got'"
  fi
}
# The two crops a human worked out by hand on real files, now the code's job.
check_crop 1344 768 16 9 "1344 756" \
  "1344x768 -> 1344x756 for 16:9 (the mai-image-2.5-flash file, hand-cropped on a real run)"
check_crop 1792 1024 16 9 "1792 1008" \
  "1792x1024 -> 1792x1008 for 16:9 (the gpt-image-2 file, hand-cropped on a real run)"
check_crop 1024 1792 9 16 "1008 1792" "1024x1792 -> 1008x1792 for 9:16"
check_crop 1024 1024 1 1 "1024 1024" "a square target crops nothing off a square file"
# Exactness is the point: a rounded division would give 1365x768 here, which
# is 1.7773 — not 16:9, just close enough to look fine and be wrong.
got="$(crop_dims_for 1344 768 16 9)"
if [ $((9 * ${got% *})) -eq $((16 * ${got#* })) ]; then
  pass "the cropped result is EXACTLY the ratio asked for, not a rounded approximation of it"
else
  fail "cropped result is not exactly 16:9" "got '$got'"
fi
if crop_dims_for 8 8 16 9 >/dev/null 2>&1; then
  fail "a file too small to hold one unit of the ratio must fail" "crop_dims_for 8 8 16 9 succeeded"
else
  pass "a file too small to hold one whole unit of the ratio fails instead of returning nonsense"
fi

echo
echo "=== Size selection: the ratio decides which size is requested ==="
check_pick() { # <tw> <th> <floor_w|""> <floor_h|""> <expected size> <desc>
  local got
  got="$(select_size_for_target "$1" "$2" "$3" "$4")" || got="NONE"
  if [ "$got" = "$5" ]; then
    pass "$6"
  else
    fail "$6" "expected '$5', got '$got'"
  fi
}
# No pixel floor: pick the candidate that survives the crop with the most
# pixels intact. 1792x1024 keeps 98.4% for 16:9; 1536x1024 keeps 84.4% and
# 1024x1024 keeps 56.3%.
check_pick 16 9 "" "" "1792x1024" "16:9 requests 1792x1024 — the least wasteful crop available"
check_pick 9 16 "" "" "1024x1792" "9:16 requests 1024x1792"
check_pick 3 2 "" "" "1536x1024" "3:2 requests 1536x1024, which needs no crop at all"
check_pick 2 3 "" "" "1024x1536" "2:3 requests 1024x1536"
# 1:1 must not fall to 256x256 just because it is cheapest and technically
# croppable — retention ranks first, so the full-size square wins.
check_pick 1 1 "" "" "1024x1024" "1:1 requests 1024x1024, not the cheapest square that would technically work"
# With a pixel floor the crop is scaled down afterwards, so pixels above the
# floor are tokens bought and thrown away: cheapest that clears it wins.
check_pick 16 9 1280 720 "1536x1024" "a 1280x720 target takes the cheapest size that clears it after cropping"
check_pick 16 9 512 288 "512x512" "a 512x288 target drops all the way to 512x512"
check_pick 16 9 1792 1008 "1792x1024" "a 1792x1008 target needs the largest size, and finds it"
check_pick 16 9 3840 2160 "NONE" "a 4K target finds nothing — this API cannot serve it without upscaling"

echo
echo "=== Measuring reads the file, and cropping actually crops ==="
if command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1; then
  SRC="$WORK/src.png"
  # 1344x768 on purpose: the exact dimensions of the real mai-image-2.5-flash
  # file whose response claimed 1354x774 and whose request said 1792x1024.
  if ffmpeg -nostdin -loglevel error -f lavfi -i "color=c=blue:s=1344x768" \
    -frames:v 1 -y "$SRC" >/dev/null 2>&1 && [ -s "$SRC" ]; then
    m="$(measure_image_file "$SRC")" || m="FAILED"
    if [ "$m" = "1344x768" ]; then
      pass "measure_image_file reports the file's real pixels"
    else
      fail "measure_image_file should report 1344x768" "got '$m'"
    fi

    if crop_image_to "$SRC" "$WORK/cropped.png" 1344 756 "" "" &&
      [ "$(measure_image_file "$WORK/cropped.png")" = "1344x756" ]; then
      pass "crop_image_to writes a file that really measures the cropped size"
    else
      fail "crop to 1344x756 did not produce a 1344x756 file" \
        "got '$(measure_image_file "$WORK/cropped.png" 2>/dev/null)'"
    fi

    if crop_image_to "$SRC" "$WORK/scaled.png" 1344 756 1280 720 &&
      [ "$(measure_image_file "$WORK/scaled.png")" = "1280x720" ]; then
      pass "a pixel target is scaled to exactly those pixels after the crop"
    else
      fail "crop+scale to 1280x720 did not produce a 1280x720 file" \
        "got '$(measure_image_file "$WORK/scaled.png" 2>/dev/null)'"
    fi
  else
    printf 'skip  ffmpeg could not synthesize a test image\n'
  fi
else
  printf 'skip  ffmpeg/ffprobe not installed — measurement and cropping not exercised\n'
fi

# ---------------------------------------------------------------------------
# integration: the flags, through the real entry point, spending nothing
# ---------------------------------------------------------------------------

echo
echo "=== --dry-run reports the requested size AND the promised ratio ==="
out="$(gen --dry-run --prompt "a rooftop at sunset" --quality high \
  --target-aspect 16:9 --out-dir "$OUT_DIR")"
code=$?
if [ "$code" -eq 0 ]; then
  pass "--target-aspect 16:9 dry-runs clean with no API key"
else
  fail "--target-aspect 16:9 should dry-run clean" "got $code: $(printf '%s' "$out" | tail -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q '^SIZE 1792x1024$'; then
  pass "the chosen request size is reported as SIZE, so an approval table can show it"
else
  fail "expected 'SIZE 1792x1024'" "$(printf '%s' "$out" | grep -i size | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q '^TARGET_ASPECT 16:9$'; then
  pass "the promised ratio is reported as TARGET_ASPECT"
else
  fail "expected 'TARGET_ASPECT 16:9'" "$(printf '%s' "$out" | grep -i target | tr '\n' ' ')"
fi
# The crop is not a footnote: the caller has to know the frame will be cut
# down, because the size they were quoted is not the size they receive.
if printf '%s' "$out" | grep -qi 'centre-cropped\|center-cropped'; then
  pass "the run says out loud that the delivered file will be cropped"
else
  fail "a crop must be announced, not discovered later" "$(printf '%s' "$out" | grep -i note | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q 'STATUS dry_run'; then
  pass "still a dry run — nothing was submitted"
else
  fail "--dry-run must print STATUS dry_run" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== --target-size reports the exact pixels as well as the ratio ==="
out="$(gen --dry-run --prompt "x" --quality high --target-size 1280x720 --out-dir "$OUT_DIR")"
if printf '%s' "$out" | grep -q '^TARGET_SIZE 1280x720$' &&
  printf '%s' "$out" | grep -q '^TARGET_ASPECT 16:9$'; then
  pass "--target-size 1280x720 reports both the pixels and the 16:9 it implies"
else
  fail "expected TARGET_SIZE 1280x720 and TARGET_ASPECT 16:9" \
    "$(printf '%s' "$out" | grep -i 'target\|size' | tr '\n' ' ')"
fi

echo
echo "=== An explicit --size is respected, only warned about ==="
out="$(gen --dry-run --prompt "x" --quality high --size 512x512 \
  --target-size 1280x720 --out-dir "$OUT_DIR")"
code=$?
if [ "$code" -eq 0 ]; then
  pass "an explicit --size that cannot cover the target is a warning, not a rejection"
else
  fail "an undersized explicit --size should warn, not fail the dry run" "got $code"
fi
if printf '%s' "$out" | grep -q '^SIZE 512x512$'; then
  pass "the caller's explicit --size is still the size requested — never silently replaced"
else
  fail "explicit --size 512x512 must survive" "$(printf '%s' "$out" | grep '^SIZE' | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -qi 'cannot cover the target'; then
  pass "the warning says the explicit size cannot cover the target, and what it would yield"
else
  fail "expected a 'cannot cover the target' NOTE" "$(printf '%s' "$out" | grep -i note | tr '\n' ' ')"
fi
# And an explicit size that DOES cover the target must not be nagged about.
out="$(gen --dry-run --prompt "x" --quality high --size 1792x1024 \
  --target-aspect 16:9 --out-dir "$OUT_DIR")"
if printf '%s' "$out" | grep -qi 'cannot cover'; then
  fail "an adequate explicit --size must not be warned about" "$(printf '%s' "$out" | grep -i note | tr '\n' ' ')"
else
  pass "an explicit --size that does cover the target draws no warning"
fi

echo
echo "=== A target that cannot be met fails loudly, before spending ==="
out="$(gen --dry-run --prompt "x" --quality high --target-size 3840x2160 --out-dir "$OUT_DIR")"
code=$?
if [ "$code" -eq 1 ]; then
  pass "a 4K target this API cannot serve is a validation error (exit 1), caught pre-request"
else
  fail "expected exit 1 for an unservable target" "got $code: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -qi 'without upscaling'; then
  pass "the error names the reason — no accepted size can cover it without upscaling"
else
  fail "the error should explain why" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q 'STATUS dry_run'; then
  fail "an unservable target must not report a successful dry run" "printed STATUS dry_run"
else
  pass "no STATUS line — the run stopped instead of quoting an impossible job"
fi

echo
echo "=== Malformed and conflicting targets are rejected before anything else ==="
expect_reject() { # <needle> <desc> <args...>
  local want="$1" desc="$2"
  shift 2
  local o c
  o="$(gen --dry-run --prompt "x" --quality high --out-dir "$OUT_DIR" "$@")"
  c=$?
  if [ "$c" -ne 1 ]; then
    fail "$desc" "expected exit 1, got $c: $(printf '%s' "$o" | head -2 | tr '\n' ' ')"
    return
  fi
  if ! printf '%s' "$o" | grep -qi -- "$want"; then
    fail "$desc" "exit 1 but message did not mention '$want': $(printf '%s' "$o" | head -2 | tr '\n' ' ')"
    return
  fi
  pass "$desc"
}
expect_reject "not both" "--target-aspect and --target-size together are refused" \
  --target-aspect 16:9 --target-size 1280x720
expect_reject "two positive integers" "--target-aspect 16x9 (wrong separator) is refused" \
  --target-aspect "16x9"
expect_reject "two positive integers" "--target-aspect 16:0 is refused" --target-aspect "16:0"
expect_reject "two positive integers" "--target-aspect 16:9:1 is refused" --target-aspect "16:9:1"
expect_reject "two positive integers" "--target-aspect with a non-integer term is refused" \
  --target-aspect "sixteen:9"
expect_reject "two positive integers" "--target-size 1280:720 (wrong separator) is refused" \
  --target-size "1280:720"
expect_reject "requires a value" "--target-aspect with no value is refused" --target-aspect

echo
echo "=== A ratio is never promised without the tools to keep the promise ==="
# The flags are a guarantee about the delivered file, so a missing ffmpeg has
# to fail loudly rather than fall open — falling open would hand back an
# unverified frame that then propagates into a paid video job. Checked with a
# PATH that has the real coreutils and no ffmpeg/ffprobe.
FAKE_BIN="$WORK/fakebin"
mkdir -p "$FAKE_BIN"
for b in bash sed awk grep cat date mktemp rm mkdir cd curl jq base64 stat printf tr head tail cut sort wc dirname basename command env; do
  src="$(command -v "$b" 2>/dev/null)" && ln -sf "$src" "$FAKE_BIN/$b" 2>/dev/null
done
out="$(PATH="$FAKE_BIN" env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --prompt "x" --quality high --target-aspect 16:9 --out-dir "$OUT_DIR" 2>&1)"
code=$?
if [ "$code" -eq 2 ]; then
  pass "--target-aspect without ffmpeg is an environment error (exit 2), same class as missing curl/jq"
else
  fail "expected exit 2 without ffmpeg" "got $code: $(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -qi 'brew install ffmpeg'; then
  pass "the failure says what to install"
else
  fail "the failure should name the install command" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -qi 'drop --target-aspect'; then
  pass "the failure also names the way out — the rest of the script still works without ffmpeg"
else
  fail "the failure should say the flag can be dropped" "$(printf '%s' "$out" | head -4 | tr '\n' ' ')"
fi
# ...and without the flag, a missing ffmpeg must change nothing at all.
out="$(PATH="$FAKE_BIN" env -u OFOX_API_KEY bash "$TARGET" generate --dry-run \
  --prompt "x" --quality high --out-dir "$OUT_DIR" 2>&1)"
code=$?
if [ "$code" -eq 0 ]; then
  pass "without a target flag, a missing ffmpeg does not affect anything (pricing still works)"
else
  fail "ffmpeg must not become a hard dependency of ordinary runs" \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== SKILL.md documents the one fact that explains every size surprise ==="
# The ratio table is the load-bearing doc here: without "16:9 cannot be
# requested" written down, the next reader treats the crop as a workaround for
# a model bug and looks for a flag that removes it.
if grep -q '1\.7778' "$SKILL_MD" && grep -q '1\.7500\|1\.75' "$SKILL_MD"; then
  pass "SKILL.md states both the reachable ratio and the real 16:9 it misses"
else
  fail "SKILL.md must carry the ratio table (1.7500 vs 1.7778)" "not found"
fi
if grep -qi 'target-aspect' "$SKILL_MD"; then
  pass "SKILL.md documents --target-aspect"
else
  fail "SKILL.md does not mention --target-aspect" "not found"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
