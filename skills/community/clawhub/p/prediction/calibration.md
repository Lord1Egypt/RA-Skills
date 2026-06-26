# Calibration and Confidence

Use this file when choosing the actual probability or scenario weights.

## Probability ladder

| Probability | Meaning |
|-------------|---------|
| 5-15% | clear long shot |
| 20-35% | plausible but against the base rate |
| 40-60% | genuinely uncertain |
| 65-80% | favored but far from locked |
| 85-95% | strong edge with limited remaining uncertainty |

Avoid 0%, 100%, or any false precision unless the resolution is already effectively known.

## Calibration rules

- If the evidence is thin, stay near the base rate.
- If a key assumption is unverified, cap confidence.
- If multiple strong unknowns remain, widen the range instead of pretending a precise point estimate exists.
- If the forecast depends on one brittle driver, say that explicitly.

## When to abstain

Hold a low-confidence or no-call position when:
- the question is not resolvable
- the reference class is nonexistent or deeply mismatched
- the forecast horizon is undefined
- critical evidence is missing and cannot be estimated responsibly
- the user really needs domain advice rather than a forecast

## Update triggers

Update only when:
- the deadline or threshold changes
- new evidence changes the reference class
- a key driver flips from bullish to bearish or vice versa
- the prior forecast is now obviously stale

Noisy headlines alone are not enough.
