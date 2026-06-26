# Mythos Skill — Tests

## Calibration approach: manual, structural-only

Mythos reasoning quality cannot be verified purely programmatically — it depends on whether the right lenses were applied to the actual primary drivers of a question, which requires judging the question itself. What **can** be tested are the **structural properties** the protocol is supposed to preserve:

- Lens completeness (did the right lenses fire?)
- Round count within Prelude budget
- Parallel vs sequential dispatch in Agent mode (must be parallel)
- Convergence detection (did it stop on a real signal, or run to max rounds by default?)
- E-injection (was the original question re-read each round?)

These are testable. Reasoning quality is not.

## Calibration script

The calibration runner lives in the **source repository only** at `install/calibrate.ps1` and `install/calibrate.sh` — it is not bundled with the marketplace skill package. Clone [the source repo](https://github.com/chitinlabs/mythos-skill) if you want to run calibration yourself.

The runner walks **5 calibration cases** interactively. For each case, the script asks the operator what lens path / round count / convergence behavior was observed, runs structural checks, and emits a timestamped report (`calibration-report-YYYYMMDD-HHMM.md`) next to itself.

The 5 cases cover different problem shapes:

| Case | Shape | Expected mode |
|---|---|---|
| 1. SQLite vs Postgres for a small SaaS | technical decision | Silent |
| 2. Pivot or stay | strategic tradeoff | Silent or Trace |
| 3. Cache strategy | multi-driver design | Silent → may upgrade to Agent |
| 4. Code-review process improvement | process change | Trace |
| 5. AI training-data ethics | contentious topic | Trace (Steelman opens) |

## Run the calibration

From the source repo root:

**Windows (PowerShell):**

```
install/calibrate.ps1
```

**macOS / Linux:**

```
bash install/calibrate.sh
```

The script generates a `calibration-report-YYYYMMDD-HHMM.md` next to itself. Reports are gitignored (local-only artifacts).

## Interpreting FAIL counts

A FAIL count is a **signal to re-read SKILL.md**, not test ground truth. If a calibration case fails, the diagnosis is almost always one of:

- Routing logic drifted (complexity score computed after keyword parse, not before)
- Standard rotation silently changed without a Lens-sequence justification in the Prelude
- Convergence detection skipped the negative-delta criterion
- Agent mode dispatched lenses sequentially instead of as parallel subagents

Re-read SKILL.md against these specifically. The skill is judged by the operator, not by an automated grader.

## Why no programmatic eval

Three structural reasons:

1. **Output format varies by mode.** Silent emits only a Coda; Trace emits the full per-round chain; Agent emits a merge. A single golden-output match would conflate format with quality.
2. **Quality depends on lens-question fit.** Whether the right lenses were applied requires judging the *question's* primary drivers — which is itself a reasoning task.
3. **Convergence is judged on substance**, not surface metrics. "Did the new round actually add something?" cannot be answered by token-count or embedding-similarity heuristics.

If you have a robust approach to programmatically evaluating multi-round reasoning quality that does not reduce to golden-output matching, please open an issue — this is an area where the project would genuinely benefit from external input.
