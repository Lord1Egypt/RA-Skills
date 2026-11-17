---
name: kroko
description: "Use when writing or reviewing code to hard limits."
version: 2.0.0
author: Sakib Dalal
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [code-quality, comments, complexity, memory-safety, recursion, linting]
    category: software-development
    related_skills: [code-quality-gates, requesting-code-review, test-driven-development, simplify-code]
  openclaw:
    emoji: "🐊"
    os: [macos, linux, windows]
---

# KROKO

Write code a tool can prove is small, leak-free, recursion-free and readable — then
prove it, with the gate shipped in this skill.

## When to Use

- Writing new code where the user wants it small, simple, safe, or "NASA-grade".
- Reviewing or refactoring code that has grown too large, too nested, or too clever.
- Setting up a repository's limits, or an `AGENTS.md` that binds every agent.
- Answering "how should an agent write code" — the answer is this procedure, run.
- Any request touching comments, docstrings, or documentation-in-source.
- Before claiming a refactor simplified something: measure both versions.

Not for: pre-commit plumbing (`requesting-code-review`), bulk mechanical cleanup
(`simplify-code`), or choosing a stack (`before-you-build`).

## The axiom

Generated code is fluent whether or not it is correct, so an agent's self-assessment
carries no signal. Measured: across 80 curated tasks and 100+ models, generated code
chose the insecure implementation **45%** of the time and missed **86%** of XSS
defects, with no improvement across model generations even as syntax correctness
rose (Veracode 2025 GenAI Code Security Report). Across 211M changed lines,
AI-assisted work shows **~4x** growth in duplicated blocks, with copy/paste exceeding
moved code for the first time in the dataset (GitClear).

Therefore: **the only trustworthy signal is tool output.** Run the gate, then report
its verdict rather than an opinion about it.

## Procedure

① **Read before writing.** Read the target files in full (not grepped), read the
neighbouring conventions, and verify every external API against its real
documentation. Never assume a signature, flag or config key from memory — that is
the single largest source of agent-introduced breakage. Zero lines written until
this is done.

② **Bound the problem.** Input ranges, each failure mode and what it returns, the
resource ceiling (memory, entries, iterations, timeouts), and the one thing that must
not break. If a loop cannot be bounded, the design is wrong, not the loop.

③ **Choose the smallest structure.** In order: delete code -> standard library ->
platform primitive -> one function -> one module -> one dependency. An abstraction
needs **two existing call sites**, never a hypothetical third.

④ **Write in gate-green increments.** Signature with asserted preconditions ->
straight-line happy path -> one branch at a time, re-running the gate after each ->
failure paths -> tests. A 400-line first draft is 400 unverified assumptions.

⑤ **Name by what a thing is.** One word per concept project-wide. No `data`, `info`,
`util`, `helper`, `handle`, `process`, `mgr`, `svc`, `cfg`, `tmp` — these are the tell
of generated code. No type suffixes. Booleans read as assertions (`canRetry`).

⑥ **Comment as a last resort that carries the why.** See the seven rules below.

⑦ **Handle failure once, visibly.** Name the exception type; never swallow; never
return a default from a failure path — a silent `return []` is a memory leak of
*information*, because the caller now believes the set is empty.

⑧ **Run the gate, then the tests, then the scan.** Any non-zero exit stops the step.
Fix it. Never suppress, never whitelist.

⑨ **Report the evidence.** Exact commands, exit codes, gate output verbatim or
faithfully summarised, and what remains unverified.

## The hard budget

Full table with quoted origins in `references/limits.md`.

| Constraint | Limit | Code |
|---|---|---|
| Lines per function | 60 | K002 |
| Nesting depth | 3 | K003 |
| Parameters | 4 | K004 |
| Cognitive complexity | 15 | K005 |
| Recursion, direct or mutual | 0 | K001 |
| Unbounded loops | 0 | review |
| Assertions per function | >=2, or >=1 plus a named raise | review |
| Module-level mutable state | 0 | K007 |
| Swallowed errors | 0 | K006 |
| Placeholder / commented-out / banner comments | 0 | K008-K010 |
| Undocumented public API | 0 | K011 |
| Compiler and analyser warnings | 0 | CI |
| Diff before splitting | 300 lines | review |

Anything over a limit is not "a large function", it is **unfinished**. A function
passes 60 lines because it is doing two jobs; finding the second job *is* the work.

## Comments — the seven rules

Full doctrine, with language-specific forms, in `references/comment-doctrine.md`.

The principle: **a comment exists to say what the code cannot say.** Apply the test
"if I delete this, what is lost?" — if nothing, delete it.

1. **Say why, not what.** The code states the mechanism; the comment states the
   reason and the constraint behind it.
2. **Never narrate the code back.** Overlapping words with the line beneath is a
   duplicated line (K014).
3. **Sentences, capitalised, punctuated** — even fragments, even one-word notes
   (K013).
4. **Document the public surface only.** Module and every exported function (K011).
   No comment on a self-evident private one-liner.
5. **State the contract the signature cannot hold**: empty input, raised errors,
   caller obligations, cost, mutation. Prescriptive mood — "Return the path", not
   "Returns the path" (PEP 257).
6. **No dead code, no decoration, no bookkeeping**: placeholders (K008),
   commented-out code (K009), banner art (K010).
7. **A stale comment is worse than none.** Update it in the same change, and never
   write a comment asserting behaviour you have not executed.

Above the line, never trailing. Never `/* */` for documentation in Dart or Go.

## Memory

`references/managed-language-leaks.md` carries the per-language table and idioms.

Power of 10 Rule 3 is a C rule; its intent — one owner, one provable release point —
transfers everywhere. In Dart, Kotlin, Swift, TypeScript and Python the leak is a
retained reference, not an unfreed pointer. The five checks:

1. Every subscription, listener, timer and controller is disposed in its teardown,
   and a test asserts it.
2. No `BuildContext` or `this` captured across an `await`.
3. No unbounded cache; if it exists it has a size and an eviction policy.
4. Structured concurrency only — no fire-and-forget task outliving its parent.
5. Every file, socket and connection closed by a scope guard.

## Interface

`references/interface-gates.md` carries the numbers and the ten design rules.

LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1 at p75; contrast >= 4.5:1; keyboard path
complete; correct roles and states; touch >= 44x44 pt; frame <= 16.7 ms. Tokens
before drawing. One primary action per screen. Every state designed, not just the
happy one. Motion explains a state change or it is removed.

## Running the gate

```bash
cargo build --release --manifest-path rust/Cargo.toml
./rust/target/release/kroko path/to/file.py                    # default gates
./rust/target/release/kroko --strict-comments path/to/file.py  # adds K012-K014
cargo test --release --manifest-path rust/Cargo.toml           # prove the gate itself
```

`rust/` builds a single static binary with one dependency tree (tree-sitter and its
Python grammar). It checks length, nesting, arity, cognitive
complexity, recursion by call-graph reachability, swallowed exceptions, module state,
placeholders, commented-out code, banners, docstring presence and comment form. It
exits 1 on any finding.

For other languages use the native levers in `references/limits.md` and
`references/managed-language-leaks.md` — ESLint, `analysis_options.yaml`, Clippy,
Ruff. **Recursion is the one limit with no off-the-shelf lint** in any mainstream
toolchain: enforce it with call-graph analysis (Frama-C or Polyspace for C, a CodeQL
query, `kroko` for Python) or an explicit review item. Never claim a linter
covers it.

## Measured performance

Corpus: the Python standard library,
1,446 files, 562,428 lines, Python 3.9.

| Metric | Default mode | Strict mode |
|---|---|---|
| Wall time | 2.34 s | — |
| Per file | 1.6 ms | — |
| Throughput | 617 files/s | — |
| Peak memory | **31.2 MB** | — |
| Crashes | 0 | 0 |
| Regression suite | `cargo test`, 26 cases | — |

The Python implementation this replaced took **9.27 s** and **63.1 MB** peak on the same
corpus: the rewrite is **4.0x faster and 2.0x smaller in memory**, measured with
`/usr/bin/time -l` rather than estimated.

## Precision, measured not claimed

Two independent implementations of the same rules, one reading the AST and one reading
tokens, run over 1,446 files:

| Code | Method | Disagreements |
|---|---|---|
| K002 function span | differential vs INDENT/DEDENT block extent | **0** |
| K004 arity | differential vs parameter count from header text | **0** |
| K006 blanket exception | differential vs token-level except clause | **0** |
| K001 recursion | 10 sampled findings adjudicated | 10 of 10 genuine |
| K005 cognitive | invariant: score never below branch count | 0 violations |

K003, K007-K011 and K012-K014 are verified by fixture only. Their precision on real
code is **unmeasured**, and this skill does not imply otherwise.

Bare `ast.parse` accounts for 11% of the run; the rest is the analysis passes. For the
real use — a pre-commit hook over the handful of files a change touches — that is
under 60 ms. Ruff does the same corpus in 0.07 s, roughly 120x faster, because it is
compiled, parallel, and checks a different rule set: it has no cognitive complexity,
no recursion graph, and no comment semantics. Compare them on capability, not seconds.

## What this skill guarantees, and what it does not

KROKO is deterministic about what it measures: on 26 fixtures with known defects, the
gate's reported code set exactly equals the expected set, asserted by `cargo test`.
Measured on the Python standard library, 1,446 files and 562,428 lines: 2.34 s,
1.6 ms per file, 617 files per second, 31.2 MB peak, **zero crashes**.

K002, K004 and K006 were also checked against an independent token-level oracle over
that whole corpus: **zero disagreements**. That is a proof about the gate, not about
your code.

It cannot guarantee that code passing the gate is correct, secure or well designed.
Complexity metrics are proxies. A function can score zero and still be wrong. The
gate removes a class of defect — size, nesting, recursion, swallows, stale comments —
and says nothing about the rest. Say so when reporting.

## Refusals

Refuse, and say that you are refusing:

1. **Asserting something works without running it.**
2. **Using an API, flag or key you have not verified.**
3. Emitting a stub or `TODO` and calling it complete.
4. Suppressing a warning instead of resolving it.
5. Catching an error and continuing with a default.
6. Copying a block instead of extracting the shared part.
7. Widening scope beyond the files the task named.
8. Leaving dead or commented-out code.
9. Hard-coding a secret, key, token or machine-specific path.
10. Writing recursion where an explicit stack is trivial.
11. **Presenting a plausible result you could not actually produce.**

1, 2 and 11 are integrity failures; the rest are quality failures.

## Pitfalls

- **Whitelisting the gate when it fires on your own code.** It fires because the
  code is over the limit. Refactor. A gate with exceptions becomes noise, then gets
  disabled — the failure mode is exemption, not enforcement.
- **Treating a false positive as an exemption.** A false positive is a bug in the
  *metric*, fixed once, centrally. Four real ones, all found by running the gate on
  itself: an `elif` ladder counted as deepening nesting; a depth tracker handed the
  grandparent instead of the parent; a shebang treated as prose; `os.path.join()`
  flagged as mutable state. Each made the gate lie in the direction that gets gates
  turned off.
- **Treating an unresolvable call as a recursion edge.** Matching call *names*
  rather than resolved targets is how recursion checks become useless: measured on
  the standard library, matching attribute calls produced 1,533 findings that were
  only 13.5% precise, because any function shares a name with some unrelated method.
  Only bare-name calls, and `self.name(...)` inside a method, are edges.
- **Running strict comment mode over legacy code.** Measured on the standard
  library, only 9.5% of existing comments end in a full stop, so strict mode reports
  ~89,000 findings there. That is the rule working, not the gate failing: strict mode
  is a gate for code being written now, not a migration tool for code written before.
- **Measuring the count instead of the cause.** LOC is a weak proxy; cognitive
  complexity and max nesting depth predict comprehension cost better, so gate on
  those.
- **Applying "no heap allocation" literally to a managed language.** Use the
  retained-reference checklist instead.
- **Shipping a 60-line *file*.** The limit is per function.
- **Commenting to look thorough.** Volume is not clarity; a file with a comment on
  every line is harder to read than one with three good ones.
- **Retrofitting limits onto a finished file.** Write the gate early; let it reject
  each increment.

## Support files

| File | Purpose |
|---|---|
| `rust/src/lib.rs` | The gate itself: every rule, K000-K014 |
| `rust/src/main.rs` | The CLI: paths, `--strict-comments`, exit codes |
| `rust/tests/fixtures.rs` | 26 cases asserting exact code sets |
| `install-hook.sh` | Installs the gate as a git pre-commit hook in any repo |
| `references/limits.md` | The budget with quoted origins, plus native config snippets |
| `references/comment-doctrine.md` | The seven comment rules, per-language forms, docstring template |
| `references/managed-language-leaks.md` | Power of 10 Rule 3 translated, per-language idioms |
| `references/interface-gates.md` | UI/UX numbers and the ten design rules |
| `templates/AGENTS.md` | Repo contract that installs the limits for every agent |
| `tests/fixtures/` | The 26 fixture files the self-test asserts against |
| `templates/pre-commit` | The hook itself, checked only staged files in strict mode |
| `rust/Cargo.toml` | Builds the binary; one dependency tree, no runtime |
| `tools/render_logo.html` | Renders the halftone logo in a browser, parametrically |

## Verification

```bash
cargo test --release --manifest-path rust/Cargo.toml    # 26 cases, must pass
cargo clippy --all-targets -- -D warnings               # must be silent
cargo fmt --check
```

Green means every fixture produces exactly its expected code set, and both scripts
pass their own gates in both modes.

## This user's preferences for this class of task

- Plain procedural code. No custom classes or OOP ceremony; repetition is acceptable
  when it buys clarity.
- Production-ready output only — no placeholders, no `TODO`, no scaffolds presented
  as done.
- Deliver the artefact, not a description of it: if a gate is the answer, write it,
  run it, quote the real output.
- Measured results in plain decimals, and substance once a constraint is stated.
