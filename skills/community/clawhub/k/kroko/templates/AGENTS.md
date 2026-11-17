# AGENTS.md

Operating contract for any coding agent working in this repository.
Read this before writing code. It is not advisory.

## Setup

```bash
cargo test --release --manifest-path rust/Cargo.toml        # the gate must be green first
./rust/target/release/kroko path/to/file.py                  # check one file
cargo clippy --all-targets -- -D warnings                    # no warnings allowed
```

## Non-negotiable limits

| Constraint | Limit |
|---|---|
| Lines per function | 60 |
| Nesting depth | 3 |
| Parameters | 4 |
| Cognitive complexity | 15 |
| Recursion, direct or mutual | forbidden |
| Unbounded loops | forbidden |
| Swallowed errors | forbidden |
| Module-level mutable state | forbidden |
| `TODO` / `FIXME` / commented-out code / banner comments | forbidden |
| Undocumented public function or module | forbidden |
| Compiler, linter, analyser warnings | zero |
| Diff size before splitting the change | 300 lines |
| Files touched | only those the task names |

Rationale: NASA/JPL Power of 10 Rules 1, 2, 4, 6, 7, 10; MISRA C:2023 Rule 17.2;
SonarSource cognitive complexity; PEP 257 and Effective Dart for documentation.

## Before writing any code

1. Read the target files in full. Do not grep and infer.
2. Read the neighbouring code and match its naming, error style and test layout.
3. Verify every external API against its real documentation. Never assume a
   signature, flag or config key from memory.
4. Write one sentence: what changes, what does not, what "done" means measurably.

## While writing

- Prefer deleting code, then the standard library, then the platform primitive,
  then one function, then one module, then one dependency.
- Introduce an abstraction only for two *existing* call sites.
- Write the contract first (`assert` preconditions), then the straight-line happy
  path, then one branch at a time, re-running the gate after each.
- No recursion. Use an explicit stack; the call graph stays acyclic.
- Every loop has a stated upper bound, asserted on overflow.

## Comments

A comment exists to say what the code cannot say. Apply the test "if I delete this,
what is lost?" If nothing, delete it.

1. Say why, not what.
2. Never narrate the code back — a comment whose words match the line beneath it is
   a duplicated line.
3. Write sentences: capitalised, ending in `.`, `!` or `?`, even for fragments.
4. Document the module and every public function. Not the self-evident private
   one-liner.
5. State the contract the signature cannot hold: empty input, raised errors, caller
   obligations, cost, mutation. Prescriptive mood — "Return the path", not
   "Returns the path".
6. No placeholders, no commented-out code, no banner art.
7. A stale comment is worse than none. Update it in the same change, and never write
   a comment asserting behaviour you have not executed.

Comments go above the line they explain, never trailing. Full doctrine in
`references/comment-doctrine.md`.

## Managed-language leak checklist

- Every subscription, listener, timer and controller is disposed in its teardown,
  and a test asserts it.
- No `BuildContext` or `this` captured across an `await`.
- No unbounded cache; if it exists it has a size and an eviction policy.
- Every spawned task is owned by a scope that cannot outlive its parent.
- Every file, socket and connection is closed by a scope guard.

## Interface gates

- LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1, all at p75.
- Contrast >= 4.5:1 body, >= 3:1 large; full keyboard path; visible focus.
- Correct roles, names and states for screen readers.
- Touch targets >= 44x44 pt / 48x48 dp; frame budget <= 16.7 ms.
- All states designed: empty, loading, error, partial, offline, over-long content.
- Tokens from the design system. No hard-coded spacing, colour or radius.

## Testing

- Run the full gate before reporting: format, lint, typecheck, unit tests, security
  scan, leak check.
- Add a test for every boundary named in the plan.

## Reporting

The final message states the exact commands run and their exit codes, the gate
output verbatim or faithfully summarised, and what remains unverified.

## Refuse, and say so, when asked to

1. Assert that something works without running it.
2. Use an API, flag or key you have not verified.
3. Add a dependency to avoid writing twenty lines.
4. Emit a stub or `TODO` and call it complete.
5. Suppress a warning instead of resolving it.
6. Catch an error and continue with a default.
7. Copy a block instead of extracting the shared part.
8. Widen the scope beyond the files the task named.
9. Leave dead or commented-out code.
10. Hard-code a secret, key, token or machine-specific path.
11. Write recursion where an explicit stack is available.
12. Present a plausible result you could not actually produce.
