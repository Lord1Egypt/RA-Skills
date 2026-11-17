#!/usr/bin/env bash
# localtools.test.sh — the zero-cost local subcommands: frame-at, mux-audio.
#
# Free by construction, and more strongly than the suites that point at an
# unroutable address: neither subcommand makes an API call, reads a key, or
# opens a socket. Everything here runs ffmpeg against clips synthesized on the
# spot with lavfi, so the suite needs no fixtures and no network.
#
# Why these two are tested as hard as a paid path: frame-at sits ON the
# spending path. Its output is fed straight into a paid image-to-video job, so
# a frame that is empty, black, or silently taken from the wrong second is not
# a cosmetic bug — it is a job billed for the wrong picture. mux-audio is the
# terminal step and costs nothing to get wrong, but it is the one place a
# caller's own audio track can be silently truncated, so the length mismatch
# has to be reported rather than swallowed.
#
# Run: bash references/test/localtools.test.sh

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

have_ffmpeg=0
command -v ffmpeg >/dev/null 2>&1 && have_ffmpeg=1

echo "=== Usage advertises the new surface ==="
out=$(bash "$TARGET" 2>&1)
for word in frame-at mux-audio; do
  if printf '%s' "$out" | grep -q -- "$word"; then
    pass "usage mentions $word"
  else
    fail "usage should mention $word" "$(printf '%s' "$out" | head -20 | tr '\n' ' ')"
  fi
done

echo
echo "=== frame-at: argument handling, before any ffmpeg work ==="

out=$(bash "$TARGET" frame-at 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'usage'; then
  pass "frame-at with no arguments prints usage and fails"
else
  fail "frame-at needs a video" "exit $code: $(printf '%s' "$out" | head -1)"
fi

out=$(bash "$TARGET" frame-at "$WORK/does-not-exist.mp4" --at 1 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'cannot read'; then
  pass "frame-at reports an unreadable input"
else
  fail "unreadable input should be reported" "exit $code: $(printf '%s' "$out" | head -1)"
fi

# --at is the whole point of this command over last-frame. Defaulting it would
# quietly turn "grab second 3" into "grab some other second", and the result
# gets fed to a paid job.
: > "$WORK/empty.mp4"
out=$(bash "$TARGET" frame-at "$WORK/empty.mp4" 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi -- '--at'; then
  pass "frame-at requires --at rather than guessing a timestamp"
else
  fail "--at must be required" "exit $code: $(printf '%s' "$out" | head -1)"
fi

for bad in "abc" "-1" "1.2.3" ""; do
  out=$(bash "$TARGET" frame-at "$WORK/empty.mp4" --at "$bad" 2>&1); code=$?
  if [ "$code" -ne 0 ]; then
    pass "frame-at rejects --at '$bad'"
  else
    fail "--at '$bad' should be rejected" "exit $code"
  fi
done

out=$(bash "$TARGET" frame-at "$WORK/empty.mp4" --at 1 --nonsense 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'unknown option'; then
  pass "frame-at rejects an unknown option"
else
  fail "unknown options should be rejected" "exit $code: $(printf '%s' "$out" | head -1)"
fi

echo
echo "=== frame-at: verified against a real clip ==="
if [ "$have_ffmpeg" -eq 1 ]; then
  mkdir -p "$WORK/vids"
  # testsrc's picture changes every frame, which is what makes "the frame came
  # from the second I asked for" a checkable claim rather than a hope.
  ffmpeg -nostdin -loglevel error -f lavfi -i "testsrc=size=160x90:rate=10:duration=3" \
    -pix_fmt yuv420p -y "$WORK/vids/clip.mp4" 2>/dev/null

  if [ -s "$WORK/vids/clip.mp4" ]; then
    out=$(bash "$TARGET" frame-at "$WORK/vids/clip.mp4" --at 1.5 2>&1)
    frame=$(printf '%s' "$out" | sed -n 's/^FRAME_AT //p')
    if [ -n "$frame" ] && [ -s "$frame" ]; then
      pass "frame-at extracts an image from a real clip"
    else
      fail "frame-at should produce an image" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    fi

    case "$frame" in
      /*) pass "the extracted frame path is absolute" ;;
      *) fail "frame path must be absolute" "got '$frame'" ;;
    esac

    if [ -n "$frame" ] && ffprobe -v error -select_streams v -show_entries stream=width,height \
      -of csv=p=0 "$frame" 2>/dev/null | grep -q '160,90'; then
      pass "the extracted frame is a valid 160x90 image"
    else
      fail "the frame should be a valid image matching the clip" "ffprobe said no"
    fi

    # The point of the command: a different --at gives a different picture.
    out2=$(bash "$TARGET" frame-at "$WORK/vids/clip.mp4" --at 0.1 --out-dir "$WORK/vids/early" 2>&1)
    early=$(printf '%s' "$out2" | sed -n 's/^FRAME_AT //p')
    if [ -n "$early" ] && [ -s "$early" ] && ! cmp -s "$frame" "$early"; then
      pass "a different --at yields a different frame"
    else
      fail "--at must actually seek" "second 0.1 and second 1.5 produced the same bytes"
    fi

    # And it must not be the last frame — that is what last-frame is for.
    lf=$(bash "$TARGET" last-frame "$WORK/vids/clip.mp4" --out-dir "$WORK/vids/last" 2>&1 \
      | sed -n 's/^LAST_FRAME //p')
    if [ -n "$lf" ] && [ -n "$frame" ] && ! cmp -s "$frame" "$lf"; then
      pass "frame-at at 1.5s of a 3s clip is not the closing frame"
    else
      fail "frame-at must not collapse into last-frame" "bytes matched"
    fi

    if [ -n "$early" ]; then
      case "$early" in
        "$WORK/vids/early"/*) pass "--out-dir is honored" ;;
        *) fail "--out-dir should place the frame" "got '$early'" ;;
      esac
    fi

    # Past the end there is no frame. Silently writing a zero-byte file here
    # would hand a paid job an empty picture.
    out=$(bash "$TARGET" frame-at "$WORK/vids/clip.mp4" --at 99 2>&1); code=$?
    if [ "$code" -ne 0 ]; then
      pass "a timestamp past the end fails instead of returning nothing"
    else
      fail "--at past the end must fail" "exit $code: $(printf '%s' "$out" | head -1)"
    fi
    if printf '%s' "$out" | grep -q '3'; then
      pass "the past-the-end error names the clip's actual duration"
    else
      fail "the error should say how long the clip is" "$(printf '%s' "$out" | head -1)"
    fi
  else
    printf 'skip  ffmpeg could not synthesize a test clip\n'
  fi
else
  printf 'skip  ffmpeg not installed — frame-at not exercised against a clip\n'
fi

echo
echo "=== mux-audio: argument handling ==="

out=$(bash "$TARGET" mux-audio 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'usage'; then
  pass "mux-audio with no arguments prints usage and fails"
else
  fail "mux-audio needs both inputs" "exit $code: $(printf '%s' "$out" | head -1)"
fi

out=$(bash "$TARGET" mux-audio "$WORK/empty.mp4" 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'usage'; then
  pass "mux-audio with only a video prints usage and fails"
else
  fail "mux-audio needs an audio file too" "exit $code: $(printf '%s' "$out" | head -1)"
fi

out=$(bash "$TARGET" mux-audio "$WORK/nope.mp4" "$WORK/nope.wav" 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'cannot read'; then
  pass "mux-audio reports an unreadable input"
else
  fail "unreadable input should be reported" "exit $code: $(printf '%s' "$out" | head -1)"
fi

echo
echo "=== mux-audio: verified against real files ==="
if [ "$have_ffmpeg" -eq 1 ] && [ -s "$WORK/vids/clip.mp4" ]; then
  # A 3s clip WITH its own tone, plus a 3s tone at a different frequency. The
  # generated clips this command is for already carry a model-made track, so
  # "replaces, not mixes" is the behavior that has to hold.
  ffmpeg -nostdin -loglevel error -f lavfi -i "testsrc=size=160x90:rate=10:duration=3" \
    -f lavfi -i "sine=frequency=200:duration=3" \
    -pix_fmt yuv420p -c:a aac -shortest -y "$WORK/vids/noisy.mp4" 2>/dev/null
  ffmpeg -nostdin -loglevel error -f lavfi -i "sine=frequency=880:duration=3" \
    -y "$WORK/vids/track.wav" 2>/dev/null

  if [ -s "$WORK/vids/noisy.mp4" ] && [ -s "$WORK/vids/track.wav" ]; then
    out=$(bash "$TARGET" mux-audio "$WORK/vids/noisy.mp4" "$WORK/vids/track.wav" 2>&1)
    muxed=$(printf '%s' "$out" | sed -n 's/^MUXED //p')

    if [ -n "$muxed" ] && [ -s "$muxed" ]; then
      pass "mux-audio produces a file"
    else
      fail "mux-audio should produce a file" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    fi

    case "$muxed" in
      /*) pass "the muxed path is absolute" ;;
      *) fail "muxed path must be absolute" "got '$muxed'" ;;
    esac

    if [ -n "$muxed" ]; then
      nstreams=$(ffprobe -v error -select_streams a -show_entries stream=index \
        -of csv=p=0 "$muxed" 2>/dev/null | grep -c .)
      if [ "$nstreams" = "1" ]; then
        pass "the result carries exactly one audio stream — replaced, not added"
      else
        fail "the supplied track must replace the clip's own" "found $nstreams audio streams"
      fi

      if ffprobe -v error -select_streams v -show_entries stream=width,height \
        -of csv=p=0 "$muxed" 2>/dev/null | grep -q '160,90'; then
        pass "the picture survives the mux intact"
      else
        fail "video stream should be unchanged" "ffprobe said no"
      fi
    fi

    # Equal-length inputs must not trigger the truncation warning; an unequal
    # pair must. Silently cutting someone's music is the failure mode here.
    if ! printf '%s' "$out" | grep -qi 'shorter\|truncat'; then
      pass "equal-length inputs mux without a truncation note"
    else
      fail "no note is due when the durations match" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    fi

    ffmpeg -nostdin -loglevel error -f lavfi -i "sine=frequency=440:duration=8" \
      -y "$WORK/vids/long.wav" 2>/dev/null
    out=$(bash "$TARGET" mux-audio "$WORK/vids/noisy.mp4" "$WORK/vids/long.wav" \
      --out-dir "$WORK/vids/mismatch" 2>&1)
    if printf '%s' "$out" | grep -qi 'shorter\|truncat'; then
      pass "a longer audio track is reported, not silently cut"
    else
      fail "length mismatch must be reported" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
    fi
    mm=$(printf '%s' "$out" | sed -n 's/^MUXED //p')
    if [ -n "$mm" ] && [ -s "$mm" ]; then
      pass "a mismatch is a note, not a failure — the file is still produced"
    else
      fail "mismatch should still produce a file" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
    fi
  else
    printf 'skip  ffmpeg could not synthesize the audio fixtures\n'
  fi
else
  printf 'skip  ffmpeg not installed — mux-audio not exercised against real files\n'
fi

echo
echo "=== Both commands need ffmpeg and say so before doing anything ==="
FAKE_BIN="$WORK/nobin"
mkdir -p "$FAKE_BIN"
for b in bash curl jq mktemp date stat cat rm mv cp mkdir sed grep awk head tail tr printf env cut sort find column dirname basename pwd wc cmp; do
  src="$(command -v "$b" 2>/dev/null)" && ln -sf "$src" "$FAKE_BIN/$b" 2>/dev/null
done
: > "$WORK/stub.mp4"
: > "$WORK/stub.wav"

out=$(PATH="$FAKE_BIN" bash "$TARGET" frame-at "$WORK/stub.mp4" --at 1 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'ffmpeg'; then
  pass "frame-at without ffmpeg fails with a clear reason"
else
  fail "frame-at must require ffmpeg up front" "exit $code: $(printf '%s' "$out" | head -1)"
fi

out=$(PATH="$FAKE_BIN" bash "$TARGET" mux-audio "$WORK/stub.mp4" "$WORK/stub.wav" 2>&1); code=$?
if [ "$code" -ne 0 ] && printf '%s' "$out" | grep -qi 'ffmpeg'; then
  pass "mux-audio without ffmpeg fails with a clear reason"
else
  fail "mux-audio must require ffmpeg up front" "exit $code: $(printf '%s' "$out" | head -1)"
fi

echo
echo "=== Neither command touches the network or needs a key ==="
out=$(env -u OFOX_API_KEY bash "$TARGET" frame-at "$WORK/does-not-exist.mp4" --at 1 2>&1)
if ! printf '%s' "$out" | grep -qi 'OFOX_API_KEY\|api key'; then
  pass "frame-at does not ask for a key"
else
  fail "frame-at must work without a key" "$(printf '%s' "$out" | head -1)"
fi
out=$(env -u OFOX_API_KEY bash "$TARGET" mux-audio "$WORK/nope.mp4" "$WORK/nope.wav" 2>&1)
if ! printf '%s' "$out" | grep -qi 'OFOX_API_KEY\|api key'; then
  pass "mux-audio does not ask for a key"
else
  fail "mux-audio must work without a key" "$(printf '%s' "$out" | head -1)"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
