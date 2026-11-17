# Flake — Measure, Classify, Fix, Quarantine

A flaky test is a test whose result depends on something you did not declare. Fixing it starts with a number, not an opinion.

## Why It Matters Arithmetically

For a per-test failure probability p across N tests, a full run is red with probability **1 − (1 − p)^N**.

| p (per test) | N = 100 | N = 300 | N = 1000 |
|---|---|---|---|
| 0.001 (1 in 1000) | 10% | 26% | 63% |
| 0.005 (1 in 200) | 39% | 78% | 99% |
| 0.01 (1 in 100) | 63% | 95% | ~100% |

One test failing 1 run in 200 makes a 300-test suite red 78% of the time. That is why "it's just one flaky test" is never true at scale, and why the fix target is p per test, not the red-run rate.

Retries turn p into roughly p^(retries+1) for the run outcome — 2 retries take p = 0.005 to about 1.25 × 10⁻⁷ — at the cost of 3× wall time whenever it fires, and total blindness to the underlying race. Retries are a shock absorber, not a fix.

## Measure Before Touching Anything

```bash
npx playwright test -g "checkout" --repeat-each=50 --workers=1   # is it the test?
npx playwright test -g "checkout" --repeat-each=50 --workers=4   # is it concurrency?
npx playwright test --repeat-each=5                              # suite-wide baseline
```

**Rule of three**: zero failures in n runs bounds p below roughly 3/n at 95% confidence. 20 clean runs only proves p ≤ 15% — useless for a 1-in-200 flake. 50 runs → p ≤ 6%. 100 runs → p ≤ 3%. To confirm a fix on a rare flake you need runs proportional to its rarity, or you need to prove the mechanism instead.

Proving the mechanism is usually cheaper: find the race in the trace, show why it can happen, fix that. Then 20 runs is confirmation rather than evidence.

## The Six Causes

| Cause | Signature | Fix |
|---|---|---|
| **Timing race** | Fails on slow runners, passes headed | Assert on the state, never sleep (`waiting.md`) |
| **Test interdependence** | Passes alone, fails in the suite; changes with `--workers` | One account per worker, per-test data (`auth.md`) |
| **Non-deterministic data** | Fails around midnight, month end, or on a specific seed | Freeze the clock, seed fixed data, use relative assertions |
| **Third-party or network** | Fails in bursts, matching an upstream incident | Mock it (`network.md`); test the integration in one dedicated spec |
| **Animation and layout** | Click lands on the wrong element; screenshot diffs jitter | Disable animations; wait for stability (`visual.md`) |
| **Real product race** | Reproduces manually if you try hard enough | File the bug — the test is doing its job |

Order of suspicion when you have no evidence: interdependence → timing → data → third party. Interdependence first because `--workers=1` distinguishes it in one run.

## Isolation Bisection

```bash
npx playwright test --workers=1                # serial: still flaky? not concurrency
npx playwright test --workers=1 -g "^A$|^B$"   # pair suspects to find the polluter
npx playwright test --repeat-each=10 -g "A"    # confirm A alone is clean
```

The polluter is usually the test **before** the failing one. Common leaks: a created record with a unique constraint, a global feature flag toggled server-side, a shared account whose session was invalidated by another test's logout, a mailbox with more messages than expected.

## Non-Determinism To Remove

```typescript
// Fixed clock (Playwright's own clock control, playwright >=1.45; also works for polling and animations)
await page.clock.setFixedTime(new Date('2026-03-01T10:00:00Z'));

// Fixed locale and timezone at the project level
use: { locale: 'en-US', timezoneId: 'UTC' }

// Kill animations for the run
await page.addStyleTag({ content: `*, *::before, *::after {
  animation-duration: 0s !important; transition-duration: 0s !important; }` });

// Deterministic randomness in the app under test: seed it via an init script or a query param
```

Anything the app reads that you did not set — clock, timezone, locale, random seed, network latency, feature flags — is a coin flip you inherited.

## Quarantine Policy

A quarantine without an expiry is a graveyard. Workable rule:

1. Tag it: `test('checkout @flaky', ...)`, with a linked issue in the annotation.
2. CI runs `--grep-invert @flaky` on the blocking job and `--grep @flaky` in a non-blocking one, so coverage is not lost (`ci-cd.md` gates).
3. Cap the quarantine: a fixed budget (for example 1% of the suite) and a deadline per test — the `Cadence` preference area in SKILL.md is where a team's own limit is recorded. Past the deadline, the test is fixed or deleted; a permanently quarantined test is a maintenance cost with no signal.
4. Report the flaky count per run. The number, not the sentiment, is the health metric.

Tag versus annotation: `@flaky` means "runs, may be red, does not block". A test that is reliably broken is not flaky — mark it `test.fixme` so it does not run at all and still shows in the report, or `test.fail()` when the failure is the assertion (`testing.md`). Deleting it instead is how coverage disappears without a decision.

## Prevention

- New test must pass `--repeat-each=10 --workers=4` before merge; that catches interdependence and the fastest races at negligible cost.
- No new `waitForTimeout` in review — grep for it in CI if you have to.
- Every test creates its own data and cleans nothing it did not create.
- Third-party calls mocked by default; a single opt-in `@integration` spec exercises the real integration on a schedule, not on every PR (`ci-cd.md` gates).
