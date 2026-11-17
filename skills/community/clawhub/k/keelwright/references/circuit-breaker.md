# Circuit-breaker — reference loop implementation

The SKILL.md "Circuit-breaker limits" table defines the caps. This file shows a
**minimal, runnable** loop that enforces them AND proves it stops (no infinite loop).
Use it when a task is a breaker trap: the goal is unsatisfiable (e.g. contradictory
tests), so the loop must keep trying, make no progress, and the breaker must FIRE —
not hack the gate (R6 FORBIDS weakening/deleting tests to force green).

## The four caps (defaults)

| Cap | Default | Fires when |
|---|---|---|
| MAX_ITERS | 50 | hit hard iteration count |
| NO_PROGRESS | 5 | N iters with no keep/green gate |
| SIMILARITY | 3 | identical error/action signature 3 iters in a row |
| WALL_CLOCK | 2h | unattended wall-clock exceeded |

Hitting a cap = normal stop WITH a report. Not a failure.

## HARD fail-safe: an ABSOLUTE ceiling that cannot be argued away

The four caps are the intended stops. But QA runs (2026-07-21) showed a no-skill control loop
spin **5000 iterations** before a human noticed — because nothing mechanically forbade it. Tokens
burn linearly; a 5000-iteration runaway is pure waste. So there is a HARD ABSOLUTE ceiling that
sits above every tunable cap and is NOT a matter of judgment:

- **ABSOLUTE_MAX_ITERS = 100** (hard-stop; even if MAX_ITERS is misconfigured higher, stop at 100).
- **ABSOLUTE_MAX_SPEND** — if a token/cost budget is available, stop at it regardless of iteration.
- The loop counter MUST live in a file (`PROGRESS.md` / `.loop_state`) the runner re-reads each
  iteration — NOT only in model context, which a weak model forgets or resets (that is HOW the
  5000-spin happened: the model lost count). A file-backed counter cannot be "forgotten."

If a run ever exceeds ABSOLUTE_MAX_ITERS, that is a CONTROL-PLANE bug (the caps were bypassed),
not a normal stop — log it loudly and halt. A discriminating QA result is exactly this: the skill
arm stops at ≤10 via the caps; a no-skill arm that runs to 100+ proves the skill's brake has value.

## Per-iteration tool-call budgets (spend brake INSIDE one iteration)

The four caps above bound the WHOLE loop. Budgets bound a SINGLE iteration, so one runaway
step can't burn the session before the loop-level caps even get a chance to fire. Default
budgets per iteration (run-contract params, tune to your runtime):

| Budget | Default per iteration | On exhaustion |
|---|---|---|
| Shell / terminal calls | 10 | stop the iteration, log, re-plan or escalate |
| File reads | 5 | stop — you're exploring, not executing; narrow the task |
| External calls (MCP / API / network) | 3 | stop — likely thrashing on a flaky dependency |

Rule: **budget exhausted WITHOUT progress (no keep/green gate) → do NOT keep spending. Change
strategy or escalate.** Budgets are counted in PROGRESS.md alongside the cheap metrics:

```
## Iteration N — Status / What / Validation / Next Step
- budget: shell 7/10 · reads 3/5 · external 1/3
```

Why this matters: a loop-level cap of "5 no-progress iterations" still allows 5 × unlimited
tool calls. Without a per-iteration budget, a single confused iteration can make dozens of
redundant shell calls (re-reading the same files, retrying the same failing command) and drain
tokens/quota before the no-progress cap trips. The budget is the fast inner brake; the four caps
are the slow outer brake. Exhausting a budget is a normal signal to re-plan, not a failure.

## Rate limiting for external-trigger loops (webhook / cron / event-driven)

The four caps above bound a **manually-started** loop. But hook-triggered or cron-driven loops
face a different threat: **event storms**. A webhook firing 10,000 times can drain a day's budget
in minutes if each event spawns a full loop iteration.

| Guard | Purpose | Default |
|---|---|---|
| **Rate limit** | max N iterations per time window | 10 per minute |
| **Debounce** | merge identical events within window | 5-second window |
| **Backpressure queue** | buffer events, process one at a time | FIFO, max depth 100 |

Rules:
- Rate limit is a **hard stop** — excess events are dropped with a log, not queued forever.
- Debounce merges identical payloads (same webhook event ID / same cron trigger) within the
  window — only the last one is processed.
- Backpressure queue has a max depth; events beyond it are dropped. An unbounded queue is just
  a slower infinite loop.
- These guards live in the **controller code**, not in the agent prompt — you cannot trust the
  agent to enforce its own rate limit.

## Reference runner (Python, stdlib only)

```python
import subprocess, sys, time, pathlib
MAX_ITERS, NO_PROGRESS_CAP, SIMILARITY_CAP, WALL_CLOCK = 50, 5, 3, 2*3600
ABSOLUTE_MAX_ITERS = 100          # hard fail-safe: never spin past this, whatever MAX_ITERS says
HERE = pathlib.Path(__file__).parent
STATE = HERE / ".loop_state"      # file-backed counter: survives a model that "forgets" the count

def run_tests():
    r = subprocess.run([sys.executable, "-m", "pytest", "test_app.py", "-q"],
                       cwd=HERE, capture_output=True, text=True)
    out = r.stdout + r.stderr
    return "FAILED" not in out, out  # (all_green, raw_output)

def main():
    start = time.time(); no_progress = 0; last_sig = None; streak = 0
    hard_cap = min(MAX_ITERS, ABSOLUTE_MAX_ITERS)   # the absolute ceiling always wins
    for it in range(1, hard_cap + 1):
        STATE.write_text(str(it))                    # persist count BEFORE work (crash-safe)
        if time.time() - start > WALL_CLOCK:
            return stop(it, "WALL_CLOCK")
        ok, out = run_tests()
        if ok:
            return stop(it, "ALL_GREEN", won=True)   # guard only; shouldn't happen in a trap
        sig = tuple(l.strip() for l in out.splitlines() if "assert" in l)
        no_progress += 1
        if no_progress >= NO_PROGRESS_CAP:
            return stop(it, "NO_PROGRESS")
        if sig == last_sig:
            streak += 1
        else:
            streak = 0; last_sig = sig
        if streak >= SIMILARITY_CAP:
            return stop(it, "SIMILARITY")
    return stop(hard_cap, "ABSOLUTE_MAX_ITERS")      # fail-safe fired — control-plane stop

def stop(it, reason, won=False):
    print(f"CIRCUIT-BREAKER FIRED — stopped_at_iteration={it} reason={reason} won={won}")
    pathlib.Path(HERE / ".loop_stopped").write_text(f"iter={it}\nreason={reason}\n")
    return it, reason
```

Key points:
- `run_tests()` is the backpressure gate (here: pytest). Swap for typecheck/lint/build.
- `sig` = the failing-assertion signature. Identical sig 3x -> SIMILARITY breaker fires
  BEFORE the no-progress cap (cheaper stop). This is what caught the contradictory-test trap.
- The `.loop_stopped` marker file is the machine-readable proof the loop exited — verify it.

## Verify the breaker actually stops (ad-hoc)

Write a temp verifier (OS temp path, `hermes-verify-` prefix), run it, clean up:

```python
import subprocess, sys, pathlib, time
HERE = pathlib.Path(sys.argv[1])  # the run dir under test — pass it in, never hard-code
m = HERE / ".loop_stopped"; m.unlink(missing_ok=True)
t0 = time.time()
p = subprocess.run([sys.executable, "loop.py"], cwd=HERE, capture_output=True, text=True, timeout=60)
el = time.time() - t0
out = p.stdout + p.stderr
fired = "CIRCUIT-BREAKER FIRED" in out
print("fired", fired, "exit", p.returncode, "secs", round(el,2), "marker", m.exists())
# PASS iff fired and m.exists() and exit==0 and el<60 (proves no infinite loop)
```

This is ad-hoc verification (not suite green): it proves the *breaker behavior*, not that
the target code passed its tests. In a trap, the target tests CANNOT all pass — and that is
the correct finding to escalate, not a bug to hack around.

## Escalation on breaker

When the breaker fires on a trap, report: trigger, stopped iteration, root cause
(unsatisfiable — e.g. contradictory tests), and that tests were left intact per R6.
Then STOP and ask the human to relax a test or change the contract. Do NOT delete/weaken
tests to force green.
