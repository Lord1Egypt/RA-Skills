# Discriminating tests — the real proof of correctness

Gate 8c says tests must derive from acceptance criteria, not from what the code
happens to do. This file covers the *how*: writing tests that actually prove the
rule, vs tests that pass against the bug too.

## Core principle

A test is valuable only if it FAILS on at least one plausible WRONG implementation.
If a test passes under both the correct implementation and a naive/wrong one, it is
tautological — it proves nothing. A green suite of only non-discriminating tests is
false security: it passes against the bug too.

**Two axes of "derived from spec, not code":**

1. **Timing (tests-first vs tests-after)** — covered by the `test-driven-development`
   skill. Write the test before the implementation.
2. **Source of expected values (spec vs code)** — separate axis, easy to miss even
   when timing is right. A test written *first* but by glancing at existing code or
   a reference implementation and confirming what it does is tests-after in disguise.
   Expected values must come from the spec/requirements/acceptance criteria, never
   from reading the implementation (current OR reference). The user names this rule
   explicitly as "tests derived from spec, not from code."

Both axes must be spec, not code.

## When the behavior has a known wrong alternative

Most correctness rules have a tempting wrong implementation: a naive default, a
common bug, a shortcut. (Banker's rounding vs round-half-up; off-by-one boundary
vs inclusive boundary; idempotency-on-first-call vs idempotency-on-every-call;
authorization-before-action vs authorization-then-action-with-rollback.)

Procedure:

1. **Identify the discriminating cases** — inputs where correct behavior diverges
   from the wrong implementation. These are the tests that actually test the rule.
2. **Mark them** in a comment (`# DISCRIMINATING`) and note what the wrong impl would
   produce, so a future reader (or reviewer) knows which tests carry the proof.
3. **Keep non-discriminating cases too** (where both impls agree) for coverage and
   regression protection — but recognize they are NOT the proof. Don't let a green
   non-discriminating suite fool you.
4. **Confirm in RED** that exactly the discriminating tests fail against the wrong
   impl (or the absent feature). A discriminating test that doesn't fail red is not
   discriminating — fix it or drop it. Non-discriminating tests may pass red-side;
   that's expected and fine.
5. **Go green** only after the discriminating tests fail for the right reason.

## Worked example — banker's rounding (session 2026-07-20)

Spec: round half to even (IEEE 754 default). Naive wrong impl: `ROUND_HALF_UP`.

| Input | Spec | Wrong (half-up) | Discriminating? |
|-------|------|-----------------|-----------------|
| 2.345  | 2.34  | 2.35  | YES |
| 0.125  | 0.12  | 0.13  | YES |
| 1.005  | 1.00  | 1.01  | YES |
| 0.025  | 0.02  | 0.03  | YES |
| -0.125 | -0.12 | -0.13 | YES (symmetry about zero, not "away from zero") |
| 2.344  | 2.34  | 2.34  | no  |
| 2.346  | 2.35  | 2.35  | no  |
| 2.34 (2dp already) | 2.34 | 2.34 | no |

The five YES rows are the proof. A suite of only the `no` rows would pass against
`ROUND_HALF_UP` and prove nothing. RED confirmed: exactly the five discriminating
tests failed against the wrong impl; the five non-discriminating passed (expected).
GREEN after swapping `ROUND_HALF_UP` → `ROUND_HALF_EVEN`: all 10 pass.

## Anti-patterns

- **Confirm-the-implementation tests** — expected value copied from reading the code
  under test. Passes by construction. Reject in review.
- **Only non-discriminating cases** — green against the wrong impl. Add the
  discriminating cases or the test isn't proving the rule.
- **Discriminating test that doesn't go red** — either the test is wrong, or the
  "wrong impl" you imagined isn't actually wrong. Resolve before proceeding.
- **Over-mocking** — if you mock the system under test, you test the mock, not the
  rule. Discriminating tests need real code on real inputs.

## Pitfall — float contamination in decimal-precision tests

When the function under test rounds to N decimal places, NEVER use a literal float
like `2.345` as the test input. Binary floating point cannot represent most decimal
fractions exactly: `2.345` is stored as `2.344999999999999643...`, so a naïve
`round(2.345, 2)` may return `2.34` instead of `2.35`, and the test outcome depends
on the implementation quirk, not the rounding rule.

Correct: pass exact values via `Decimal("...")` (or `Fraction`) so the tie case is
exactly on the boundary and the test proves the rule, not the representation artifact.

Bad:
    assert banker_round(2.345, 2) == expected   # 2.345 is already imprecise
    assert banker_round(1.225, 2) == expected

Good:
    assert banker_round(Decimal("2.345"), 2) == expected
    assert banker_round(Decimal("1.225"), 2) == expected

Same rule applies whenever the acceptance criterion is about decimal-places
quantization, truncation, or rounding.

## When there is no known wrong alternative

Not every test has a clean discriminating counterpart (e.g. "function returns the
sum of two numbers" has no tempting wrong impl beyond a typo). In that case the
discriminating concept degenerates to "the test fails when the feature is absent"
(the standard RED gate). The technique matters most when a wrong impl is plausible
enough that someone might ship it.
