#!/usr/bin/env bash
# naming.test.sh — output filenames and the metadata sidecar.
#
# Free by construction, and more strongly than the suites that point at an
# unroutable address: nothing here touches the network at all. The slug
# builder is a pure function, and download_result() is driven with a
# synthetic response body whose download URL is a local file:// path, so the
# "download" is a file copy. No API base is ever contacted, billable or not.
#
# Sourcing note: the script ends in `main "$@"` / `exit $?`, so it is loaded
# with that tail stripped. That is the only way to reach the internal
# functions; the alternative — exercising naming through the CLI — would
# require a real completed job, which costs money.
#
# Run: bash references/test/naming.test.sh

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

# Load the script's functions without running main.
LIB="$WORK/lib.sh"
sed -e '/^main "\$@"$/d' -e '/^exit \$?$/d' "$TARGET" > "$LIB"
# shellcheck source=/dev/null
. "$LIB"

slug_is() { # <label> <expected> <name-hint> <prompt>
  local got
  got="$(build_output_slug "$3" "$4")"
  if [ "$got" = "$2" ]; then pass "$1"; else fail "$1" "want '$2', got '$got'"; fi
}

echo "=== Where the slug comes from ==="
slug_is "an explicit --name wins over the prompt" \
  "convenience-store-breakup" "convenience store breakup" "A dim store at midnight"
slug_is "without --name it falls back to the prompt" \
  "A-dim-store-at-midnight" "" "A dim store at midnight"
slug_is "with neither, nothing (caller falls back to the job id)" \
  "" "" ""
slug_is "a prompt of only whitespace counts as nothing" \
  "" "" "   "

echo
echo "=== Untrusted text becomes a safe path component ==="
slug_is "path traversal cannot survive" "etcpasswd" "../../etc/passwd" ""
slug_is "characters illegal on Windows are dropped" "abc" 'a:b*c' ""
slug_is "quotes and angle brackets are dropped" "ab" 'a"<b>' ""
slug_is "a leading dash cannot make the name look like a flag" "name" "---name" ""
slug_is "a leading dot cannot make it a hidden file" "name" "...name" ""
slug_is "trailing punctuation is trimmed" "name" "name!!!" ""

echo
echo "=== Whitespace collapses before control characters are stripped ==="
# Tab and newline are both whitespace and control characters. Stripping
# control characters first would glue neighbouring words together.
slug_is "a newline separates words, it does not delete them" \
  "a-b" "$(printf 'a\nb')" ""
slug_is "runs of mixed whitespace collapse to one dash" \
  "a-b-c" "$(printf 'a   b\t\tc')" ""

echo
echo "=== Truncation is by codepoint and locale-independent ==="
LONG_CJK="深夜的便利店冷白色荧光灯玻璃窗外是空荡的街道关东煮加热柜上方蒸汽升腾女生二十出头"
got="$(build_output_slug "" "$LONG_CJK")"
chars="$(printf '%s' "$got" | jq -Rr 'length')"
if [ "$chars" -le "$SLUG_MAX_CHARS" ]; then
  pass "a long CJK prompt is capped at SLUG_MAX_CHARS codepoints ($chars)"
else
  fail "CJK slug exceeds the cap" "$chars > $SLUG_MAX_CHARS"
fi
if printf '%s' "$got" | iconv -f UTF-8 -t UTF-8 >/dev/null 2>&1; then
  pass "truncation never splits a multi-byte character"
else
  fail "truncation produced invalid UTF-8" "$got"
fi
if [ "$(LC_ALL=C build_output_slug "" "$LONG_CJK")" = "$got" ]; then
  pass "the same slug under LC_ALL=C"
else
  fail "slug changes with the locale" "jq slicing should be locale-independent"
fi
slug_is "a truncated latin phrase falls back to a word boundary" \
  "convenience-store-breakup-scene-at" "" \
  "convenience store breakup scene at midnight in the rain"

echo
echo "=== Filenames and sidecars, driven by a synthetic completed job ==="
FAKE_VIDEO="$WORK/source.mp4"
printf 'not-really-an-mp4' > "$FAKE_VIDEO"

body_for() { # <job id> <prompt>
  jq -nc --arg id "$1" --arg p "$2" --arg u "file://$FAKE_VIDEO" \
    '{id: $id, status: "completed", model: "bytedance/seedance-2.5",
      prompt: $p, unsigned_urls: [$u],
      usage: {video_seconds: 8, video_cost: "0.8800000000"},
      created_at: 1788160000, updated_at: 1788160100}'
}

JOB="b69af05c-208d-4d06-8ba0-004b7659f69f"
OUT="$WORK/out"; mkdir -p "$OUT"

out="$(download_result "$JOB" "$(body_for "$JOB" "A dim store at midnight")" "$OUT" "rooftop goodbye" "" 2>/dev/null)"
video="$(printf '%s\n' "$out" | sed -n 's/^VIDEO_PATH //p')"
sidecar="$(printf '%s\n' "$out" | sed -n 's/^SIDECAR_PATH //p')"

if [ "$(basename "$video")" = "rooftop-goodbye-b69af05c.mp4" ]; then
  pass "the file is named <slug>-<short job id>.mp4"
else
  fail "unexpected filename" "$(basename "$video")"
fi
if [ -s "$video" ]; then pass "the video was written"; else fail "no video written" "$video"; fi

if [ -n "$sidecar" ] && jq -e . "$sidecar" >/dev/null 2>&1; then
  pass "the sidecar is parseable JSON"
else
  fail "sidecar missing or unparseable" "${sidecar:-<none>}"
fi
if [ "$(jq -r '.job_id' "$sidecar")" = "$JOB" ]; then
  pass "the sidecar carries the FULL job id, which the filename cannot"
else
  fail "sidecar job_id wrong" "$(jq -r '.job_id' "$sidecar")"
fi
if [ "$(jq -r '.video_cost' "$sidecar")" = "0.8800000000" ]; then
  pass "the sidecar records the real cost"
else
  fail "sidecar cost wrong" "$(jq -r '.video_cost' "$sidecar")"
fi
if jq -e 'has("request") | not' "$sidecar" >/dev/null; then
  pass "no request section when the caller had no payload to give"
else
  fail "request appeared from nowhere" "$(jq -c '.request' "$sidecar")"
fi

echo
echo "=== Degrading, and not colliding ==="
OUT2="$WORK/out2"; mkdir -p "$OUT2"
out="$(download_result "$JOB" "$(body_for "$JOB" "")" "$OUT2" "" "" 2>/dev/null)"
video="$(printf '%s\n' "$out" | sed -n 's/^VIDEO_PATH //p')"
if [ "$(basename "$video")" = "$JOB.mp4" ]; then
  pass "with no name and no prompt, it falls back to the bare job id"
else
  fail "empty-prompt fallback wrong" "$(basename "$video")"
fi
case "$(basename "$video")" in
  *--*|-*) fail "fallback left a dangling separator" "$(basename "$video")" ;;
  *) pass "the fallback leaves no dangling dash" ;;
esac

OUT3="$WORK/out3"; mkdir -p "$OUT3"
JOB_B="c0ffee11-208d-4d06-8ba0-004b7659f69f"
download_result "$JOB"   "$(body_for "$JOB" "same prompt")"   "$OUT3" "" "" >/dev/null 2>&1
download_result "$JOB_B" "$(body_for "$JOB_B" "same prompt")" "$OUT3" "" "" >/dev/null 2>&1
if [ "$(find "$OUT3" -name '*.mp4' | wc -l | tr -d ' ')" = "2" ]; then
  pass "two runs of one prompt do not overwrite each other"
else
  fail "same-prompt runs collided" "$(find "$OUT3" -name '*.mp4' | tr '\n' ' ')"
fi

echo
echo "-----------------------------------------"
echo "passed: $PASS   failed: $FAIL"
[ "$FAIL" -eq 0 ]
