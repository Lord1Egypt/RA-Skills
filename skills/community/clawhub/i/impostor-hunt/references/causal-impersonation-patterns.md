# Causal Impersonation Patterns

This is the core knowledge asset of the skill. Each pattern is organized as:

- **Expected causal chain** — what the user's purpose requires.
- **Actual causal chain** — what the artifact actually runs.
- **Why invisible at surface** — why the surface output still looks correct.
- **Where to look** — concrete inspection sites.

Use this file during Step 6. For every main-line purpose-critical claim, walk the relevant patterns. Record both hits and misses (recording misses is what makes "Causally aligned" credible).

---

## P1 — Hardcoded return impersonating computation

- **Expected**: function computes result from inputs via a real algorithm.
- **Actual**: function returns a literal, a lookup of the test inputs, or a value derived from arguments via a trivial shortcut.
- **Why invisible**: tests pass because they use the same fixed inputs.
- **Where to look**: short function bodies for purpose-critical names; functions whose body does not reference all declared parameters; constants whose values match expected outputs.

## P2 — Test assertion matched to actual output

- **Expected**: tests encode the specification; implementation is checked against spec.
- **Actual**: tests were written *after* observing the implementation's output, so they assert what the code already does.
- **Why invisible**: tests are green.
- **Where to look**: tests with oddly specific expected values (long strings, exact floats with no rationale); commit history where test and impl land in the same commit; absence of negative tests.

## P3 — Mock leakage into production path

- **Expected**: mocks live in test setup only; production code calls real dependencies.
- **Actual**: a mock, stub, or fixture is reachable from a production code path (default arg, conditional import, env flag defaulting to mock).
- **Why invisible**: demos and tests hit the mock and succeed.
- **Where to look**: default parameter values; `if DEBUG` / `if TESTING` branches; conditional imports; in-memory fakes referenced outside `tests/`.

## P4 — Train/test leakage (data and ML)

- **Expected**: model accuracy reflects generalization to unseen data.
- **Actual**: training set overlaps with test set; features computed using future information; target encoded into a feature.
- **Why invisible**: held-out metrics look strong.
- **Where to look**: split logic; feature engineering using full dataset before split; target-derived features; time-series splits not respecting order.

## P5 — Pre-filtered data masquerading as full coverage

- **Expected**: analysis or system handles the full data distribution the user cares about.
- **Actual**: data was silently filtered (NaN drop, outlier removal, sample restriction) before the "success" was measured.
- **Why invisible**: charts and metrics look clean.
- **Where to look**: `.dropna()`, `.filter()`, `WHERE` clauses, sampling calls, early `continue`/`skip` in loops.

## P6 — Configured but not read

- **Expected**: a configuration item changes runtime behavior.
- **Actual**: the config exists in a file but no code path reads it, or reads it then ignores it.
- **Why invisible**: the config file is present, well-formatted, and reviewed.
- **Where to look**: search for the config key as a string across the codebase; verify call sites actually branch on the value.

## P7 — Swallowed exception faking success

- **Expected**: failures surface as errors.
- **Actual**: `try`/`except` (or `catch`) around the critical step silently passes, often with a misleading default return.
- **Why invisible**: process exits 0; logs show no error.
- **Where to look**: broad `except Exception:` / `catch (...)`; bare `except:`; empty catch blocks; `return None`/`return []` in except branches on purpose-critical functions.

## P8 — Log says success, return code unchecked

- **Expected**: downstream behavior reflects upstream success.
- **Actual**: upstream subprocess fails (non-zero exit) but the wrapper only inspects stdout for a "success" string, or doesn't check at all.
- **Why invisible**: the success message is present in the log.
- **Where to look**: subprocess calls without `check=True` / return-code inspection; log-grep based success criteria; CI steps with `|| true`.

## P9 — Happy-path-only implementation

- **Expected**: the system handles the realistic input distribution including failures, edge cases, partial states.
- **Actual**: only the canonical input shape works. Empty input, large input, concurrent access, retries, partial failures are unhandled or crash silently.
- **Why invisible**: demo input is canonical.
- **Where to look**: absence of empty/boundary/error tests; no retry/timeout logic on I/O; no idempotency on writes; no transaction rollback paths.

## P10 — Correlation relabeled as causation

- **Expected**: causal claim is supported by a design that isolates the cause.
- **Actual**: a correlation is observed and described in causal language ("drove", "caused", "because of") without controls, counterfactual, or mechanism.
- **Why invisible**: the correlation is real; the prose reads as analysis.
- **Where to look**: any "X caused Y" claim in reports; absence of a comparison group, an intervention, or a mechanistic explanation linking X to Y.

## P11 — Static demo impersonating dynamic system

- **Expected**: the system operates over time/state/users.
- **Actual**: the working demo is a fixed snapshot — hardcoded date, pre-baked state, single-user, no persistence.
- **Why invisible**: the demo runs and looks like the real thing.
- **Where to look**: `now()` replaced by a constant; state initialized to a fixed dict; absence of write paths; single-tenant assumptions.

## P12 — Name-matches-but-semantics-differ

- **Expected**: a field/function/metric named X has the meaning X conventionally implies.
- **Actual**: the implementation of X computes something materially different (e.g. `accuracy` is actually F1 on a filtered subset; `revenue` excludes refunds without note).
- **Why invisible**: the name is correct and consistent; reviewers don't open the definition.
- **Where to look**: definitions of any named metric/field used in the verdict; cross-check against the user's likely understanding of the term.

## P13 — Validation that cannot fail

- **Expected**: validation step can reject bad outputs.
- **Actual**: the "validation" is tautological — checks that the output equals itself, or asserts properties guaranteed by construction.
- **Why invisible**: validation passes.
- **Where to look**: assertions of the form `assert f(x) == f(x)`; schema checks against a schema derived from the output; "tests" that re-run the production code and check it ran.

## P14 — Capability claim backed only by example

- **Expected**: claim of general capability is backed by general evidence.
- **Actual**: one or two cherry-picked examples are presented as proof of a broad claim ("the agent can refactor code" supported by one successful refactor).
- **Why invisible**: the example genuinely works.
- **Where to look**: any sweeping capability claim with single-instance evidence; absence of failure-case enumeration.

## P15 — Reused output impersonating fresh computation

- **Expected**: each run produces a fresh result for current inputs.
- **Actual**: results are cached, memoized, or copied from a prior run, and the cache key does not include the relevant inputs.
- **Why invisible**: outputs are produced quickly and look reasonable.
- **Where to look**: caches keyed on partial inputs; written-out result files reused without regeneration check; "fast" suspicious latency on what should be expensive computation.

---

## How to use during Step 6

For each main-line purpose-critical claim:

1. Pick the 3–6 patterns most likely to apply given the artifact type.
2. For each picked pattern, fill the three rows: expected chain / actual chain / why surface still looks correct.
3. Record the inspection sites you checked (file paths, function names, query lines).
4. State the conclusion for that pattern: **hit / clean / cannot determine**.

A "Causally aligned" verdict in Step 9 must reference at least 3–5 patterns marked **clean** with named inspection sites.
