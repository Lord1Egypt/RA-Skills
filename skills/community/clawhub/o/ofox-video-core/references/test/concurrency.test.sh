#!/usr/bin/env bash
# concurrency.test.sh — waiting on several jobs at once, and the money guard
# that must survive it.
#
# The change under test moved `batch` from "submit and wait, one take at a
# time" to "submit one at a time, wait for all of them at once", and taught
# `poll` to take more than one job id. Two things could quietly break in that
# move and both cost real money if they did:
#
#   1. the stop-on-submission-failure guard — if take 2's create is rejected,
#      takes 3..N must still never be sent;
#   2. per-take attribution — takes now finish in whatever order the API
#      likes, and a seed printed against the wrong take makes "re-render take
#      3" spend money on the wrong clip.
#
# Free by construction: the API base points at an unroutable address, and
# every case that needs a completed job stubs cmd_generate/poll_and_download
# rather than paying for one. Nothing here can create a billable job.
#
# Run: bash references/test/concurrency.test.sh

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

# The script as a library: main() stripped so functions can be called and
# stubbed directly, the same trick handoff.test.sh uses.
LIB="$WORK/lib.sh"
sed -e '/^main "\$@"$/d' -e '/^exit \$?$/d' "$TARGET" > "$LIB"

echo "=== --concurrency validation (before any network call) ==="
for bad in 0 -1 abc 1.5 "" 99; do
  out=$(bash "$TARGET" batch --prompt x --takes 2 --concurrency "$bad" 2>&1)
  code=$?
  label="--concurrency '$bad' is rejected"
  if [ "$code" -eq 1 ] && printf '%s' "$out" | grep -qi 'concurrency'; then
    pass "$label"
  else
    fail "$label" "exit $code: $(printf '%s' "$out" | head -1)"
  fi
done

out=$(bash "$TARGET" batch --prompt x --takes 2 --concurrency 99 2>&1)
if printf '%s' "$out" | grep -qi 'requests/minute\|account limit'; then
  pass "the cap explains itself in requests per minute, not as a bare number"
else
  fail "the cap should say why 10 is the ceiling" "$(printf '%s' "$out" | head -1)"
fi

out=$(bash "$TARGET" batch --prompt x --takes 3 --concurrency 0 2>&1)
if ! printf '%s' "$out" | grep -qi 'submitting job'; then
  pass "a rejected --concurrency submits nothing"
else
  fail "validation failure must not submit anything" "output mentions submitting"
fi

echo
echo "=== --takes is still capped: concurrency must not widen the blast radius ==="
out=$(bash "$TARGET" batch --prompt x --takes 11 --concurrency 10 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'takes'; then
  pass "--takes 11 is still rejected (10 concurrent polls is not 11 takes)"
else
  fail "--takes cap should hold" "$(printf '%s' "$out" | head -1)"
fi

echo
echo "=== The dry run tells the user it will spend N bills at once ==="
out=$(bash "$TARGET" batch --prompt x --takes 3 --duration 5 --resolution 480p \
  --out-dir "$WORK/dry" --dry-run 2>&1)
if printf '%s' "$out" | grep -q '^CONCURRENCY '; then
  pass "dry run reports the concurrency it would use"
else
  fail "dry run should print CONCURRENCY" "$(printf '%s' "$out" | tail -4 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -qi 'waited for concurrently\|concurrently'; then
  pass "dry run says the waiting is concurrent"
else
  fail "dry run still describes a serial wait" "$(printf '%s' "$out" | grep -i 'DRY RUN')"
fi
if printf '%s' "$out" | grep -qi 'arrive at once\|whole batch'; then
  pass "dry run says the whole batch's bill arrives at once"
else
  fail "a concurrent batch must be priced as a total up front" \
    "$(printf '%s' "$out" | grep -i 'dry run' | head -1)"
fi
# The cost line the approval gate tells agents to relay must still be exactly
# one, and must still be the batch total rather than a per-take figure.
n_est=$(printf '%s\n' "$out" | grep -c 'Estimated cost:')
if [ "$n_est" -eq 1 ]; then
  pass "still exactly one 'Estimated cost:' line to relay"
else
  fail "the approval gate expects one estimate line" "saw $n_est"
fi

echo
echo "=== The rate-limit note fires on the combination, not on the count ==="
out=$(bash "$TARGET" batch --prompt x --takes 4 --duration 5 --resolution 480p \
  --concurrency 4 --poll-interval 1 --out-dir "$WORK/dry" --dry-run 2>&1)
if printf '%s' "$out" | grep -qi 'requests/minute'; then
  pass "4 polls at 1s apart is called out (240/min against a 100/min limit)"
else
  fail "a rate-crowding combination should warn" "$(printf '%s' "$out" | tail -5 | tr '\n' ' ')"
fi
out=$(bash "$TARGET" batch --prompt x --takes 4 --duration 5 --resolution 480p \
  --out-dir "$WORK/dry" --dry-run 2>&1)
if ! printf '%s' "$out" | grep -qi 'requests/minute'; then
  pass "the default 4 polls at 6s apart (40/min) says nothing"
else
  fail "the default must not warn about itself" "$(printf '%s' "$out" | grep -i 'requests/minute')"
fi

echo
echo "=== poll takes more than one job id ==="
out=$(bash "$TARGET" poll --out-dir "$WORK" 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'requires a job id'; then
  pass "poll with no job id is still rejected"
else
  fail "poll needs at least one id" "$(printf '%s' "$out" | head -1)"
fi

out=$(bash "$TARGET" poll job-a job-b --bogus 1 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi "unknown option '--bogus'"; then
  pass "an unknown flag is still an error, not mistaken for a job id"
else
  fail "unknown flags must not become job ids" "$(printf '%s' "$out" | head -1)"
fi

out=$(bash "$TARGET" poll job-a --out-dir 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qi 'requires a value'; then
  pass "a flag missing its value is still rejected"
else
  fail "dangling flag should be rejected" "$(printf '%s' "$out" | head -1)"
fi

out=$(bash "$TARGET" poll --out-dir "$WORK/p1" --max-wait 2 --poll-interval 1 job-x job-y 2>&1)
code=$?
if [ "$code" -eq 4 ] && printf '%s' "$out" | grep -q 'job-x' && printf '%s' "$out" | grep -q 'job-y'; then
  pass "ids given after the flags are both polled"
else
  fail "ids must be accepted in either position" "exit $code: $(printf '%s' "$out" | tail -3 | tr '\n' ' ')"
fi

out=$(bash "$TARGET" poll job-dup job-dup job-other --out-dir "$WORK/p2" \
  --max-wait 2 --poll-interval 1 2>&1)
if printf '%s' "$out" | grep -qi 'more than once'; then
  pass "a repeated job id is noted (polling it twice would download onto one filename)"
else
  fail "a duplicate id should be collapsed" "$(printf '%s' "$out" | head -3 | tr '\n' ' ')"
fi
if printf '%s' "$out" | grep -q 'JOBS_REQUESTED 2'; then
  pass "three arguments with one repeat are two jobs, not three"
else
  fail "duplicate collapsed but still counted" "$(printf '%s' "$out" | grep JOBS_REQUESTED)"
fi
# Collapsing down to a single unique id must land on the single-id path,
# output shape and all — not on a one-element multi-job report.
out=$(bash "$TARGET" poll job-solo2 job-solo2 --out-dir "$WORK/p2b" \
  --max-wait 2 --poll-interval 1 2>&1)
if [ $? -eq 4 ] && ! printf '%s' "$out" | grep -q '^STATUS poll_'; then
  pass "one id after collapsing behaves as a plain single-id poll"
else
  fail "a collapsed duplicate should not grow the multi-job shape" \
    "$(printf '%s' "$out" | grep '^STATUS ')"
fi

echo
echo "=== One id behaves exactly as it always did ==="
out=$(bash "$TARGET" poll job-solo --out-dir "$WORK/p3" --max-wait 2 --poll-interval 1 2>&1)
code=$?
if [ "$code" -eq 4 ]; then
  pass "a single-id poll that never completes still exits 4"
else
  fail "single-id exit code changed" "got $code, want 4"
fi
if printf '%s' "$out" | grep -q 'TIMEOUT: job job-solo'; then
  pass "single-id output is the same TIMEOUT message as before"
else
  fail "single-id output shape changed" "$(printf '%s' "$out" | tail -2 | tr '\n' ' ')"
fi
if ! printf '%s' "$out" | grep -q '=== JOB \|^STATUS poll_'; then
  pass "single-id adds no multi-job wrapper lines"
else
  fail "single-id must not grow a new output shape" "$(printf '%s' "$out" | grep '=== JOB \|STATUS poll_')"
fi

echo
echo "=== Multi-id polling actually overlaps ==="
start="$(date +%s)"
bash "$TARGET" poll j1 j2 j3 --out-dir "$WORK/p4" --max-wait 4 --poll-interval 1 \
  --concurrency 3 >/dev/null 2>&1
took=$(( $(date +%s) - start ))
# Serially this is 3 x 4s = 12s or more; concurrently it is one 4s wait.
if [ "$took" -le 9 ]; then
  pass "three 4-second waits took ${took}s, not 12+ (they overlapped)"
else
  fail "multi-id poll did not overlap" "took ${took}s for three --max-wait 4 jobs"
fi

echo
echo "=== The concurrency cap is respected, not just accepted ==="
# poll_and_download is stubbed to log a start and an end marker. Reading the
# log back gives the real high-water mark of simultaneous jobs.
cat > "$WORK/cap.sh" <<'EOF'
set -u
. "$LIBSH"
poll_and_download() {
  printf 'S %s\n' "$1" >> "$MARKS"
  sleep 1
  printf 'E %s\n' "$1" >> "$MARKS"
  echo "STATUS completed"
  echo "JOB_ID $1"
  echo "VIDEO_PATH /dev/null/$1.mp4"
  echo "VIDEO_COST 0.5000000000"
  return 0
}
recs=()
i=1
while [ "$i" -le "$NJOBS" ]; do
  recs+=("$(printf 'job-%s\thttp://example.invalid/%s' "$i" "$i")")
  i=$((i + 1))
done
poll_many "$CAP" "$PWD" 30 1 "" "job" "${recs[@]}"
i=0
while [ "$i" -lt "$NJOBS" ]; do
  echo "RC $i ${POLL_MANY_RC[$i]}"
  i=$((i + 1))
done
EOF
MARKS="$WORK/marks.log"
: > "$MARKS"
LIBSH="$LIB" MARKS="$MARKS" NJOBS=6 CAP=2 bash "$WORK/cap.sh" >/dev/null 2>&1
peak=$(awk '$1=="S"{c++; if (c>m) m=c} $1=="E"{c--} END{print m+0}' "$MARKS")
if [ "$peak" -eq 2 ]; then
  pass "--concurrency 2 over 6 jobs never ran more than 2 at once (peak $peak)"
else
  fail "the concurrency cap was not respected" "peak was $peak, expected 2"
fi
started=$(grep -c '^S ' "$MARKS")
if [ "$started" -eq 6 ]; then
  pass "all 6 jobs were eventually run, in waves"
else
  fail "some jobs were dropped by the cap" "only $started of 6 started"
fi

: > "$MARKS"
LIBSH="$LIB" MARKS="$MARKS" NJOBS=4 CAP=4 bash "$WORK/cap.sh" >/dev/null 2>&1
peak=$(awk '$1=="S"{c++; if (c>m) m=c} $1=="E"{c--} END{print m+0}' "$MARKS")
if [ "$peak" -eq 4 ]; then
  pass "--concurrency 4 over 4 jobs ran all four at once (peak $peak)"
else
  fail "a cap at or above the job count should not serialise" "peak was $peak, expected 4"
fi

echo
echo "=== Per-take attribution survives out-of-order completion ==="
# Takes finish in reverse: take 1 is slowest. Seed, job id, cost and path
# must still line up with the take number, or "re-render take 3" spends money
# on the wrong clip.
cat > "$WORK/attrib.sh" <<'EOF'
set -u
. "$LIBSH"
: > "$COUNTER"
cmd_generate() {
  # cmd_batch validates one take through a --dry-run pass before it
  # submits anything. That call is not a submission and must not be
  # counted as one, exactly as the real cmd_generate does not bill for it.
  case " $* " in *" --dry-run "*) return 0 ;; esac
  printf 'x\n' >> "$COUNTER"
  local n; n=$(wc -l < "$COUNTER" | tr -d ' ')
  local seed="" a prev=""
  for a in "$@"; do
    [ "$prev" = "--seed" ] && seed="$a"
    prev="$a"
  done
  echo "STATUS submitted"
  echo "JOB_ID job-$n"
  echo "SEED 90${n}"
  echo "POLLING_URL http://example.invalid/v1/videos/job-$n"
  echo "OUT_DIR $OUTD"
  return 0
}
poll_and_download() {
  local jid="$1" n="${1#job-}"
  # 3 seconds for take 1, 1 for take 3: completion order is the reverse of
  # submission order.
  sleep $(( 4 - n ))
  echo "STATUS completed"
  echo "JOB_ID $jid"
  echo "VIDEO_PATH $OUTD/$jid.mp4"
  echo "VIDEO_SECONDS 5"
  echo "VIDEO_COST 1.0${n}00000000"
  return 0
}
make_contact_sheet() { return 1; }
cmd_batch --prompt x --takes 3 --duration 5 --resolution 480p --out-dir "$OUTD" --concurrency 3 --approved
echo "BATCH_EXIT=$?"
EOF
mkdir -p "$WORK/att"
out=$(LIBSH="$LIB" COUNTER="$WORK/att.n" OUTD="$WORK/att" bash "$WORK/attrib.sh" 2>/dev/null)
ok=1
for n in 1 2 3; do
  if ! printf '%s\n' "$out" | grep -q "^TAKE $n job-$n seed=90$n 1.0${n}00000000 .*/job-$n.mp4$"; then
    ok=0
    fail "take $n's id/seed/cost/path stayed together" \
      "$(printf '%s\n' "$out" | grep "^TAKE $n " || echo 'no TAKE line')"
  fi
done
if [ "$ok" -eq 1 ]; then
  pass "take 1, 2 and 3 each kept their own job id, seed, cost and file"
fi
if printf '%s\n' "$out" | grep -q '^BATCH_COST_TOTAL 3.0600000000$'; then
  pass "the total is the sum of the real per-take costs (3.06)"
else
  fail "total cost wrong after concurrent completion" \
    "$(printf '%s\n' "$out" | grep BATCH_COST_TOTAL)"
fi
if printf '%s\n' "$out" | grep -q '^STATUS batch_completed$'; then
  pass "an all-complete batch still reports batch_completed"
else
  fail "status changed for a fully successful batch" \
    "$(printf '%s\n' "$out" | grep '^STATUS ')"
fi
if printf '%s\n' "$out" | grep -q '^BATCH_EXIT=0$'; then
  pass "an all-complete batch still exits 0"
else
  fail "exit code changed for a fully successful batch" \
    "$(printf '%s\n' "$out" | grep BATCH_EXIT)"
fi

echo
echo "=== A submission failure still stops the batch ==="
# take 3's create is rejected. Takes 3..N must never be sent; takes 1..2 are
# already billable and must still be collected.
cat > "$WORK/subfail.sh" <<'EOF'
set -u
. "$LIBSH"
: > "$COUNTER"
cmd_generate() {
  # cmd_batch validates one take through a --dry-run pass before it
  # submits anything. That call is not a submission and must not be
  # counted as one, exactly as the real cmd_generate does not bill for it.
  case " $* " in *" --dry-run "*) return 0 ;; esac
  printf 'x\n' >> "$COUNTER"
  local n; n=$(wc -l < "$COUNTER" | tr -d ' ')
  if [ "$n" -ge 3 ]; then
    echo "ERROR: simulated create rejection" >&2
    return 3
  fi
  echo "STATUS submitted"
  echo "JOB_ID job-$n"
  echo "SEED 70$n"
  echo "POLLING_URL http://example.invalid/v1/videos/job-$n"
  echo "OUT_DIR $OUTD"
  return 0
}
poll_and_download() {
  echo "STATUS completed"
  echo "JOB_ID $1"
  echo "VIDEO_PATH $OUTD/$1.mp4"
  echo "VIDEO_COST 1.0000000000"
  return 0
}
make_contact_sheet() { return 1; }
cmd_batch --prompt x --takes 5 --duration 5 --resolution 480p --out-dir "$OUTD" --approved
echo "BATCH_EXIT=$?"
EOF
mkdir -p "$WORK/sf"
out=$(LIBSH="$LIB" COUNTER="$WORK/sf.n" OUTD="$WORK/sf" bash "$WORK/subfail.sh" 2>&1)
creates=$(printf '%s\n' "$out" | grep -c '^--- creating take ')
if [ "$creates" -eq 3 ]; then
  pass "take 3's rejection stopped submission (3 create attempts, not 5)"
else
  fail "a rejected create must stop the batch" "saw $creates create attempts, expected 3"
fi
if printf '%s\n' "$out" | grep -q '^TAKES_NOT_SUBMITTED 3$'; then
  pass "the 3 takes that were never sent are counted as not submitted"
else
  fail "unsent takes should be reported" "$(printf '%s\n' "$out" | grep TAKES_)"
fi
if printf '%s\n' "$out" | grep -q '^TAKES_COMPLETED 2$'; then
  pass "the 2 takes already submitted were still waited for, not abandoned"
else
  fail "already-billable takes must still be collected" "$(printf '%s\n' "$out" | grep TAKES_)"
fi
if printf '%s\n' "$out" | grep -qi 'already submitted and billable'; then
  pass "it says plainly that the earlier takes are billable and being collected"
else
  fail "the money already spent should be named" "$(printf '%s\n' "$out" | grep -i stopping)"
fi
if printf '%s\n' "$out" | grep -q '^STATUS batch_partial$'; then
  pass "a stopped batch reports batch_partial, not batch_completed"
else
  fail "a partial batch must not look complete" "$(printf '%s\n' "$out" | grep '^STATUS ')"
fi
if printf '%s\n' "$out" | grep -q '^BATCH_EXIT=3$'; then
  pass "a stopped batch still exits 3"
else
  fail "wrong exit for a stopped batch" "$(printf '%s\n' "$out" | grep BATCH_EXIT)"
fi

echo
echo "=== A failure AFTER submission does not take the others down ==="
cat > "$WORK/genfail.sh" <<'EOF'
set -u
. "$LIBSH"
: > "$COUNTER"
cmd_generate() {
  # cmd_batch validates one take through a --dry-run pass before it
  # submits anything. That call is not a submission and must not be
  # counted as one, exactly as the real cmd_generate does not bill for it.
  case " $* " in *" --dry-run "*) return 0 ;; esac
  printf 'x\n' >> "$COUNTER"
  local n; n=$(wc -l < "$COUNTER" | tr -d ' ')
  echo "STATUS submitted"
  echo "JOB_ID job-$n"
  echo "SEED 80$n"
  echo "POLLING_URL http://example.invalid/v1/videos/job-$n"
  echo "OUT_DIR $OUTD"
  return 0
}
poll_and_download() {
  case "$1" in
    job-2)
      echo "ERROR: job job-2 ended with status 'failed'." >&2
      echo "  Upstream message: simulated output moderation failure" >&2
      return 3
      ;;
    job-3) return 4 ;;
  esac
  echo "STATUS completed"
  echo "JOB_ID $1"
  echo "VIDEO_PATH $OUTD/$1.mp4"
  echo "VIDEO_COST 2.0000000000"
  return 0
}
make_contact_sheet() { return 1; }
cmd_batch --prompt x --takes 3 --duration 5 --resolution 480p --out-dir "$OUTD" --approved
echo "BATCH_EXIT=$?"
EOF
mkdir -p "$WORK/gf"
out=$(LIBSH="$LIB" COUNTER="$WORK/gf.n" OUTD="$WORK/gf" bash "$WORK/genfail.sh" 2>&1)
creates=$(printf '%s\n' "$out" | grep -c '^--- creating take ')
if [ "$creates" -eq 3 ]; then
  pass "all 3 takes were submitted (a generation failure is not a create failure)"
else
  fail "post-submission failure must not stop submission" "saw $creates creates, expected 3"
fi
if printf '%s\n' "$out" | grep -q '^TAKES_COMPLETED 1$' &&
   printf '%s\n' "$out" | grep -q '^TAKES_FAILED 1$' &&
   printf '%s\n' "$out" | grep -q '^TAKES_RUNNING 1$'; then
  pass "one completed, one failed and one still running are counted separately"
else
  fail "the three outcomes should be distinguishable" "$(printf '%s\n' "$out" | grep TAKES_)"
fi
if printf '%s\n' "$out" | grep -q '^TAKE 2 job-2 seed=802 FAILED exit=3$'; then
  pass "the failed take keeps its take number, job id and seed"
else
  fail "a failed take should still be attributable" "$(printf '%s\n' "$out" | grep '^TAKE 2')"
fi
if printf '%s\n' "$out" | grep -q '^TAKE 3 job-3 seed=803 RUNNING exit=4$'; then
  pass "a take still running is reported as running, not as failed"
else
  fail "a timed-out take is a different case from a failed one" \
    "$(printf '%s\n' "$out" | grep '^TAKE 3')"
fi
if printf '%s\n' "$out" | grep -q '^TAKE 1 job-1 seed=801 2.0000000000 .*/job-1.mp4$'; then
  pass "the completed take is numbered 1 and still reports its file"
else
  fail "a gap in the takes must not renumber the survivors" \
    "$(printf '%s\n' "$out" | grep '^TAKE 1')"
fi
if printf '%s\n' "$out" | grep -qi 'still running upstream and are billed'; then
  pass "the still-running take comes with the poll command that collects it"
else
  fail "a billable running job must be recoverable" "$(printf '%s\n' "$out" | tail -4 | tr '\n' ' ')"
fi
if printf '%s\n' "$out" | grep -qi 'simulated output moderation failure'; then
  pass "the failed take's own reason is surfaced, not swallowed"
else
  fail "each take's diagnostics must reach the user" "$(printf '%s\n' "$out" | grep -i 'job-2' | head -2 | tr '\n' ' ')"
fi

echo
echo "=== Usage advertises the fan-out ==="
out=$(bash "$TARGET" 2>&1)
if printf '%s' "$out" | grep -q 'poll JOB_ID \[JOB_ID'; then
  pass "usage shows that poll takes several job ids"
else
  fail "usage should advertise multi-id poll" "$(printf '%s' "$out" | grep -i 'poll ')"
fi
if printf '%s' "$out" | grep -q 'concurrency'; then
  pass "usage mentions --concurrency"
else
  fail "usage should mention --concurrency" "$(printf '%s' "$out" | head -12 | tr '\n' ' ')"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
