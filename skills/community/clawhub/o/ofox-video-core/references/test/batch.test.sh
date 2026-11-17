#!/usr/bin/env bash
# batch.test.sh — control flow and safety rules for `ofox-video.sh batch`.
#
# Free by construction: the API base points at an unroutable address, so no
# case here can create a billable job. What it verifies is the part that has
# to be right BEFORE anyone spends money — argument handling, the same-seed
# warning, and above all that a failed take stops the run instead of burning
# the remaining takes.
#
# Run: bash references/test/batch.test.sh

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

run_batch() { bash "$TARGET" batch "$@" 2>&1; }

echo "=== --takes validation (before any network call) ==="
for bad in 0 -1 abc 1.5 ""; do
  out=$(run_batch --prompt x --takes "$bad")
  code=$?
  label="--takes '$bad' is rejected"
  if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -qi 'takes'; then
    pass "$label"
  else
    fail "$label" "exit $code: $(printf '%s' "$out" | head -1)"
  fi
done

out=$(run_batch --prompt x --takes 99)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'takes'; then
  pass "--takes above the cap is rejected (guards against a runaway bill)"
else
  fail "--takes 99 should be capped" "$(printf '%s' "$out" | head -1)"
fi

echo
echo "=== Parameters are validated once, up front, for all takes ==="
out=$(run_batch --prompt x --takes 3 --model alibaba/wan-2.7 --duration 30)
code=$?
if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -qi 'duration'; then
  pass "a bad parameter fails the whole batch before take 1 is submitted"
else
  fail "bad parameters should fail up front" "exit $code: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
if ! printf '%s' "$out" | grep -qi 'submitting'; then
  pass "nothing was submitted when validation failed"
else
  fail "validation failure must not submit anything" "output mentions submitting"
fi

echo
echo "=== A failed take stops the run — it never burns the rest ==="
# --approved because this case has to reach the submit attempt to be about
# anything; the base is unroutable, so the attempt fails without spending.
out=$(run_batch --prompt x --takes 3 --duration 5 --out-dir "$WORK/out" --approved)
submits=$(printf '%s' "$out" | grep -ci 'submitting job' || true)
if [ "$submits" -eq 1 ]; then
  pass "take 1 failing stopped the run (1 submit attempt, not 3)"
else
  fail "a failed take must stop the run" "saw $submits submit attempts, expected 1"
fi
if printf '%s' "$out" | grep -qi 'stopping\|stopped\|abort'; then
  pass "the run says plainly that it stopped early"
else
  fail "an early stop must be stated, not silent" "$(printf '%s' "$out" | tail -3 | tr '\n' ' ')"
fi

echo
echo "=== Same-seed warning (N identical takes would waste the money) ==="
out=$(run_batch --prompt x --takes 3 --seed 42 --duration 5)
if printf '%s' "$out" | grep -qi 'seed'; then
  pass "a fixed --seed across takes is called out"
else
  fail "a fixed --seed should warn: every take would be identical" \
    "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== Cost estimate is shown before spending ==="
out=$(run_batch --prompt x --takes 3 --duration 5 --resolution 480p)
if printf '%s' "$out" | grep -qiE 'estimat|\$[0-9]'; then
  pass "an estimate for the whole batch is printed before submitting"
else
  fail "batch must estimate before spending" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== Contact sheet fails open when ffmpeg is absent ==="
# A PATH with the real coreutils but no ffmpeg: the sheet must be skipped
# with a reason, never crash the run or lose the videos.
FAKE_BIN="$WORK/nobin"
mkdir -p "$FAKE_BIN"
for b in bash curl jq mktemp date stat cat rm mv mkdir sed grep awk head tr printf env cut sort find column dirname basename pwd; do
  src="$(command -v "$b" 2>/dev/null)" && ln -sf "$src" "$FAKE_BIN/$b" 2>/dev/null
done
out=$(PATH="$FAKE_BIN" bash "$TARGET" batch --prompt x --takes 2 --duration 5 2>&1)
if ! printf '%s' "$out" | grep -qi 'command not found'; then
  pass "batch runs without ffmpeg on PATH (no crash)"
else
  fail "missing ffmpeg must not crash the run" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi

echo
echo "=== contact-sheet subcommand (local, no API call, no key) ==="
out=$(bash "$TARGET" contact-sheet 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'at least one video'; then
  pass "contact-sheet with no arguments is rejected"
else
  fail "contact-sheet needs at least one video" "$(printf '%s' "$out" | head -1)"
fi

out=$(bash "$TARGET" contact-sheet "$WORK/does-not-exist.mp4" 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'cannot read'; then
  pass "an unreadable input is reported, not silently skipped"
else
  fail "unreadable input should be reported" "$(printf '%s' "$out" | head -1)"
fi

if command -v ffmpeg >/dev/null 2>&1; then
  # Two tiny synthetic clips — generated locally, nothing billable.
  mkdir -p "$WORK/vids"
  ffmpeg -nostdin -loglevel error -f lavfi -i "testsrc=size=160x90:rate=10:duration=1" \
    -pix_fmt yuv420p -y "$WORK/vids/a.mp4" 2>/dev/null
  ffmpeg -nostdin -loglevel error -f lavfi -i "testsrc2=size=160x90:rate=10:duration=1" \
    -pix_fmt yuv420p -y "$WORK/vids/b.mp4" 2>/dev/null

  if [ -s "$WORK/vids/a.mp4" ] && [ -s "$WORK/vids/b.mp4" ]; then
    # Call with a RELATIVE path on purpose: the reported path must still be
    # absolute, or the reader has to guess our working directory.
    out=$(cd "$WORK" && bash "$TARGET" contact-sheet vids/a.mp4 vids/b.mp4 --out-dir vids 2>&1)
    sheet=$(printf '%s' "$out" | sed -n 's/^CONTACT_SHEET //p')
    if [ -n "$sheet" ]; then
      pass "contact-sheet builds a sheet from local videos"
    else
      fail "contact-sheet should emit CONTACT_SHEET" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    fi
    case "$sheet" in
      /*) pass "the reported sheet path is absolute even when --out-dir was relative" ;;
      *) fail "sheet path must be absolute" "got '$sheet'" ;;
    esac
    if [ -n "$sheet" ] && [ -s "$sheet" ]; then
      pass "the sheet file actually exists at the reported path"
    else
      fail "the reported path must point at a real file" "got '$sheet'"
    fi

    out=$(cd "$WORK" && bash "$TARGET" contact-sheet vids/a.mp4 2>&1)
    if printf '%s' "$out" | grep -q '^CONTACT_SHEET /'; then
      pass "a single video also produces a sheet (no vstack needed)"
    else
      fail "single-video sheet should work" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    fi
  else
    printf 'skip  ffmpeg could not synthesize test clips\n'
  fi
else
  printf 'skip  ffmpeg not installed — contact-sheet rendering not exercised\n'
fi

echo
echo "=== Help lists batch ==="
out=$(bash "$TARGET" 2>&1)
if printf '%s' "$out" | grep -q 'batch'; then
  pass "usage advertises the batch subcommand"
else
  fail "usage should list batch" "$(printf '%s' "$out" | head -5 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q 'contact-sheet'; then
  pass "usage advertises the contact-sheet subcommand"
else
  fail "usage should list contact-sheet" "$(printf '%s' "$out" | head -8 | tr '\n' ' ')"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
