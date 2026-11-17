---
name: prove-it-works
description: Before saying a coding task is done, fixed, working or passing, run the project's real tests, build, typecheck and lint, show the real output, and inspect the change for the quiet ways "done" is not done (skipped or weakened tests, test commands that cannot fail, swallowed errors, hardcoded results, files outside the task, broken project rules, debug leftovers, secrets, dependency and migration mistakes). Use it at the end of every coding task, before committing or opening a PR, and whenever someone asks "did you test it?", "is it really done?" or "prove it". Also use it when the person corrects a mistake ("don't do that again") to turn the correction into a rule checked on every later proof.
---

# Prove It Works

Before you say "done", prove it. This skill runs the project's real checks, shows their real output, and inspects your change for the problems that pass every check but still mean the work is not done.

**The rule that matters:** never say a check passed unless you ran it in this turn and its output is in front of you. A check that did not run is NOT RUN, never PASS. The script's first line is the verdict; it goes first in your reply, word for word.

## Pick the mode

| The situation | Mode | Run |
|---|---|---|
| You finished (or think you finished) a coding task, or someone asks whether it works | **Prove it** | `scripts/prove.py` |
| The person corrected a mistake and it could happen again | **Never twice** | `scripts/rules.py add` |
| You want to see which written project rules exist and how they are checked | List rules | `scripts/rules.py <repo>` |

## Prove it

1. Save the task you were given (the request plus any acceptance criteria) to a temporary file **outside the repo**, then run, with the Bash tool timeout set to 600000 ms (or in the background for longer suites):

```bash
python3 <skill-dir>/scripts/prove.py <repo> --task-file <tmp-task-file>
```

   - The change is worked out for you: on a feature branch, everything since the merge-base with the default branch (commits and uncommitted work); on the default branch, uncommitted work, or the last commit if it is from the last 24 hours. A merge commit or an old commit on a clean tree is "no change to inspect". `--base <ref>` overrides this.
   - Each command gets `--timeout` seconds (default 300); all commands together get `--budget` seconds (default 540), after which the rest are NOT RUN. If the Bash tool would stop the script sooner, the script's children are stopped with it, so raise the Bash timeout instead of lowering these.
   - Without a task file the checks still run, but scope and task items cannot be judged, and the verdict says so.

2. **Lead with the verdict.** Your first line quotes the script's first line exactly. Then the checks table (command, result, exit code, time). Never paraphrase a FAIL into something softer, never round NOT RUN up to PASS.

| Verdict | Means | You say |
|---|---|---|
| `PROVEN: ...` | A task was given, every check ran and passed, no problems in the change | Done, with the proof and your requirements list (step 4) |
| `CHECKS PASS (...)` | Nothing failed, but something was not covered: no task, no test command, nothing to inspect, or a check that fails only on untouched lines | The checks pass, and exactly what the line says was not covered |
| `NOT VERIFIED: ...` | Checks could not run (dependencies, tools, time budget, unsafe to run) | It is not proven; name the command that would let them run, and ask once |
| `NOT DONE: ...` | A check fails or the change has a problem | "Not done yet", then each item |

3. **If NOT DONE:** fix each failing check and each problem, then run the proof again, until it passes or what is left needs the person.
   - Fix the code, not the check: do not skip, loosen, delete or re-record a test, add `.only`, add `@ts-ignore` / `# type: ignore` / `eslint-disable`, catch and ignore the error, special-case the test input, stub out the code under test, lower a coverage threshold, add `|| true`, or switch off a CI job. The script flags all of these.
   - **NOT RUN:** do not install anything without asking. Give the person the exact command from the reason column, or ask whether you may run it. If the Stop hook reported it, ask once, then stop.
   - A problem the task really asked for (a dependency the person requested) is not a defect: quote the task sentence that asks for it, in one line, and move on.

4. **Do your own review pass** with `references/review-checklist.md`, even when the verdict is PROVEN. The scripts match names and patterns; they cannot tell whether the change does what the task meant.
   - **Write the requirements as a numbered list** (every behaviour, name, file, flag, default, limit, error case, output format, every "also" and "and"). Next to each, the `file:line` in the diff that delivers it, or **MISSING**. Docs, comments, usage strings and your own summary are not evidence. Any MISSING row means not done, whatever the first line says.
   - Read every changed test: is each assertion still exact, does it run the real code, did the test count grow?
   - Open each **Check these** item and decide: real problem, intended (say why), or not applicable.
   - Check the **rules Claude must check by reading** that apply to the change.

5. **Report** with the wording in the checklist's last section: verdict first, then what is not done or not covered, then the evidence.

## Never twice

When the person corrects a mistake that a pattern, a path or a command could catch next time, offer to add a rule, then run:

```bash
python3 <skill-dir>/scripts/rules.py add --repo <repo> --kind grep --pattern '<regex>' --why '<the mistake, in one line>' [--glob 'src/**']
python3 <skill-dir>/scripts/rules.py add --repo <repo> --kind forbid-path --pattern 'src/generated/' --why '<why it must not change>'
python3 <skill-dir>/scripts/rules.py add --repo <repo> --kind require-cmd --pattern 'npm run e2e' --why '<why it must pass>'
```

- `grep`: the regex must not appear in lines a change adds (optionally only in files matching `--glob`).
- `forbid-path`: files matching the glob or folder must not be added, edited or deleted.
- `require-cmd`: the command must pass. Only check-like commands are accepted (no installs, deletes, git writes, network or redirects).

Show the person the rule as written and the dry run. Rules live in `<repo>/.shipsnag/rules.md`, run on every later proof, and can be edited or deleted by hand. Mention the file the first time.

## How to present results

- First line: the verdict, copied from the script.
- Every problem keeps its four parts: Finding, Evidence (file:line or command output), Impact, Fix. Trim repetition, keep the evidence.
- Quote command output from the report; never invent output or a test count.
- Say plainly what was not checked: NOT RUN checks, checks skipped with `--only`, the "Not covered" line, and "What this can't see" when it applies.
- Never print a secret. The report masks them (first and last four characters); refer to a key that way.

## What it can't see

- CI-only differences (other runtime versions, secrets or services that exist only in CI), flaky or order-dependent tests, and anything that needs a human or a browser.
- Whether the change does what the task meant beyond the names, files and flags the task mentions: a flag that is parsed but ignored, a wrong comparison, a missing edge case. That is your requirements list.

## The saves ledger

Add `--ledger` to append one line to `<repo>/.shipsnag/ledger.md`: date, verdict, check counts and cause numbers, never code or secrets. Use it unless the person doesn't want files added; mention the file the first time.

## Reference

- `scripts/prove.py`: detects and runs the project's commands (package.json scripts with the package manager from `packageManager` or the lockfile; Makefile targets; pyproject task tables; pytest or unittest; ruff, flake8, mypy; cargo; go; Maven, Gradle, Bundler, Composer, .NET, Deno; documented and conventional commands) with a timeout, a total budget and an offline environment. Commands named or doing deploy, release, publish, migrate, install or network work are never run automatically. `--json` for machine output (with a `coverage` block); exit codes 0 PROVEN, 1 NOT DONE, 3 CHECKS PASS or NOT VERIFIED, 2 tool error. `--hook` is the optional Claude Code Stop hook (see README).
- `scripts/diffcheck.py` and `scripts/fakes.py`: the change inspection (causes 5-17), including test commands and CI jobs that cannot fail, tests that cannot fail, swallowed exceptions, special-cased inputs, hardcoded results, rewritten golden files, lowered coverage, lockfiles not updated, schema changes without migrations and conflict markers. Minified, generated and vendored files are skipped by the line checks. `scripts/rules.py`: project rules from CLAUDE.md, AGENTS.md, .cursorrules, .cursor/rules, .github/copilot-instructions.md, CONTRIBUTING.md, .windsurfrules and `.shipsnag/rules.md`.
- `references/review-checklist.md`: your review pass, how to read tests, how to judge each "check these" item, and what to say instead of "done".
- Python 3.8+ standard library only. The scripts never write to the repo except `.shipsnag/`; the project's own commands may write their usual outputs, and the change is read before any command runs.
