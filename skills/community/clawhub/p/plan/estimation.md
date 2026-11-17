# Estimation — Ranges, Spikes, Calibration

An estimate is a prediction with stated uncertainty. Everything here serves one output: a range whose width is honest and whose high end has a name.

## Ranges, Not Points

- Point estimates read as commitments and hide uncertainty (SKILL.md, Traps).
- Low = everything known works. High = the named risks fire. A high end with no nameable driver is padding — name it: "high end fires if the API needs an auth change."
- Ratio rule (canonical: SKILL.md, Core Rules): high/low ratio >3x means it is not an estimate, it is an unknown — spike first. 2-8h (4x) → spike; 3-6h (2x) → plan.

## Building the Range

1. Estimate per step (each its own low-high), then sum lows and sum highs.
2. Check the summed ratio against the 3x rule at plan level.
3. Correlation check: one wrong assumption usually hits several steps at once, so when steps share an assumption the true high exceeds the sum. Name the shared assumption as the range driver instead of widening silently.
4. Outside view (Kahneman's planning fallacy: inside-view step-summing is systematically optimistic): the agent's outside view is its own outcome log — per-type actual-vs-estimate history (`outcomes.md`). If the log says this task type runs 2x its estimates, multiply before presenting, and say you did.

## Buffers

One buffer at plan level, never per step. Per-step buffers get silently consumed and hide the real range; the plan-level buffer already exists — it is the gap between low and high. If you feel the need to add a separate "buffer" line, your high was actually a low.

## Anchors

- The user's hoped-for number ("should be quick, right?") is an anchor, not data. Compute from steps first, compare after, state the difference plainly with its driver — never adjust your sum toward the hope.
- Your own first glance anchors too: write per-step estimates before totaling, not after deciding what the total "should" be.

## Novel Work

- No reference class and no decomposable steps → timebox, not estimate. A timebox caps spend ("2h to learn whether X is feasible"); an estimate predicts it. Presenting a timebox as an estimate is how "about 2 hours" becomes a broken promise.
- The spike's answer re-estimates the plan (`strategies.md`, Spike-First) — the post-spike range is the real one; the pre-spike range was a placeholder.

## Re-Estimating Mid-Plan

After a deviation or replan, re-estimate remaining steps only; the original number is sunk and defending it compounds the error. Report all three parts: "original 3-6h; 2h spent; remaining now 4-8h because [driver]." Estimate drift is itself a deviation — it feeds the replan trigger (`replanning.md`).

## Calibration Loop

Every L2+ outcome records estimate and actual (`outcomes.md`). At review, compare per type: consistent overrun in one type = that type's multiplier for next time; overrun everywhere = your lows describe the best case, not the likely one. This log is the only calibration data an agent has — an unlogged actual is a calibration point burned.
