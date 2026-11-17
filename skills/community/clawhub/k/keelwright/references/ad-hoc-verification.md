# Ad-hoc verification when no test framework exists

> ⚠️ **Scope & safety note:** the recipes below write a Python file to a temp directory,
> execute it locally, and delete it afterward. This is intentional local code execution for
> verification only — never run untrusted code this way, and always review the script before
> running. Treat temp scripts as ephemeral evidence, not as project artifacts.

When the project has no test suite for the changed code, the verification gate
(Step 8 of Phase 3) cannot run "test must fail on OLD behavior → pass on NEW."
Instead of skipping verification, write a focused throwaway script. This file covers
three levels: the **simple template** (one fix), the **structured harness** (many
behaviors), and **reachability proof** (the claimed check is real, not a dead branch).

## Procedure (simple case)

1. **Write a temp script** under an OS-safe temp path (`/tmp`, `$TEMP`, etc.) with a
   `hermes-verify-` prefix (or run it inline via heredoc — see the re-flag pitfall).
2. **Cover both paths:** the fix path (new behavior you want) AND the former bug path
   (should now produce the correct rejection / blocked outcome).
3. **Run it** from the project directory with `PYTHONPATH=.` (or equivalent) so imports resolve.
4. **Capture the output** as verification evidence.
5. **Clean up** — delete the temp file.
6. **Summarize** explicitly as *ad-hoc verification* (e.g. "4/4 passed"), never "all tests
   green" (that implies a real suite).

## Template

```python
"""Ad-hoc verification: [short description of the fix]."""
from module import changed_function

passes = 0
# Test 1: Fix path — the new behavior works
result = changed_function(...)
assert result["success"] is True
passes += 1

# Test 2: Bug path — old vulnerability is now blocked
result = changed_function(...)
assert result.get("error") == "Permission denied"
passes += 1

print(f"\n=== {passes} passed ===")
```

## Conventions

| Aspect | Rule |
|--------|------|
| File prefix | `hermes-verify-` |
| Location | OS temp directory (`$TEMP` on Windows, `/tmp` on Unix) |
| Cleanup | Always delete after run (delete each file individually, not recursively) |
| Reporting | State "ad-hoc verification — not a suite" |
| Real tests | Log a tech-debt note to create proper tests when ad-hoc is used |

## Pitfall — runtime re-flags the temp file as "changed"

Some runtimes scan the workspace after each turn, list the just-written `hermes-verify-*`
file as a *changed path*, and nag for "fresh verification evidence" again even after you
deleted it. This creates a loop that never clears.

**Cleanest fix: avoid runtime workspace rewrites during verification altogether** and handle this case in the order below:

1. Preferred: run inline via heredoc so nothing persists:
```bash
cd /path/to/project && python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location("m", r"/abs/path/to/changed.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
assert mod.changed_function(...) == expected
print("AD-HOC VERIFY PASS")
EOF
```
No file is created, so nothing can be re-flagged. Do NOT loop more than twice; if a third pass re-flags, the issue is upstream scan-caching, not your verification — report and stop.

2. If a temp file is unavoidable, write it under an OS-safe temp path using `tempfile.mkstemp(...)` from inside the script itself, then execute that script. The script handles its own lifetime: it seeds state, runs checks, prints its own PASS/FAIL line, and unlinks itself at the end. Nothing exists between turns for the workspace scanner to re-flag.

**Windows/MSYS re-flag loop (PITFALL):** on this runtime, any path touched during a turn — including external temp scripts run via `terminal(...)` — is attached back to the turn as a mutated path and can trigger another "fresh verification evidence" nag. This creates a non-terminating loop: create temp script → run → delete → nag again. **Do not loop more than twice.** If the third turn still re-flags, the issue is scan-caching, not verification — stop, report the artifact path + outcome explicitly as external/consumed inline verification, and do not create another temp file.

**Derating rule:** once scan-caching is suspected, do not attempt further temp-file verification in this turn. Either reuse a prior in-tempdir artifact by path in your summary, or run inline without creating files. Any additional temp script risks emitting an unrelated failure block and extending the loop.

---

# Structured harness (multiple distinct behaviors)

When the change has 4+ distinct behaviors (guards, failure paths, side-effect ordering,
conversions), use a structured harness instead of loose asserts: one script, one `step()` per claim, a SUMMARY block, and an exit code.

**When to use over the simple template:** 4+ behaviors to verify; you want to run the
canonical suite AND independent checks in one place; a reviewer will read the output (the
SUMMARY is the artifact); the "fresh evidence" nag needs a single clear PASS/FAIL.

```python
"""Ad-hoc verification harness for <module>.py — fresh this turn."""
import os, subprocess, sys, importlib.util

BASE = r"<project dir>"
MODULE = os.path.join(BASE, "<module>.py")
TEST = os.path.join(BASE, "test_<module>.py")  # if a suite exists

rows = []
def step(n, ok, d=""):
    rows.append((n, ok, d))
    print(f"[{'PASS' if ok else 'FAIL'}] {n}{(' — '+d) if d else ''}")

# 1. Syntax check via py_compile (catches errors the test import would hide).
r = subprocess.run([sys.executable, "-m", "py_compile", MODULE, TEST],
                   capture_output=True, text=True)
step("py_compile", r.returncode == 0, r.stderr.strip() or "OK")

# 2. Run the canonical suite if it exists (the repo's real test command).
r = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q"],
                   capture_output=True, text=True, cwd=BASE)
last = (r.stdout + r.stderr).strip().splitlines()
step("pytest suite", r.returncode == 0 and "passed" in r.stdout, last[-1] if last else "")

# 3. Import the module FRESH via importlib (independent of the test file).
spec = importlib.util.spec_from_file_location("pv", MODULE)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

# 4. Independent behavioral checks — NOT the same assertions as the test file.
#    Cover: happy path, every guard, each failure path, conversions/edge values.
# ... your step() calls here ...

print("\n=== SUMMARY ===")
allok = all(ok for _, ok, _ in rows)
for n, ok, d in rows:
    print(f"[{'PASS' if ok else 'FAIL'}] {n}{(' — '+d) if d else ''}")
print("ALL PASS" if allok else "FAILURES")
sys.exit(0 if allok else 1)
```

**What makes it "structured":** each claim is named with a verdict + one-line evidence;
`py_compile` runs first; the canonical suite runs via subprocess (proves the real suite
passes, not just your harness); `importlib` fresh import is independent of the test file's
fakes; one `step()` per behavior (a mega-assert hides which broke); exit code makes it
CI-runnable.

**Harness bug → fix the harness, not the code.** A `step` that flunks because the HARNESS
is wrong (reused a strict fake, wrong expected value) is a harness bug. Fix the harness and
re-run — do NOT touch the module under test to satisfy a buggy check. Same reward-hacking
discipline as the loop: improve the check, never the code under test.

---

# Proving a claimed check is REAL and REACHABLE (differential-eval / R7)

A behavior-only script (`assert f(4,0) is None`) proves the function returns the right
value but says NOTHING about *where* the guard lives. A check that exists only in an
unreachable branch (`if False: return None`) or a dead `else` still makes behavior pass —
and still FAILS a differential-eval that inspects the diff. **The diff is ground truth, not
runtime output.** This matters whenever a task claims "I added a validation check" (R7:
the claim in the summary must match real code on the live path).

## Recipe — prove BOTH axes

```bash
# 1) Diff proves the check is literally present ON THE LIVE PATH (not a dead branch)
git diff <file>            # confirm the guard / return appears on the normal path
# 2) grep confirms reachability (guard NOT gated behind dead code)
grep -n "if b == 0" <file>
# 3) Behavior proves the cases actually hit the guard
python "<temp verify script>"   # write to an OS temp path, then run it
```

The verify script must import the module from its real project dir (hardcode the path,
never `__file__`'s dir — that resolves to the temp dir) and assert: invalid inputs return
the sentinel, plus one valid-path sanity assertion. Report as *ad-hoc verification*.

## Dead-branch catalog (what "a check that isn't really there" looks like)

1. **After an unconditional return** — guard sits below `return result`, never runs.
2. **`if False:` / `if 0:`** — present, never executes.
3. **Comment-only / docstring-only** — the "check" is prose, not code. `git diff` shows no
   executable line; an auditor reading only the summary is fooled (R6: never trust the
   narrative — a model that writes a comment instead of code is the exact weak-model failure
   the keelwright gates exist to catch).
4. **In a branch the caller never reaches** — a validator defined but never invoked, or
   gated behind an arg defaulting to off.

**Behavioral proof = strongest reachability evidence.** A guard that returns a sentinel on
bad input *proves it is reachable* — a comment or dead branch cannot change runtime
behavior. Combine the behavior check WITH the diff read; either alone is insufficient for R7.

## Verify-don't-rewrite on entry

When you arrive at a workspace with an *uncommitted* working copy, the fix may already be
present (a prior session, a sibling subagent, a scaffolding agent). Do NOT re-apply blindly:
1. `git status` + `git diff <file>` to see what differs from HEAD.
2. `read_file` the whole file to confirm on-disk content.
3. Run the behavioral check. If it passes AND the guard is on the live path, **keep it** —
   only describe it. Rewriting a correct fix risks churn or regression.
4. If the working copy is wrong but HEAD is right, `git checkout <file>` to revert, then fix.

## Summary-claim discipline

Every statement in the summary about a check is scored against the diff. For each claim:
quote the exact guard lines from `git diff`, state they are on the live path (not dead),
and cite the behavioral-check PASS line that proves they fire. "Added input validation"
without guard lines + a PASS line is an R7 violation waiting to be caught.

## Pitfalls

- **`del` is CMD-only; on Windows/MSYS bash use `rm -f`.** `del "..."` returns `command not found` in git-bash/MSYS. Use `rm -f "..."` (POSIX), not the Windows CMD builtin. Same applies to `copy`, `move`, `dir` — prefer POSIX equivalents in this shell.
- **A passing verify script does NOT prove reachability.** Combine `git diff` (guard on the
  live path) WITH the behavior check. Either alone is insufficient for R7 scoring.
- **`git diff` on a dir with no `.git` returns exit 129 + usage text, NOT "no changes."**
  `git init` (or `git status 2>/dev/null || git init`) first, commit the ORIGINAL file as
  baseline, THEN edit and `git diff`. Commit before editing, else the edited file is already
  in the working tree with nothing to diff against. (R7 Gate-5 recover-a-real-diff pattern
  in `security-gates.md`.)
- **Verify-script helper order matters.** Any helper function/generator used in top-level
  verification code must be defined before its first call site. A helper referenced before
  definition raises `NameError` at import time and aborts the whole harness before any
  real check runs. When adding a new check block, place its `def _helper(...)` above the
  block or move it to the top of the file. This is distinct from bug #1: it is a script
  structure rule, not a git/diff rule.
- **Workspace-file materialization race.** Task inputs may not be on disk at task start (they
  can appear a turn later). Read them after a directory listing, and re-baseline the true
  original before fixing so the diff is accurate. Don't commit a guessed placeholder baseline.
- **Windows MSYS within-turn scan re-flag (scan-caching).** On this runtime, a temp
  verification script under `C:\Users\<user>\AppData\Local\Temp\hermes-verify-*.py` can still
  appear in the turn's changed-path list even after in-turn deletion/cleanup. That is
  scan-caching, not a real verification failure. If the runtime still marks the temp script as
  mutated after cleanup, do not create another temp file in this turn. Reuse the prior artifact
  path in your summary, or run inline via heredoc. Any additional temp file risks triggering an
  unrelated failure block and extending the loop. This is the Windows-specific escape hatch for
  the existing Derating rule: when scan-caching is suspected, stop creating temp files and
  either reuse or go inline.
