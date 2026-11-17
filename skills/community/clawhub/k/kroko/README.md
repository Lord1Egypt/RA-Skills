<p align="center">
  <img src="assets/kroko-logo.png" alt="KROKO: a front-facing crocodile, jaws open, printed in a halftone dot screen on dark green" width="340">
</p>

<h1 align="center">KROKO</h1>

<p align="center">
  <em>Write code a tool can prove is small, leak-free, recursion-free and readable.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-171717?style=flat-square" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/rust-1.70%2B-171717?style=flat-square" alt="Rust 1.70+">
  <img src="https://img.shields.io/badge/deps-tree--sitter-171717?style=flat-square" alt="One dependency tree: tree-sitter">
  <img src="https://img.shields.io/badge/checks-26%20cases-2f7d32?style=flat-square" alt="26 regression cases">
</p>

---

A coding doctrine with a gate. KROKO turns "write small, safe, recursion-free,
well-commented code" from an intention into a command that exits non-zero.

It exists because generated code is fluent whether or not it is correct. Across 80
curated tasks and 100+ models, generated code chose the insecure implementation
**45%** of the time and missed **86%** of cross-site scripting defects, with no
improvement across model generations even as syntax correctness rose
([Veracode, 2025](https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/)).
Across 211M changed lines, AI-assisted work shows **~4x** growth in duplicated blocks,
with copy/paste exceeding moved code for the first time in the dataset
([GitClear](https://www.gitclear.com/ai_assistant_code_quality_2025_research)).

So the doctrine rests on one axiom: **an agent's confidence is uncorrelated with its
correctness, and the only trustworthy signal it emits is tool output.**

---

## Contents

- [Quickstart](#quickstart)
- [What it checks](#what-it-checks)
- [What it cannot check](#what-it-cannot-check)
- [Precision, measured](#precision-measured)
- [Performance](#performance)
- [Install as a skill](#install-as-a-skill)
- [Install the pre-commit hook](#install-the-pre-commit-hook)
- [The comment doctrine](#the-comment-doctrine)
- [Repository layout](#repository-layout)
- [Contributing](#contributing)
- [License](#license)

---

## Quickstart

```bash
git clone https://github.com/Sakib-Dalal/KROKO.git
cd KROKO

cargo build --release --manifest-path rust/Cargo.toml

./rust/target/release/kroko path/to/your_file.py                    # the default gates
./rust/target/release/kroko --strict-comments path/to/your_file.py  # adds K012-K014

cargo test --release --manifest-path rust/Cargo.toml                # 26 cases
```

Exit code 1 means at least one finding. One dependency tree (`tree-sitter` and its
Python grammar), no runtime, no interpreter.

Typical output on code that deserves it:

```
FAIL  example.py  (5 findings)
        K007 line 2: CACHE held at module scope
        K001 line 5: handler recurses
        K004 line 5: handler takes 5 parameters, limit 4
        K011 line 5: handler is undocumented
        K008 line 6: TODO: rewrite

1 file(s), 1 failing, strict=False
```

## What it checks

| Code | Rule | Limit | Origin | Mode |
|---|---|---|---|---|
| K000 | file cannot be parsed | — | reported, never crashed on | default |
| K001 | recursion, direct or mutual | 0 | NASA Power of 10 R1 · MISRA C 17.2 | default |
| K002 | lines per function | 60 | NASA Power of 10 R4 | default |
| K003 | nesting depth | 3 | ESLint `max-depth` | default |
| K004 | parameters | 4 | ESLint `max-params` | default |
| K005 | cognitive complexity | 15 | SonarSource | default |
| K006 | blanket exception swallowed | 0 | NASA Power of 10 R7 | default |
| K007 | module-level mutable state | 0 | NASA Power of 10 R6 | default |
| K008 | placeholder comment | 0 | finish it, or file it | default |
| K009 | commented-out code | 0 | version control owns history | default |
| K010 | banner / decorative comment | 0 | they lie after every refactor | default |
| K011 | missing public docstring | 0 | PEP 257 · Effective Dart · Go · Rust | default |
| K012 | docstring summary is not a sentence | 0 | Effective Dart · Go | strict |
| K013 | comment is not a sentence | 0 | Effective Dart | strict |
| K014 | comment restates the line beneath it | 0 | the comment says why, not what | strict |

Recursion is matched on bare function calls and on `self.name(...)` inside a method. An
arbitrary `object.name(...)` call cannot be resolved without type inference, and treating
it as an edge flags every function whose name matches an unrelated method — measured at
13.5% precision before the rule was tightened.

Every limit traces to a published standard, quoted with its source in
[`references/limits.md`](references/limits.md).

## What it cannot check

KROKO is deterministic about what it measures. It cannot tell you code is correct,
secure or well designed.

- Complexity metrics are proxies. A function can score zero on every gate and still be
  wrong.
- K003 and K007-K014 are verified by fixture only. Their precision on real-world code is
  **unmeasured**, and this README does not imply otherwise.
- Syntax support is bounded by the grammar, not by a Python install. The gate accepts
  modern syntax — `match`, walrus, `except*` — on any machine. What it cannot parse it
  reports as K000 rather than crashing.

## Precision, measured

Two independent implementations of the same rules — one reading the AST, one reading
`tokenize` output — over 1,446 files and 562,428 lines of the Python standard library:

| Code | Method | Disagreements |
|---|---|---|
| K002 function span | differential vs INDENT/DEDENT block extent | **0** |
| K004 arity | differential vs parameter count from header text | **0** |
| K006 blanket exception | differential vs token-level `except` clause | **0** |
| K001 recursion | 10 sampled findings adjudicated by hand | 10 of 10 genuine |
| K005 cognitive | invariant: score never below branch count | 0 violations |

Building the oracle found six defects — four in the oracle, two in the gate. The worst
gate defect: `def f(a, b, c, d, e, /, f)` scored as **arity 1**, so a single slash
defeated the parameter limit entirely. Both are fixed and locked with fixtures.

The oracle was a second, token-level implementation in Python, used during development
to find those defects. It is not shipped: the shipped guarantee is the 26-case corpus in
`rust/tests/fixtures.rs`, which asserts exact code sets and runs on every `cargo test`.

## Performance

Over the Python standard library — 1,446 files, 562,428 lines — measured with
`/usr/bin/time -l`:

| Metric | Rust (now) | Python (replaced) | Change |
|---|---|---|---|
| Wall time | **2.34 s** | 9.27 s | **4.0x faster** |
| Per file | 1.6 ms | 6.4 ms | 4.0x |
| Throughput | 617 files/s | 156 files/s | 4.0x |
| Peak memory | **31.2 MB** | 63.1 MB | **2.0x smaller** |
| Crashes | 0 | 0 | — |

On the real use — a pre-commit hook over the handful of files a change touches — it is
**under 15 ms**. The binary is statically linked: no interpreter, no runtime, and nothing
in the analyser can reach undefined behaviour.

Noise matters as much as speed. Default mode reports 10,363 findings across that corpus,
about 18 per 1,000 lines. Strict mode reports 103,185, of which 89,417 are the sentence
rule firing on legacy comments: only 9.5% of existing comments in that corpus end in a
full stop. **Strict mode is a gate for code being written now, not a migration tool.**

## Install as a skill

KROKO is a Hermes / ClawHub skill: `SKILL.md` sits at the repository root.

```bash
hermes skills install Sakib-Dalal/KROKO
```

Or install a local copy into every profile:

```bash
./install.sh
```

It builds the binary, runs the corpus, copies into `~/.hermes/skills/kroko` and every
`~/.hermes/profiles/*/skills/kroko`, then re-runs the suite from each installed location
to prove the copy works where it now lives.

## Install the pre-commit hook

```bash
./install-hook.sh /path/to/repo
```

The hook checks only the staged Python files, in strict comment mode, so a commit costs
tens of milliseconds rather than a full sweep. Existing hooks are preserved with a
timestamped backup. Verified end to end: a commit containing a recursive, undocumented,
`TODO`-bearing function is blocked with exit 1; a clean commit passes.

Paths the hook must never police — a fixture corpus of deliberately bad code, generated
files — go in `.krokoignore` at the repository root:

```
tests/fixtures/
```

Escape hatch: `git commit --no-verify`. Each use is evidence of a finding worth fixing.

## The comment doctrine

The principle: **a comment exists to say what the code cannot say.** Apply the test *"if I
delete this, what is lost?"* — if nothing, delete it.

1. **Say why, not what.** The code states the mechanism; the comment states the reason.
2. **Never narrate the code back.** Overlapping words with the line beneath is a
   duplicated line (K014).
3. **Sentences, capitalised, punctuated** — even fragments (K013).
4. **Document the public surface only** — the module and every exported function (K011).
5. **State the contract the signature cannot hold**: empty input, raised errors, caller
   obligations, cost, mutation. Prescriptive mood — "Return the path", not "Returns the
   path" (PEP 257).
6. **No dead code, no decoration, no bookkeeping** — placeholders, commented-out code and
   banner art (K008-K010).
7. **A stale comment is worse than none.** Update it in the same change, and never write a
   comment asserting behaviour you have not executed.

Full doctrine, with per-language forms for Python, Dart, Go, Rust, Swift, TypeScript and
C/C++: [`references/comment-doctrine.md`](references/comment-doctrine.md).

## Repository layout

```
SKILL.md                          the skill itself, at the repo root
README.md  LICENSE  AGENTS.md     this file, MIT, and the agent contract
install.sh  install-hook.sh       profile installer, git hook installer
rust/src/lib.rs                   the gate, codes K000-K014
rust/src/main.rs                  the CLI: paths, --strict-comments, exit codes
rust/tests/fixtures.rs            26 cases asserting exact code sets
rust/Cargo.toml                   the only dependency tree
references/limits.md              the budget, with quoted origins
references/comment-doctrine.md    the seven comment rules, per-language forms
references/managed-language-leaks.md   Power of 10 Rule 3 translated
references/interface-gates.md     UI/UX numbers and ten design rules
templates/AGENTS.md               drop-in repo contract for any project
templates/pre-commit              the hook, strict mode, staged files only
tests/fixtures/                   26 fixtures the test suite asserts against
tools/halftone-core.js            the halftone engine (from the halftone-art skill)
tools/render_logo.html            renders the mark in a browser; parametric
assets/kroko-logo.png             the mark
assets/source/                    the public-domain photograph and its CREDITS
.github/workflows/ci.yml          fmt, clippy -D warnings, cargo test
```

The analyser is held to `cargo clippy --all-targets -- -D warnings` and `cargo fmt
--check`; every rule is held to the 26-case corpus. CI runs all three on every push.

## Contributing

The gate is meant to be argued with — by measurement, not by opinion.

1. A new rule needs a fixture that fails and a fixture that passes.
2. A false positive is a bug in the *metric*, fixed once, centrally — never a whitelist,
   never an exemption. Four such bugs are documented in `SKILL.md` under Pitfalls.
3. Changing a limit means changing `references/limits.md` and citing the standard that
   justifies it.
4. Before opening a pull request:

```bash
cd rust
cargo test --release
cargo clippy --all-targets -- -D warnings
cargo fmt --check
```

CI runs the same three commands.

## License

MIT © 2026 Sakib Dalal. See [LICENSE](LICENSE).
