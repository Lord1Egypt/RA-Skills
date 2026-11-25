# paper-rewriter

[![GitHub Stars](https://img.shields.io/github/stars/docsor1212/paper-rewriter?style=social&label=Star)](https://github.com/docsor1212/paper-rewriter)

> **Current: v5.19.0** — see `scripts/hxt_core.py` (`__version__`) and per-release notes on the GitHub Releases page; in-package verification: `python scripts/selfcheck.py`.

Bilingual (CN/EN) style naturalization for academic & medical writing: find stiff,
templated or machine-flavored patterns, clean mechanical debris, revise for clarity
and natural register — with integrity guardrails on every step.

Deterministic cleanup (model artifacts, punctuation, filler), style-pattern
self-check reports (local heuristic, detection only), sentence-level rewrite
planning, a deterministic deep-polish mode, and a whole-document integrity guard
(numbers, DOIs, PMIDs, terminology must survive untouched). 100% local, zero
upload, Python standard library only.

## Install / Quick Start

Install via your skill manager (skills CLI / ClawHub / SkillHub), or clone this
repository and run the scripts directly with Python 3 (no dependencies):

```bash
# one command: self-check -> cleanup -> revision brief -> integrity guard
python scripts/pipeline.py draft.txt -o out.txt --terms terms.txt

# or step by step
python scripts/detect.py draft.txt            # style-pattern self-check
python scripts/transform.py draft.txt -o step1.txt
python scripts/verify.py draft.txt step1.txt  # integrity guard (exit 0/1/2)

# full guide, boundaries and agent invocation protocol
cat SKILL.md
```

**China mirror (ModelScope 魔搭)**: <https://modelscope.cn/skills/Docsor/paper-rewriter> — if you find this skill useful, a like there helps others find it.

## What you get

- **Style self-check** — pattern-level hits with line numbers and a plain-language
  rationale per hit (local heuristic scoring; explicitly *not* an AI-detection score)
- **Deterministic cleanup** — model artifacts (oaicite/[cite:] debris), punctuation,
  filler phrases; every edit logged for audit (`--track`)
- **Sentence-level plan** — P0 queue of what to rewrite first, with section context
- **Integrity guard** — numbers, p-values, DOIs, PMIDs, years and terminology must
  survive rewriting; violations fail loudly with a printable prescription report
- **Submission bundle** — 12 numbered items (dashboard, compare sheet, guard
  prescription, write manifest) in one directory
- **In-package selfcheck** — `python scripts/selfcheck.py` verifies environment,
  structure, core features and doc reconciliation in one command (exit 0 = healthy)
- **External lexicon** — `--lexicon file.json` appends team/discipline word families
  without touching the package (single source, shareable across skills)

## Verification

```bash
python scripts/selfcheck.py          # in-package: env/structure/smoke/reconciliation
python scripts/calibrate.py          # density-threshold evidence table (reproducible)
python3 -m pytest tests/ -q          # full offline battery (repo clone)
```

## Integrity guardrails

Permitted: polishing your own drafts; aligning AI-assisted text with your voice
where disclosure is allowed or required. Not permitted: misrepresenting
authorship, concealing required AI disclosure, or defeating integrity review —
the toolkit refuses that framing. See `references/compliance.md`.
