#!/usr/bin/env bash
# approval.test.sh — the --approved spend gate.
#
# What is under test: generate / create / batch / chain refuse to run without
# --approved, and nothing else does.
#
# The split is derived here at run time, not retyped: the subcommand list comes
# out of the script's own usage text, every subcommand is then run without the
# flag, and the two resulting sets are asserted. A subcommand added later that
# reaches the billable POST without a guard lands in the wrong set and turns
# this red; an extractor that quietly starts matching fewer subcommands trips
# the count assertion instead of passing silently.
#
# Two defects are planted, in throwaway copies, because a guard nobody has
# watched fail is not a guard:
#   D1  require_approved always returns 0 (the "if false" version) — the
#       refusal must disappear and the run must reach the submit line.
#   D2  batch stops forwarding --approved to each take's cmd_generate — an
#       approved batch must then break at take 1, which is what makes the
#       forwarding load-bearing rather than decorative.
#
# Free by construction: OFOX_API_BASE_URL points at a loopback port nothing
# listens on, so the one case that gets past the gate dies on connect. No job
# can be created from this file.
#
# Run: bash references/test/approval.test.sh

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
OUT="$WORK/out"
mkdir -p "$OUT"

# Not a credential — the script only checks that OFOX_API_KEY is non-empty.
PLACEHOLDER=placeholder
export OFOX_API_KEY="$PLACEHOLDER"
# Loopback port 1: legal to override to, and nothing is listening, so anything
# that reaches the network fails to connect instead of spending.
export OFOX_API_BASE_URL="http://127.0.0.1:1/v1"
# This file is about one guard, not about per-model limits.
export OFOX_SKIP_MODEL_VALIDATION=1

pass() {
  printf 'ok    %s\n' "$1"
  PASS=$((PASS + 1))
}
fail() {
  printf 'FAIL  %s\n      %s\n' "$1" "$2"
  FAIL=$((FAIL + 1))
}

# The one string that means "the spend gate refused this run". Everything below
# classifies on it rather than on an exit code: plenty of these invocations
# exit non-zero for their own reasons, and an exit code cannot tell those apart
# from a refusal.
GATE_MARK='was run without --approved'

# run_sub SUBCOMMAND -- prints combined output of a representative, free
# invocation of that subcommand, WITHOUT --approved.
run_sub() {
  case "$1" in
    check|models|providers)
      bash "$TARGET" "$1" 2>&1 ;;
    generate|create)
      bash "$TARGET" "$1" --prompt x --duration 4 --resolution 480p \
        --out-dir "$OUT" 2>&1 ;;
    batch)
      bash "$TARGET" batch --prompt x --takes 2 --duration 4 --resolution 480p \
        --out-dir "$OUT" 2>&1 ;;
    chain)
      # One shot: a multi-shot chain needs ffmpeg, which is not what this file
      # is measuring.
      bash "$TARGET" chain --shot a --duration 4 --resolution 480p \
        --out-dir "$OUT" 2>&1 ;;
    poll)
      bash "$TARGET" poll job-does-not-exist --max-wait 1 --poll-interval 1 \
        --out-dir "$OUT" 2>&1 ;;
    contact-sheet|last-frame)
      bash "$TARGET" "$1" "$WORK/nope.mp4" --out-dir "$OUT" 2>&1 ;;
    frame-at)
      bash "$TARGET" frame-at "$WORK/nope.mp4" --at 1 --out-dir "$OUT" 2>&1 ;;
    mux-audio)
      bash "$TARGET" mux-audio "$WORK/nope.mp4" "$WORK/nope.wav" --out-dir "$OUT" 2>&1 ;;
    *)
      echo "UNMODELLED SUBCOMMAND $1" ;;
  esac
}

# ---------------------------------------------------------------------------
# The split, derived from the shipped usage text
# ---------------------------------------------------------------------------

echo "=== Which subcommands the gate covers, read off the script itself ==="

SUBS=$(bash "$TARGET" 2>&1 | sed -n 's/^  ofox-video\.sh \([a-z][a-z-]*\).*/\1/p' | sort -u)
n_subs=$(printf '%s\n' "$SUBS" | grep -c .)
# A subject count, so an extractor that stops matching goes red rather than
# passing with less to check. 12 today: check, models, providers, generate,
# create, batch, poll, chain, contact-sheet, last-frame, frame-at, mux-audio.
if [ "$n_subs" -eq 12 ]; then
  pass "usage advertises 12 subcommands, and all 12 were extracted"
else
  fail "the subcommand extractor changed what it matches" \
    "got $n_subs: $(printf '%s' "$SUBS" | tr '\n' ' ')"
fi

gated=""
free=""
unmodelled=""
for sub in $SUBS; do
  out="$(run_sub "$sub")"
  if printf '%s' "$out" | grep -q 'UNMODELLED SUBCOMMAND'; then
    unmodelled="$unmodelled $sub"
  elif printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
    gated="$gated $sub"
  else
    free="$free $sub"
  fi
done

if [ -z "$unmodelled" ]; then
  pass "every advertised subcommand has a case in this file"
else
  fail "a subcommand exists that this test does not exercise" \
    "unmodelled:$unmodelled — add it to run_sub and decide which set it belongs in"
fi

# shellcheck disable=SC2086
n_gated=$(printf '%s\n' $gated | grep -c .)
# shellcheck disable=SC2086
n_free=$(printf '%s\n' $free | grep -c .)

want_gated="batch chain create generate"
# shellcheck disable=SC2086
got_gated="$(printf '%s\n' $gated | sort | tr '\n' ' ' | sed 's/ $//')"
if [ "$got_gated" = "$want_gated" ]; then
  pass "exactly these 4 refuse without --approved: $want_gated"
else
  fail "the guarded set changed" "expected '$want_gated', got '$got_gated'"
fi
if [ "$n_gated" -eq 4 ] && [ "$n_free" -eq 8 ]; then
  pass "4 subcommands are gated, 8 are not, and 4 + 8 is the whole list"
else
  fail "the gated/free split does not account for every subcommand" \
    "$n_gated gated + $n_free free, out of $n_subs"
fi

# There is exactly one billable request in the script. If a second POST ever
# appears, the reasoning above ("the gated set is the set that reaches the
# POST") stops holding, and whoever added it has to come back here.
n_post=$(grep -c -- '-X POST' "$TARGET")
if [ "$n_post" -eq 1 ]; then
  pass "the script still makes exactly one POST — the create call"
else
  fail "a second write request appeared; the gated set has to be re-derived" \
    "$n_post occurrences of '-X POST'"
fi

# ---------------------------------------------------------------------------
# The free 8 really ran — "the gate did not fire" is not evidence on its own
# ---------------------------------------------------------------------------

echo
echo "=== The 8 ungated subcommands still work with no --approved ==="

for sub in check models; do
  if bash "$TARGET" "$sub" >/dev/null 2>&1; then
    pass "$sub exits 0 with no --approved"
  else
    fail "$sub must not need --approved" "it exited non-zero"
  fi
done
# providers needs catalog data, and this suite runs against an unroutable base
# with no warm cache — so it exits 1 on its own, saying so, with or without
# this change. Assert what is actually about the gate: it was not turned away,
# and it got as far as its own catalog handling.
out=$(bash "$TARGET" providers 2>&1)
if ! printf '%s' "$out" | grep -qF -- "$GATE_MARK" &&
  printf '%s' "$out" | grep -qi 'provider list'; then
  pass "providers is not gated, and reached its own catalog lookup"
else
  fail "providers must not need --approved" "$(printf '%s' "$out" | tail -2 | tr '\n' ' ')"
fi

# poll is the most important must-not-fire in this file: it is the recovery
# command printed whenever a run is refused, times out or is interrupted, so
# gating it would strand a job that has already been paid for.
out=$(bash "$TARGET" poll job-does-not-exist --max-wait 1 --poll-interval 1 \
  --out-dir "$OUT" 2>&1)
code=$?
if ! printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
  pass "poll is never gated — a paid job must always be collectable"
else
  fail "poll must not require --approved" "it would strand already-billed jobs"
fi
if [ "$code" -ne 1 ] && printf '%s' "$out" | grep -qi 'poll'; then
  pass "and poll really reached its polling loop (exit $code), it did not bail early"
else
  fail "the poll probe did not get far enough to mean anything" \
    "exit $code: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

# The four ffmpeg tools: each must fail for its OWN reason (a file that is not
# there), which is the evidence that it ran rather than being turned away.
for sub in contact-sheet last-frame frame-at mux-audio; do
  out="$(run_sub "$sub")"
  if printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
    fail "$sub is local ffmpeg work and must not be gated" "the gate fired"
  elif printf '%s' "$out" | grep -qi 'nope\.\(mp4\|wav\)\|ffmpeg\|not readable\|no such file\|cannot read'; then
    pass "$sub ran and failed on its own missing input, not on the gate"
  else
    fail "$sub did not reach its own argument handling" \
      "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  fi
done

# ---------------------------------------------------------------------------
# --dry-run is the way through the gate, so it can never be behind it
# ---------------------------------------------------------------------------

echo
echo "=== --dry-run works without --approved (the quote is the point) ==="

dry_case() {
  # dry_case DESC -- ARGS...
  local desc="$1"; shift 2
  local out code
  out=$(bash "$TARGET" "$@" --dry-run 2>&1)
  code=$?
  if [ "$code" -eq 0 ] &&
    printf '%s' "$out" | grep -q '^STATUS dry_run$' &&
    ! printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
    pass "$desc"
  else
    fail "$desc" "exit $code: $(printf '%s' "$out" | grep -E "STATUS|$GATE_MARK" | head -1)"
  fi
}
dry_case "generate --dry-run quotes and stops, no --approved needed" -- \
  generate --prompt x --duration 4 --resolution 480p --out-dir "$OUT"
dry_case "create --dry-run too" -- \
  create --prompt x --duration 4 --resolution 480p --out-dir "$OUT"
dry_case "batch --dry-run too" -- \
  batch --prompt x --takes 2 --duration 4 --resolution 480p --out-dir "$OUT"
dry_case "chain --dry-run too" -- \
  chain --shot a --duration 4 --resolution 480p --out-dir "$OUT"

# And the quote a refused run is told to go and get is really on that output.
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --out-dir "$OUT" --dry-run 2>&1)
if printf '%s' "$out" | grep -q 'Estimated cost:'; then
  pass "the dry run prints the 'Estimated cost:' line the refusal points at"
else
  fail "the refusal's step 2 names a line the dry run must print" \
    "$(printf '%s' "$out" | tail -3 | tr '\n' ' ')"
fi

# ---------------------------------------------------------------------------
# What the refusal says, and what it does not do
# ---------------------------------------------------------------------------

echo
echo "=== The refusal is actionable, and nothing was submitted ==="

out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --out-dir "$OUT" 2>&1)
code=$?
if [ "$code" -eq 1 ]; then
  pass "a paid subcommand without --approved exits 1"
else
  fail "the refusal must exit 1 (usage error, nothing sent)" "exit $code"
fi
if ! printf '%s' "$out" | grep -qi 'submitting job'; then
  pass "and it never reached the submit line"
else
  fail "a refused run must not submit" "output mentions submitting"
fi
# A mode added in front of an output is where documentation turns into fiction:
# the estimate's non-dry wording ends "Actual billing is reported below", and
# below a refusal there is no billing at all.
if printf '%s' "$out" | grep -q 'Estimated cost:' &&
  ! printf '%s' "$out" | grep -q 'reported below'; then
  pass "the estimate on a refused run does not promise a bill below it"
else
  fail "the refused run's estimate still claims billing follows" \
    "$(printf '%s' "$out" | grep 'Estimated cost:' | head -1)"
fi
# …and the ordinary approved run must still carry that promise, or the fix
# above would have been a global downgrade rather than a mode-specific one.
approved_out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --out-dir "$OUT" --approved 2>&1)
if printf '%s' "$approved_out" | grep -q 'Actual billing is reported below'; then
  pass "an approved run still says the real figure follows"
else
  fail "the approved run lost its billing promise" \
    "$(printf '%s' "$approved_out" | grep 'Estimated cost:' | head -1)"
fi

for want in \
  "--dry-run" \
  "Estimated cost:" \
  "approval-gate.md" \
  "again with --approved" \
  "cannot prove"; do
  if printf '%s' "$out" | grep -qF -- "$want"; then
    pass "the message says what to do next: mentions '$want'"
  else
    fail "the refusal must be actionable: nothing mentioned '$want'" \
      "$(printf '%s' "$out" | grep -i error | head -1)"
  fi
done

# It names the subcommand the caller typed, not the function that ran. 'create'
# and 'batch' both run cmd_generate, so the naive version says "generate" to
# someone who never typed it.
out=$(bash "$TARGET" create --prompt x --duration 4 --resolution 480p \
  --out-dir "$OUT" 2>&1)
if printf '%s' "$out" | grep -qF "'create' spends real money"; then
  pass "the refusal names the subcommand the caller actually typed ('create')"
else
  fail "create's refusal must not say 'generate'" \
    "$(printf '%s' "$out" | grep -i 'spends real money' | head -1)"
fi

# Must-not-fire: the flag is read from the flag position only. A prompt is free
# text and a user may well write the word in it.
out=$(bash "$TARGET" generate --prompt "remember to pass --approved" \
  --duration 4 --resolution 480p --out-dir "$OUT" 2>&1)
if printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
  pass "--approved inside a --prompt value does not satisfy the gate"
else
  fail "the gate was satisfied by prompt text" \
    "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

# Must-not-fire: a parameter error still reports itself as a parameter error.
# If the gate ran first, an agent would learn "add --approved" as the way to
# get past a wrong duration.
out=$(bash "$TARGET" generate --prompt x --duration nope --out-dir "$OUT" 2>&1)
if printf '%s' "$out" | grep -qi 'duration' &&
  ! printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
  pass "a bad parameter is still reported as a bad parameter, not as a missing approval"
else
  fail "the gate must not preempt validation" \
    "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi
out=$(bash "$TARGET" batch --prompt x --takes 2 --duration nope --out-dir "$OUT" 2>&1)
if printf '%s' "$out" | grep -qi 'duration' &&
  ! printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
  pass "batch validates one take before the gate, so its errors read the same way"
else
  fail "batch's gate must sit behind its parameter validation" \
    "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

# ---------------------------------------------------------------------------
# With the flag, the run proceeds — including through batch and chain, which
# have to forward it to every take/shot
# ---------------------------------------------------------------------------

echo
echo "=== With --approved the run goes all the way to the request ==="

approved_case() {
  # approved_case DESC -- ARGS...
  local desc="$1"; shift 2
  local out
  out=$(bash "$TARGET" "$@" --approved 2>&1)
  if printf '%s' "$out" | grep -qi 'submitting job' &&
    ! printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
    pass "$desc"
  else
    fail "$desc" "$(printf '%s' "$out" | grep -iE "submitting|$GATE_MARK" | head -1)"
  fi
}
approved_case "generate --approved reaches the create call" -- \
  generate --prompt x --duration 4 --resolution 480p --out-dir "$OUT"
approved_case "create --approved reaches the create call" -- \
  create --prompt x --duration 4 --resolution 480p --out-dir "$OUT"
approved_case "batch --approved forwards it to take 1" -- \
  batch --prompt x --takes 2 --duration 4 --resolution 480p --out-dir "$OUT"
approved_case "chain --approved forwards it to shot 1" -- \
  chain --shot a --duration 4 --resolution 480p --out-dir "$OUT"

# ---------------------------------------------------------------------------
# Planted defects
# ---------------------------------------------------------------------------

echo
echo "=== D1: with the guard neutered, the refusal disappears ==="

BROKEN1="$WORK/broken-guard.sh"
# The guard reduced to 'always allow' — the "if false" version of itself. The
# single quotes are the point: $approved is sed's pattern, not this shell's.
# shellcheck disable=SC2016
sed 's/^  \[ -n "\$approved" \] && return 0$/  return 0  # PLANTED DEFECT/' \
  "$TARGET" > "$BROKEN1"
if [ "$(grep -c 'PLANTED DEFECT' "$BROKEN1")" -eq 1 ]; then
  pass "the defect was planted at exactly one site (require_approved's test)"
else
  fail "the plant did not apply — the assertions below would be meaningless" \
    "$(grep -c 'PLANTED DEFECT' "$BROKEN1") sites patched"
fi
out=$(bash "$BROKEN1" generate --prompt x --duration 4 --resolution 480p \
  --out-dir "$OUT" 2>&1)
if printf '%s' "$out" | grep -qi 'submitting job' &&
  ! printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
  pass "planted: generate with no --approved runs straight to the create call"
else
  fail "the planted defect changed nothing, so the guard is not what stops the run" \
    "$(printf '%s' "$out" | grep -iE "submitting|$GATE_MARK" | head -1)"
fi
for sub_args in \
  "batch --prompt x --takes 2 --duration 4 --resolution 480p" \
  "chain --shot a --duration 4 --resolution 480p"; do
  # shellcheck disable=SC2086
  out=$(bash "$BROKEN1" $sub_args --out-dir "$OUT" 2>&1)
  sub="${sub_args%% *}"
  if printf '%s' "$out" | grep -qi 'submitting job'; then
    pass "planted: $sub with no --approved submits too — all four share one guard"
  else
    fail "planted $sub should have submitted" \
      "$(printf '%s' "$out" | grep -iE 'submitting|ERROR' | head -1)"
  fi
done
# Green on the unmodified file, immediately after: the assertion above is
# discriminating, not just noisy.
out=$(bash "$TARGET" generate --prompt x --duration 4 --resolution 480p \
  --out-dir "$OUT" 2>&1)
if [ $? -eq 1 ] && printf '%s' "$out" | grep -qF -- "$GATE_MARK"; then
  pass "and the shipped file refuses again — red on the plant, green on revert"
else
  fail "the shipped file stopped refusing" "$(printf '%s' "$out" | head -2 | tr '\n' ' ')"
fi

echo
echo "=== D2: with the forwarding removed, an approved batch breaks at take 1 ==="

BROKEN2="$WORK/broken-forward.sh"
# shellcheck disable=SC2016
sed 's/^        batch_approved=1; passthrough+=("\$key"); shift; continue$/        batch_approved=1; shift; continue  # PLANTED DEFECT/' \
  "$TARGET" > "$BROKEN2"
if [ "$(grep -c 'PLANTED DEFECT' "$BROKEN2")" -eq 1 ]; then
  pass "the forwarding defect was planted at exactly one site (batch's parser)"
else
  fail "the second plant did not apply" \
    "$(grep -c 'PLANTED DEFECT' "$BROKEN2") sites patched"
fi
out=$(bash "$BROKEN2" batch --prompt x --takes 2 --duration 4 --resolution 480p \
  --out-dir "$OUT" --approved 2>&1)
if printf '%s' "$out" | grep -qF -- "$GATE_MARK" &&
  ! printf '%s' "$out" | grep -qi 'submitting job'; then
  pass "planted: an approved batch is refused by take 1's own guard instead"
else
  fail "removing the forwarding changed nothing, so it is not load-bearing" \
    "$(printf '%s' "$out" | grep -iE "submitting|$GATE_MARK" | head -1)"
fi

echo
echo "-----------------------------------------"
printf 'passed: %s   failed: %s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
