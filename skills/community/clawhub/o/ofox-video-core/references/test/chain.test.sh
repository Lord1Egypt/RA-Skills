#!/usr/bin/env bash
# chain.test.sh — multi-shot chaining for ofox-video.sh.
#
# Free by construction: the API base points at an unroutable address, so no
# case can create a billable job. What this covers is everything that has to
# be right before money is spent — argument handling, the estimate, stop-on-
# failure — plus the frame-extraction step verified against a real local clip.
#
# Run: bash references/test/chain.test.sh

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

run_chain() { bash "$TARGET" chain "$@" 2>&1; }

echo "=== Argument handling, before any network call ==="
out=$(run_chain --duration 5)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'shot'; then
  pass "chain with no shots is rejected"
else
  fail "chain needs at least one shot" "$(printf '%s' "$out" | head -1)"
fi

out=$(run_chain --shot "a" --shots-file "$WORK/nope.txt" --duration 5)
if [ $? -eq 1 ]; then
  pass "a missing --shots-file is reported"
else
  fail "missing shots file should exit 1" "$(printf '%s' "$out" | head -1)"
fi

printf 'first shot\nsecond shot\nthird shot\n' > "$WORK/shots.txt"
out=$(run_chain --shots-file "$WORK/shots.txt" --duration 5)
if printf '%s' "$out" | grep -qi '3 shots\|shot 1/3'; then
  pass "--shots-file is read, one prompt per line"
else
  fail "--shots-file should yield 3 shots" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

# Blank lines and comments shouldn't become shots.
printf 'one\n\n# a comment\ntwo\n' > "$WORK/shots2.txt"
out=$(run_chain --shots-file "$WORK/shots2.txt" --duration 5)
if printf '%s' "$out" | grep -qi '2 shots\|shot 1/2'; then
  pass "blank lines and # comments are skipped in a shots file"
else
  fail "shots file should yield 2 shots" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== A templated prompt in a shots file is refused, not billed line by line ==="
# The defect this guards: references/prompt-structure.md teaches multi-line
# templated prompts, --shots-file is one prompt per LINE, and nothing connected
# the two. A 5-line prompt became 5 full-length jobs with a plausible estimate.
printf 'STYLE: 35mm film texture, warm grade\nSUBJECT: a red ceramic mug on a light table\nCAMERA: locked, breathing sway\nSOUND: room tone, no music\nAVOID: subtitles, on-screen text, watermarks\n' > "$WORK/template.txt"
out=$(run_chain --shots-file "$WORK/template.txt" --duration 29 --resolution 720p)
code=$?
if [ "$code" -ne 0 ]; then
  pass "a shots file of template labels is rejected (exit $code)"
else
  fail "a templated shots file must be refused" "exit 0: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q 'line 1' && printf '%s' "$out" | grep -q 'STYLE: 35mm film texture'; then
  pass "the refusal names the offending line and quotes it"
else
  fail "the refusal must name the offending line" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q -- '--shot'; then
  pass "the refusal names the way out (one --shot per prompt)"
else
  fail "the refusal must give a way out" "$(printf '%s' "$out" | tr '\n' ' ')"
fi
if ! printf '%s' "$out" | grep -qi 'submitting job'; then
  pass "nothing was submitted when the shots-file guard fired"
else
  fail "must not submit when the shots-file guard fires" "output mentions submitting"
fi
# It has to beat the estimate too: a plausible-looking price is most of how
# this defect survived review.
if ! printf '%s' "$out" | grep -qi 'estimated cost'; then
  pass "the guard fires before any cost estimate is printed"
else
  fail "the guard must precede the estimate" "$(printf '%s' "$out" | grep -i 'estimated cost' | head -1)"
fi
# One bad line in an otherwise fine file is still a refusal — that line would
# have been billed as a job.
printf 'a white cup on a dark table, steam rising\nAVOID: subtitles, watermarks\n' > "$WORK/mixed.txt"
out=$(run_chain --shots-file "$WORK/mixed.txt" --duration 4 --resolution 480p)
if [ $? -ne 0 ] && printf '%s' "$out" | grep -q 'line 2'; then
  pass "a single template line in an otherwise valid file is caught"
else
  fail "one label line should still refuse" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

# The guard must not swallow real prompts. A numbered shot heading, a
# lowercase label and a mid-sentence colon are all legitimate one-line shots.
printf 'SHOT 1: a cup on a table, static camera\nfoo: the camera pushes in\nthe cup, seen from above: steam rising\n' > "$WORK/notatemplate.txt"
out=$(run_chain --shots-file "$WORK/notatemplate.txt" --duration 4 --resolution 480p --dry-run)
if printf '%s' "$out" | grep -qi '3 shots'; then
  pass "numbered, lowercase and mid-sentence colons are not treated as labels"
else
  fail "the guard is over-eager" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

# A repeated --shot is the documented way out, so it must actually take a
# multi-line value as ONE prompt.
out=$(run_chain --shot "STYLE: 35mm film texture
SUBJECT: a red ceramic mug
AVOID: subtitles" --duration 4 --resolution 480p --dry-run)
if printf '%s' "$out" | grep -qi 'chaining 1 shots' && printf '%s' "$out" | grep -q 'SHOTS_REQUESTED 1'; then
  pass "a multi-line --shot stays one prompt, one job"
else
  fail "--shot must accept a multi-line prompt whole" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== Argument handling, continued ==="
out=$(run_chain --shot "a" --shot "b" --duration 99)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'duration'; then
  pass "a bad parameter fails the chain before shot 1 is submitted"
else
  fail "bad params should fail up front" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== The whole sequence is priced before anything is spent ==="
out=$(run_chain --shot "a" --shot "b" --shot "c" --duration 4 --resolution 480p)
amount=$(printf '%s' "$out" | sed -n 's/.*Estimated cost: ~\$\([0-9.]*\).*/\1/p' | head -1)
expect=$(awk 'BEGIN{printf "%.2f", 3*4*0.11}')
if [ "$amount" = "$expect" ]; then
  pass "estimate covers all 3 shots (\$$amount at the i2v/t2v rate)"
else
  fail "3-shot estimate should be \$$expect" "got '\$$amount'"
fi

echo
echo "=== A failed shot stops the run ==="
# --approved because this case has to reach the submit attempt; the base is
# unroutable, so the attempt fails without spending.
out=$(run_chain --shot "a" --shot "b" --shot "c" --duration 5 --out-dir "$WORK/out" --approved)
submits=$(printf '%s' "$out" | grep -ci 'submitting job' || true)
if [ "$submits" -eq 1 ]; then
  pass "shot 1 failing stopped the run (1 submit attempt, not 3)"
else
  fail "a failed shot must stop the chain" "saw $submits submit attempts"
fi
if printf '%s' "$out" | grep -qi 'stopping\|stopped'; then
  pass "the early stop is stated plainly"
else
  fail "an early stop must not be silent" "$(printf '%s' "$out" | tail -2 | tr '\n' ' ')"
fi

echo
echo "=== Framing rules are explained, not left to surprise ==="
out=$(run_chain --shot "a" --shot "b" --duration 5 --aspect-ratio 9:16)
if printf '%s' "$out" | grep -qi 'adaptive\|first shot\|inherit'; then
  pass "the run explains that shots 2+ inherit framing from the fed frame"
else
  fail "aspect-ratio behavior across shots should be stated" \
    "$(printf '%s' "$out" | head -4 | tr '\n' ' ')"
fi

echo
echo "=== Frame extraction, verified against a real clip ==="
if command -v ffmpeg >/dev/null 2>&1; then
  mkdir -p "$WORK/vids"
  # A 2s clip whose content changes over time, so a near-final frame is
  # visibly different from the first — that is what makes the check meaningful.
  ffmpeg -nostdin -loglevel error -f lavfi -i "testsrc=size=160x90:rate=10:duration=2" \
    -pix_fmt yuv420p -y "$WORK/vids/clip.mp4" 2>/dev/null

  if [ -s "$WORK/vids/clip.mp4" ]; then
    out=$(bash "$TARGET" last-frame "$WORK/vids/clip.mp4" 2>&1)
    frame=$(printf '%s' "$out" | sed -n 's/^LAST_FRAME //p')
    if [ -n "$frame" ] && [ -s "$frame" ]; then
      pass "last-frame extracts an image from a real clip"
    else
      fail "last-frame should produce an image" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    fi
    case "$frame" in
      /*) pass "the extracted frame path is absolute" ;;
      *) fail "frame path must be absolute" "got '$frame'" ;;
    esac
    # It must be a real image, not a zero-byte file with a .png name.
    if [ -n "$frame" ] && ffprobe -v error -select_streams v -show_entries stream=width,height \
      -of csv=p=0 "$frame" 2>/dev/null | grep -q '160,90'; then
      pass "the extracted frame is a valid 160x90 image"
    else
      fail "the frame should be a valid image matching the clip" "ffprobe said no"
    fi
    # Near-final, not first: testsrc's counter differs, so the bytes must too.
    ffmpeg -nostdin -loglevel error -i "$WORK/vids/clip.mp4" -frames:v 1 \
      -y "$WORK/vids/first.png" 2>/dev/null
    if [ -n "$frame" ] && ! cmp -s "$frame" "$WORK/vids/first.png"; then
      pass "the extracted frame is from the end, not the start"
    else
      fail "last-frame must not return the opening frame" "bytes matched frame 1"
    fi
    # How far before the end, exactly. SKILL.md states 0.1s, and a number in a
    # doc that nothing checks is the kind that drifts. This clip is 2.000s at
    # 10fps, so duration-0.1 lands on the frame at 1.9s.
    ffmpeg -nostdin -loglevel error -ss 1.9 -i "$WORK/vids/clip.mp4" -frames:v 1 \
      -y "$WORK/vids/at1.9.png" 2>/dev/null
    if [ -n "$frame" ] && cmp -s "$frame" "$WORK/vids/at1.9.png"; then
      pass "last-frame steps back 0.1s from the ffprobe duration, as documented"
    else
      fail "last-frame's step-back should be 0.1s" "frame did not match t=1.9s of a 2.000s clip"
    fi
    # And it is not the 0.5s fallback window, which only runs when the seek
    # above yields nothing.
    ffmpeg -nostdin -loglevel error -ss 1.5 -i "$WORK/vids/clip.mp4" -frames:v 1 \
      -y "$WORK/vids/at1.5.png" 2>/dev/null
    if [ -n "$frame" ] && ! cmp -s "$frame" "$WORK/vids/at1.5.png"; then
      pass "the 0.5s fallback window is not the normal path"
    else
      fail "last-frame took the fallback on a clip with a readable duration" "matched t=1.5s"
    fi
  else
    printf 'skip  ffmpeg could not synthesize a test clip\n'
  fi

  out=$(bash "$TARGET" last-frame "$WORK/does-not-exist.mp4" 2>&1)
  if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'cannot read'; then
    pass "last-frame reports an unreadable input"
  else
    fail "unreadable input should be reported" "$(printf '%s' "$out" | head -1)"
  fi
else
  printf 'skip  ffmpeg not installed — frame extraction not exercised\n'
fi

echo
echo "=== Chaining needs ffmpeg and says so up front ==="
FAKE_BIN="$WORK/nobin"
mkdir -p "$FAKE_BIN"
for b in bash curl jq mktemp date stat cat rm mv cp mkdir sed grep awk head tail tr printf env cut sort find column dirname basename pwd wc cmp; do
  src="$(command -v "$b" 2>/dev/null)" && ln -sf "$src" "$FAKE_BIN/$b" 2>/dev/null
done
out=$(PATH="$FAKE_BIN" bash "$TARGET" chain --shot "a" --shot "b" --duration 5 2>&1)
code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'ffmpeg'; then
  pass "chain without ffmpeg fails early with a clear reason, before spending"
else
  fail "chain must require ffmpeg up front" "exit $code: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if ! printf '%s' "$out" | grep -qi 'submitting job'; then
  pass "nothing was submitted when the ffmpeg check failed"
else
  fail "must not submit before the ffmpeg check" "output mentions submitting"
fi

echo
echo "=== Usage advertises the new surface ==="
out=$(bash "$TARGET" 2>&1)
for word in chain last-frame; do
  if printf '%s' "$out" | grep -q -- "$word"; then
    pass "usage mentions $word"
  else
    fail "usage should mention $word" "$(printf '%s' "$out" | head -10 | tr '\n' ' ')"
  fi
done

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
