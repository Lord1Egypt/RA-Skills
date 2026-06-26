---
name: gstack-openclaw-diagnose
description: "Structured diagnosis for hard bugs and performance regressions. Builds a deterministic feedback loop FIRST, then reproduces, hypothesises (3-5 ranked), instruments, fixes with regression test, cleans up. Use when: bug resists a quick fix, flaky failure, performance regression, user has tried 2+ things, or user says diagnose."
---

# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

**Core insight:** If you have a fast, deterministic, agent-runnable pass/fail
signal for the bug, you will find the cause. Everything else is mechanical.
If you don't have one, no amount of staring at code will save you.

## Phase 1 — Build a feedback loop

**This is the skill.** Spend disproportionate effort here.

### Construction strategies — try roughly in this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real request/payload/event log to disk; replay through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) exercising the bug path with a single function call.
7. **Property / fuzz loop.** "Sometimes wrong output" → run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** Bug appeared between two known states → automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Same input through old-version vs new-version (or two configs), diff outputs.
10. **HITL script.** Last resort. If a human must click, drive them with a structured bash script so the loop is still reproducible. Captured output feeds back to you.

### Iterate on the loop itself

Treat the loop as a product:
- **Faster?** Cache setup, skip unrelated init, narrow scope.
- **Sharper signal?** Assert on the specific symptom, not "didn't crash."
- **More deterministic?** Pin time, seed RNG, isolate filesystem, freeze network.

A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.

### Non-deterministic bugs

Goal: raise reproduction rate. Loop 100x, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake is debuggable; 1% is not.

### When you genuinely cannot build a loop

Stop and say so. List what you tried. Ask the user for:
(a) access to the reproducing environment,
(b) a captured artifact (HAR file, log dump, core dump, screen recording), or
(c) permission to add temporary production instrumentation.
Do NOT proceed to hypothesise without a loop.

## Phase 2 — Reproduce

Run the loop. Watch the bug appear. Confirm:

- The failure matches what the **user** described — not a nearby different failure.
- Reproducible across multiple runs (or high enough rate for non-deterministic bugs).
- Exact symptom captured (error message, wrong output, timing) for later verification.

## Phase 3 — Hypothesise

Generate **3-5 ranked hypotheses** before testing any. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**:
> "If <X> is the cause, then <changing Y> will make it disappear / <changing Z> will make it worse."

If you can't state the prediction, the hypothesis is a vibe — discard or sharpen it.

Show the ranked list to the user before testing. They often re-rank instantly with domain knowledge. Don't block — proceed with your ranking if AFK.

## Phase 4 — Instrument

Each probe maps to a specific prediction from Phase 3. **One variable at a time.**

Tool preference:
1. **Debugger / REPL** if available. One breakpoint beats ten logs.
2. **Targeted logs** at boundaries that distinguish hypotheses.
3. Never "log everything and grep."

**Tag every debug log** with a unique prefix: `[DEBUG-a4f2]`. Cleanup = single grep. Untagged logs survive; tagged logs die.

**Performance bugs:** logs are usually wrong. Establish a baseline measurement (timing harness, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix + regression test

Write the regression test **before the fix** — but only if there's a correct seam.

A correct seam exercises the real bug pattern as it occurs at the call site. If the only seam is too shallow, a regression test there gives false confidence.

If no correct seam exists, that itself is the finding — note it.

1. Turn the minimised repro into a failing test at the seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original scenario.

## Phase 6 — Cleanup + post-mortem

Before declaring done:

- Original repro no longer reproduces (re-run Phase 1 loop)
- Regression test passes (or absence of seam is documented)
- All `[DEBUG-...]` instrumentation removed (grep the prefix)
- Throwaway harnesses deleted
- Root cause stated in the commit/PR message

Then ask: **what would have prevented this bug?** If the answer involves architectural change, note it for the user — don't bundle it into this fix.

## Completion Status

- **DONE** — root cause found, fix applied, regression test written, all tests pass
- **DONE_WITH_CONCERNS** — fixed but cannot fully verify (intermittent, needs staging)
- **BLOCKED** — root cause unclear after investigation, escalated
