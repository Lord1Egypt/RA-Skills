#!/usr/bin/env bash
# keyguard.test.sh — where OFOX_API_KEY is allowed to go, and what the
# --extra-json escape hatch is not allowed to overwrite.
#
# Three guards are under test, and each one is exercised by constructing the
# input it exists to refuse, not by watching a good input pass:
#
#   R1  the create response's own `polling_url` is followed only when it is
#       on the same scheme://host:port as API_BASE. The poll loop sends
#       `Authorization: Bearer $OFOX_API_KEY`, so this is the one path here
#       that needs no compromised local environment — a tampered or
#       misconfigured response is enough to redirect the key.
#   R2  OFOX_API_BASE_URL must be https (loopback excepted) and says out loud
#       which host is about to receive the key.
#   R3  --extra-json is merged last and wins over the flags, so a key that has
#       a flag is refused; and an EXPLICITLY EMPTY value is refused, because
#       until now it was indistinguishable from the flag not being passed —
#       which silently dropped the whole payload and billed the job anyway
#       (measured 2026-09-17, see references/api-params.md).
#
# Free by construction: every rejection happens before or instead of a network
# call, the accepted cases point at an unroutable base, and the one case that
# needs a 202 stubs curl rather than paying for a job. Nothing here can create
# a billable job.
#
# Run: bash references/test/keyguard.test.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/../ofox-video.sh"

if [ ! -f "$TARGET" ]; then
  echo "FATAL: cannot find ofox-video.sh at $TARGET" >&2
  exit 1
fi

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
# Loopback, so the override is legal, and port 1 is not listening anywhere, so
# anything that does reach the network fails to connect instead of spending.
export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"
# Every case here is about credentials and the escape hatch, never about
# per-model limits; skipping them keeps the catalog fetch out of the way.
export OFOX_SKIP_MODEL_VALIDATION=1

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "$2"
  FAIL=$((FAIL + 1))
}

# ---------------------------------------------------------------------------
# R2 — OFOX_API_BASE_URL
#
# `check` makes no network call at all, which makes it the right probe: what
# is being tested is the startup guard, not any request.
# ---------------------------------------------------------------------------

echo "=== R2: OFOX_API_BASE_URL is validated and announced ==="

base_case() {
  # base_case DESC WANT_EXIT WANT_PATTERN -- BASE_VALUE ("" means unset)
  local desc="$1" want_code="$2" want="$3" value="$5"
  local out code
  if [ -z "$value" ]; then
    out=$(env -u OFOX_API_BASE_URL bash "$TARGET" check 2>&1)
  else
    out=$(OFOX_API_BASE_URL="$value" bash "$TARGET" check 2>&1)
  fi
  code=$?
  if [ "$code" -ne "$want_code" ]; then
    fail "$desc" "expected exit $want_code, got $code: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    return
  fi
  if [ -n "$want" ] && ! printf '%s' "$out" | grep -q -- "$want"; then
    fail "$desc" "exit $want_code as expected, but nothing mentioned '$want': $(printf '%s' "$out" | head -3 | tr '\n' ' ')"
    return
  fi
  pass "$desc"
}

base_case "a plaintext non-loopback base is refused" 2 "not https://" -- \
  "http://staging.example.com/v1"
base_case "the refusal says why: the key rides in a header on every request" 2 "Authorization" -- \
  "http://staging.example.com/v1"
base_case "a value that is not a URL at all is refused" 2 "not an http:// or https:// URL" -- \
  "staging.example.com"
base_case "a non-http scheme is refused" 2 "not an http:// or https:// URL" -- \
  "ftp://staging.example.com/v1"
base_case "https to another host is allowed" 0 "" -- \
  "https://staging.example.com/v1"
base_case "and it names the host that will receive the key" 0 "staging.example.com" -- \
  "https://staging.example.com/v1"
base_case "plaintext IS allowed on loopback (local test servers)" 0 "" -- \
  "http://127.0.0.1:1/v1"
base_case "plaintext IS allowed on localhost by name" 0 "127.0.0.1\|localhost" -- \
  "http://localhost:8080/v1"

# Must-not-fire: with no override there is nothing to announce, and a NOTE on
# every ordinary run is how a warning stops being read.
out=$(env -u OFOX_API_BASE_URL bash "$TARGET" check 2>&1)
if printf '%s' "$out" | grep -q 'OFOX_API_BASE_URL'; then
  fail "an unset OFOX_API_BASE_URL must say nothing" "$(printf '%s' "$out" | head -1)"
else
  pass "no override, no notice (the warning stays worth reading)"
fi

# The announcement has to reach a human, i.e. stderr, and must not contaminate
# the parsed stdout contract.
out=$(OFOX_API_BASE_URL="https://staging.example.com/v1" bash "$TARGET" check 2>/dev/null)
if printf '%s' "$out" | grep -q 'OFOX_API_BASE_URL'; then
  fail "the override notice must go to stderr" "it appeared on stdout"
else
  pass "the override notice goes to stderr, not into the stdout contract"
fi

# ---------------------------------------------------------------------------
# R1 — the polling URL the API hands back
#
# The script as a library, with curl stubbed: one POST answers 202 with a body
# this test chooses, and every invocation is logged so the test can assert
# WHERE the key was sent, not just what was printed. Both drivers pass
# --approved because the thing under test happens after the create call, so
# they have to get past the spend gate; the stub means nothing is billed.
# ---------------------------------------------------------------------------

echo
echo "=== R1: a polling_url off the configured host is never followed ==="

LIB="$WORK/lib.sh"
sed -e '/^main "\$@"$/d' -e '/^exit \$?$/d' "$TARGET" > "$LIB"

cat > "$WORK/drive.sh" <<'EOF'
set -u
. "$LIBSH"
curl() {
  local out="" prev="" a
  for a in "$@"; do
    [ "$prev" = "-o" ] && out="$a"
    prev="$a"
  done
  printf '%s\n' "$*" >> "$CURLLOG"
  [ -n "$out" ] && printf '%s' "$BODY" > "$out"
  printf '202'
  return 0
}
OFOX_SUBMIT_ONLY=1 cmd_generate --prompt x --duration 4 --resolution 480p \
  --seed 42 --out-dir "$OUTD" --approved
echo "RC=$?"
EOF

# The same stub, but generate is allowed to go on and POLL. This is the driver
# that can actually leak: without the guard the loop issues an authenticated
# GET to whatever the response said, and the curl log records it. Running the
# key-destination assertion against the submit-only driver above would be a
# check that cannot fail, since that path returns before polling either way.
cat > "$WORK/drive-poll.sh" <<'EOF'
set -u
. "$LIBSH"
curl() {
  local out="" prev="" a
  for a in "$@"; do
    [ "$prev" = "-o" ] && out="$a"
    prev="$a"
  done
  printf '%s\n' "$*" >> "$CURLLOG"
  [ -n "$out" ] && printf '%s' "$BODY" > "$out"
  printf '202'
  return 0
}
cmd_generate --prompt x --duration 4 --resolution 480p --seed 42 \
  --out-dir "$OUTD" --max-wait 1 --poll-interval 1 --approved
echo "RC=$?"
EOF

create_with_body() {
  # create_with_body BODY_JSON -> prints the run's combined output
  local body="$1"
  : > "$WORK/curl.log"
  LIBSH="$LIB" CURLLOG="$WORK/curl.log" BODY="$body" OUTD="$WORK/out" \
    bash "$WORK/drive.sh" 2>&1
}

create_and_poll_with_body() {
  # Same, but the run goes on to poll — so the curl log below is evidence
  # about where the Authorization header really went.
  local body="$1"
  : > "$WORK/curl.log"
  LIBSH="$LIB" CURLLOG="$WORK/curl.log" BODY="$body" OUTD="$WORK/out" \
    bash "$WORK/drive-poll.sh" 2>&1
}

mkdir -p "$WORK/out"

out=$(create_with_body '{"id":"job-evil","polling_url":"https://evil.example/v1/videos/job-evil"}')
if printf '%s' "$out" | grep -q '^RC=3$'; then
  pass "a polling_url on another host makes generate exit 3"
else
  fail "a foreign polling_url must not be accepted" "$(printf '%s' "$out" | grep '^RC=')"
fi
if printf '%s' "$out" | grep -q "evil.example" &&
  printf '%s' "$out" | grep -qi 'different host'; then
  pass "the error names the host it refused and the host it expected"
else
  fail "the error must name the host" "$(printf '%s' "$out" | grep -i error | head -1)"
fi
# The point of the guard: the key must not have been sent there. Read the curl
# log, not the message — a message is not evidence about a request — and read
# it from a run that WOULD have polled, or the assertion cannot fail.
poll_out=$(create_and_poll_with_body '{"id":"job-evil","polling_url":"https://evil.example/v1/videos/job-evil"}')
if grep -q 'evil.example' "$WORK/curl.log"; then
  fail "the key was sent to the foreign host anyway" \
    "$(grep 'evil.example' "$WORK/curl.log" | head -1)"
else
  pass "a full generate makes no request of any kind to the foreign host"
fi
if [ "$(grep -c 'Authorization' "$WORK/curl.log")" -eq 1 ]; then
  pass "exactly one authenticated request was made, and it was the create"
else
  fail "authenticated request count changed" \
    "$(grep -c 'Authorization' "$WORK/curl.log") authenticated requests: $(grep 'Authorization' "$WORK/curl.log" | tail -1)"
fi
# Exit 3 alone would not distinguish this from the poll loop failing for its
# own reasons, so the reason has to be in the message too.
if printf '%s' "$poll_out" | grep -q '^RC=3$' &&
  printf '%s' "$poll_out" | grep -qi 'different host'; then
  pass "and a full generate stops for THAT reason, not by failing later"
else
  fail "a full generate must stop on a foreign polling_url, and say why" \
    "$(printf '%s' "$poll_out" | grep -E '^RC=|different host' | tr '\n' ' ')"
fi
out=$(create_with_body '{"id":"job-evil","polling_url":"https://evil.example/v1/videos/job-evil"}')
# Refusing must not strand a job that already exists and is already billable.
if printf '%s' "$out" | grep -q '^JOB_ID job-evil$'; then
  pass "the job id is still printed, so the paid job can be collected"
else
  fail "a refused polling_url must not lose the job id" "$(printf '%s' "$out" | grep JOB_ID)"
fi
if printf '%s' "$out" | grep -q 'poll job-evil'; then
  pass "and the recovery command is spelled out"
else
  fail "the refusal should say how to collect the job" "$(printf '%s' "$out" | tail -3 | tr '\n' ' ')"
fi

# Must-not-fire: the ordinary case, where the API returns its own URL on the
# host we are talking to. This is the shape every real response has had.
out=$(create_with_body '{"id":"job-ok","polling_url":"http://127.0.0.1:1/v1/videos/job-ok"}')
if printf '%s' "$out" | grep -q '^RC=0$' &&
  printf '%s' "$out" | grep -q '^POLLING_URL http://127.0.0.1:1/v1/videos/job-ok$'; then
  pass "a polling_url on the configured host is used exactly as given"
else
  fail "the normal polling_url path regressed" "$(printf '%s' "$out" | grep -E '^RC=|^POLLING_URL')"
fi

# Must-not-fire: the documented fallback when the field is absent.
out=$(create_with_body '{"id":"job-nourl"}')
if printf '%s' "$out" | grep -q '^RC=0$' &&
  printf '%s' "$out" | grep -q '^POLLING_URL http://127.0.0.1:1/v1/videos/job-nourl$'; then
  pass "an absent polling_url still falls back to API_BASE/videos/<id>"
else
  fail "the fallback path regressed" "$(printf '%s' "$out" | grep -E '^RC=|^POLLING_URL')"
fi

# The three ways a URL can look like ours and not be.
for bad in \
  'http://127.0.0.1:1@evil.example/v1/videos/j' \
  'http://127.0.0.1:2/v1/videos/j' \
  'https://127.0.0.1:1/v1/videos/j' \
  'not-a-url' ; do
  out=$(create_with_body "{\"id\":\"job-x\",\"polling_url\":\"$bad\"}")
  if printf '%s' "$out" | grep -q '^RC=3$'; then
    pass "refused: $bad"
  else
    fail "should have been refused: $bad" "$(printf '%s' "$out" | grep '^RC=')"
  fi
done
# The userinfo case is the one a reader would wave through, so assert the
# message names the host that would really have received the request.
out=$(create_with_body '{"id":"job-x","polling_url":"http://127.0.0.1:1@evil.example/v1/videos/j"}')
if printf '%s' "$out" | grep -q "'evil.example'"; then
  pass "userinfo before the host does not launder it: the message says evil.example"
else
  fail "a userinfo@host URL must be reported by its real host" \
    "$(printf '%s' "$out" | grep -i error | head -1)"
fi

echo
echo "=== R1 again, at the request itself: poll_and_download's own check ==="
# The same guard sits next to the authenticated request, not only next to the
# place the URL came from — a future caller will not remember.
cat > "$WORK/pollcall.sh" <<'EOF'
set -u
. "$LIBSH"
poll_and_download "job-z" "$URL" "$OUTD" 1 1
echo "RC=$?"
EOF
out=$(LIBSH="$LIB" URL="https://evil.example/v1/videos/job-z" OUTD="$WORK/out" \
  bash "$WORK/pollcall.sh" 2>&1)
if printf '%s' "$out" | grep -q '^RC=3$' && printf '%s' "$out" | grep -q 'evil.example'; then
  pass "poll_and_download refuses a foreign URL before its first request"
else
  fail "the poll loop must check the URL it is about to authenticate to" \
    "$(printf '%s' "$out" | tail -2 | tr '\n' ' ')"
fi
out=$(LIBSH="$LIB" URL="http://127.0.0.1:1/v1/videos/job-z" OUTD="$WORK/out" \
  bash "$WORK/pollcall.sh" 2>&1)
if printf '%s' "$out" | grep -q '^RC=4$'; then
  pass "a URL on the configured host still polls (and times out, unrouted)"
else
  fail "the canonical URL must still be polled" "$(printf '%s' "$out" | tail -2 | tr '\n' ' ')"
fi

# ---------------------------------------------------------------------------
# R3 — the escape hatch
# ---------------------------------------------------------------------------

echo
echo "=== R3: an explicitly empty --extra-json is an error, not 'not passed' ==="

out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --out-dir "$WORK/out" --dry-run --extra-json "" 2>&1)
code=$?
if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -qi 'empty value'; then
  pass "--extra-json '' is rejected before anything is submitted"
else
  fail "an empty --extra-json must not be treated as 'flag not passed'" \
    "exit $code: $(printf '%s' "$out" | grep -i error | head -1)"
fi
if printf '%s' "$out" | grep -qi 'ARG_MAX'; then
  pass "the error names the way this actually happens (a jq over ARG_MAX)"
else
  fail "the error should explain where an empty value comes from" \
    "$(printf '%s' "$out" | grep -i error | head -1)"
fi
# It has to fire through batch too: batch forwards the flag verbatim, and a
# batch is N times the bill.
out=$(bash "$TARGET" batch --prompt x --takes 2 --duration 4 --resolution 480p \
  --out-dir "$WORK/out" --extra-json "" --approved 2>&1)
code=$?
# "exit non-zero" alone would pass even with the guard gone, because the base
# is unroutable and the submission would fail anyway. What distinguishes them
# is that nothing was ever SENT — no "Submitting job" line — and that the
# reason given is the empty value.
if [ "$code" -ne 0 ] &&
  printf '%s' "$out" | grep -qi 'empty value' &&
  ! printf '%s' "$out" | grep -qi 'submitting job'; then
  pass "batch stops on the same empty value, before submitting anything"
else
  fail "batch must not attempt takes with a silently dropped --extra-json" \
    "exit $code: $(printf '%s' "$out" | grep -iE 'submitting job|empty value' | head -1)"
fi

echo
echo "=== R3: omitting the flag behaves byte-for-byte as it always did ==="
payload_of() {
  bash "$TARGET" generate --prompt x --duration 4 --resolution 480p --seed 42 \
    --out-dir "$WORK/out" --dry-run --print-payload "$@" 2>&1 |
    sed -n 's/^PAYLOAD //p'
}
omitted="$(payload_of)"
empty_obj="$(payload_of --extra-json '{}')"
if [ -n "$omitted" ] && [ "$omitted" = "$empty_obj" ]; then
  pass "no --extra-json produces the same body as --extra-json '{}'"
else
  fail "the omitted path changed" "omitted='$omitted' vs '{}'='$empty_obj'"
fi
if printf '%s' "$omitted" | grep -q '"seed":42' && ! printf '%s' "$omitted" | grep -q 'extra'; then
  pass "and it is still the plain flag-built body"
else
  fail "the omitted path should build the body from flags alone" "$omitted"
fi

echo
echo "=== R3: a key that has a flag cannot be smuggled in through the hatch ==="
clash_case() {
  # clash_case JSON WANT_MENTION
  local json="$1" want="$2" out code
  out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
    --out-dir "$WORK/out" --dry-run --extra-json "$json" 2>&1)
  code=$?
  if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -q -- "$want"; then
    pass "rejected: $json"
  else
    fail "should be rejected: $json" "exit $code: $(printf '%s' "$out" | grep -i error | head -1)"
  fi
}
clash_case '{"model":"bytedance/seedance-2.0-mini"}' 'model'
clash_case '{"duration":30}' 'duration'
clash_case '{"resolution":"1080p"}' 'resolution'
clash_case '{"aspect_ratio":"9:16"}' 'aspect_ratio'
clash_case '{"size":"1920x1080"}' 'size'
clash_case '{"seed":7}' 'seed'
clash_case '{"generate_audio":false}' 'generate_audio'
clash_case '{"real_person":true}' 'real_person'
clash_case '{"callback_url":"http://example.com/h"}' 'callback_url'
clash_case '{"frame_images":[]}' 'frame_images'
clash_case '{"provider":{"type":"volcengine"}}' 'provider.type'
clash_case '{"provider":"volcengine"}' 'provider'
clash_case '{"duration":30,"resolution":"1080p"}' 'duration, resolution'
# The dearest one: a 30s 1080p body behind a 4s 480p quote is the whole reason
# this rule exists, so assert the estimate never got printed with it.
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --out-dir "$WORK/out" --dry-run --extra-json '{"duration":30,"resolution":"1080p"}' 2>&1)
if ! printf '%s' "$out" | grep -qi 'estimated cost'; then
  pass "the clash is caught before a price is quoted for the wrong job"
else
  fail "a quote was printed for parameters the body would have overridden" \
    "$(printf '%s' "$out" | grep -i 'estimated cost' | head -1)"
fi

echo
echo "=== R3: everything without a flag still passes through ==="
allow_case() {
  # allow_case JSON WANT_IN_PAYLOAD
  local json="$1" want="$2" out
  out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p --seed 42 \
    --out-dir "$WORK/out" --dry-run --print-payload --extra-json "$json" 2>&1)
  if [ $? -eq 0 ] && printf '%s' "$out" | sed -n 's/^PAYLOAD //p' | grep -q -- "$want"; then
    pass "accepted and merged: $json"
  else
    fail "this must keep working: $json" "$(printf '%s' "$out" | grep -E '^PAYLOAD|ERROR' | head -1)"
  fi
}
allow_case '{"input_references":[{"type":"image_url","image_url":{"url":"https://example.com/a.jpg"}}]}' \
  'input_references'
allow_case '{"provider":{"options":{"byteplus":{"x":1}}}}' '"options"'
allow_case '{"some_field_with_no_flag":"v"}' 'some_field_with_no_flag'
# provider.options must merge WITH the pinned type, not replace the object.
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p --seed 42 \
  --out-dir "$WORK/out" --dry-run --print-payload \
  --extra-json '{"provider":{"options":{"byteplus":{"x":1}}}}' 2>&1 | sed -n 's/^PAYLOAD //p')
if printf '%s' "$out" | jq -e '.provider.type == "byteplus" and (.provider.options | has("byteplus"))' >/dev/null 2>&1; then
  pass "provider.options merges alongside the pinned provider.type"
else
  fail "the documented provider.options passthrough broke" "$out"
fi

echo
echo "=== R3: a non-object --extra-json is refused instead of emptying the body ==="
for bad in '[1,2]' '"text"' '42' 'null' 'false'; do
  out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
    --out-dir "$WORK/out" --dry-run --extra-json "$bad" 2>&1)
  code=$?
  if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -qi 'must be a JSON object'; then
    pass "refused a non-object --extra-json: $bad"
  else
    fail "a non-object --extra-json must be refused: $bad" \
      "exit $code: $(printf '%s' "$out" | grep -i error | head -1)"
  fi
done
# And the pre-existing checks still hold.
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --out-dir "$WORK/out" --dry-run --extra-json '{nope}' 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'not valid JSON'; then
  pass "invalid JSON is still reported as invalid JSON"
else
  fail "the pre-existing JSON check regressed" "$(printf '%s' "$out" | grep -i error | head -1)"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
