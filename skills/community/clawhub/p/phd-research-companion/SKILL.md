---
name: phd-research-companion
description: Full-lifecycle research management for CS PhD students — literature search over real APIs, LaTeX skeletons that compile, proof ledgers, priority checks, exact-arithmetic certificates, revision tracking and pre-submission audit. Use when a research project needs to be set up, tracked, checked for novelty, or audited before submission. Supports --track=theory (proof-first) and --track=empirical (experiment-first).
version: 2.4.0
---

# PhD Research Companion v2.4.0

Research lifecycle management with scientific traceability. Every command is
executable and every result is derived from real data — nothing in this skill
produces placeholder or fabricated output.

## Core rule

**This skill never invents a result.** If a source cannot be reached, a PDF
cannot be parsed, or a claim is unproved, the tool reports the gap. A gap that
is reported is useful; a gap that is silently filled is a liability.

## Two tracks

Choose once, at project creation:

| | `--track=theory` | `--track=empirical` |
|---|---|---|
| Primary artifact | proof ledger + certificates | experiment designs + results |
| Novelty gate | `priority` before claiming | baseline comparison |
| Evidence | exact rational arithmetic | repeated seeded runs |

Theory track adds `ledger`, `priority`, `certify`, `audit`, `session`.

## Entry point

`./run` is gone (bash-only, unusable on Windows). Use:

```bash
python run.py <command> [args...]
python run.py help
```

Relative output paths resolve against **your current directory**, not the skill
install directory — run commands from inside the project, or pass an absolute
`-o` / `-p`.

Two conventions hold across every command: the project directory is `-p`
(`-d` is accepted as an alias), and the output directory is `-o` (`--out` is
accepted as an alias).

| Command | Script | What it does |
|---|---|---|
| `init` | `init_research_project.py` | create project skeleton |
| `search` | `scripts/multi_source_search.py` | real literature search |
| `analyze` | `scripts/paper_analyzer.py` | extract structure from PDFs |
| `template` | `scripts/generate_latex_template.py` | compiling LaTeX skeleton |
| `experiment` | `scripts/create_experiment_design.py` | baseline/ablation/robustness designs |
| `revision` | `scripts/revision_tracker.py` | revision rounds + evidence hashes |
| `math` | `scripts/verify_math_notation.py` | notation lint |
| `check` | `scripts/check_compliance.py` | pre-submission audit |
| `ledger` | `scripts/proof_ledger.py` | claim DAG (theory) |
| `priority` | `scripts/priority_check.py` | novelty check (theory) |
| `certify` | `scripts/rational_certificate.py` | exact-arithmetic certificate (theory) |
| `audit` | `scripts/self_audit.py` | proven vs publishable (theory) |
| `session` | `scripts/long_horizon_session.py` | mid-proof persistence (theory) |

`score` and `selftest` (§10) score **this repository** and exist only in the
full build; `run.py help` prints a `self-check:` block listing what the current
build actually ships, and calls a missing optional command exit 2 with a clear
message rather than a bare "missing script".

## 1. Project setup

```bash
python run.py init -d "mirror descent vs diagonal GD" -j JMLR --track theory -o ./proj
```

Creates `00-dashboard/` … `07-audit-trail/`, plus `02-methodology-dev/proofs`
and `certificates` on the theory track. Dashboard `index.html` is written to
`00-dashboard/`, `project.json` holds metadata, `README.md` reflects the domain
you passed (not a canned example).

## 2. Literature search — real APIs

```bash
python run.py search -q "regression data selection" -s arxiv dblp openalex -l 30 \
    -o ./proj/01-literature-survey
python run.py search -q "..." --year-from 2020 --year-to 2026 -s arxiv
```

Sources: `arxiv` (Atom API), `dblp`, `openalex`, `semanticscholar`.
Rate-limited with retry and backoff; 429/503 back off harder.

Measured availability (verified 2026-10-11, subject to change):

| Source | Status |
|---|---|
| `arxiv` | works over **https**; returns 429 when polled too fast |
| `openalex` | works, no key required |
| `semanticscholar` | frequently 429 without an API key |
| `dblp` | the public JSON endpoint sits behind a bot challenge and usually returns an HTML page |

A source that answers with the wrong content type is rejected outright — the
response is never parsed as data it is not. If every source fails, the command
exits 2 and writes nothing.

Guarantees:
- A failed source is reported in the output and in the summary, never hidden.
- If **no** source succeeds, the command exits 2 and writes nothing.
- A BibTeX entry is emitted only for a record with a title; entries are checked
  for brace balance before being written.

Outputs `search-results-<ts>.bibtex` and `search-summary-<ts>.md`.

## 3. PDF analysis

```bash
python run.py analyze -i ./proj/01-literature-survey --mode deep -o ./analysis
```

Needs `pypdf` (see `requirements.txt`); `PyPDF2` and `pymupdf` also work.
A PDF yielding fewer than 50 words is reported **UNEXTRACTABLE** (probably
scanned) — never summarised from the filename.

## 4. LaTeX skeleton

```bash
python run.py template -j JMLR --track theory -t "Title" -a "A Author" -o ./proj/03-paper-drafting
```

Venues: `IEEEtran`, `ACM`, `NeurIPS`, `ICLR`, `JMLR`, `article`.
Theory track emits theorem/proof/appendix structure; empirical track emits
algorithm/experiment/ablation structure.

## 5. Experiment design

```bash
python run.py experiment --type comparison --datasets "A,B" --baselines "X,Y" -o ./proj/04-experiments
python run.py experiment --type ablation --components "c1,c2" --base-model M -o ./proj/04-experiments
python run.py experiment --type robustness --attack-types "FGSM,PGD" --perturbation-budgets "0.1,0.3" -o ./proj/04-experiments
```

Design files contain `results: null`. A design is not a result.

## 6. Revision tracking

```bash
python run.py revision --action add_round -r 2 \
    -i "weak baseline" "lemma 4 gap" -x "fixed both" \
    -e ./proj/05-revision-rounds/round2.diff -d ./proj/05-revision-rounds
python run.py revision --action report -d ./proj/05-revision-rounds
python run.py revision --action summary -d ./proj/05-revision-rounds
```

Evidence files are hashed (sha256). Missing evidence is recorded as MISSING,
not skipped.

## 7. Math notation lint

```bash
python run.py math -i ./proj/03-paper-drafting/main.tex --strict
```

Pass **every** `.tex` file of the project, otherwise symbols defined elsewhere
are false positives. Reports commands used but neither standard LaTeX nor
defined in the scanned files, and labels never referenced.

## 8. Theory track

### Claim ledger

```bash
python run.py ledger -d ./proj/02-methodology-dev --init
python run.py ledger -d ./proj/02-methodology-dev --add L1 --kind lemma \
    --statement "bound on B1" --status proven --proof proofs/lemma1.tex
python run.py ledger -d ./proj/02-methodology-dev --add T1 --kind theorem \
    --statement "main" --depends L1
python run.py ledger -d ./proj/02-methodology-dev --set T1 --to proven
```

`--set ... proven` is **refused** while any dependency is unproven. Statuses:
`open`, `conditional`, `proven`, `refuted`. The report flags cycles and
dependencies on unknown claims.

### Priority check — run before claiming novelty

```bash
python run.py priority -d ./proj/02-methodology-dev --claim "C(d,n) = A_leq d(n)"
python run.py priority -d ./proj/02-methodology-dev --resolve P1 --verdict covered \
    --evidence https://arxiv.org/abs/2502.01234 --note "same identity, Thm 3"
```

Verdict defaults to `unchecked`. Resolving requires an `http(s)` evidence URL.
`--strict` exits 1 while anything is unresolved. **Unresolved means the paper
must not call the claim novel.**

### Exact certificates

```bash
python run.py certify --script ./proj/07-audit-trail/check_bound.py --strict
python run.py certify --demo
```

Scans the script for float contamination (float literals, `float()`, bare `/`,
`math`/`numpy`) and requires a `CERTIFIED` / `REFUTED` verdict line. Write
certificates with `fractions.Fraction`.

### Self-audit

```bash
python run.py audit -p ./proj --strict
```

Cross-reads ledger, priority records, certificates and revision history.
Prints blockers (submission-stopping) and warnings (must be disclosed).
A clean audit is necessary, not sufficient.

### Mid-proof persistence

```bash
python run.py session --start "prove C(d,n) = A_leq d(n)" -d ./proj/session
python run.py session -d ./proj/session --attempt "LP duality" --outcome failure \
    --why "dual unbounded; envelope not polyhedral"
python run.py session -d ./proj/session --resume
```

A failed attempt **must** record `--why`, so the dead end is not re-walked next
session. `--resume` prints goal, last state, next action and all dead ends.

## 9. Pre-submission audit

```bash
python run.py check -p ./proj
```

Every check is either implemented or reported **UNVERIFIED**. Unverified is
not a pass. Thresholds: >= 50 BibTeX entries, >= 5 revision rounds.

`check` reads the track from `project.json` (written by `init`):

- **theory** — baseline / ablation / robustness designs are reported **N/A**,
  not failed. A theory paper has no such suite; demanding one is a category
  error. Instead `check` grades theory artifacts: a claim ledger with at least
  one claim, and at least one certificate in `07-audit-trail/`.
- **empirical** — experiment designs are graded; theory artifacts are N/A.

N/A rows are excluded from both the pass count and `--strict`'s exit code.

## 10. Scoring this skill

> Maintainer-only. These two commands score **this repository's** publishing
> hygiene and are omitted from trimmed builds (see `scripts/export_coze.py`).
> If `run.py help` does not list them under `self-check:`, they are not present.

```bash
python run.py score
```

Scores 9 dimensions by executing probes (compile, `--help`, mock detection,
doc/code cross-check, test run, portability, theory-track coverage,
**substance**, hygiene). Appends to `score-history.json`. Use it after any
change.

| Dimension | Weight | What the probe does |
|---|---:|---|
| compilability | .12 | `py_compile` every shipped module |
| runnability | .12 | every script answers `--help` with exit 0 |
| authenticity | .12 | mock-placeholder scan + real academic API hosts |
| doc_consistency | .10 | every file/command SKILL.md advertises exists, is wired, **and every documented flag exists in that command's real CLI** |
| test_integrity | .14 | suite runs green, is non-tautological, and **catches an injected mutation** |
| portability | .08 | no bash-only entrypoint, no unix-only paths |
| fitness | .10 | theory modules present **and non-trivial**, `--track` routing |
| substance | .18 | LOC / top-level defs / real `--help` text / documented commands |
| hygiene | .04 | one version string, no dead files, no foreign attribution |

`substance` and the mutation-catch component of `test_integrity` exist because
a file with the right name is not a module, and a test that cannot fail is
worse than no test.

A dimension score below its floor **caps the total**, because one catastrophic
failure must not be diluted by the other dimensions' weights:
`test_integrity < 5 → 60`, `substance < 3 → 50`, `authenticity < 4 → 70`.

A perfect score is worthless if the scorer cannot go down, so audit the scorer
itself in two phases:

```bash
python run.py selftest                  # both phases
python scripts/score_selftest.py --phase mutation
python scripts/score_selftest.py --phase vacuity
```

- **Phase 1 (mutation)** copies the skill to a temp directory, breaks one thing
  per dimension, and requires the matching score to drop. A dimension that does
  not react is a **BLIND SPOT**: it is printing a number, not measuring
  anything.
- **Phase 2 (vacuity)** removes the substance instead of adding a defect, and
  requires the total to stay under a ceiling. Mutation testing cannot catch
  this: 37 `assert True` tests once scored a genuine **100.00**.

Current status: 9/9 dimensions falsifiable; 4/4 vacuity attacks held below
their ceiling (60 / 60 / 50 / 23.2 against ceilings 70 / 70 / 60 / 40).

Both run in CI (`.github/workflows/ci.yml`) on every push.

## Testing

```bash
python -m pytest tests -q          # or: python -m unittest discover -s tests
```

Tests carry real assertions. A failing check fails the run — there is no
"completed successfully" fallback.

## Packaging

```bash
python scripts/package_skill.py --check-only
python scripts/package_skill.py
```

Validates the frontmatter (slug-shaped `name`, description <= 1024 chars),
compiles every module, runs `--help` on every command, then writes
`dist/phd-research-companion.zip` with a `MANIFEST.txt` (sha256 per file) and a
`.sha256` beside the archive. Bytecode caches, `_skillhub_meta.json` (local
install state, contains absolute paths) and regenerable reports are excluded.
Publishing the zip is safe: it was verified by extracting it and running the
full test suite and lifecycle from the extracted copy.

## Integrity rules

1. Never cite an entry not verified against its source venue.
2. A claim is `proven` only with a proof artifact; otherwise `open`/`refuted`.
3. Numerical evidence must be reproducible by a script in `07-audit-trail/`.
4. Novelty requires a resolved priority record with a URL.
5. Report gaps; do not fill them.

## Known limitations (deliberate, not bugs)

- `run.py score` is written by this skill, so 100/100 is **self-certified**.
  The probes are executable, the weights are stated in `scripts/self_score.py`
  (change them if you disagree), and `run.py selftest` proves each dimension
  actually drops when a defect is injected and that hollow skills stay capped.
  What it still cannot prove is that the *choice* of dimensions is the right
  one — that judgement is yours.
- The mutation-catch probe breaks ONE module (the one most referenced by tests)
  inside a temp copy. It costs a second suite run, so `self_score.py --fast`
  skips it; a light suite may then score higher than it deserves.
- `analyze` reports keyword frequencies, not semantic understanding. It is
  labelled as such in its output.
- `math` is a linter with a standard-command whitelist. It narrows the search
  space; it does not certify that notation is correct.
- `check` reads DPI from PNG (pHYs) and JPEG (JFIF APP0) headers with stdlib
  only. A raster file with no density header stays UNVERIFIED.
- `certify` detects float contamination statically. It will not catch a value
  that becomes inexact at runtime through a different path.
- `check`'s theory/empirical split depends on `project.json` recording the
  track. A project created without `init` has no track, and experiment checks
  then default to **graded**.
- `priority` record IDs are a hash of the claim text. Editing a claim's wording
  creates a new record rather than updating the old one.

## Requirements

Core is stdlib-only. Optional: `pypdf` (PDF analysis), `pytest` (tests).
See `requirements.txt`.

Version: 2.4.0
