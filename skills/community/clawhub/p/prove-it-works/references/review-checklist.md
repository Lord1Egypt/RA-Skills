# Review checklist: what the scripts can't judge

`prove.py` runs the checks and flags the patterns. This checklist is your own pass on top, done before you tell the person anything. It has six parts: the task, the tests, the "check these" list, the rules to read, NOT RUN checks, and what to say.

Checked against: Anthropic Claude Code hooks reference (code.claude.com/docs/en/hooks) and obra/superpowers `verification-before-completion`, both read 2026-10-13. See the workspace `evidence.md`.

## 1. The task vs the change (cause 15): do this explicitly, every time

The script matches names: it reports a task item (a backticked name, a `--flag`, a route, a file to create) only when no code contains it, and its "Task items matched mechanically" note lists what it found. Everything else is yours. Do it in writing, not in your head:

1. **List the requirements.** Number every behaviour, name, file, flag or option, argument, default, limit or range, output format, error case and message the task mentions, plus every "also", "and", "must" and "then". Split compound sentences: "add `--limit N` that caps the results at N, validated the same way as `--page`" is three rows (the option is parsed, the cap is applied, a bad value is rejected exactly like `--page`).
2. **Map each row to code.** For each, write the `file:line` in the diff (`git diff <base>` plus untracked files) that delivers it, or **MISSING**. Only code that runs counts. A README table, a CHANGELOG line, a usage string, a docstring, a comment, a test name, or the agent's own summary saying it is done is **not** evidence; a doc that claims an unimplemented feature is itself a problem to fix.
3. **Any MISSING row means not done**, even when every check is green. Say which row in the first lines of the reply.
4. **Look for silent substitutions.** The task asked for `fetch_profile` and the change adds `get_profile`; a 10% discount and the constant is `0.01`; "over $100" and the code uses `>=`; "on or after" and the code uses `>`; "1-10 items (default 5)" and there is no bound or the default is 20.
5. **Check that the new code is reachable:** wired into the route, exported, called from the CLI's command switch, registered in the config. A flag that is parsed but never used, or a correct function nothing calls, is not a feature.
6. **Check "the same way as X" literally:** open X's code and compare (same parser, same error message and exit code).
7. **If the task named a file**, check that the change is in that file and not in a copy. If the task limited the files ("only touch a.py and the tests"), every other changed file is a problem; the script flags these, but confirm none slipped through as a rename or a new file.
8. **Check each requirement has a test that exercises it** (at least the main path and one edge case the task names). A requirement with code but no test is weaker evidence: say so.

## 2. Reading the tests (causes 5 and 6)

For every changed test file, compare old and new side by side (`git diff <base> -- <file>`):

| Look for | Weakened when | Fine when |
|---|---|---|
| Expected values changed (`toBe(108)` became `toBe(118.8)`) | The task did not ask for that behaviour to change: the test was edited to match a bug | The task changed exactly that behaviour, and the new value is what the task describes |
| Exact matcher replaced (`toEqual` / `strictEqual` / `assertEqual` became `toBeTruthy` / `assert.ok` / `assertTrue` / `toBeDefined`) | Always, unless the value really is non-deterministic | Never "fine" without a comment explaining why |
| A new test for the new feature | It asserts only that something exists or is truthy, never checks the value, or mocks the very function under test | It asserts the exact result for normal input and at least one edge case from the task |
| `.skip`, `xit`, `@unittest.skip`, `pytest.mark.skip`, `{ skip: true }`, `test.todo` | Added by this change | Pre-existing, or a platform guard with a real reason (`skipIf(sys.platform == "win32")`) |
| `.only`, `fit`, `fdescribe` | Always: remove it | Never |
| Snapshot files rewritten | The new snapshot has `NaN`, `undefined`, `[object Object]`, an error string, or changes the task did not ask for | The diff of the snapshot shows exactly the output change the task asked for |
| Test command or config changed (`--test-name-pattern`, `-k`, `--passWithNoTests`, `testPathIgnorePatterns`, `|| true`) | It narrows what runs or ignores failures | It only adds a path for genuinely new tests |
| Test files deleted | The behaviour still exists | The task removed that feature, and the deleted tests only covered it |
| Assertions commented out | Always | Never |
| Golden or expected-output files rewritten (`tests/golden/*`, `*.expected.*`) | Lines change that the task did not ask for: the expectation was regenerated from buggy output | Each changed line is exactly what the task asked for |
| A test that cannot fail (`assert.ok(true)`, its own copy of the function under test, a stub that returns the expected value in place of the real code) | Always | Never; stub only the network, clock or disk |
| Coverage threshold lowered, test timeout or retries raised | Always, unless the task asked | Never as a way to get to green |
| CI job switched off (`if: false`, `continue-on-error: true`, `|| true`, a test step removed) | Always, unless the task asked | A new job added, nothing muted |

Also confirm the test run actually exercised the new tests: the checks table shows the test count; it should have grown when you added tests. The script flags a new test file whose name the test command never collects (unittest `test*.py`, pytest `test_*.py` / `*_test.py` or the project's `python_files`, `node --test` defaults, jest and vitest defaults). For any other runner, or a custom config, compare the count yourself: if it did not grow by the number of tests you added, find out why before saying anything passed.

## 3. The "Check these" list

Open every item. For each one, decide: real problem, intended (say why in one line), or not applicable. Typical calls:

- **Outside the task (docs, env templates, snapshots, files the in-scope code imports, stylesheets for the new markup, files in the same package as the named files):** fine when the change there is needed for the task (a README usage line the task asked for, a helper the new code calls, a CSS rule for the class the new template uses); otherwise revert it. A changed default, timeout or config constant "while you were there" is not needed: revert it.
- **Conditional skip:** fine for a true platform limit with the reason in the message; not fine as a way around a failure.
- **Expected values changed:** see the table above.
- **Untracked caches or build output not gitignored:** usually left by a local run. Don't commit them; suggest the `.gitignore` line.
- **Dependency change the task loosely asked for, or no task was given:** say which package and why it is needed. A lockfile where only versions moved (a security update) is fine when the person asked for it.
- **Exception swallowed (returns a default) or hardcoded result:** fine only when the task defines that fallback; otherwise the error or the real lookup is the feature.
- **Schema changed without a migration:** generate the migration with the command the item names, unless the project has no migrations for that model.
- **Generated file changed with its source:** run the project's generate command and confirm the file comes out identical.
- **Fails on lines the change did not touch:** an inferred check (run because its config exists) that was probably failing before. Say so; do not fix unrelated code unless the task covers it.
- **Test timeout or retries raised:** find out why the test was slow or flaky.

## 4. Rules Claude must check by reading

The report lists written rules that could not become mechanical checks ("prefer dataclasses", "keep components small", "use named exports", "components use PascalCase; everything else kebab-case", "test files follow the runner's naming", "log through the project logger, not print", "never commit secrets"). For each one that touches the files you changed, check the diff against it. A broken rule is a problem: fix it or say plainly that you broke it and why.

Rules that say user-facing texts (replies, error messages, CLI output) are a contract become a mechanical check on string literals the change rewrote in code. Text that lives elsewhere (templates, i18n JSON, Markdown help) is yours to compare by reading.

If a rule is easy to check mechanically and the person cares about it, suggest a Never Twice rule (`rules.py add`).

## 5. NOT RUN checks

- NOT RUN means the check did not happen. Never write "passed", "green" or "should pass" about it.
- The reason column says why: dependencies not installed (including a missing `node_modules`: a global eslint or tsc is never used in its place), a tool missing, a download needed, the time budget ran out, or a command that looked unsafe to run automatically (deploy, release, publish, migrate, install, network).
- Ask before installing anything. Give the person the exact command (for example `pnpm install`), or ask whether you may run it, then prove again.
- If it cannot be run here at all (CI-only, needs a service or secrets), say so and say where it will run.
- If the Stop hook reported it, ask once, then stop; do not loop on it.

## 6. What to say instead of "done"

Never: "Done!", "should work now", "all tests pass" (without output), "I believe this fixes it", "everything looks good".

The first line is one of four verdicts. **PROVEN**: a task was given, every check ran and passed, nothing found. **CHECKS PASS (...)**: nothing failed, but something was not covered (no task, no test command, no change to inspect, a check failing only on untouched lines); quote what it says was not covered. **NOT VERIFIED**: checks could not run; nothing is proven. **NOT DONE**: a check fails or the change has a problem.

When the proof says **PROVEN** and your review pass found nothing:

> Proof: `PROVEN: all 3 checks passed, no problems in the change` (tests 14 passed, build ok, lint clean, run just now).
> Requirements:
> 1. `search` prints matching rows: src/search.js:18, wired in src/main.js:44.
> 2. `--limit N` caps the results: src/main.js:47, applied in src/search.js:25.
> 3. Bad `--limit` rejected like `--page`: src/main.js:46 (same `parsePositiveInt`, same exit code 2).
> Not checked here: visual layout of the new banner (needs a browser).

If a requirement row is MISSING, the reply starts "Not done yet" and names it, whatever the proof's first line says.

When it says **NOT DONE**, or your review found a gap:

> Not done yet: `NOT DONE: 1 failing check, 2 problems in the change`.
> - Tests: `test/cart.test.js` "applies a 10% discount" fails (expected 108, got 118.8): the rate is 0.01, not 0.1.
> - A `console.log` is left in src/cart.js:13.
> I'm fixing these now and will run the proof again.

When something is left for the person:

> Code is done and lint and build pass, but tests are NOT RUN: dependencies aren't installed (`pnpm install`). Want me to run it?

Keep the proof's first line verbatim, keep the numbers, and put anything not done first. When you dismiss a problem as "the task asked for it", quote the task sentence that asks for it.
