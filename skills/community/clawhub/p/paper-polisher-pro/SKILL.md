---
name: paper-polisher
version: 7.7.0
author: DoctorQ Lab
description: >-
  AI-rate self-check and polish guidance for academic writing: sentence-level rewrite
  suggestions (locates and advises, never auto-rewrites), terminology and consistency
  checks, translation-smell, paragraph attribution, journal precheck with discipline
  context, style-norm conventions check, quality report, AIGC label check, plus
  `--batch DIR` with HTML summary. Reads .docx directly.
  Not for: document/PDF translation (doc-holmes), plagiarism checking (institutional
  systems), ghost-writing or executing rewrites (paper-rewriter); texts under 100
  chars get no verdict by design.
  100% local, zero upload; bundled tests + AST zero-network self-verification.
  Multi-layer rule engine + token spectrum + optional supervised Qwen3-0.6B ONNX
  layer + LLM fingerprint attribution + freshness pipeline. Base-engine numbers
  reproduce from bundled held-out evals; supervised columns are author-side
  (model not bundled).
tags: [ai-detection, deai, academic-writing, paraphrase, paper-polish]
---

# Paper Polisher Pro

AI writing detection (AI-rate self-check for authors) · academic polishing guidance · terminology standardization · translation-smell check · quality report · AIGC compliance label check · paragraph-level attribution · journal precheck.
100% local, zero upload, zero credentials, pure standard library (optional onnxruntime enhancement layer).

> ## ⛔ Iron laws
> 1. **Only reproducible numbers.** Every metric comes from the held-out (test split) evaluation in `eval/run_eval.py`; unsupported claims like "100% detection rate / F1 98.3%" from older docs have been removed.
> 2. **No verdict on short text.** Texts under 100 characters get `risk=unknown` (community lesson: short-text false positives are uncontrollable).
> 3. **Fingerprints attribute, never score.** (Measured 2026-08-15: injecting fingerprints into the detector doubled human false positives.)
> 4. **Calibration/evaluation separation.** Spectrum, weights and thresholds are built on the calib half only; the test half is reserved for final evaluation (an in-sample AUROC of 0.9972 collapsed to a real 0.9187 once split).

## TL;DR

- **What**: 100% local AI-rate self-check + academic polishing toolkit for Chinese academic text (optional supervised model for best accuracy; English gets advisory rules-only scores).
- **30-second start**: `python3 scripts/pp.py quickstart` (zero-model, zero-file demo) · `python3 scripts/pp.py detect draft.txt --format json` · sentence-level rewrite suggestions: `python3 scripts/pp.py fix draft.txt` · full self-check report: `python3 scripts/pp.py workflow draft.txt` · environment: `python3 scripts/pp.py doctor` (one entry routes all subcommands)
- **Measured** (held-out, fingerprint-bound md5 2631df3d388b): AUROC 0.9998 pre-2026 / 0.9400 current-generation; human FPR@medium 2.3%.
- **Know the limits**: texts <100 chars get `risk=unknown` by design · medical text in degraded mode is over-scored · mixed human+AI docs: the document-level score is unreliable (paragraph attribution is the actionable signal) · authors' self-check only — never for evading institutional AI detection.
- **Where to look next**: scenario how-to in `references/best-practices.md` · capability boundary matrix below · end-to-end example in § Quick start · FAQ grouped in five parts (verdicts → modes & install → output & interpretation → safety & verification → tools & workflow), jump to the group you need · full history in `CHANGELOG.md`.

### 30-second task routing

| You want to… | Run | Deep doc |
|---|---|---|
| Check AI-rate of a draft | `pp.py detect draft.txt --format json` | § Measured performance + boundary matrix below |
| See which sentences read AI-like | `pp.py fix draft.txt` | `pp_fix_suggest.py --help` |
| Compare before/after your rewrite | `pp.py rewrite-check orig.txt rev.txt` | FAQ: rewrite suggestions |
| Translate a PDF keeping layout | `pp.py bundle` not this — use doc-holmes | Related tools |
| Check writing conventions | `pp.py norm draft.txt` | FAQ: style-norm |
| Batch a whole thesis folder | `ai_detector.py --batch DIR --csv s.csv --report r.html` | FAQ: batch CSV |
| Verify the zero-upload claim | `pp.py verify` + `pp.py test` | Safety statement |
| Journal precheck (discipline context) | `ai_detector.py draft.txt --profile journal` | § journal precheck |
| Environment trouble-shooting | `pp.py doctor` / `pp.py freshness --status` | FAQ: modes |
| One visual dashboard of all results | `pp.py html-report draft.workflow.json -o report.html` | Script cheat sheet: pp_report_html.py |
| Tracking a draft across rewrite rounds | `pp.py trend 轮次目录/ -o trend.html` | Script cheat sheet: pp_trend.py |
| Not sure which command fits? | `pp.py recommend "把这段的AI率降一降"` | `pp.py recommend --help` |

### The three limits that matter most (full detail in the matrix below)

1. **Medical register over-scoring in degraded mode** — rules-only human FPR @medium ≈59% medical vs ≈2% general; trust only `@high` verdicts on medical text, or install the supervised model.
2. **Mixed human+AI documents** — document-level AUROC 0.52-0.54 (inherent averaging limitation); use paragraph attribution as a human-review ranking, never as an automatic verdict.
3. **Data-coverage scope** — the term bank is 2,344 medical/academic terms (non-medical texts standardize low by design); style layers calibrate on academic prose (colloquial/narrative input = advisory only). Per-tool scope: sub-tool matrix below.

## Academic integrity

This tool is for **authors self-reviewing and improving their own writing quality** — clearer sentences, consistent terminology, natural style. It is not designed to evade institutional AI-detection systems, and it must not be used to misrepresent AI-generated work as human-written. Follow your institution's AI-use and disclosure policies; the bundled `aigc_label_check.py` exists to help you **comply** with disclosure and labeling rules (e.g., China's 2025-09 labeling measures) — to declare AI assistance properly, not to hide it. Every AI-risk report (`ai_detector.py` / `deai_gate.py`) carries an explicit `integrity_notice` to this effect.

## Measured performance (C-ReD + DetectRL-ZH, held-out test half, n=5,251)

> Corpus scope note (v4.8.0): the v3.0-era table below was measured on the **full** held-out test half (n=5,251). The **bundled** sample corpus is a subset — its test half is n=1,304; reproducible per-corpus numbers: rules-only (PP_NO_SUP) 0.8985 old-gen / 0.7149 current-gen, fused 0.9998 / 0.9400 (`eval/results/v480_rules_*.json`, `v35ctl_*.json`; cache keys bind model fingerprint AND engine mode).

| Metric | v2.0 baseline | v3.0 rules+spectrum | v3.1 +supervised | v3.4 supervised（版本时代记录，现行见下方重测行） |
|---|---|---|---|---|
| AUROC (test half) | 0.7046 | 0.9187 | 0.9997 | **1.0** |
| TPR@FPR5% | 30.4% | 49.0% | 99.95% | **100%** |
| TPR@FPR1% | 16.7% | 24.9% | 99.88% | **100%** |
| Human FPR @calibrated p99 | not measured | not measured | 3.56% (30/844) | **0.71% (6/844)** |
| Paraphrase/mixed-attack AUROC | 0.64 | 0.89 | 1.0 (in-corpus) | **1.0** |
| Attack "AI-assisted" recall | — | — | 71.1% | **86.6%** |
| OOD plain-narrative/film recall | — | — | 1/6 | **5/6 supervised-only · 6/6 local fusion** |

> **v4.4.0 fingerprint-bound re-measurement** of the shipping supervised model (md5 `2631df3d388b`): AUROC **0.9998** (test half, n_base=927), TPR@FPR1% 99.4%, human FPR@medium 2.3% — `eval/results/v35ctl_oldgen.json`. Columns above are preserved as version-era records (earlier model lineage; binaries were not fingerprinted before v4.4.0).

**Which column applies to you?** (Caliber navigation: the only citable current baselines are `v35ctl_*` in [`eval/results/CURRENT.md`](eval/results/CURRENT.md); columns to the left are version-era records.) The base package runs the **v3.0 rules+spectrum engine** (0.9187 AUROC column, measured on the full held-out corpus; pre-4.4.0 archived baselines predate fingerprint binding — every eval result since v4.4.0 carries the deployed model's md5 as `model_fp`, current bound numbers in `eval/results/v35ctl_*.json`). The two right-hand columns require the optional local supervised model (see below). The engine tells you honestly which mode you are in: every report carries `degraded_mode` / `degraded_notice` when the supervised layer is absent or skipped.

### Capability boundary matrix (read before trusting any detector)

| Scenario | Behavior |
|---|---|
| Chinese academic prose, full stack | Best case (AUROC 0.9998 held-out, human FPR@medium 2.3% — v4.4.0 fingerprint-bound) |
| Base package without model | Rules+spectrum (0.9187); **medical register over-scored** (rules-only human FPR @medium: ~59% medical vs ~2% general) → trust only @high verdicts on medical text |
| English text | Language gating skips the Chinese-trained supervised layer by design; rules-only English skeleton, advisory only |
| Mixed human+AI documents | Document-level AUROC 0.52-0.54 (inherent averaging limitation); paragraph-level AUROC 0.69 with **calibrated best operating point P=0.60 at 63% coverage** (`references/para_thresholds.json`) — below the automatic-verdict bar; use `pp_workflow.py`/`paragraph_report.py` rankings for human review only |
| Edit-extent regression head | ρ=0.540 — reported as metadata, never used in verdicts |
| **Current-generation models (2026-09 sampling)** | **AUROC 0.9400** (v4.4.0 fingerprint-bound re-measurement, 443-doc current-gen eval set: 9 families incl. K3/K2.7/Qwen3.7-3.8/DS-V4/V4.1/GLM-5.3/M3) vs 0.9998 pre-2026 held-out — a modest verified gap. The earlier 0.6542-vs-0.9022 figure was a measurement artifact (stale score-cache replay + unverified model lineage); both classes are structurally prevented since v4.4.0 (`model_fp` in every result JSON)
| Colloquial / oral-register text | The style layer is calibrated on academic prose; treat style scores as advisory outside that register |

### Sub-tool scope matrix (each sub-tool's calibrated domain)

| Sub-tool | Calibrated domain | Outside-domain behavior |
|---|---|---|
| ai_detector / deai_gate | Chinese academic prose (held-out calibrated) | Medical register over-scored in degraded mode; English advisory rules-only; narrative/colloquial input gets a register notice |
| paragraph_report / pp_rewrite_check | Same engine criteria as above, per paragraph | Same limitations; rewrite_check compares two drafts under identical criteria |
| pp_fix_suggest | Chinese AI-writing pattern library (academic register) | English text gets basic connective/rhythm checks only; findings are style observations, never detections |
| term_check | Chinese medical/academic terminology (2,344-term bank) | Non-medical text: the standardization rate reads low — that is bank scope, not an error; `--auto-fix` respects context |
| translation_smell_check | Chinese academic prose (translationese patterns) | English-style source text: output lists its blind-spot terms instead of pretending coverage |
| style_distance | Academic prose stylometry | Outside the academic register the style score is advisory only (stated in the output) |
| style_norm | Mechanical conventions — register-independent | No score by design; statistical checks (numbers/abbreviations) are weak on short samples and say so |
| aigc_label_check | File metadata / C2PA / explicit label statements | Not a content detector; verifies labeling compliance, not authorship |
| quality_report | Readability/quality dimensions for the manuscript | Not an AI-rate measure; scoring heuristics are generic, not journal-tuned |
| docx_text | .docx text extraction (paragraph-preserving) | Not a PDF converter — PDFs are rejected with conversion advice (zero-dep Chinese PDF extraction cannot be guaranteed) |
| batch mode (--batch) | .txt/.md/.docx <5 MB per file | >5 MB skipped by design; encrypted/image-only docx yield an explicit error, not silent empty output |

## Safety and behavior statement

- **100% local**: every feature runs on-device. The codebase makes zero outbound network calls — no network client libraries, no network utilities. The single listener-capable component is the optional MCP HTTP form (`--transport http`), which binds 127.0.0.1 loopback only (binding asserted by the AST verifier's allowlist rule); the AST scan treats any listener without a loopback bind as a violation. Verify structurally: `python3 scripts/pp_verify.py` (AST-level scan; exit 0 = zero network calls, all scripts compile). Legacy text grep `grep -rEin "urllib|requests|socket|import http" scripts/` may show a few URL *strings* in report footers — those are data in string constants, not network code; the AST verifier distinguishes the two.
- **No upload, no credentials**: reads and transmits no credentials, keys, or personal data; the only two environment variables are `PP_NO_SUP` (skip the supervised layer) and `PP_LANG` (`en` switches the `pp.py` entry surface to English) — both local behavior toggles.
- **Install integrity self-check**: `data/INTEGRITY_MANIFEST.json` records the SHA256 of every data/wordlist JSON; `python3 scripts/pp_doctor.py --deep` verifies each file's hash and parse — if a distribution path truncates a file, this names the exact file and expected/actual hash.
- **No persistence**: creates no scheduled tasks, autostart entries, or system config changes; temp files (inter-layer JSON, probe text) are deleted after use.
- **No remote code**: loads no remote models or scripts; the optional supervised model is placed by the user at a local path.
- **Data boundary**: reads/writes only user-specified files, the system temp dir, and its own package data directories (calibration/freshness artifacts); reports go only where the user points them.
- **Academic integrity**: see the section above — for author self-review and quality improvement with policy-compliant disclosure; not for evading detection.

### Exit-code contract (stable since v5.8.0)

| Exit | Meaning | Typical cases |
|---|---|---|
| 0 | Success | report produced · `verify` zero-network pass · `test` suite green |
| 1 | Ran but did not pass | engine runtime failure (recovery advice in the message) · `test` failures · `verify` drift · `freshness` baseline drift |
| 2 | Usage or input error | unknown subcommand · file missing · text under 100 chars · unparseable input file |
| 3 | Environment not ready | `pp_setup.py` model install/verification failure — run `pp.py doctor` first |

Programmatic mirror: `pp_api` raises `ValueError` for invalid input (↔ exit 2) and `RuntimeError` for runtime failure (↔ exit 1), both carrying recovery advice in the message. These codes are a stability promise — future releases will not repurpose them.

## Anti-patterns (each with the right way)

> This section lists **judgment-type** rules only (what not to do); operational how-to questions live in [`references/faq.md`](references/faq.md) (searchable via `pp.py faq <keyword>`) — the two cross-reference each other instead of repeating.

- **Don't feed <100 chars** and expect a verdict — `risk=unknown` is by design (short-text false positives are uncontrollable). ✅ Instead: submit 300+ chars, or use the style-norm check (`pp.py norm`) which has no verdict and works on short samples.
- **Don't trust degraded-mode scores on medical text** — rules-only over-scores medical register (~59% human FPR @medium). ✅ Instead: install the supervised model, or trust only `@high` verdicts and lean on paragraph attribution.
- **Don't treat scores as CNKI/Wanfang equivalents** — thresholds are calibrated on our own held-out corpus. ✅ Instead: use scores as relative triage and let the journal precheck give the distribution view.
- **Don't substitute or re-quantize the model file** — measured probability drift. ✅ Instead: only author-signed fingerprints pass `pp_setup.py`; if unavailable, stay in documented degraded mode.
- **Don't use it to evade institutional AI detection** — the integrity notice ships on every report. ✅ Instead: use findings to improve the writing itself and disclose per your institution's policy.
- **Don't run batch on >5 MB files** — skipped by design. ✅ Instead: split first, or point the batch at the exported text/docx versions.
- **Don't repeat the same analysis on unchanged input, or re-run a call that was already rejected** — it burns time without new information. ✅ Instead: change one input (text, engine mode, check scope) or resolve the blocker (missing model, encoding) before retrying.

## Quick start

Every command below is annotated with **when to use it** — pick by situation, not by name.
The full annotated catalog (17 scenarios, filterable): `python scripts/pp.py scenarios`.

```bash
# First time, no files yet — see what this toolkit does (zero-model demo)
python scripts/pp.py quickstart
# Drafted 300+ chars — how AI-like is it, which paragraphs are worst
python scripts/pp.py detect draft.txt --format json
# Score is high — which sentences to fix and how (locates, never auto-rewrites)
python scripts/pp.py fix draft.txt --top 10
# Before submission — one end-to-end pass (detect + norms + terms + gate)
python scripts/pp.py workflow draft.txt
# Got a report JSON you don't follow — plain-language verdict/evidence/actions
python scripts/pp.py explain draft.workflow.json
# Questioned about AI use — faithful evidence archive (HTML+MD, fixed integrity statements)
python scripts/pp.py evidence draft.txt --outdir evidence/
# Whole directory to process — per-file CSV + HTML summary (auto-retry + per-file
# crash isolation via --isolate auto: on when the supervised model is installed)
python scripts/ai_detector.py --batch manuscript_dir --csv scores.csv --report report.html
# Thesis split across chapter files — cross-file terminology consistency matrix
python scripts/pp.py term-project 章节目录/ --html matrix.html
# Thesis/book as chapter files — project-wide pass (per-file reports + term matrix + overview HTML)
python scripts/pp.py project 章节目录/ --outdir project_report/
# Several revision rounds done — score trajectory across runs
python scripts/pp.py trend 轮次目录/ -o trend.html
# Something errors / unsure which tier you're on
python scripts/pp.py doctor
```

More situations (style norms, terminology, rewrite comparison, dashboards, bundles,
compliance labels, MCP integration): `python scripts/pp.py scenarios` — every entry
states when to use it, the command, and what you get. Scenario-level how-to advice:
[`references/best-practices.md`](references/best-practices.md).


### Optional supervised layer (recommended, v3.2+)

```bash
pip install onnxruntime regex numpy    # the optional supervised-layer trio (see requirements.txt)
# Place the two model files exactly as shipped by the authors:
#   ~/.cache/paper-polisher/qwen3-detector/model.int8.onnx
#   ~/.cache/paper-polisher/qwen3-detector/tokenizer.json
python scripts/layers_lm.py            # self-test: supervised_available: true
# ai_detector.py fuses automatically afterwards (0.9*supervised + 0.1*rules);
# PP_NO_SUP=1 temporarily falls back to rules-only.
# ⚠️ Do not substitute other exports or quantizations — measured probability drift; use exactly these files.
```

### Python API (programmatic use)

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from pp_api import detect_text, gate_text, doctor_summary
r = detect_text("中文学术文本，建议 300 字以上。" * 10, lang="zh")
print(r["overall_ai_score"], r["overall_risk"], r["degraded_mode"])
```

`detect_text` runs in-process (no subprocess) and returns the same JSON structure as the CLI. Every function returns JSON-able dicts and raises on bad input — no silent failures. Zero network, stdlib-only.

### Output contract schemas (v7.7.0)

The four core outputs (detect / fix_suggest / workflow / term_report) ship JSON-Schema contracts (`schemas/*.schema.json`, draft-2020-12 subset). Self-check: `python3 scripts/pp.py schema --selfcheck` runs real engine outputs against every contract — contract/implementation drift surfaces immediately (top-level required keys and types are the compatibility promise: additive keys never break it; removals/type changes are declared in CHANGELOG). Integrators can validate what they received via `pp_api.schema_selfcheck()`.

### MCP server (direct agent-client integration, v6.5.0)

Zero-dependency MCP stdio server (JSON-RPC in pure stdlib — nothing to pip install), eight tools sharing the CLI engine and semantics:

```jsonc
// mcpServers config for Claude Code / Cursor etc.
{ "mcpServers": { "paper-polisher-pro": {
    "command": "python3",
    "args": ["<skill>/scripts/pp_mcp_server.py"] } } }
```

Tools: `pp_detect` (AI-rate + layered evidence) | `pp_fix_suggest` (sentence suggestions, never rewrites) | `pp_style_norm` (style norms) | `pp_term_check` (terminology) | `pp_workflow` (full end-to-end report) | `pp_explain` (plain-language reading) | `pp_faq` (search) | `pp_doctor` (environment tier). All local, zero network; output auto-truncated (12k chars).

Local HTTP form (v7.2.0, multi-client reuse): `python scripts/pp_mcp_server.py --transport http --port 8815` — listens on 127.0.0.1 loopback only (consistent with the zero-network posture; do not expose via port forwarding); `POST /mcp` for JSON-RPC, `GET /health` probe.

### One-command supervised setup

```bash
# Not sure how to obtain the model? python scripts/pp_setup.py --guide (acquisition guide: channel / placement / verification / degraded-mode semantics)
python3 scripts/pp_setup.py --model <author-signed model.onnx>   # verify md5 -> install -> inference canary
python3 scripts/pp_setup.py --check                              # current installation status
```

Only author-signed fingerprints (`references/supervised_models.json`) are accepted; unknown weights are rejected before anything is touched. Nothing is downloaded — the model always comes from the authors' channel as a local file. Model acquisition: the author-signed files are not publicly downloadable — open an issue at the GitHub repo (docsor1212/paper-polisher-pro) to request the current signed build; until then the package runs in documented degraded mode with full functionality minus the accuracy uplift.

### End-to-end workflow (one command)

```bash
python3 scripts/pp_workflow.py draft.txt      # writes draft.workflow.md + draft.workflow.json
```

Runs the full self-check in one pass — AI-rate detection (fused engine), paragraph-level
attribution with hi/med/lo classification, the 4-layer gate, terminology, translation-smell,
style, quality report and AIGC label self-check — and produces a single readable Markdown
report plus machine-readable JSON. Programmatic: `from pp_api import workflow`.

## FAQ (top 3 — full grouped FAQ in [`references/faq.md`](references/faq.md), searchable via `pp.py faq <keyword>`)

**Q: Why no risk verdict for texts under 100 characters?**
Short-text false positives are uncontrollable. The tool returns `risk=unknown` by design; submit 100+ chars (300+ recommended).

**Q: Why is my medical text scored high?**
You are most likely in degraded mode (supervised model not installed) — rules-only scoring systematically over-scores medical register. Trust only `@high` verdicts there, or install the supervised layer (`pp_setup.py --guide`).

**Q: Is this score interchangeable with CNKI/Wanfang official checks?**
No. Thresholds are calibrated on our own held-out corpus and are not interchangeable with any institutional detector; self-check only.

## Architecture & fingerprint freshness (reference)

Everyday use needs none of this. The full architecture diagram, module map and the
fingerprint-freshness pipeline notes (calibration split strategy, monthly freshness
workflow, model-generation coverage) moved to [`references/architecture.md`](references/architecture.md) —
read on demand. Scenario-level how-to advice lives in [`references/best-practices.md`](references/best-practices.md).

## Trigger words (Chinese)

`润色论文`查AI率` `论文AI率` `AIGC检测` `AIGC率` `GPT检测` `查AI写作` `论文润色` `改写论文` `AI论文检测` `学术写作助手` `AI写作检测` `毕业论文润色` `学位论文降重` `SCI论文编辑` `手稿润色` `AI写作评分` `AI改写检测` `文风对标顶刊` `这篇文章像不像AI`

## Related tools

- **cn-med-oa** — free Chinese medical literature (OA) download & citation metadata
- **pubmed-verifier** — verify PMID/DOI references before submission
- **cite-holmes** — deep research with machine-verified citations
- **academic-figures** — publication-ready scientific figures in one command
- **doc-holmes** — layout-preserving PDF translation
- **paper-rewriter** — same-source de-AI rewriting companion (full rewrite pipeline)

Docs & site: **docsor.cn**

## Version history (condensed)

- **v7.7.0 (2026-11-12)** — output contract schemas (`schemas/*.schema.json` + zero-dep validator `pp.py schema --selfcheck`, real-output-validated); manifest generator single-sourced (generated reads skill.json, --check byte-compare, gated); pp_api parity completed (trend_data / schema_selfcheck).
- **v7.6.0 (2026-11-07)** — install integrity self-check: `data/INTEGRITY_MANIFEST.json` (SHA256 per data/wordlist JSON) + `pp_doctor --deep` (hash+parse per file) + trunk/package manifest gates; `eval/gen_integrity_manifest.py`.
- **v7.5.0 (2026-11-06)** — dual-form acceptance parity (`verify_forms.py --form sh|ch|both`, package-copy harness); archive/README caliber discipline rewritten with a gate; skill.json layer count aligned to the L12 map.
- **v7.4.0 (2026-11-05)** — physical caliber separation (29 historical result files archived; top level = CURRENT.md + 3 baselines + cache, gated); version-era pointer in the measured table; pp_api SDK gains fix_suggest/evidence_sections/term_project/scenarios.
- **v7.3.0 (2026-11-03)** — MCP three-primitive parity (3 resources + 3 workflow prompts alongside 8 tools); SKILL_ZH title fossil removed + bilingual-title gate; requirements declares regex with a requirements-vs-docs gate; SH package form stated in the doc header.
- **v7.2.0 (2026-10-31)** — MCP HTTP transport (loopback-only, /mcp + /health); server version single-sourced from skill.json; AUROC caliber cleanup in skill.json/SKILL_ZH with a zero-residue gate; eval/results caliber navigation (CURRENT.md) with reconciliation gates.
- **v7.1.0 (2026-10-31)** — custom terminology banks (`--bank` for term_check & term-project; project-owned standard spellings merged over the built-in bank with same-cn override, line-numbered validation); title version fossil removed + README AUROC aligned to the fingerprint-bound 0.9998 caliber, both gated.
- **v7.0.0 (2026-10-30)** — package-form adaptive consistency major: bundled tests & smoke run in both package forms (CH English package: ZH assertions skip honestly); cross-file gates unify Python floor at 3.9 and forbid hardcoded test counts; fix gains `--worksheet` rewrite checklist.
- **v6.9.0 (2026-10-29)** — project workbench (`pp.py project`): directory-wide full self-check + embedded term-consistency matrix + overview HTML/JSON, same-source engine, per-file failure isolation.
- **v6.8.0 (2026-10-27)** — per-file process isolation for batch (`--isolate auto`: on with the supervised model; hard crash costs one row, scoring bit-identical); error glossary + worker-crash/timeout/encoding; Traceback-residue hygiene lock.
- **v6.7.0 (2026-10-27)** — scenario catalog (`pp.py scenarios`, 17 entries with when-to-use/output, single-source JSON); quick start restructured scenario-first (~30 lines slimmer); FAQ technical section split into user-facing vs integrator tiers.
- **v6.6.0 (2026-10-26)** — evidence report (`pp.py evidence`, HTML+MD with fixed limitation/integrity statements) and cross-file terminology consistency (`pp.py term-project`, thesis-wide writing matrix + unification advice).
- **v6.5.0 (2026-10-24)** — MCP stdio server (`pp.py mcp`): eight tools over pure-stdlib JSON-RPC for agent clients (Claude Code/Cursor), zero dependencies, zero network; anti-patterns ↔ FAQ de-duplicated with cross-pointers and a reading-tier note.
- **v6.4.0 (2026-10-23)** — batch auto-retry (`--retries`, default 2) with a `failed_files` aggregate + diagnostic hints (transient failures self-heal, no manual re-run); guided tour (`pp.py tour`, five live stations incl. the report explainer and a visuals/trends map); quick start now references the bundled real outputs and documents the `--batch --csv --report` one-pass combination.
- **v6.3.0 (2026-10-22)** — standalone searchable FAQ (`references/faq.md` + `pp.py faq <keyword>` with technical-questions section), SKILL.md keeps top-3 + link, friendly errors now carry the FAQ pointer.
- **v6.2.0 (2026-10-21)** — side-by-side rewrite comparison (`pp_rewrite_check.py --html`): aligned per-paragraph original/revised excerpts with colored score migration, plus a signal-details section in the workflow dashboard.
- **v6.1.0 (2026-10-20)** — report explainer (`pp.py explain`), error-glossary extension (AST/drift/signature/gate-layer phrases), quickstart timeouts + stability contract in docs, architecture deep-dive moved to `references/architecture.md`, new `references/best-practices.md`, examples annotated by scenario.
- **v6.0.0 (2026-10-19)** — reporting & experience major: multi-run trend dashboard (`pp.py trend`); unified plain-language error presentation (`pp_errors.py`, wired into four entry points); grouped `pp.py` help with a beginner path and an English entry surface (`PP_LANG=en`); batch chaos test suite.
- **v5.9.0 (2026-10-18)** — zero-config onboarding & batch robustness: supervised-model acquisition guide (`pp_setup.py --guide`, wired into doctor/check), batch circuit breaker (`--circuit`, default 5) + fix for one corrupt docx killing the whole batch, opt-in out-of-dictionary neologism probe (`term_check.py --neologism`), version-header hygiene with a release gate, FAQ group navigation.
- **v5.8.1 (2026-10-17)** — terminology bank extended with practice-derived standardization aliases; term matching fixed to single-pass longest-first resolution (a short standard term no longer shadows a longer alias); count claims updated to 2,335.
- **v5.8.0 (2026-10-16)** — visual dashboard release: `pp_report_html.py` renders workflow/detect/fix/norm JSON into one self-contained HTML (gauge, histogram, paragraph/finding/ledger tables); `pp.py recommend` natural-language command router; exit-code contract documented and locked; top-3 limits surfaced next to the TL;DR; ZH version history slimmed to match EN.
- **v5.7.1 (2026-10-16)** — sample sanitation: an internal LAN link embedded in the bundled sample document text (`examples/outputs/detect_sample.json`) was redacted after the hygiene gate flagged it; no code or engine changes (bit-identical scoring to 5.7.0).
- **v5.7.0 (2026-10-16)** — release-integrity overhaul: version-scoped guards, post-packaging version assertion, sample outputs shipped, sentence-locating in the jargon check; CHANGELOG/SKILL.md dedup.
- **v5.6.0 (2026-10-14)** — llm-jargon release: three-tier AI-flavor self-check with case-library contrasts (cross-line port, credited); engine scoring of the signal tried and honestly reverted (negative result archived with retry conditions).
- Releases **v5.4.1 and earlier**: see `CHANGELOG.md` (single source of history).
