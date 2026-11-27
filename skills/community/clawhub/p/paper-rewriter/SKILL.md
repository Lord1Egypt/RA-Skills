---
name: paper-rewriter
description: >
  Academic writing style toolkit, bilingual CN/EN: paper rewriting with AI-flavor
  self-check and style naturalization (scan reports are detection only),
  deterministic cleanup (model artifacts, punctuation, filler phrases), integrity
  guardrails (numbers, DOIs, PMIDs, terminology must survive untouched), and
  agent-guided revision for clearer, more natural academic prose. Built for
  scholars whose formal writing reads stiff, templated or machine-flavored —
  especially non-native (ESL) authors. Skip when: pure grammar polish, full-text
  translation, or rewriting unrelated to academic writing — use a dedicated tool.
  Includes AIGC-disclosure compliance checks (China 2025-09 labeling rules) and
  academic-integrity guardrails: this tool improves writing quality for
  self-review; it does not help misrepresent authorship, conceal required AI
  disclosure, or defeat integrity review. 100% local, zero upload, Python stdlib
  only. Related: paper-polisher-pro (broad polishing), pubmed-verifier,
  cite-holmes, academic-figures.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# Academic Style Toolkit (paper-rewriter)

Bilingual (CN/EN) style naturalization for academic & medical writing: find stiff,
templated or machine-flavored patterns, clean mechanical debris, revise for clarity
and natural register — with integrity guardrails on every step.
**Reading map (30-second routing; equivalent of [references/INDEX.md](references/INDEX.md))** — take what you need:

- **Start / troubleshoot**: quick start · [pitfalls](references/pitfalls.md) + [errors](references/errors.md)
- **Flow / scenarios**: [deep_rewrite_guide](references/deep_rewrite_guide.md) · [best_practices](references/best_practices.md) · CI/agent → automation
- **Limits / compliance**: [honest_boundaries](references/honest_boundaries.md) · [permissions](references/permissions.md) · [compliance](references/compliance.md)
- **Reference / tools**: [api](references/api.md) · [pdf_confidence](references/pdf_confidence.md) · [calibration](references/calibration.md) · [customization](references/customization.md)
**Two layers in one line**: mechanical cleanup (transform/pipeline, deterministic) vs quality revision (agent per style guide) — run pipeline first, read the report, then decide what to deep-revise.

> **Routing in one line**: grammar/fluency/journal-format polish → use a polisher
> (paper-polisher-pro); de-templating, model-residue cleanup, AI-flavor style
> self-check and rewriting → this tool. Need both? Polish first, then run this pipeline.

## Feature status (v5.21.0)

⚠️ rows = experimental (may reject valid files; review output). **The full per-generation capability list has moved to [references/feature_status.md](references/feature_status.md)**; per-item details live in references/errors.md and topic docs. Stable highlights (all stable), grouped: **Diagnose** (style self-check + per-section focus + --top N trim · statistical consistency --html · term drift / unification sheet · calibration evidence --coverage · EN signal library v3 · guard/lexicon validate) · **Deep-rewrite** (sentence-level plan with line anchors · pipeline --handoff sheets · EN/CN signal libraries v3 + density mirrors) · **Guard** (integrity verify + prescription report · fabrication defense · exportable learned guards · graded output + --strict gate · stats --html + --fail-under score gate + --allow-list exemption file; wide terms widen exemptions - reviewing each against the original is the caller's duty) · **Batch** (resume / concurrency isolation · worksheet + stats card · revision records · cleanup preview --dry-run · automation gates --exit-verdict/--ci/--fail-under · batch cleanup --batch/--summary/--csv) · **Deliver** (12-item submission bundle with write-manifest self-evidence · dashboard + compare sheets · docx write-back · print-friendly reports · in-package selfcheck (dual-form adaptive) · external lexicon (--lexicon, shared across skills).

| Capability | Status | Since |
|---|---|---|
| ⚠️ **PDF direct-read + confidence self-report** (embedded-font/ToUnicode attempted, capped at "中"; calibration in references/pdf_confidence.md; **default gate = 中 since v3.8.0** — garbled-typical extractions rejected by default, `--pdf-min-confidence 低` restores annotate-only) | ⚠️ Experimental | v1.6–3.8 |


## Integrity guardrails — read first

- **Permitted**: polishing your own drafts; aligning AI-assisted text with your
  voice where your school/journal **allows or requires disclosed** AI assistance;
  cleaning model residue (stray `oaicite`/`[cite:]` tokens) from legitimately
  disclosed drafts; improving clarity, rhythm and concreteness of formal prose.
- **Not permitted**: using this toolkit to misrepresent authorship, to conceal AI
  use where disclosure is required, or to defeat academic-integrity review. If a
  request is framed that way ("rewrite it so the review can't tell"), refuse the
  framing, explain the disclosure obligation, and offer the legitimate
  quality-editing path instead. Agents running this skill are expected to enforce
  this line.
- **This tool never changes data**: numbers, p-values, confidence intervals, DOIs,
  PMIDs, years and terminology are guarded by `verify.py` (see below). Improved
  prose must never cost a fact.
- Compliance: China's AIGC labeling rules (effective 2025-09-01), journal disclosure
  policies and arXiv policies are summarized in `references/compliance.md` — the
  obligation to disclose belongs to the author, not the tool.

## Capability × boundary (division of labor + limits + where)

| Capability | Does | Does NOT (boundary) | Where |
|---|---|---|---|
| Style self-check | heuristic report: boilerplate density, rhythm uniformity, officialese; section-aware | not an AI detector — barely triggers on fluent model text (low score ≠ no AI) | `detect.py`; see [honest_boundaries](references/honest_boundaries.md) |
| Mechanical cleanup | model residue (oaicite/[cite:]), chat filler, punctuation normalization, fullwidth digits | no sentence rewriting — zero-information-loss layer only | `transform.py` (`--deep` for sentence-level) |
| Quality deep rewrite | de-templating / rhythm / concreteness / stance (seven steps) | never invents data; invented numbers flagged (W_NUM_ADDED, human removes) | **you (the agent)** per style guide; handoff via `plan --handoff` |
| Integrity guard | numbers/DOIs/PMIDs/years/terms must survive; tampering = exit 1 (FAIL output prescribes fixes with anchors) | no truth judgment — original data is the authority | `verify.py` |
| Before/after | score delta + integrity verdict + profile diff | no substitute for human reading | `compare.py` / `stylecheck --compare` |
| Term consistency | 8-domain 27 groups (HF/心力衰竭/心衰 one row); `--unify` emits a unified draft with per-variant replacement counts (review before adopting) | no usage correctness — synonym unification only | `check_terms.py --pack` / `--unify` |
| Numeric consistency | percent-list sums (partition-cued) / cross-file group-n / p-vs-P style | not a statistics review — original data is the authority | `check_stats.py` (`--batch`) |


## Quick start

**Run the in-package selfcheck first**: `python scripts/selfcheck.py` — environment / structure / core-feature smoke / doc reconciliation in one command; exit 0 means installed correctly (ships with the published package; `--json` for CI/agents).

**How to ask for this in plain words** (EN digest of the full phrase table in
SKILL_ZH.md): "remove the AI flavor from this paper" / "this reads too templated" /
"clean up oaicite and [cite:] residue" / "tell me which sentences to fix first" /
"check my rewrite broke no numbers" / "give me a style profile" / "stop flagging
this legitimate term" — each maps to the pipeline, `plan.py`, `transform.py`,
`verify.py`+`compare.py`, `stylecheck.py` and `learn_guards.py` respectively.
No agent is required — every capability below runs directly in a terminal.
Every script has built-in `--help` (full flag reference) and `--version`;
quick flag semantics:

| Flag | Meaning |
|---|---|
| `--profile general` | non-academic text: down-weight formulaic/boilerplate signals |
| `--deep` | deterministic sentence-level transforms (canned openers, not-only merge) |
| `--exit-verdict` | machine exit codes for CI/agent gating (see below) |
| `--structure` | section-aware scoring (IMRaD) |
| `--step-timeout SEC` | per-step wall-clock budget (default 120) |
| `--terms FILE` | term list for the integrity guard (build via extract_terms.py) |
| `--unify SHEET` | check_terms: emit a term-unified draft (advisory — review the replacement list) |
| `--section abstract` | detect: diagnose one section in isolation (the abstract is what reviewers read first) |
| `-o revised.docx` | `-o` on pipeline/transform/compare writes Word when the path ends in `.docx` (plain paragraphs; merge manually for complex layouts) |

One command (self-check → cleanup → revision brief → integrity guard):

```bash
python scripts/pipeline.py draft.txt -o out.txt --terms terms.txt
```

- **Visualization / batch**: `--html report.html` on detect/pipeline/compare for a
  self-contained report (compare adds sentence-level diff); `--batch dir` scans a
  whole directory (pipeline writes a CSV; the batch `-o` summary stays CSV — no
  docx write-back for the table); `-o` on pipeline/transform/compare ending in
  `.docx` is written back as Word (plain paragraphs — closes the loop
  with `.docx` direct-read; tables/images/styles are not rebuilt, merge complex
  layouts manually).
- **Section-aware**: `detect --structure` scores abstract/intro/methods/results
  separately; methods/results phrasing is genre convention — normalized in the
  aggregate only, raw per-section scores always shown.
- **Rewrite plan**: `plan.py draft -o plan.md` ranks sentences (P0 queue +
  budget projection); add `--handoff` for a per-sentence operation sheet.
- **Inputs**: `.txt`/`.md` direct (**UTF-8/UTF-16〔with BOM〕/GBK auto-transcoded**, v4.0), `.docx` direct, PDF **experimental** (**default safe gate = medium since v3.8**; `低` restores annotate-only; [references/pdf_confidence.md](references/pdf_confidence.md)).
- **Term list**: `python scripts/extract_terms.py draft.txt -o terms.txt` (confirm
  by hand); any run accepts `--suggestions path.md` for a revision worksheet.
- **Non-academic text**: add `--profile general` to down-weight formal boilerplate.

Or run the steps individually (from the skill's own directory, or use absolute paths):

```bash
python scripts/detect.py draft.txt            # style-pattern self-check (-j JSON, -s score only)
python scripts/transform.py draft.txt -o step1.txt
# ... agent quality revision of step1.txt per the style guide ...
python scripts/verify.py draft.txt step2.txt --terms terms.txt
python scripts/compare.py draft.txt step2.txt
```

Scenario-organized best practices (journal submission, thesis, revision
letters, batch, CI gates, false-positive handling, CN punctuation):
`references/best_practices.md`.
Worked end-to-end examples: `references/examples.md`. Unified exit codes,
violation categories and remedies: `references/errors.md`. **Centralized
common-mistakes list (27 items): `references/pitfalls.md`** — read it before
your first real run. Python API reference: `references/api.md`. FAQ:
`references/faq.md`.

- **Revision tracking**: `--track base` records every mechanical-layer change to
  `base.md` + `base.json` (auditable: rule, count, deleted sentences, flagged).
- **PDF (experimental)**: text PDFs incl. embedded-font/ToUnicode since v3.0.0 —
  extraction attempted, confidence capped at "中" with a spot-check note; CJK CID
  files still rejected by the garbage probes with export guidance. Scale: 800K-char
  chunks (2K overlap) · 50MB cap · whole-document integrity guard.


### Agent invocation protocol

When invoked, decide the path first, then run it:

- **Trigger words**: 写作风格自查 / 论文改写润色 / 去模板腔 / 翻译腔清理 /
  学术改写 / 段落改写 / 表达优化 / style self-check /
  style naturalization / naturalize academic writing / de-templating /
  academic rewriting / passage rewrite / expression polish /
  translationese cleanup (= Europeanized syntax: stacked passives, nominalization
  chains, long attributives — see style_guide_en steps 1/3) /
  make my writing sound less machine-written / reduce the templated tone /
  clean up model residue or stray citation tokens / fix stiff formal prose /
  polish my draft for submission without changing the data /
  check that numbers and citation IDs survived editing → run the pipeline
  above.（中文变体触发词见 SKILL_ZH.md——CH 分寸词不入英文文件；
  数字自洽/术语混用类请求路由到 check_stats.py / check_terms.py，见下）
  （Parameter cheat sheet lives in Quick start; exit-code tables in
  references/errors.md — both are linked from here to avoid hunting across
  sections.）
- **Disambiguation (this tool vs a polisher)**: 「论文改写润色」 here means
  style naturalization / de-templating (removing the machine flavor from
  academic prose). Decision rule — route to a polisher (paper-polisher-pro)
  when the ask is only about language correctness/fluency: 「帮我改下语法」
  「按期刊风格改写摘要」; route to this toolkit when it is about templated tone
  or model residue: 「这篇读起来像 AI 写的」「文里有 [cite: 1] 这种残留」;
  when both apply, polish first, then run this pipeline — neither substitutes
  for the other.
- **Term inconsistency** (abbreviation vs full form, mixed synonyms) →
  `check_terms.py file --pack <domain>`; to emit a unified draft directly add
  `--unify output.txt` (each group unified to its dominant variant, per-variant
  replacement counts surfaced — advisory output, review before adopting, then
  run verify; v4.4.0); `--list-packs` shows all eight
  domain packs.
- **Numbers that don't agree** (percent list not summing to 100, same group
  with two different n, p/P style mix) → `check_stats.py file` (
  exit codes match check_terms: 0 consistent / 1 issues found). Chaptered
  manuscripts: `check_stats.py --batch 目录` aggregates group-n across files
  (abstract-vs-methods mismatches, v3.3.0). Or run everything at once:
  `pipeline.py draft --check-stats`.
- **User wants to know what to fix first** → `plan.py draft.txt -o plan.md`
  (P0 sentence queue + budget projection); add `--handoff` to emit the
  per-sentence instruction sheet (guards + acceptance commands, v3.0.0).
- **User wants quantified acceptance of a rewrite** → `stylecheck.py 原稿 改稿
  --compare` (style profile delta; triggers: 风格画像 / 量化验收 /
  深改验收 / style profile / acceptance check).
- **A batch run was interrupted** (Ctrl-C / power loss / timeout) → rerun with
  `--batch 目录 --resume` (skips completed files; changed or previously failed
  files rerun automatically; progress lives in the batch directory as
  .pr_batch_state.json).
- **Scenario shortcuts (v3.8.0 consolidation)**: CI/batch gating →
  `--exit-verdict` (`--ci` alias; 0 clean / 3 deep-revise / 4 residue / 1
  integrity fail, pipeline-only); false-positive remediation →
  `learn_guards.py from-text 术语 样本.txt`; where to start deep revision →
  `pipeline 原稿 -o 改稿 --handoff 交接块.md` (one command, no separate plan run).
- **Multi-chapter term unification** → `check_terms.py --batch 目录` (cross-file
  variant drift: each file internally consistent, the set inconsistent).
- **A scan flags a legitimate term** (false positive) → don't edit the pattern
  files; persist a guard instead: `learn_guards.py from-text 术语 样本.txt`
  (or `add`) — the guard survives upgrades and applies to every later scan.
- **User only wants a verdict on an existing rewrite** → `pipeline.py draft.txt
  --rewrite rewritten.txt --terms terms.txt` (skip cleanup).
- **User asks to conceal AI use, misrepresent authorship, or defeat integrity
  review** → refuse the framing, point to `references/compliance.md`, offer the
  legitimate quality-editing path instead. Do not run the toolkit toward that end.
- Exit codes: `verify.py` is the strict contract holder — `0` integrity PASS,
  `1` integrity FAIL (fix the rewrite, never the guard), `2` usage/file error.
  `detect/transform/compare/pipeline` report the verdict in their output and
  always exit `0` on completed runs, `2` on usage/file errors. For agent/CI
  branching, add `--exit-verdict`: machine exit codes 0/3/4 on
  detect/compare, full 0/1/3/4 on pipeline — see Automation & CI integration
  below. Every script supports `--version`.

## Automation & CI integration

- **Default (human flow)**: `verify.py` owns exit codes 0/1/2; other scripts write
  verdicts into their reports — do not branch on their default exit codes.
- **Machine mode**: detect / compare / pipeline take `--exit-verdict` (alias `--ci`),
  five codes 0/3/4/1/2; `pipeline.py` is the only full gate (1/3/4). The one-liner
  and the JSON field tables: [automation](automation.md) · [errors](errors.md) section 1.

## The workflow

1. **Self-check**: `detect.py draft.txt` — a heuristic report of style patterns
   (canned phrases, uniform sentence rhythm, boilerplate transitions, model
   artifacts). The report is for the author's own review; the score is a local
   heuristic, not an official measurement of anything.
2. **Mechanical cleanup**: `transform.py draft.txt -o step1.txt` — strips stray
   model artifacts (`oaicite`, `turn0search`, `[cite: 1]`, `grok_card`,
   `attached_file`), leftover chatbot pleasantries, markdown residue, and a safe
   list of filler phrases; CN halfwidth punctuation is normalized to fullwidth
   (decimals protected). `-a` adds em-dash reduction and empty-opener removal.
   `--deep` adds sentence-level deterministic transforms — canned
   opener deletion, 「不仅X，而且Y」→「X，且Y」 merging — zero-information-loss
   only, every operation logged to `--track` — the log is the audit trail.
   Text with no hits passes through with zero edits (fullwidth alnum
   normalization is the only exception; per-replacement counts are
   re-runnable via `--track`, so any claim here can be verified locally).
3. **Quality revision** (the real work): optionally rank the work first —
   `python scripts/plan.py draft.txt -o plan.md` gives a sentence-level P0
   queue (worst offenders with section, category and advice) so deep effort
   lands where the score lives; add `--handoff` to emit a per-sentence
   operation sheet (original sentence + directive + guard rules + acceptance
   commands) that a rewriting agent can follow verbatim.
   Then read the guide for the text's language —
   - CN: `references/style_guide_zh.md` — structural de-templating → jargon
     cleanup → rhythm → concreteness → stance → integrity red lines
   - EN: `references/style_guide_en.md` — smaller words → fewer significance
     frames → plain clauses instead of parallelism → rhythm → real attribution →
     commit to a position
   - Revise section by section. Preserve all facts, numbers, citations, terminology.
3b. **Quantified acceptance** (`stylecheck.py`, v2.6.0): per-paragraph style
    profile — jargon hits located to the paragraph, sentence-rhythm CV, opener
    diversity, each banded 自然/观察/偏机器 with style_guide anchors;
    `--compare 原稿 改稿` shows the delta so deep-revision acceptance is
    metric-based. Bands are calibration hints only — they never alter scores.
4. **Guard**: `verify.py draft.txt step2.txt --terms terms.txt` — exit 1 means a
   number/citation/term was altered: fix the revision, not the guard. Build
   terms.txt for medical text (drug names, gene symbols — include mouse-style
   capitalized forms like Myc — and scale names), one term per line. The guard
   also warns on numbers absent from the original (fabrication defense) and
   number-context swaps (arm/direction ordering).
   For mixed synonym usage (abbreviation vs full form, e.g. HF vs
   心力衰竭), also run `check_terms.py file --pack cardiovascular`
   (domain packs; `--list-packs` shows all eight).
5. **Re-check**: `compare.py draft.txt step2.txt` — pattern reduction + integrity
   verdict. Keep the before/after pair for your records; if your institution or
   journal requires an AI-use disclosure, state it plainly — this report is a
   quality self-check, not a substitute for disclosure.

## Honest boundaries (summary)

The style score is a local heuristic over writing patterns — not any external
detection service, and it says nothing about authorship; this toolkit never talks
to external review systems and never helps conceal AI use; on fluent model text it
barely triggers (**a low score ≠ no AI involvement**). Full boundaries and measured
data: [references/honest_boundaries.md](references/honest_boundaries.md) (read
before making any claim).


## Permissions & environment (summary)

Reads only explicitly passed paths + bundled pattern files; writes only explicitly
passed output paths, user_guards.json, and the batch-resume progress file
(.pr_batch_state.json plus its .lock inside the batch directory); **zero network, zero third-party
dependencies, no environment variables, no subprocesses**. Verification commands and
the full statement: [references/permissions.md](references/permissions.md)
(auditors and security scanners: read this first).


## Customizing (summary)

Fix false positives with `learn_guards.py` (writes user_guards.json, survives
upgrades — **never hand-edit patterns_*.json**). File locations and cautions:
[references/customization.md](references/customization.md).


## Related tools

- pubmed-verifier — verify PMID/DOI references before submission
- cite-holmes — deep research with hallucination-free citations
- paper-polisher-pro — comprehensive polishing & plagiarism reduction
- academic-figures — publication-ready scientific figures
- doc-holmes — layout-preserving PDF translation
