# PhD Research Companion v2.4.0

Research lifecycle management for CS PhD students, with scientific
traceability. Two tracks: `--track=theory` (proof-first) and
`--track=empirical` (experiment-first).

**This skill never invents a result.** Unreachable sources, unparsable PDFs and
unproved claims are reported as gaps, never filled with plausible data.

## Install

```bash
# from a clone
git clone <repo> && cd phd-research-companion

# or from a release archive
unzip phd-research-companion.zip && cd phd-research-companion

# smoke-test your install before trusting it
python scripts/self_score.py --no-history        # expect 100.00/100
python -m unittest discover -s tests             # expect all green
```

Requirements: **Python 3.9+, stdlib only.** `pip install -r requirements.txt`
is optional and only adds PDF text extraction (`pypdf`) and `pytest`. No API
key, no account, no network for the core workflow.

## Packaging for publication

```bash
python scripts/package_skill.py --check-only    # validate, write nothing
python scripts/package_skill.py                 # -> dist/phd-research-companion.zip
```

The packager refuses to build a package that a platform would reject: it
validates the `SKILL.md` frontmatter (slug-shaped `name`, description inside the
platform limit), compiles every module, runs `--help` on every command, and
strips bytecode caches, local install state (`_skillhub_meta.json`, which
contains this machine's absolute paths) and regenerable reports. It writes a
`MANIFEST.txt` with a sha256 per file, plus a `.sha256` beside the archive.

## Quick start

```bash
python run.py init -d "mirror descent vs diagonal GD" -j JMLR --track theory -o ./proj
python run.py search -q "regression data selection" -s arxiv dblp openalex -l 30 -o ./proj/01-literature-survey
python run.py template -j JMLR --track theory -o ./proj/03-paper-drafting
python run.py check -p ./proj
```

`./run` (bash) is gone; `run.py` works on Windows, macOS and Linux.

## Commands

| Command | Purpose |
|---|---|
| `init` | create project skeleton |
| `search` | literature search over arXiv / DBLP / OpenAlex / Semantic Scholar |
| `analyze` | extract structure from PDFs |
| `template` | LaTeX skeleton (IEEEtran, ACM, NeurIPS, ICLR, JMLR) |
| `experiment` | baseline / ablation / robustness designs |
| `revision` | revision rounds with hashed evidence |
| `math` | notation and proof-consistency lint |
| `check` | pre-submission compliance audit |
| `score` | automated quality score for this skill (9 dimensions) |
| `selftest` | audit the scorer itself: mutation + vacuity |
| `ledger` | claim DAG — refuses to mark a claim proven over unproven deps |
| `priority` | novelty check; unresolved blocks any novelty claim |
| `certify` | exact rational-arithmetic certificate (flags float contamination) |
| `audit` | proven vs publishable gap report |
| `session` | long-horizon state machine; failed attempts must record why |

## Project structure after `init`

```
proj/
├── 00-dashboard/           # index.html + compliance-status.json
├── 01-literature-survey/   # BibTeX + PDFs + search summaries
├── 02-methodology-dev/     # claims.json, priority-records.json, proofs/, certificates/
├── 03-paper-drafting/      # main.tex + references.bib
├── 04-experiments/         # design YAML (results stay null until measured)
├── 05-revision-rounds/     # revision-history.json + evidence
├── 06-collaboration/       # advisor and peer feedback
└── 07-audit-trail/         # certificates and traceability logs
```

## What changed in 2.0

v1.x shipped documentation for functionality that did not run. Specifically:
4 of 6 scripts failed to compile, 2 more crashed at runtime, the test suite
reported success regardless of outcome, the literature search returned
fabricated entries, and `./run` did not exist.

v2.0 is executable end to end:

- every module compiles and answers `--help` with exit 0;
- literature search uses real APIs and refuses to write unverified entries;
- the compliance audit has no dead checklist entries (implemented or UNVERIFIED);
- the test suite has real assertions and a non-zero exit code on failure;
- a theory track covering the proof workflow: ledger, priority, certificates,
  self-audit, mid-proof persistence;
- `python run.py score` measures all of the above after every change.

## What changed in 2.2

v2.1 audited the *scorer*. v2.2 ran the skill end to end and fixed what that
found:

- **Outputs no longer leak into the installation.** `run.py` used to pin its
  working directory to the skill folder, so every command with a relative
  default (`math`, `session`, `certify`, `search`, ...) wrote its report there.
  Relative paths now resolve against your current directory.
- **`check` is track-aware.** A `--track theory` project is no longer failed for
  missing baseline/ablation/robustness designs; those rows are N/A, and a
  theory-artifacts check takes their place. N/A rows do not trigger `--strict`.
- **One CLI vocabulary.** `-p` works everywhere a project dir is taken (`-d`
  still accepted), `-o` everywhere an output dir is taken (`--out` accepted),
  and `--deps` is an alias for `--depends`.
- The scorer now checks that **every flag shown in the docs actually exists** in
  that command's parser (62 flags checked), and that no generated artifact has
  leaked into the skill directory.

## What changed in 2.4

v2.2 fixed a 14× performance bug and proved the scorer cannot be gamed.
v2.4 makes the skill publishable to a second platform and closes two
correctness holes found while doing it:

- **A Coze skill package, generated not copied.** `scripts/export_coze.py`
  emits `dist/coze/phd_research_companion-coze.zip` with Coze's slug-shaped
  `skill_id`, Chinese description and tags, and pre-filled store listing text
  length-checked against the platform's 20-char name / 200-char description
  limits. Regenerating it on every version bump is the point — a hand-copied
  package goes stale silently.
- **`run.py` degrades instead of crashing on a trimmed build.** The exporter
  drops `score`/`selftest` (they score this repository; an installed user has
  no repository). Those commands moved to `OPTIONAL_COMMANDS`; `run.py help`
  now prints a `self-check:` block listing what the build actually ships, and
  calling an absent command exits 2 with "not available in this build" instead
  of a missing-script error. The exporter's validator caught the original bug —
  `run.py` hard-referenced the dropped modules, so the first published build
  would have failed on first use.
- **The leak guard now scans subdirectories.** `07-audit-trail/certificate-*.json`
  leaked unnoticed because only the skill root was checked. A leak is a leak
  wherever it lands inside the installation.
- **The mutation probe stopped re-running the whole suite.** `variants` leaked
  out of the ranking loop, so the `-k` selector was empty and every score paid
  a second full suite run: 130s → 9.4s.
- Test suite 70 → 76 cases, all passing.

## What changed in 2.1

v2.0 proved each dimension reacts to its own defect, but that only catches
defects *added* to real code. A skill with no substance still scored 100:

| Hollow input | v2.0 | v2.1 |
|---|---:|---:|
| 37 tests that are all `assert True` | 100.00 | 60.00 |
| every module replaced by a stub | 94.40 | 50.00 |
| no tests at all | 88.00 | 60.00 |
| empty shell, one file, no code | 32.50 | 23.20 |

v2.1 closes that:

- new `substance` dimension — LOC, top-level defs, real `--help` text,
  documented commands. A file with the right name is not a module.
- `test_integrity` now rejects tautological assertions and requires the suite
  to **fail** when a module is deliberately broken; `fitness` no longer
  credits a stub named `proof_ledger.py`.
- a dimension below its floor **caps the total**
  (`test_integrity<5 → 60`, `substance<3 → 50`, `authenticity<4 → 70`), so one
  catastrophic failure cannot be diluted by the other weights.
- `python run.py selftest` gained phase 2 (vacuity): it removes the substance
  and requires the total to stay under a ceiling.

## Publishing to Coze

The Coze artifact is **generated, never hand-copied** — the two platforms share a
directory shape but not a metadata contract, so a manual copy silently goes
stale on the next version bump.

```bash
python scripts/export_coze.py --check-only
python scripts/export_coze.py
```

Writes `dist/coze/phd_research_companion-coze.zip` (upload this), plus
`COZE_STORE.md` (the store listing fields, pre-filled and length-checked against
Coze's 20-char name / 200-char description limits) and a sha256 `MANIFEST.txt`.

What the export changes and why:

| | ClawHub / WorkBuddy | Coze |
|---|---|---|
| folder / `name` | `phd-research-companion` | `phd_research_companion` (slug: `[a-z0-9_]`) |
| description | English | Chinese (store audience) + `tags` |
| `score`, `selftest` | shipped | **dropped** — they score this repo, and a Coze user has no repo |
| `self_score`/`score_selftest`/`package_skill`/`export_coze`/`tests` | shipped | dropped (maintainer-only) |
| `install_verify.sh` | shipped | dropped (bash-only; no bash in the sandbox) |

Because the scoring commands are absent, `run.py` keeps them in a separate
`OPTIONAL_COMMANDS` table and degrades them honestly: `run.py help` prints a
`self-check:` block listing what the build actually ships, and calling an
unshipped command exits 2 with "not available in this build" instead of a bare
missing-script error. Every **required** command is validated to resolve to a
file present in the package — that check is what caught the bug during the first
export.

Uploading to Coze itself is still a manual step: import the zip, **deploy**, then
apply for 上架资质 before listing. See `COZE_STORE.md` for the listing text, the
three required showcase cases, and the pre-submission checklist.

### Why free, not paid

Coze's 按次付费 only applies to skills that expose an HTTP API to call
(platform's own wording). This skill is a CLI plus a methodology — there is no
public endpoint, so per-call billing is structurally unavailable. 一次买断
derives quarterly/annual prices from a monthly tier, which is a negative asset for
a graduate-student audience. The `按次付费` fallback would also price out the
academic use case entirely.

## Requirements

Core is stdlib-only. Optional: `pypdf` for PDF analysis, `pytest` for tests.
See `requirements.txt`.

## Testing

```bash
python -m pytest tests -q        # or: python -m unittest discover -s tests
```

## Integrity rules

1. Never cite an entry not verified against its source venue.
2. A claim is `proven` only with a proof artifact; otherwise `open`/`refuted`.
3. Numerical evidence must be reproducible by a script in `07-audit-trail/`.
4. Novelty requires a resolved priority record with a URL.
5. Report gaps; do not fill them.

See SKILL.md for full documentation.
