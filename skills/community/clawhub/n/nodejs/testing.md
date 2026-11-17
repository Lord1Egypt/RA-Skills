# Testing — Runners, Isolation, and Flake

## Choosing the Runner

- `node:test` is stable on node >=20: native ESM, no transform layer, no mock hoisting magic — default it for new libraries. Jest earns its weight on existing suites and heavy matcher/snapshot use; Vitest fits projects already running a Vite pipeline (→ SKILL.md Where Experts Disagree).
- `node --test` discovers `*.test.js` and friends and runs each file in its own process; `--test-reporter` selects the output format (a machine-readable one for CI), `--test-concurrency` controls parallelism, and `--test-only`/`--test-name-pattern` narrow a run. Coverage flags exist but have moved between majors — check the flag on your target version rather than copying a snippet.
- Assertions: `node:assert/strict` (`assert.deepStrictEqual`) is enough for most libraries; a matcher library is a preference, not a requirement.
- Whatever the runner, the suite must be runnable with one command, from a clean checkout, with no external service — anything else erodes into "run it on CI and see".

## Isolation (where flake actually comes from)

- Parallel test files: bind servers to port 0 and read `server.address().port`. Hardcoded ports mean EADDRINUSE under parallel runners — the classic "passes alone, fails in CI" (→ `debug.md`).
- The same rule applies to every shared name: temp directories (`mkdtemp`), database schemas, queue names, and cache prefixes must be per-run unique, not per-suite constant.
- Module-level state is shared within a file: a cache mutated by test 1 silently changes test 2. Reset modules between tests, or import a fresh instance via dynamic `import()`.
- Tests that must run in a fixed order are already broken — the ordering is a hidden dependency the runner is free to change. Make setup explicit per test.
- Clean up in a hook that runs on failure too (`after`/`afterEach`, not the end of the test body), or one failing test poisons every later one.
- Global mutations leak across files in the same process: `process.env`, `Date`, `Math.random`, and prototype patches. Save and restore, or set them in a per-file setup that the runner isolates.

## Async Assertions

- A missing `await` lets the test pass before the assertion runs — the failure surfaces as an unhandled rejection after the suite went green. Lint test files with `no-floating-promises` too.
- Assert on rejection with the runner's own helper (`assert.rejects`, `expect(...).rejects`), never a try/catch whose `catch` block might simply not run — a test that passes when nothing throws is not testing anything.
- Never assert "after a delay": `setTimeout(..., 100)` in a test is a race that passes on your laptop and fails on a loaded CI box. Wait on the actual event, poll with a deadline, or expose a hook.
- Fake timers don't advance microtasks: after `advanceTimersByTime`, pending promise callbacks still haven't run — use the async variant (`advanceTimersByTimeAsync`), or `await Promise.resolve()` before asserting.
- Unfinished work at the end of a test (an open server, a live interval, a pending request) keeps the worker alive and turns "suite passed" into "suite hangs". If the runner reports open handles, treat it as a failure.

## Mocks

- Mock the boundary, not the internals: HTTP calls, the clock, the filesystem, the queue. Mocking your own module's internal function pins the implementation and makes every refactor a test rewrite.
- `jest.mock()` is hoisted above imports — its factory cannot close over file-level variables; use `jest.doMock` when it must.
- Mock state persists between tests — set `clearMocks`/`restoreMocks: true` once in config instead of remembering `clearAllMocks()` in every file. `node:test` mocks reset per test file, not per test: call `mock.reset()` in a hook.
- ESM cannot be re-bound at runtime the way CJS can: mocking an ESM import needs the runner's loader support or dependency injection. Passing a collaborator into a constructor removes the whole problem and is usually the better design (→ `modules.md`).
- Freezing time makes date-dependent tests deterministic — and hides timezone bugs. Run the suite once under a non-UTC `TZ` before trusting date logic.
- A mock that returns a happy path only tests the happy path. Assert the failure branch with a mock that rejects, times out, or returns a partial payload.

## Integration and Fixtures

- Prefer a real dependency in a container over an in-memory fake for databases: SQL dialects, index behavior, and transaction semantics are exactly what an in-memory substitute gets wrong.
- Roll back or recreate state per test rather than sharing a seeded database: shared fixtures produce tests that depend on each other's leftovers.
- HTTP: test through the app's real routing (`server.listen(0)` plus a real request) instead of calling handlers with fabricated request objects — half the bugs live in parsing, routing, and middleware order.
- Snapshots are for output whose shape you would otherwise not review: keep them small enough to read in a diff. A 200-line snapshot gets rubber-stamped, which is worse than no assertion.
- `toBe` is `===` and fails on structurally equal objects; use the structural comparison (`toEqual`, `deepStrictEqual`) and be aware it ignores `undefined` properties in some runners — assert on the exact key set when that matters.

## In CI

- `npm ci`, never `npm install` (SKILL.md rule 6), and pin the Node major to the one production runs (→ `runtime.md`).
- Run the suite with the production module format and NODE_ENV once per pipeline; a suite that only ever runs in development mode never tests the code path that ships.
- Fail on unhandled rejections and open handles rather than tolerating warnings — those warnings are the next production incident, rehearsed.
- Quarantine a flaky test with a deadline and an owner, or delete it. A retried flaky test is a test that reports success while telling you nothing.
