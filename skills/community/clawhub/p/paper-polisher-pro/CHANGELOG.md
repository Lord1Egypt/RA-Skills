# Changelog

> **只想快速上手？** 回 `SKILL.md` § TL;DR（30 秒任务路由表）——本文件仅是完整版本历史，新用户无需阅读。
> Historical release notes. Newest first. SKILL.md § Version history keeps only the last three releases; everything older lives here (single source, no duplication).

## What's new in v7.7.0

- **Output contract schemas (`schemas/*.schema.json`, `pp.py schema --selfcheck`)**: the four core outputs (detect / fix_suggest / workflow / term_report) now ship JSON-Schema contracts (draft-2020-12 subset), and a zero-dependency minimal validator (`scripts/pp_schema.py`) runs real engine outputs against all four on every self-check. First run caught a real drift (mixed_document is an object, not the boolean the draft assumed) — the validator's purpose in one line. Top-level required keys and types are the compatibility promise: additive keys never break the contract; removals/type changes get declared in CHANGELOG. Integrators validate their received structures via `pp_api.schema_selfcheck()`.
- **Manifest reproducibility closure**: the review flagged the integrity manifest's structure vs its generator; a byte-diff proved them identical on our side, but the generator's hardcoded "generated" version was a real single-source violation — it now reads skill.json, gained a `--check` mode (byte-compare without writing), and a release gate asserts generator output == shipped manifest byte-for-byte.
- **pp_api parity completed**: `trend_data` (trajectory data from workflow JSONs/directories) and `schema_selfcheck` — the Python SDK now covers the full CLI surface.

## What's new in v7.6.0

- **Install integrity self-check (`pp_doctor.py --deep`)**: the 11-05 review reported "JSON data files truncated at the tail" — not reproducible on any of our copies (trunk/SH package/CH package all byte-identical and parsing). The mechanism-level answer works regardless of where the corruption happens: the package now ships `data/INTEGRITY_MANIFEST.json` (SHA256 + size for every data and wordlist JSON), `pp_doctor --deep` verifies each file's hash AND parse against it, and two release gates reconcile the manifest against trunk and against both packaged copies. If a distribution path ever truncates a file, users get the exact file name plus expected/actual hash — machine evidence, not a guess.
- **`eval/gen_integrity_manifest.py`**: regenerate the manifest after any data/wordlist change; a stale manifest fails the deep check by design (hash drift is exactly what it must catch).

## What's new in v7.5.0

- **Dual-form acceptance parity (`eval/verify_forms.py`)**: the two shipped forms now have a single, symmetric acceptance runner — `--form sh` builds a package copy where SKILL_ZH.md is published AS SKILL.md (the SkillHub convention), `--form ch` builds one without SKILL_ZH.md, both sharing the package-copy harness (copy-isolated, O_EXCL lock, canonical read-only trunk) and running the full smoke. `--form both` runs the pair serially; the release chain exercises it before every release so a form regression can never ship unnoticed (the 10-31 review's "form-related doc/test mismatch" class closes structurally).
- **archive/README caliber discipline**: the archived-results README still called historical files "reproducible baselines" (v480/v500 etc.) — exactly what two consecutive reviews flagged. It now states the archive boundary up front (nothing here is citable) and points at CURRENT.md as the only caliber authority, with a gate rejecting the old claim's return.
- **Layer-count alignment**: skill.json said "11-layer" while the docs map already ships the L12 discourse layer — aligned to 12-layer with a gate tying the count to the map.

## What's new in v7.4.0

- **Physical caliber separation**: v7.3.0's CURRENT.md declared which result files are citable, but the directory still physically mixed 29 historical/voided files among them. All history is now `git mv`-ed into `eval/results/archive/` — the top level holds only `CURRENT.md`, the three citable baselines and the runtime cache — with two gates: top-level `*.json` must all appear in the CURRENT.md table, and the archive layer must exist. The review's "lots of historical files, hard to tell the valid caliber" is closed structurally, not by convention.
- **Version-era pointer**: SKILL.md's measured-performance table keeps version-era columns as evolution records; a caliber-navigation pointer now says explicitly that only `v35ctl_*` (fingerprint-bound) is current, closing the stale-number misreading the review noted.
- **pp_api SDK parity (`fix_suggest` / `evidence_sections` / `term_project` / `scenarios`)**: programmatic users get the capabilities that previously existed only as CLI commands — sentence-level suggestions (same structured suggestions), the evidence report's sectioned chain, the cross-file terminology matrix (with `--bank` support), and the filterable scenario catalog. Same-source engines, same error semantics (ValueError ↔ exit 2, RuntimeError with recovery advice).

## What's new in v7.3.0

- **MCP three-primitive parity**: the server now exposes resources and prompts alongside its 8 tools — resources: `ppp://capability-matrix` (the boundary matrix, read-before-trusting detections), `ppp://current-caliber` (the citable-baseline index from `eval/results/CURRENT.md`), `ppp://changelog-latest`; prompts: `paper-selfcheck` (detect→suggest→norms→action list), `rewrite-loop` (suggestion intent → revision check → honest score migration), `submission-precheck` (workflow → journal precheck → evidence report → label compliance), each rendered with arguments into an executable workflow template. Same zero-dependency zero-network server; capabilities now declared.
- **Consistency (the review caught three real ones)**: the SKILL_ZH title still carried the "v3" fossil plus a stale marketing tail (v7.1.0 fixed only the English title — the SH package publishes SKILL_ZH as SKILL.md, so reviewers saw it there); removed and a bilingual-title-parity gate added. `requirements.txt` never declared `regex` while SKILL.md's pip line teaches `onnxruntime regex` and pp_doctor probes it — declared with a requirements-vs-docs gate. The SH package form (SKILL_ZH.md published AS SKILL.md, no duplicate) is now stated in the doc header so the packing convention can't read as a missing file.

## What's new in v7.2.0

- **MCP HTTP transport (`--transport http`)**: alongside stdio, the server now listens on 127.0.0.1 (loopback only) — `POST /mcp` takes one JSON-RPC message per request, `GET /health` is a liveness probe. This follows the MCP direction of streamable HTTP and enables same-machine multi-client reuse (several agent sessions sharing one server). Honest boundary stated in code and docs: loopback only, no auth, cross-machine exposure out of scope — consistent with the zero-network posture (listening locally is not an outbound service).
- **Zero-network verifier precision (`pp_verify`)**: the HTTP transport introduced an `http.server` import and the AST scan flagged it (caught in the release battery — exactly what the verifier exists for). The verifier now distinguishes listeners from clients: `http.server` passes only when the same file carries a loopback (`127.0.0.1`) bind assertion, which is also tested in both directions (a `0.0.0.0` bind still fails). SKILL safety statements (EN+ZH) state the precise posture: zero **outbound** calls; the single listener-capable component binds loopback only.
- **Version single-sourcing**: the server reported its own hardcoded version ("6.5.0" while the package was at 7.x — caught during the HTTP verification); it now reads `skill.json` at import, one source of truth.
- **AUROC caliber cleanup completed**: the "AUROC 1.0" legacy caliber survived in `skill.json` and the SKILL_ZH frontmatter (the 10-31 review caught both after v7.1.0 cleaned only README/EN title); all shipped surfaces now state the fingerprint-bound 0.9998, with a gate asserting zero "AUROC 1.0" residue across skill.json/SKILL_ZH/README.
- **Caliber navigation (`eval/results/CURRENT.md`)**: the results directory mixed current and archived evaluation artifacts with no guidance; a single index table (file / fingerprint / eval set / key numbers / referencing section) now declares the only citable baselines, archived files are marked non-citable, and a gate reconciles the table against files on disk and against SKILL.md references.

## What's new in v7.1.0

- **Custom terminology banks (`--bank`)**: thesis writers have their own abbreviations, institution names and project-internal conventions that will never be in the built-in 2,344-term bank. `term_check.py --bank 项目词表.json` and `pp_term_consistency.py --bank` accept a project bank (JSON array, same entry format as the built-in bank: `cn`/`en`/`aliases`/`source`) merged over the built-in entries with same-`cn` override — the project decides which spelling is standard, and cross-file consistency uses the same bank. Entries are validated with line numbers (a malformed entry is reported, never silently dropped). The built-in bank stays untouched.
- **Consistency**: the SKILL.md title carried a version fossil ("Paper Polisher Pro v3" while the package was at 7.0.0 — the review flagged it); the title is now version-free and a gate rejects version markers in the title. README's AUROC claim ("1.0, author-side") predated the fingerprint-bound recalibration — aligned to the current 0.9998 caliber with a gate anchoring the number in both SKILL.md and README.

## What's new in v7.0.0

- **Package-form adaptive consistency (major)**: the review ran the package in its CH-English form and found real breakage — the bundled smoke battery and several tests hard-read `SKILL_ZH.md`, which the language rule deliberately excludes from the English package. The suite is now form-adaptive: `tests/_docs.py` turns ZH document reads into honest `SkipTest` (CH form: 235 tests run, 8 ZH assertions skip, zero errors; SH form: all 235 run), and the smoke battery's version/frontmatter/desc/FAQ/trigger assertions condition on the same flag with explicit package-form labels. The failure class "works in the author's tree, breaks in a shipped package form" is now structurally covered — both forms are exercised before release.
- **Cross-file consistency gates**: Python minimum version is unified at 3.9 everywhere (requirements.txt said 3.8+ while pp_doctor enforces 3.9) and a new gate asserts every declared floor matches the doctor threshold; README no longer hardcodes a test count (it said "44 cases" while the suite grew to 235) and a gate forbids the pattern from returning.
- **Rewrite worksheet (`pp_fix_suggest.py --worksheet`)**: the sentence-level suggestions become an executable document — a Markdown checklist (summary table + per-sentence sections with original/issues/strategy and a blank "改后" checkbox line for the author's own rewrite), closing the loop with `pp.py rewrite-check` for acceptance. The tool still never rewrites; the author writes every word.

## What's new in v6.9.0

- **Project workbench (`pp_project.py`, `pp.py project`)**: the thesis/book scenario gets its one-command form — point it at a directory of chapter files and it runs the full per-file self-check (each chapter's `workflow.json`/`.md` lands as usual), embeds the cross-file terminology consistency matrix, and renders a project overview (self-contained HTML + machine-readable JSON): per-file score/risk-band/paragraph-grading/gate table, project-level aggregates (mean/max, high-risk count, unification counts), and per-concept unification advice. Same-source engine (`pp_workflow.workflow` called in-process — no new scoring code); a per-file failure costs only that row, same philosophy as batch mode; fixed integrity statement in the overview (self-check aid, not a compliance certificate).

## What's new in v6.8.0

- **Per-file process isolation (`--isolate`, default auto)**: Python-exception isolation (v5.9.0) now has a process-level sibling — each batch file runs in its own worker subprocess (the CLI itself is the worker, so scoring stays bit-identical; a test locks on/off equivalence). A hard crash in one file — a native segfault/abort in the optional onnxruntime layer, the class of failure the review called out — now costs only that file's row while the batch continues, with the failure honestly recorded (`worker 崩溃` + exit code/signal). `auto` enables isolation exactly when the supervised model is installed (the native layer is the crash source; the rules-only tier keeps the in-process fast path); `on`/`off` override. Input-type failures (exit 2 — the worker already printed its friendly message) pass through verbatim instead of being wrapped as crashes.
- **Error glossary extended**: worker-crash, processing-timeout, and text-encoding failures now translate to plain language with next steps.
- **Hygiene**: a residue lock asserts no raw `Traceback`/`print_exc` in any shipped script (technical-phrase leakage class), and the duplicate anti-patterns header that slipped into SKILL.md in v6.5.0 was caught and removed by the new docs test.

## What's new in v6.7.0

- **Scenario catalog (`references/scenarios.json` + `pp.py scenarios`)**: a single-source catalog of 17 scenarios where each entry states **when to use it**, the command, and what you get — answering "which command for this situation" without reading reference docs. The builtin filters by keyword (bilingual, space-insensitive for compact CJK queries like 测AI率), and is reachable from `pp.py` help and the natural-language router ("什么时候用哪个命令").
- **Quick start restructured scenario-first**: every command in the SKILL quick-start block now carries a when-to-use annotation line (the review noted the block was a bare command dump); the long tail moved out from behind a pointer, slimming both language files by ~30 lines back under 290.
- **FAQ technical section tiered**: the technical Q&A is reorganized into「用户高频」(circuit breaker, batch retries, thesis-wide terminology, evidence packs, PDF stance, English advisory) and「集成者与进阶」(exit codes, AST verification, model signatures, score drift) — same content, explicit audience split matching the reading-tier note.

## What's new in v6.6.0

- **Evidence report (`pp_evidence_report.py`, `pp.py evidence`)**: for the real moment when a reader asks "is this AI-written?" — one command renders the full detection evidence chain into a deliverable, self-contained HTML + Markdown report: verdict card (score/risk band/mode/supervised fingerprint), per-feature evidence with located excerpts, paragraph grading, threshold caliber as-is, and fixed limitation & academic-integrity statements that cannot be turned off. Honest positioning stated in the report header: it presents the engine's judgment and evidence faithfully for self-check and explanation — it is **not** a certificate of "no AI use", and the score is engine-relative, not equivalent to any institutional detector.
- **Cross-file terminology consistency (`pp_term_consistency.py`, `pp.py term-project`)**: theses and group reports live as multiple chapter files, and single-file term checking cannot see "chapter 2 says X, chapter 5 says Y". Point it at a directory (≥2 files) and it builds the writing matrix per in-bank concept across files, lists inconsistent concepts with a unification recommendation (the bank's standard name; falling back to the most widely used variant when the standard name is absent), and renders a JSON/text/HTML matrix. Honest boundary stated everywhere: only in-bank concepts are visible; out-of-bank free phrasings need `term_check --neologism` as a companion probe. Scanning logic is same-source with `term_check` (longest-first claiming, derivation/organization-suffix exclusions), with the standard-name hits retained for matrix statistics.

## What's new in v6.5.0

- **MCP server (`scripts/pp_mcp_server.py`, `pp.py mcp`)**: paper-polisher-pro is now directly callable from agent clients (Claude Code, Cursor, anything speaking MCP) — a zero-dependency stdio server implementing JSON-RPC in pure stdlib, so nothing to pip install and the zero-network posture is unchanged. Eight tools share the CLI engine and exit-code semantics: `pp_detect`, `pp_fix_suggest`, `pp_style_norm`, `pp_term_check`, `pp_workflow`, `pp_explain`, `pp_faq`, `pp_doctor`. Inputs are size-capped (2M chars), outputs auto-truncated (12k chars), engine timeouts and errors are reported honestly as `mcp_error` instead of being masked. Usage config lives in SKILL.md § MCP server.
- **Anti-patterns ↔ FAQ de-duplication**: the review noted the two overlapped (medical-text caveats appeared in both). The anti-patterns section now states its scope explicitly (judgment-type rules — what not to do), the FAQ states its own (operational how-to), the two cross-reference each other instead of repeating, and the FAQ header gains a reading-tier note (first five groups for everyone; the technical-questions section is for integrators/advanced debugging).

## What's new in v6.4.0

- **Batch auto-retry (`--retries`, default 2)**: batch runs no longer leave transient failures (file locked, read hiccup) for manual re-runs — after the first pass, files that errored are automatically re-scanned up to `--retries` rounds; recovered rows are marked `retried: true` with `attempts`. Files still failing after the retry budget land in a new `failed_files` aggregate with a per-file diagnostic hint (`pp.py detect <file>` for the full error). The first-pass circuit breaker is unchanged, and a tripped circuit skips the retry rounds (a clearly bad batch gains nothing from re-scans); `--retries 0` restores the v6.3.0 behavior. Retry rounds stop early when a round recovers nothing (persistent corrupt files are not re-burned). Text summary lines show the actual retry rounds and the diagnostic pointer.
- **Guided tour (`pp.py tour`)**: five stations, each a live run on real data — detection on the built-in sample, the report explainer on the bundled real `workflow_sample.json`, top-3 rewrite suggestions, a visuals/trends command map (pointing at the bundled real `report_html_sample.html`), and the environment tier check — ~10 seconds, all local, zero network. Follows `PP_LANG=en`; also reachable via the natural-language router ("功能太多不知从哪开始" → tour). Built for discoverability: the advanced tools (trend, paragraph attribution, bundle) were easy to miss.
- **Quick-start now shows real outputs**: SKILL.md quick start references `examples/outputs/` (with a preview line) so new users can see what results look like before running anything; the `--batch --csv --report` one-pass combination and the new `--retries`/`--circuit` interaction are documented with copyable commands (EN + ZH).
- **FAQ**: new entry on batch failures (auto-retry semantics, when to re-run manually — answer: usually never).
- **Sample outputs regenerated on public data**: the bundled real-output samples (`detect_sample.json`, `workflow_sample.json`, `report_html_sample.html`) were rebuilt from a real public article (Chinese Wikipedia "免疫系统", CC BY-SA, source linked in `examples/outputs/README.md`) instead of an internal working note; the packaging hygiene gate now also rejects internal identifiers, private-range IPs and internal note IDs in any shipped text file, and bundled tests lock the samples clean.

## What's new in v6.3.0

- **Standalone FAQ (`references/faq.md`, `pp.py faq <keyword>`)**: the FAQ moved out of SKILL.md into its own searchable file — the full grouped Q&A (verdicts / modes / output / safety / tools) plus a new technical-questions section (why no PDF, why English is advisory-only, what the AST scan means, what the circuit breaker is, the exit-code contract, model-signature failures, why scores differ between runs). `pp.py faq 医学` / `faq PDF` / `faq 退出码` searches entries with header-hit ranking and a no-match fallback; SKILL.md keeps the top-3 questions plus a link (main file shrinks again).
- **Errors link to the FAQ**: every friendly-error output now ends with a `pp.py faq <keyword>` pointer, closing the loop from failure message to answer.

## What's new in v6.2.0

- **Side-by-side rewrite comparison (`pp_rewrite_check.py --html out.html`)**: the rewrite-effect check was text-only; it now renders one self-contained HTML with the original and revised drafts side by side per aligned paragraph (difflib pairing, similarity shown), per-paragraph score migration colored ↓improved/↑rebounded, header cards for the document-level move and risk-band migration, and the per-feature-type delta table. Aligned rows now carry ≤100-char excerpts (additive JSON fields `original_excerpt`/`revised_excerpt`). All text HTML-escaped; zero external resources; zero network.
- **Signal details in the dashboard (`pp_report_html.py`)**: workflow-based dashboards now include a signal section — register hint, mixed-writing warning, discourse-structure hits and LLM-jargon hit counts (advisory-only, as everywhere) — rendered only when the report actually carries them.

## What's new in v6.1.0

- **Report explainer (`pp_explain.py`, `pp.py explain`)**: any workflow/detect JSON becomes a three-part plain-language reading — verdict (score, risk band, engine mode with degraded-mode medical caveat), evidence (paragraph hi/med/lo with top excerpts, gate verdict, style/term findings aggregated, sentence-suggestion stats), and an action checklist of concrete next commands (paragraph review for mixed-writing, `fix`, `norm`, `term`, trend, bundle). Also reachable through the natural-language router ("解读这份报告").
- **Error glossary extended (`pp_errors.py`)**: the remaining technical phrases the review called out now translate too — AST self-verification hits, baseline drift, author-signature rejection, per-layer gate parse fallback; `pp_verify` prints the next-step line on findings, and the `pp.py` passthrough prints the exit-code meaning whenever a subcommand exits abnormally.
- **Timeout hardening**: `pp.py quickstart` sub-steps now carry a 180s timeout each (a hung step can no longer wedge the demo); the gate layers' existing 120s-timeout + single-retry behavior is now stated in the docs as part of the stability contract.
- **Deep-dive sections moved to `references/`**: the architecture diagram and fingerprint-freshness pipeline notes (calibration split, model-generation coverage) moved from SKILL.md to `references/architecture.md` (linked, read-on-demand) — the main file stays a getting-started document.
- **`references/best-practices.md` (new)**: scenario-level guidance — which profile for which discipline, the correct (human-review) way to use paragraph attribution, the rewrite loop with `rewrite-check`/`trend`, batch organization with the circuit breaker, mode/trust boundaries and compliance; `examples/outputs/` samples are now annotated with the scenario each one answers.

## What's new in v6.0.0

- **Multi-run trend dashboard (`pp_trend.py`, `pp.py trend`)**: single reports answer "what's the score now"; authors iterating on a manuscript need "is the score actually coming down across rounds". Feed it the workflow JSONs from each round (files or a directory), get one self-contained HTML: score trajectory as inline SVG (risk-band colored points, degraded-mode runs hollow), a per-run delta table (↓ improved / ↑ rebound flagged), first→last net-change cards. Honest boundary in the output: a lower score is not a better manuscript — quality is the goal; degraded-mode and full-mode runs are not directly comparable and are marked.
- **Unified error presentation (`pp_errors.py`)**: error handling no longer lives scattered per-script with technical raw messages (zip-bomb guard text etc.). Known guardrail exceptions now render as a two-line, plain-language explanation plus a concrete next step (what to do with an oversized/corrupt .docx, a mislabeled file, a missing model → points to the acquisition guide). Exit-code contract untouched (0/1/2/3). Wired into ai_detector / pp_workflow / pp_report_bundle / docx_text entry points.
- **Grouped entry + English surface (`pp.py`)**: the flat 21-command list is now grouped by scenario (detection / rewrite guidance / conventions & terms / reports & visuals / compliance & assurance / environment) with a three-step beginner path on top; `PP_LANG=en` switches the whole entry surface (help, unknown-command messages, recommend output) to English — the second environment variable alongside `PP_NO_SUP`, both documented in the safety statement.
- **Batch chaos suite**: the bundled tests now include a mixed-chaos batch fixture (corrupt/empty/short/encoding-odd/valid files together) asserting per-file isolation, circuit disclosure and CSV integrity — the long-batch robustness the previous release asked for, now locked by tests.

## What's new in v5.9.0

- **Supervised-model acquisition guide (`pp_setup.py --guide`)**: the biggest remaining zero-config gap was that the optional supervised layer told you how to install a model file but not how to obtain one. The new guide command spells out what the layer is, the author-signed acquisition channel (GitHub issue), placement/verification steps, and the documented degraded-mode semantics when you skip it; `pp_doctor` and `pp_setup --check` now point to the guide whenever the engine runs without the model.
- **Batch circuit breaker (`ai_detector.py --batch ... --circuit N`)**: N consecutive unreadable/failing files now abort the remaining queue (default 5, `--circuit 0` to disable) instead of grinding through a whole folder of garbage — completed files still produce their CSV/report, and the abort is disclosed in both the JSON (`circuit` field) and the text summary. Includes a real stability fix found by the new tests: one corrupt .docx previously killed the entire batch via an uncaught SystemExit; per-file failures now degrade to ERROR rows as designed.
- **Out-of-dictionary neologism probe (`term_check.py --neologism`)**: opt-in heuristic that surfaces high-frequency character strings absent from the term bank as human-review leads (born from the cross-line manuscript standardization review; the bank was blind to self-coined words). Honest boundary stated in the output: uncalibrated, advisory-only, never scored, never feeds the gate; default runs are unchanged.
- **Version-header hygiene**: four scripts still carried engine-file-era version headers (v1.x fossils) inconsistent with the package version — headers are now version-neutral, a release gate (smoke check + unit test) prevents the class from recurring.
- **Progressive disclosure**: the TL;DR now maps the five FAQ groups explicitly, and the architecture section is marked read-on-demand.

## What's new in v5.8.1

- **Terminology bank extended with practice-derived standardization mappings (+27 entries/aliases)**: cross-line review of a medical manuscript surfaced self-coined abbreviations and colloquial metaphors (e.g., informal shorthand for age-specific re-interpretation, pre-vaccination evaluation, primary monitoring parameter) that the bank could not see. They are now registered as aliases of the standard names, so `term_check.py` / `pp.py term` flags each occurrence and suggests the standard term; bank count claim updated to the real loaded figure (2,335 standard terms).
- **Matching-mechanism fix**: candidate resolution is now single-pass longest-first across standards AND aliases — previously a short standard term could claim a span and silently suppress a longer alias overlapping it (a standard 2-char word shadowing a 4-char alias). Legacy behavior (derivation/organization-suffix exclusions, English word boundaries) preserved and now covered by a canary regression test.

## What's new in v5.8.0

- **Single-document visual dashboard (`pp_report_html.py`, `pp.py html-report`)**: renders workflow / detect / fix-suggest / style-norm JSON outputs into one self-contained HTML file — score gauge (inline SVG), paragraph-score histogram, top-paragraph heat table, rewrite-suggestion table, style-norm findings (with jargon hit sentences), and workflow blocks (mixed-document assessment, 4-layer gate, terminology/translation-smell/style/quality, AIGC label evidence, findings ledger). Inline CSS only, zero external resources, zero network, stdlib-only; every text field is HTML-escaped. Inputs are auto-classified by feature keys and can be mixed freely.
- **Natural-language command router (`pp.py recommend "..."`)**: describe the task in plain Chinese or English ("把这段的AI率降一降", "environment trouble"), get the top-3 matching subcommands with ready-to-run commands — lowers the first-contact navigation cost of a 21-subcommand toolkit.
- **Exit-code contract (documented and locked)**: 0 success / 1 ran-but-not-passed / 2 usage-or-input error / 3 environment-not-ready, mirrored by `pp_api`'s `ValueError`/`RuntimeError` — a stability promise for scripts and integrations, stated in SKILL.md and in `pp.py --help`.
- **Docs**: the three most consequential limitations (medical over-scoring in degraded mode, mixed-document averaging, data-coverage scope) now sit right next to the TL;DR instead of only deep in the boundary matrix; a fourth real workflow JSON sample and a rendered HTML sample ship in `examples/outputs/`; the ZH version history was slimmed to match the EN condensation (single source of history: this file); a stale internal identifier was scrubbed from two historical entries.
## What's new in v5.7.1

- **Sample sanitation**: an internal LAN link embedded in the bundled sample document text (examples/outputs/detect_sample.json) was redacted after the hygiene gate flagged it. No code or engine changes — scoring bit-identical to 5.7.0; this build supersedes the ClawHub v5.7.0 package that carried the unsanitized sample.

## What's new in v5.7.0

- **Release-integrity overhaul (mechanistic fix for a live incident)**: v5.6.0 on ClawHub shipped with stale v5.5.0 files under a 5.6.0 label (version-agnostic completion guard blocked re-packaging; a retry then published the stale package). v5.7.0 fixes the mechanism: version-scoped completion guards, immediate post-packaging version assertion in the chain, builder archives version-agnostic guard files at generation time.
- **Sample outputs shipped (`examples/outputs/`)**: real engine JSON responses — detect / llm-jargon norm / fix suggestions — for integration reference.
- **Sentence-level locating** in the llm-jargon check findings; CHANGELOG quick-start banner; SKILL.md version history slimmed to the last three releases (single source of history).

## What's new in v5.6.0

- **LLM-jargon self-check (`pp_style_norm.py` check 7, `--checks llm_jargon`)**: three-tier detection of high-frequency AI-flavor phrasing in Chinese output — L1 metaphor-abuse blacklist, L2 tone words, L3 sentence patterns; findings carry case-library 原句→改句 contrasts and medical-register whitelist phrasings. Cross-line port credited to the immunology deep-read line's 2026-08-31 rejection post-mortem; ported corpus summarized in `eval/results/meddocs_20261014.json`.
- **Honest negative result**: engine scoring of these signals was tried and reverted same-day (held-out: human FPR@medium +1.5pt, current-gen AUROC −1pt). The detector reports hits (`jargon_hits`) without scoring; retry conditions documented in source.

## What's new in v5.5.0

- **Term-consistency check (`pp_style_norm.py` check 5, `--checks consistency`)**: same-concept variant mixing detection driven by a curated bank (`references/term_variants.json`, 23 groups) — flags mixing within one document (never correctness) with per-group unification advice; wired into `pp_workflow` §9.
- **Findings ledger in workflow reports (§10)**: each check marked answered / partially answered / unresolved (mixed-writing stays partially — calibrated attribution is triage-quality) with a budget note.
- **Docs**: sub-tool scope matrix extended; supervised-model acquisition stated; performance-table legend; deep-doc entry header; What's-new condensed into CHANGELOG.

## What's new in v5.4.1

- **Icon release**: new skill icon in the family flat style (white ground, steel-blue frame, signal-yellow hatch, bold "AI%" badge), shipped as `assets/icon-512.png`. No code changes.

## What's new in v5.4.0

- **Journal precheck 2.0 — discipline context**: the journal profile now detects the text's discipline (medical / engineering & CS / social sciences & humanities / general; keyword-density heuristic, `--discipline` override) and adds a per-discipline reading guide. Honest boundary explicit: the 20-25% reference line stays the cross-discipline convention — per-discipline thresholds have no recognized standard and this tool does not invent them.
- **Fingerprint freshness status (`freshness_refresh.py --status`, also `pp.py freshness`)**: last pipeline run, latest held-out evaluation record, bit-exact drift check against the four published baselines, due indicator (35-day interval); `--json` for pipelines, exit 1 on drift.
- **Binary-input guard**: PDF/image/zip at any text entry point → clear explanation with conversion advice (zero-dependency Chinese PDF extraction cannot be guaranteed — the tool says so and exits cleanly).

## What's new in v5.3.0

- **Word documents as first-class input (`scripts/docx_text.py`)**: every entry point now reads .docx directly — single-file detection, `--batch` (auto-collects `*.docx`), `pp_workflow`, `pp_fix_suggest`, `pp_style_norm`, `pp_rewrite_check`, `deai_gate`, and the bundle command. Zero dependencies (stdlib zipfile + XML), paragraph-preserving extraction, zip-bomb guards (uncompressed-size / member-count caps).
- **Submission self-check bundle (`scripts/pp_report_bundle.py`, also `pp.py bundle`)**: one command produces a dated self-check directory — workflow report (MD+JSON), paragraph-attribution HTML, rewrite suggestions, style-norm findings, README manifest with reading order and the integrity notice.
- **Docs**: Sub-tool scope matrix (each sub-tool's calibrated domain and outside-domain behavior — terminology bank scope, translation-smell coverage honesty, stylometry register limits); FAQ reorganized into grouped numbered sections (verdicts → modes → output → safety → tools).

## What's new in v5.2.0

- **Academic style-norm self-check (`scripts/pp_style_norm.py`, also `pp.py norm`)**: mechanical formatting conventions rather than AI-flavor — full/half-width mixing, number-usage consistency, abbreviation first-use definitions (with a common exempt list), unit formatting including the invisible U+03BC/U+00B5 mu mixing. Findings with concrete advice only; no score, no risk band, independent of AI-rate detection. Wired into `pp_workflow` (§9) and exposed as `pp_api.style_norm()`.
- **`--batch --report` direct output**: `ai_detector --batch DIR --csv scores.csv --report report.html` renders the HTML summary in the same run.
- **Eval archive hygiene**: `eval/results/archive/README.md` explains the `STALE-cache-poisoned` filename markers — deliberately-kept voided results of the 2026-10-02 cache-poisoning incident (evidence, not live data; incident and structural fix in CHANGELOG v4.4.0).

## What's new in v5.1.0

- **Rewrite-effect regression check (`scripts/pp_rewrite_check.py`, also `pp.py rewrite-check`)**: engine-source comparison of the original vs the revised draft — document-level score and risk-band migration, paragraph-level difflib-aligned per-paragraph deltas, feature-type counts cleared vs remaining (same seven types as `pp_fix_suggest`), edit extent (char ratio + replaced-paragraph rate). A relative reference under this engine's criteria only — never an institutional verdict. Ships with `--json`, `--demo`, and `pp_api.rewrite_check()`.
- **Batch HTML summary report (`scripts/pp_batch_report.py`, also `pp.py batch-report`)**: renders `--batch --csv` output into a single self-contained HTML — totals/mean/risk-band cards, a score histogram, and a per-file table sorted by score with ERROR/unknown rows surfaced. Zero dependencies; renders the existing CSV without re-running the engine.
- **Docs**: batch CSV concurrency semantics (atomic temp+rename since v4.9.0) and a `degraded_notice` reading guide are now explicit in the FAQ.

## What's new in v5.0.0

- **Sentence-level rewrite suggestions (`scripts/pp_fix_suggest.py`, also `pp.py fix`)**: the natural next question after a score — which sentences, why, and how to improve them. Each flagged sentence lists its concrete features (AI clichés, filler phrases, template patterns, vague qualifiers, connective openers, dash/colon habits, uniform rhythm) with a per-type rewrite strategy. Guidance only: it locates and suggests, never auto-rewrites. Ships with `--json`, a built-in two-sample demo (`--demo`), and a `fix_suggest` block in `pp_workflow` reports.
- **Bundled unit-test suite (`tests/`, `pp.py test`)**: 44 stdlib-unittest cases covering the iron laws (short text / empty / GBK), report field contracts, JSON purity, the gate, the workflow Markdown layout, data files, and the new tools — verifiable on your own machine without the model.
- **Structured zero-network self-verification (`scripts/pp_verify.py`, also `pp.py verify`)**: an AST-level scan of every script — flags network imports/calls and curl/wget-style subprocess commands, while URL strings in report footers are correctly treated as data (the old grep advice could not tell the two apart). Exit 0 = zero network calls.
- **Register awareness 2.0**: literary-narrative texts get a dedicated register notice (this register sits outside the academic calibration domain; measured literary classics can reach high band here) so the result is not mistaken for AI evidence. Disclosure only — no scoring change; all previously published numbers remain reproducible.
- **Packaging**: `requirements.txt` ships (core zero-dependency; optional supervised-layer extras commented); `pp.py quickstart` (zero-model demo: detect → fix → doctor); `pp_doctor` reports the latest held-out evaluation record; quality_report row added to the script cheat sheet.

## What's new in v4.9.0

- **Mixed-document calibration (closing the v4.7.0 backlog)**: paragraph-level hi/med/lo thresholds calibrated on the controlled mixed benchmark (333 paragraphs with ground truth; best operating point ≥50: precision 0.60 at 63% coverage — honestly below the automatic-verdict bar, ranking aid only). Calibration semantics corrected mid-flight: the earlier grid excluded the middle band from the binary classification, inflating F1 to 0.85; recalculated with full-below-threshold semantics (true F1 0.6131). Ships as `references/para_thresholds.json` and surfaces in every `mixed_document` assessment.
- **Unified entry (`scripts/pp.py`)**: one command routes all eleven subcommands — script-navigation cost zeroed.
- **Reliability**: batch CSV writes are now atomic (temp+rename, concurrent batch runs safe); gate layers retry once on crash/timeout before the neutral fallback.

## What's new in v4.8.0

- **Measurement integrity fixes from an independent third-party test round** (13 findings, verified one by one; the real bugs are fixed here, the capability observations are disclosed honestly):
  - `run_eval.py` cache keys now include the engine mode (`:nosup` suffix) — a rules-only evaluation could previously replay supervised-layer cached scores, making the base-engine numbers unreproducible. Reproducible now, fingerprint-and-mode-bound: rules-only **0.8985** old-gen / **0.7149** current-gen (bundled sample).
  - `--profile journal --format json` now emits **pure JSON** (journal precheck embedded as a `journal_precheck` field with both statistics explained — distribution vs intensity口径 measure different things).
  - `risk_bands` (active medium/high thresholds + calibration tier) is now surfaced in every report — the supervised and rules tiers carry independently calibrated thresholds, which fully explains score-band differences across modes.
  - `mixed_signal` denoised: both extremes must each cover ≥25% of paragraphs (a pure-AI document with one low-scoring outlier no longer flags as mixed).
  - Single files >5 MB now print a warning in single-file mode (batch still skips them); `--batch` directory requirement stated in the error message.
- **Honest disclosures**: real-world medical papers (PDF→text) can score elevated even in full mode — paragraph attribution is the actionable signal; fingerprint attribution is heuristic (top-n, never scored) and may misattribute. See FAQ.
- **Doc precision**: bundled-corpus scope clarified (n=1,304 sample vs n=5,251 full); terminology count corrected to 2,308 loaded; zero-network verification command made import-precise.

---

## What's new in v4.7.0

- **Mixed-document special**: a controlled mixed-writing benchmark with per-paragraph ground truth (54 synthesized docs built from held-out test-half sources only; `eval/build_mixed_bench.py`, results in `eval/results/mixed_para_20261005.json`) quantifies what the boundary matrix could only hint at: document-level AUROC 0.52-0.54 is an inherent averaging limitation, while **paragraph-level AUROC reaches 0.69** — paragraph attribution is triage-quality for locating suspect paragraphs (not an auto-verdict). `pp_workflow.py` now emits a `mixed_document` assessment (detection, AI-fraction estimate, guidance) and flags mixed documents prominently in the Markdown report.
- **Discoverability**: description gained a "Trigger on" routing-word block; README gained the China mirror (ModelScope) link. No behavior change.

## What's new in v4.6.0

- **End-to-end workflow (`scripts/pp_workflow.py` / `pp_api.workflow()`)**: one command runs the full self-check — AI-rate detection, paragraph-level attribution, 4-layer gate, terminology, translation-smell, style, quality report, AIGC label self-check — and writes a single Markdown report plus the full JSON. Worked example in § Quick start.
- **TL;DR layer & docs restructure**: a 30-second orientation section now sits at the top; historical release notes moved to `CHANGELOG.md`; anti-pattern guidance is consolidated in one section; the English FAQ is now on par with the Chinese one.
- **Cleaner eval archive & actionable errors**: superseded eval artifacts moved to `eval/results/archive/`; pp_api/pp_setup errors now carry recovery hints.

## What's new in v4.5.0

- **Python API (`scripts/pp_api.py`)**: the engine is now importable. `detect_text(text)` runs the full detector in-process (same code path as the CLI — parity-checked) and returns a plain JSON-able dict; helpers cover the rest of the toolkit: `gate_text`, `term_report`, `smell_report`, `style_report`, `quality_report_file`, `attribution`, `model_fingerprint`, `doctor_summary`. Zero network, zero third-party dependencies, exceptions instead of silent failures. Programmatic integration no longer requires wrapping subprocess calls.
- **One-command supervised setup (`scripts/pp_setup.py`)**: `--model <file>` replaces manual multi-step model placement. The file's md5 is checked against the author-signed fingerprint registry (`references/supervised_models.json`) — unknown weights are rejected (exit 2) — then the model is installed, inference-canaried, and confirmed GREEN; `--check` shows current status. The model still never ships inside the package and nothing is ever downloaded (the 100%-local contract is intact).

## What's new in v4.4.0

- **Headline numbers re-measured under verified conditions — they changed**: pre-2026 held-out AUROC **0.9998** (was believed 0.9022) and current-generation AUROC **0.9400** (was believed 0.6542), human FPR@medium **2.3%** (was believed ~20%). The old figures were measurement artifacts: eval score-cache keys did not bind the model (stale scores replayed across releases) and the deployed model binary was never fingerprinted. Both failure modes are structurally impossible since v4.4.0: cache keys carry the model md5 (`model_fp` in every result JSON) and `pp_doctor` prints the model fingerprint for audit.
- **Model rollout halted by the new data-hygiene audit (negative result, data-closed)**: the planned supervised-layer retrain (v36: 7187 prior rows + 285 fresh current-generation samples) was deployed and initially evaluated at near-perfect separation (old-gen 0.9994) — then rejected by our own new contamination audit: those 285 "fresh" samples had been drawn from the current-generation eval set itself (64.6% of gen2026 eval docs entered training, 154 of them from the held-out half). All v36 numbers are void; the shipped supervised model remains **v35** (fingerprint `2631df3d388b`, re-export verified; the contamination audit shows v35's training data shares only 1 held-out doc with the eval corpora, so its numbers are clean). An honest retrain needs a fresh sampling round (currently frozen); `eval/check_leak.py` now gates every future training run.
- **Evaluation score cache binds the deployed model fingerprint**: `run_eval.py` cache keys now include the model md5 — swapping models can no longer silently replay stale scores (a 10-02 v36 eval reading "bit-identical 0.9022" was exactly this failure; the true v36 numbers surfaced only after the fix). Result JSONs carry `model_fp`.
- **ONNX export self-test + ONNX thread budget**: export now runs variable-length inference assertions before a binary ships (a transformers 4.57.6 regression baked the dynamic axes into a static seq=150 graph — it now dies at export, not in production); `PP_ORT_THREADS` caps the ONNX thread pool (default auto) — on 56-vCPU hosts the unrestricted pool thrashed (24.9 s/doc → ~1 s/doc at 8 threads); `pp_doctor` prints the model md5 fingerprint for audit.

## What's new in v4.3.0

- **Generation-split evaluation (infrastructure + first numbers)**: a 443-doc current-generation eval set (312 fresh AI samples from 9 families + 131 held-out human docs) now ships in `eval/corpora_small/eval_gen2026.jsonl`; `run_eval.py --layer` fixed. First quantified generational breakdown: pre-2026 corpus AUROC 0.9022 vs current-gen 0.6542 — the generation gap is now measured, not assumed.
- **Negative results ×2, data-closed**: spectrum v2 blend and the L13 surprisal signal both show no current-gen gains (bit-identical and 0.32 respectively) — the remaining remedy is supervised-layer retraining on fresh samples (planned).

## What's new in v4.2.0

- **Batch recursion**: `--batch DIR --recursive` walks subdirectories; per-file paths are reported relative to the root.
- **GitHub README**: the repository landing page now carries the tool description, quick start, family table, and compliance statement (agents discovering via `skills add` see the full picture).
- **Gate layer-3 distribution check**: post-revival verdict distribution verified on 40 held-out documents — zero parse failures, no systematic band shift (data archived).

## What's new in v4.1.0

- **Smoothness layer fused into the score (A/B-verified)**: the L13 surprisal-variation signal (0.06 weight in all length bands) is now part of the fusion. Held-out A/B: **AUROC bit-identical to baseline (0.9022), human FP unchanged** — the signal has real influence on current-generation text where it fires, at zero measured cost on the evaluation corpus.
- **Batch CSV output**: `--batch DIR --csv PATH` writes per-file results as CSV (Excel-friendly UTF-8 BOM).
- **Paragraph report disclosures**: the HTML attribution report now carries mixed-register warnings, register hints, and encoding warnings — consistent with the JSON report.

## What's new in v4.0.0

- **Cross-references**: reports and docs now include next-step pointers to adjacent tools (citation verification, deep research, figures) with the arXiv hallucinated-citation policy note.
- **Word-root coverage**: description now carries the full task-language root set (academic writing / polish / batch rewriting guidance / terminology) for search discoverability.
- **Family section cleanup**: docsor.cn placed after the member list; list continuity fixed (EN/ZH).

## What's new in v3.12.0

- **Translation-smell layer revived in the gate (substantive fix)**: deai_gate's layer-3 parser expected a `hits[]` array while `translation_smell_check --json` emitted only `total_hits` — the layer had been silently neutral (fallback 50) since the schema drifted. Schema aligned; the layer now genuinely contributes to the fused score.
- **Integrity notice on every report**: term_check / quality_report / style_distance / translation_smell outputs now carry the same academic-integrity notice as ai_detector/deai_gate — the "every report" claim is now literally true.
- **Paragraph-count consistency**: quality_report now counts paragraphs with the same whitespace/short-segment filtering as ai_detector (trailing-newline mismatch fixed).
- Negative results recorded: spectrum v2 blend (fresh-generation 0.15 mix) produced a bit-identical held-out AUROC — not adopted; L13 mid-length (300-800 chars) extension evaluated and declined (human-side evaluable sample too small, FPR 2/10 at threshold).

## What's new in v3.11.0

- **Batch detection (`--batch DIR`)**: score every `.txt`/`.md` file in a directory in one run — per-file scores, aggregate stats (mean/max/high-risk count), deterministic, files >5 MB skipped. Built for thesis-scale self-review.
- **Paragraph report consistency**: the HTML attribution report now carries the same academic-integrity notice as the CLI reports.
- **Negative result, honestly recorded**: cross-family tier-2 n-gram mining over 285 fresh samples yielded nothing beyond topic-word noise after guards (the two real markers were already registered) — pattern-recall expansion via n-grams has hit its ceiling, consistent with the v3.0 recalibration. Fingerprint registrations this cycle: none qualified (quality gate held).

## What's new in v3.10.0

- **Fingerprint freshness phase 3 (current-generation coverage)**: 135 fresh samples across four model families (kimi-k2.7 / minimax-m3 / deepseek-v4.1 / glm-5.3) via the OpenCode Go channel; **kimi-k2.7 registered** (zero-FP pattern, Kimi-family attribution verified), contaminated candidates (topic words, cross-family markers) rolled back per quality gate, glm-5.3 refreshed with no new patterns. Registry: 13 families. Quality over quantity — every registration is attribution-verified.

## What's new in v3.9.0

- **Discourse smoothness disclosure (L13, DivEye-inspired)**: a new surprisal-variation layer measures how uniformly word choice varies across sliding windows — AI generation tends to be smooth, human writing uneven. Held-out long-document stats: AUROC 0.8256 as a standalone signal, detection 66/146 at threshold 6, human false-positive 1/14. **By the reproducible-numbers iron law it is NOT fused into the score** (single-layer SNR insufficient); it appears as an evidence line in reports (`layers_surface.surprisal_variation_layer`, with a spectrum-coverage guard at 0.35 and an evidence discount for low-coverage text).
- **Layer evaluation mode**: `python eval/run_eval.py --layer surprisal --split test` gives any report layer a reproducible AUROC/detection/FPR card (results saved to `eval/results/layer_*.json`) — the framework that let us measure L13 honestly instead of shipping it fused on faith.

## What's new in v3.8.0

- **Mixed-register signal (`mixed_signal`)**: when paragraph scores diverge sharply, reports now say so explicitly ("document may combine human and AI writing; document-level score unreliable") and point to `paragraph_report.py` — turning the documented mixed-document limitation (AUROC 0.38 document-level) into an in-engine guardrail (aligned with the field's move to three-class human/AI/mixed evaluation and bidirectional paraphrase benchmarks).
- **Register hint (`register_hint`)**: colloquial/narrative features in Chinese text trigger an advisory that scores are calibrated on academic prose.
- **Encoding warning (`encoding_warning`)**: many undecodable bytes (GBK/binary) trigger a distortion warning.
- **Gate layer-divergence disclosure**: deai_gate reports when the word layer and style layer disagree sharply (≥30), a pattern seen in deliberate style-imitation rewrites and register mixing.
- **Safety and behavior statement**: self-verifiable local-only / no-upload / no-credential / no-persistence commitments (aligned with platform review trends).
- **Fingerprint freshness second pass**: qwen3.8 balanced sampling (35 docs) yielded no low-FP patterns — honestly not registered (same as deepseek-v4); kimi-k3 registration stands.

## What's new in v3.7.0

- **Discourse-structure heuristic layer (L12)**: detects social-media-style document-level AI patterns — hook ("先看一个场景"/"imagine…") + reversal ("不是X，是Y") + slogan ("把这句话记住"/"划重点") + engagement bait / parallelism / self-Q&A / spoken-word closing / emotional intensifiers — eight pattern groups; ≥2 distinct groups add a density-scaled bump (8×groups + hits capped at 8, total cap 30); single-group hits are recorded without scoring (zero false-positive impact on academic prose). Fixes a sentence-layer blind spot: pure discourse-pattern text previously scored 21-32/low; held-out academic regression bit-identical (AUROC 0.9022, zero false positives).
- **FAQ section (evaluation-driven: C dimension "lacks a centralized FAQ")**: ten high-frequency questions — short-text policy, medical-register over-scoring, supervised-layer install/verification, degraded_mode semantics, non-interchangeability with CNKI/Wanfang, layer-failure fallback, edit_extent scope, English support boundary, label-check usage.
- **Script cheat sheet (C: "per-script usage could be more detailed")**: purpose/flags/output for all eight entry points in one table.
- **Clearer edge-case errors (R)**: style_distance now explains *why* no style score was produced (no sentence boundaries / no body paragraphs) instead of a generic "too short".

## What's new in v3.6.0

- **Academic-integrity guardrails**: every report now carries an explicit `integrity_notice` field/line; new "Academic integrity" section; positioning stated plainly — author self-review and writing quality, compliance with disclosure rules, not detector evasion.
- **Positioning clarified**: documentation wording aligned to the quality-framed scope (detection and revision guidance stay; no detector-evasion framing).

## What's new in v3.5.0

- **Degraded-mode disclosure**: `ai_detector.py` now reports `degraded_mode` + `degraded_notice` (JSON and text) whenever the supervised layer is absent, disabled (`PP_NO_SUP=1`), or skipped by language gating — including the medical-register over-score warning with the actual held-out numbers.
- **Iron law #2 enforced**: texts under 100 characters now return `risk=unknown` with an explicit no-verdict notice (previously documented but not implemented; short texts also show as "cannot judge" in `quality_report.py` instead of a misleading green).
- **`scripts/pp_doctor.py`**: one-command environment self-check — data integrity, script compilation, optional deps, model presence, supervised-layer loadability, short-text/long-text/determinism probes, deai_gate guard. Exit 0 = green.
- **`deai_gate.py` usage guard + closed fallback loop**: `--help` / missing file no longer run the gate on a bogus filename; layer timeouts are caught (neutral 50); a failed smell layer now falls back to a neutral 50 instead of 0, and a failed terminology layer no longer dumps tracebacks into notes.
- **Chinese-Windows encoding hardening**: every entry point forces UTF-8 stdout/stderr and tolerates non-UTF-8 (e.g. GBK) input files — no more crashes on default zh-CN consoles (found by adversarial multi-expert testing).
- Docs rebuilt in honest dual-language form (this file + SKILL_ZH.md); trigger words expanded (AI率 / 查AI率 / AIGC 检测 …).
---
---
---
---
---
---
---
---
---

# 更新日志（中文）

> v4.6.0 起历史更新说明移出 SKILL_ZH.md（新用户更快触达工作流）。最新在前。各版本摘要亦见 SKILL_ZH.md § 版本历史。

## v7.7.0 更新内容

- **输出契约 Schema 化（`schemas/*.schema.json`，`pp.py schema --selfcheck`）**：四大核心输出（detect / fix_suggest / workflow / term_report）随包 JSON Schema 契约（draft-2020-12 子集），零依赖最小验证器（`scripts/pp_schema.py`）在每次自证时用真引擎输出逐一过四契约。首跑即抓真漂移（mixed_document 是对象而非草稿臆断的布尔）——一句话说明这个验证器存在的意义。顶层必填键与类型是兼容性承诺：新增键不破坏契约；删除/改型在 CHANGELOG 声明。集成方用 `pp_api.schema_selfcheck()` 验证自己拿到的结构。
- **清单可复现性闭环**：评审点名完整性清单的结构与生成器逻辑；字节 diff 证明我方一致，但生成器硬编码 "generated" 版本串是真实的单一来源违规——现改为读 skill.json，新增 `--check` 模式（不落盘、字节级比对），发布闸断言生成器输出与随包清单逐字节一致。
- **pp_api 对齐收官**：`trend_data`（workflow JSON/目录 → 轨迹数据）与 `schema_selfcheck`——Python SDK 覆盖 CLI 全部能力面。

## v7.6.0 更新内容

- **安装完整性自证（`pp_doctor.py --deep`）**：11-05 评审报告「JSON 数据文件尾部截断」——在我们三方副本（trunk/SkillHub 包/ClawHub 包）均不可复现（逐字节一致且全部解析通过）。无论损坏发生在哪一环，机制层答案：包内随附 `data/INTEGRITY_MANIFEST.json`（全部数据与词表 JSON 的 SHA256+字节数），`pp_doctor --deep` 对每文件核对哈希与解析，两道发布闸把清单对 trunk 与两份打包副本各对账一次。若分发链路真截断文件，用户拿到精确到文件名与期望/实际哈希的证据——机器证据而非猜测。
- **`eval/gen_integrity_manifest.py`**：任何数据/词表变更后重新生成清单；过期清单会故意让深检 FAIL（哈希漂移正是它必须抓的东西）。

## v7.5.0 更新内容

- **双形态验收对偶（`eval/verify_forms.py`）**：两种随包形态共用一个对称验收器——`--form sh` 构造「SKILL_ZH.md 以 SKILL.md 名义发布」的副本（SkillHub 约定），`--form ch` 构造无 SKILL_ZH.md 的副本，共用包副本骨架（副本隔离+O_EXCL 锁+正本只读）并跑全量 smoke；`--form both` 串行跑双形态，发布链接入——形态回归从此不可能无声上船（10-31 评审的「形态相关文档/测试不匹配」类结构性关闭）。
- **archive/README 口径纪律**：历史结果 README 仍把 v480/v500 等历史文件称作「可复现基线」——连续两届评审点名。现开头即声明目录边界（本目录任何文件不可引用）并指向 CURRENT.md 为唯一口径权威，加闸拒绝旧声明回潮。
- **层级计数对齐**：skill.json 写 "11-layer" 而文档结构图已有 L12 篇章层——对齐为 12-layer 并加闸把计数与结构图绑定。

## v7.4.0 更新内容

- **评测口径物理分层**：v7.3.0 的 CURRENT.md 已逻辑声明哪些结果可引用，但目录里 29 个历史/作废文件仍与其物理混存。现全部 `git mv` 入 `eval/results/archive/`——顶层只留 CURRENT.md、三个现行基线与运行缓存——并加两道闸：顶层 `*.json` 必须全部入 CURRENT.md 表、archive 分层必须在位。评审点名的「历史文件多、难辨有效口径」从约定变成结构。
- **版本时代表指针**：SKILL.md 实测表的版本时代列保留为演进记录；现明确标注只有 `v35ctl_*`（指纹绑定）是现行口径，评审点名的旧数字误读风险关闭。
- **pp_api SDK 补齐（`fix_suggest` / `evidence_sections` / `term_project` / `scenarios`）**：编程用户拿到此前仅 CLI 可用的能力——句子级建议（同构结构化输出）、证据报告区块化证据链、跨文件术语矩阵（含 --bank）、可过滤场景目录。引擎同源、错误语义一致（ValueError↔退出码 2，RuntimeError 带恢复建议）。

## v7.3.0 更新内容

- **MCP 三原语对齐**：server 在 8 个 tools 之外新增 resources 与 prompts——resources：`ppp://capability-matrix`（能力边界矩阵，采信检测结论前先读）、`ppp://current-caliber`（现行可引用评测基线索引）、`ppp://changelog-latest`（最新更新说明）；prompts：`paper-selfcheck`（检测→建议→规范→行动清单）、`rewrite-loop`（建议意图→改稿核对→如实分数迁移）、`submission-precheck`（工作流→期刊口径→证据报告→标识合规），带参数渲染成可执行工作流模板。同一个零依赖零网络 server；capabilities 已声明。
- **一致性（评审抓到三处实的）**：SKILL_ZH 标题仍带 "v3" 化石与旧营销尾注（v7.1.0 只修了英文标题——SH 包把 SKILL_ZH 以 SKILL.md 名义发布，评审正是在那里看到）；已移除并新增双语标题一致闸。`requirements.txt` 一直没声明 `regex`，而 SKILL 的 pip 安装行教的是 `onnxruntime regex`、pp_doctor 也探针它——已声明并新增 requirements↔文档一致闸。SH 包形态（SKILL_ZH.md 以 SKILL.md 名义发布、包内不重复附带）现写入文档头部，打包约定不再会被误读为文件缺失。

## v7.2.0 更新内容

- **MCP HTTP transport（`--transport http`）**：stdio 之外新增本地回环 HTTP 形态——仅监听 127.0.0.1，`POST /mcp` 每请求一条 JSON-RPC，`GET /health` 存活探针。跟进 MCP 规范的 streamable HTTP 方向，支持同机多客户端复用一个 server（多个 agent 会话共享）。诚实边界代码与文档双写：仅回环、无鉴权、跨机暴露不在支持范围——与零网络立场一致（本地监听不构成对外服务）。
- **零网络自证精确化（`pp_verify`）**：HTTP transport 引入的 `http.server` import 被 AST 扫描命中（发布电池当场抓获——这正是自证存在的意义）。自证器现在区分监听器与客户端：`http.server` 仅在同文件携带回环（127.0.0.1）绑定断言时放行，双向测试锁定（0.0.0.0 绑定仍 fail）。SKILL 安全声明（中英）改为精确表述：零**出站**调用；唯一监听组件仅绑回环。
- **版本单一来源化**：server 自报版本硬编码 "6.5.0"（包已到 7.x——HTTP 验证时当场抓获）；现改为 import 时读 `skill.json`，唯一权威源。
- **AUROC 口径清尾**：'AUROC 1.0' 旧口径残留在 `skill.json` 与 SKILL_ZH frontmatter（10-31 评审在 v7.1.0 只清了 README/EN 标题后抓到这两处）；现在全部随包面均声明指纹绑定 0.9998，新增闸断言三处零残留。
- **口径导航（`eval/results/CURRENT.md`）**：结果目录历史/作废/现行混存无导航；现有一张唯一索引表（文件/指纹/评测集/关键数字/引用节），声明唯一可引用基线，档案标记不可引用，新增闸按表与磁盘、SKILL.md 引用三方对账。

## v7.1.0 更新内容

- **项目自定义术语库（`--bank`）**：学位论文有自己的缩写、机构名与课题组内部约定，这些永远不会进内置 2,344 条词库。`term_check.py --bank 项目词表.json` 与 `pp_term_consistency.py --bank` 接受项目词表（JSON 数组，条目格式同内置库：`cn`/`en`/`aliases`/`source`），与内置条目合并、同 `cn` 覆盖——哪个写法算标准由项目词表说了算，跨文件一致性同样走该词表。条目逐条带行号校验（坏条目如实报告，绝不静默吞掉）。内置词库不动。
- **一致性**：SKILL.md 标题带版本化石（包已到 7.0.0 标题仍是 "v3"——评审点名）；标题现不含版本号，并新增闸拒绝标题版本标记回潮。README 的 AUROC 声明（"1.0，作者侧实测"）早于指纹绑定重校准——对齐现行 0.9998 口径，新增闸把该数字锚定在 SKILL.md 与 README 两处。

## v7.0.0 更新内容

- **包形态自适应一致性（major 主题）**：评审在 CH 英文包形态下实测出真缺陷——随包 smoke 电池与多个测试硬读 `SKILL_ZH.md`，而语言铁律规定英文包不含该文件。全套现在双形态自适应：`tests/_docs.py` 把 ZH 文档读取转为诚实的 `SkipTest`（CH 形态 235 例全跑、8 个 ZH 断言如实跳过、零 error；SH 形态 235 例全跑）；smoke 的版本/frontmatter/desc/FAQ/触发词断言按同一开关条件化并显式标注包形态。「作者目录里好好的、发出去的包形态里失效」这一失效类从此结构性覆盖——发布前两种形态都会被演练。
- **跨文件一致性闸**：Python 最低版本全文档统一为 3.9（requirements.txt 写 3.8+ 而 pp_doctor 实际执行 3.9），新增闸断言所有声明与 doctor 门槛同源；README 不再硬编码测试计数（原文写「44 用例」而套件已增长到 235），新闸禁止该写法回潮。
- **改稿工作单（`pp_fix_suggest.py --worksheet`）**：句子级建议升级为可执行文档——Markdown 复选框清单（汇总表+逐句原句/问题/策略+「改后」留白复选行，由作者亲笔填写），闭环 `pp.py rewrite-check` 验收。工具仍然绝不代改；每个字由作者写。

## v6.9.0 更新内容

- **项目工作台（`pp_project.py`，`pp.py project`）**：学位论文/书稿场景的一条命令形态——对章节目录跑逐文件完整自查（每章 workflow.json/.md 照常落盘）、内嵌跨文件术语一致性矩阵、渲染项目总览（自包含 HTML + 机读 JSON）：逐文件分数/风险带/段落分级/门禁对照表、项目级聚合（均分/最高/高风险文件数/统一建议数）、逐概念统一建议。引擎同源（进程内调用 pp_workflow.workflow——无新打分代码）；单文件失败只损失该行（与批量同哲学）；总览带固定诚信声明（自查辅助，非合规证明）。

## v6.8.0 更新内容

- **批处理逐文件进程隔离（`--isolate`，默认 auto）**：v5.9.0 的 Python 异常隔离之上补齐进程级容错——每个文件在独立 worker 子进程中检测（CLI 本身作 worker，打分逐位不变；测试锁定 on/off 等价）。单文件硬崩溃（可选监督层 onnxruntime 原生层的段错误/abort——正是评审点名的失效类）只损失该文件的错误行，批处理继续，失败如实记录（worker 崩溃+退出码/信号）。auto=装了监督模型即开启（原生层是崩溃源；纯规则档保持进程内快路径），on/off 显式覆盖；输入类失败（退出码 2，worker 已打印友好提示）原样透传不包装成崩溃。
- **错误词典扩展**：worker 崩溃、处理超时、文本编码三类失效转人话+下一步。
- **卫生锁**：新增残留锁断言全部随包脚本无裸 `Traceback`/`print_exc`（技术词泄漏类）；v6.5.0 滑入 SKILL.md 的反模式重复标题由新文档测试抓出并移除。

## v6.7.0 更新内容

- **场景目录（`references/scenarios.json` + `pp.py scenarios`）**：17 个场景的单一来源目录，每条写明**什么时候用**、命令、你会得到什么——按情形挑命令，不用翻参考文档。内建命令支持关键词过滤（双语；紧凑中文查询去空格兜底匹配，如「测AI率」命中「测 AI 率」），可从 pp.py 帮助与自然语言路由（"什么时候用哪个命令"）到达。
- **快速开始场景化重构**：SKILL 快速开始块里每条命令都带一行「什么时候用」注解（此前是裸命令堆叠）；长尾命令经指引外移，双语文档各瘦身约 30 行回到 290 行内。
- **FAQ 技术节分层**：技术问答重组为「用户高频」（熔断/批量补扫/全稿术语统一/证据报告/PDF 立场/英文参考）与「集成者与进阶」（退出码/AST 自证/装模指纹/分数漂移）——内容不变，受众分层显式化，与阅读分层提示一致。

## v6.6.0 更新内容

- **检测证据报告（`pp_evidence_report.py`，`pp.py evidence`）**：面向「被质疑是不是 AI 写的」这一真实时刻——一条命令把完整检测证据链渲染成可交付的自包含 HTML + Markdown 报告：结论卡（分数/风险带/档位/监督模型指纹）、逐特征命中定位摘录、段落分级、阈值口径原样呈现、以及**不可关闭**的固定局限声明与学术诚信声明。报告头部即写明诚实定位：如实呈现引擎判定与证据，供自查与说明；**不构成「未使用 AI」的任何证明**；分数为引擎口径相对参考，不与任何机构检测器等价。
- **多文档术语一致性（`pp_term_consistency.py`，`pp.py term-project`）**：学位论文/课题组报告由多个章节文件组成，单文件术语检查看不见「第 2 章写 A、第 5 章写 B」。对目录（≥2 份文稿）构建库内概念的跨文件写法矩阵，列出不一致概念并给统一建议（以库标准名为准；标准名未出现时回落到使用最广的写法并如实标注依据），JSON/文本/HTML 三形态。诚实边界处处声明：只覆盖库内概念，库外自由写法不可见，可配合 `term_check --neologism`；扫描逻辑与 term_check 同源（最长优先认领、派生词/机构名排除），额外保留标准词命中供矩阵统计。

## v6.5.0 更新内容

- **MCP server（`scripts/pp_mcp_server.py`，`pp.py mcp`）**：paper-polisher-pro 现在可被 agent 客户端（Claude Code、Cursor 及一切 MCP 客户端）直接调用——零依赖 stdio server，纯标准库实现 JSON-RPC，无需安装任何第三方包，零网络立场不变。八个工具与 CLI 同引擎同退出码语义：`pp_detect`、`pp_fix_suggest`、`pp_style_norm`、`pp_term_check`、`pp_workflow`、`pp_explain`、`pp_faq`、`pp_doctor`。输入限幅（200 万字符）、输出自动截断（1.2 万字符）、引擎超时与异常如实以 `mcp_error` 回传不伪装成功。配置示例见 SKILL.md § MCP server。
- **反模式 ↔ FAQ 去重**：评审指出两处重叠（医学语域告诫双份）。反模式节现明确自身分工（判断类铁律——不该做什么），FAQ 明确自身分工（操作型怎么做），两边互为指针不再重复展开；FAQ 头部新增阅读分层提示（前五组面向所有用户，「具体技术问题」节面向集成者与进阶排障）。

## v6.4.0 更新内容

- **批量自动补扫（`--retries`，默认 2）**：批处理不再把瞬时失败（文件被占用、读取抖动）留给手动重跑——首轮结束后对失败文件自动补扫至多 `--retries` 轮，补扫成功的行如实标注 `retried: true` 与 `attempts`；耗尽仍失败的进新增的 `failed_files` 聚合清单并附逐文件诊断指引（`pp.py detect <文件>` 看完整错误）。首轮熔断器行为不变，且已熔断则跳过补扫（明确的坏批次重扫无益）；`--retries 0` 恢复 v6.3.0 行为。补扫整轮无一恢复即提前停止（持久坏文件不白烧）。文本摘要行显示实际补扫轮数与诊断指引。
- **五站导览（`pp.py tour`）**：五站全部现场真实运行——内嵌样例检测、随包真实 workflow 产物的报告解读、前三条改写建议、可视化与多轮趋势命令地图（指向随包真实 `report_html_sample.html`）、环境档位自检——约 10 秒，全部本地零网络。跟随 `PP_LANG=en` 切英文面；自然语言路由可达（"功能太多不知从哪开始"→tour）。为可发现性而做：趋势、段落归因、自查包等增值功能此前容易被错过。
- **快速开始引用真实产物**：SKILL.md 快速开始新增 `examples/outputs/` 预览行，新用户跑命令前就能看到输出长什么样；`--batch --csv --report` 一条龙组合与新的 `--retries`/`--circuit` 交互已配可直接复制的命令（中英双语）。
- **FAQ**：新增批量失败条目（自动补扫语义、什么时候还需要手动重跑——答案通常是永远不用）。
- **随包样例换真实公开数据重制**：`detect_sample.json` / `workflow_sample.json` / `report_html_sample.html` 改用真实公开文稿重新生成（维基百科「免疫系统」条目，CC BY-SA，溯源见 `examples/outputs/README.md`），不再使用内部工作笔记；打包卫生闸同步扩充——内部编号、内网 IP、内部笔记 ID 一律不得进随包文本文件，随包测试加样例卫生锁。

## v6.3.0 更新内容

- **独立 FAQ（`references/faq.md`，`pp.py faq <关键词>`）**：FAQ 从 SKILL.md 迁出成独立可检索档案——完整分组问答（判定/模式/输出/安全/工具）外加新增的「具体技术问题」节（为什么不支持 PDF、英文为什么仅参考、AST 自证是什么、熔断是什么、退出码契约、装模签名失败、分数为什么和上次不一样）。`pp.py faq 医学` / `faq PDF` / `faq 退出码` 按标题命中加权检索条目，无命中给兜底指引；SKILL.md 保留高频三条+链接（主文档再度瘦身）。
- **错误信息联动 FAQ**：所有友好错误输出末尾附 `pp.py faq <关键词>` 指针——从报错到答案一条线走完。

## v6.2.0 更新内容

- **改写对照双栏 HTML（`pp_rewrite_check.py --html out.html`）**：改写效果对比此前只有文本输出，现在可渲染一份自包含 HTML——按 difflib 对齐逐段并排展示原稿/改稿摘录（含相似度），逐段分数迁移着色（↓改善/↑回升），顶部卡片呈现文档级变化与风险带迁移，附特征类型增减表。对齐行新增 ≤100 字摘录字段（JSON 加法字段 `original_excerpt`/`revised_excerpt`）。全部文本 HTML 转义；零外部资源；零网络。
- **仪表盘信号细节节（`pp_report_html.py`）**：workflow 仪表盘新增「信号细节」——语域提示、混写预警、篇章结构特征命中、LLM 腔命中数（与全工具一致：只提示不计分），仅在报告实际携带时渲染。

## v6.1.0 更新内容

- **报告解读器（`pp_explain.py`，`pp.py explain`）**：任意 workflow/detect JSON → 三段人话——【结论】分数/风险带/档位（降级档医学警告如实转述）、【证据】段落 hi/med/lo 与最高分段摘录、门禁判定、规范与术语 findings 聚合、句子建议统计、【行动清单】按报告内容给出可执行命令（混写→逐段复核、fix/norm/term、趋势、投稿打包）。自然语言路由「解读这份报告」可达。
- **错误词典扩展（`pp_errors.py`）**：评审点名的剩余技术话术全部人话化——AST 自证命中、基线漂移、作者签发拒绝、门禁层解析回退；`pp_verify` 命中时输出下一步指引；`pp.py` 透传遇到异常退出码时打印契约含义与 doctor 指路。
- **超时加固**：`pp.py quickstart` 三个子步各加 180 秒超时（单步卡死不再拖死演示）；门禁层既有的 120 秒超时+一次重试行为写入文档稳定性契约。
- **深水区外迁 `references/`**：架构图与指纹保鲜流水线说明（校准切分、代际覆盖）从 SKILL.md 迁至 `references/architecture.md`（保留链接、按需阅读）——主文档回归上手文档定位。
- **`references/best-practices.md`（新增）**：场景级指南——什么学科选什么口径、段落归因的正确（人工复核）用法、改写循环（rewrite-check/trend）、批量组织与熔断、档位与可信度边界、合规；`examples/outputs/` 每个样例标注了它回答什么场景。

## v6.0.0 更新内容

- **多轮趋势仪表盘（`pp_trend.py`，`pp.py trend`）**：单次报告只回答「现在多少分」，多轮改稿真正要问的是「改了这么多版分数到底有没有降」。把每轮的 workflow JSON（文件或目录）喂给它，得到一张自包含 HTML：分数轨迹内联 SVG（风险带着色、降级轮空心点）、逐轮 delta 表（↓改善/↑回升醒目标注）、首末净变化卡片。诚实边界写入输出：分数下降不等于内容更好——改稿以质量为准；降级档与融合档轮次不可直接互比且有标注。
- **统一错误呈现（`pp_errors.py`）**：错误处理不再分散各脚本、技术原文直出（如 zip-bomb 护栏文案）。已知护栏异常统一渲染为「人话解释 + 具体下一步」两行（过大/损坏 docx 怎么办、扩展名与实际格式不符怎么办、缺模型 → 指向获取指南）。退出码契约不动（0/1/2/3）。已接入 ai_detector / pp_workflow / pp_report_bundle / docx_text 四入口。
- **分组入口 + 英文面（`pp.py`）**：21 个子命令的平铺清单改为按场景分组（检测/改写建议/规范与术语/报告与可视化/合规与自证/环境），顶部置新手三步；`PP_LANG=en` 把入口面（帮助/未知命令提示/推荐输出）整体切英文——与 `PP_NO_SUP` 并列的第二个环境变量，均已写入安全声明。
- **批处理混沌压测套件**：随包测试新增混合混沌夹具（损坏/空/过短/编码异常/正常文件同目录），断言逐文件隔离、熔断披露与 CSV 完整性——上一版点名的长批健壮性，现在有测试锁定。

## v5.9.0 更新内容

- **监督模型获取指南（`pp_setup.py --guide`）**：零配置体验的最后一块缺口——可选监督层只讲「怎么装」不讲「去哪拿」。新指南命令写清该层是什么、作者签发获取渠道（GitHub issue）、放置与验证步骤、以及不装时的降级档语义；`pp_doctor` 与 `pp_setup --check` 在引擎处于降级档时会主动指到指南。
- **批处理熔断器（`ai_detector.py --batch ... --circuit N`）**：连续 N 个文件解析/检测失败即中止剩余队列（默认 5，`--circuit 0` 关闭），不再对着整目录坏文件白烧时间——已完成部分照常出 CSV/报告，中止事实写入 JSON（`circuit` 字段）与文本摘要。随附一个由新测试抓出的真实稳定性修复：此前一个损坏 .docx 会经未捕获 SystemExit 炸掉整批，现在按设计降级为逐文件 ERROR 行。
- **词典外新造词探测（`term_check.py --neologism`）**：opt-in 启发式，把「高频出现却不在术语库」的字串作为人工复核线索输出（源自跨线文稿规范化复盘——词典对自创词不可见）。诚实边界写入输出：未校准、只提示不判定对错、永不计分、永不汇入门禁；默认运行完全不变。
- **版本头卫生**：四个脚本仍带着引擎文件时代（v1.x 化石）的版本头，与包版本不一致——头已中性化，并新增发布闸（smoke 检查+单元测试）防此类复发。
- **渐进披露**：TL;DR 明示 FAQ 五个分组，架构节标注「按需阅读」。

## v5.8.1 更新内容

- **术语库扩充实战对照映射（+27 条/别名）**：跨线文稿复盘发现一批自创缩略语与口语隐喻（如「龄化复判」「活疫苗门禁」「头号盯防」类表述）此前词典无法识别。现全部以别名挂靠规范名——`term_check.py` / `pp.py term` 逐词命中并给出规范名建议；文档计数声明更新为真实加载量（2,335 个规范名）。
- **匹配机制修复**：候选裁决改为单遍「最长优先」（标准词与别名同池全局裁决）——旧两遍扫描中短标准词可占位静默压制重叠的更长别名（2 字标准词挡住 4 字别名即漏报）。既有行为（派生词/机构名后缀排除、英文词边界）全部保留并由金丝雀回归测试锁定。

## v5.8.0 更新内容

- **单文档可视化仪表盘（pp_report_html.py，`pp.py html-report`）**：把 workflow / detect / fix_suggest / style_norm 的 JSON 产物渲染成一份自包含 HTML——分数半环仪表（内联 SVG）、段落分数直方图、段落热表、改写建议表、规范 findings 表（含 LLM 腔命中句），以及 workflow 附加块（混写评估/四层门禁/术语/翻译腔/文体/质量/AIGC 证据/台账）。内联 CSS、零外部资源、零网络、纯标准库；全部文本字段经 HTML 转义。输入按特征键自动识别，可任意混搭。
- **自然语言命令路由（`pp.py recommend "..."`）**：用一句中文或英文描述需求（如「把这段的AI率降一降」「环境跑不起来」），返回命中度最高的三个子命令与可直接复制的命令行——降低 21 个子命令工具箱的首次定位成本。
- **退出码契约（入档并锁定）**：0 成功 / 1 运行完成但未通过 / 2 用法或输入错误 / 3 环境不满足，与 `pp_api` 的 `ValueError`/`RuntimeError` 同构——对脚本与集成方的稳定性承诺，写入 SKILL.md 与 `pp.py --help`。
- **文档**：三条最重要的限制（降级档医学高估/混写均值稀释/数据覆盖范围）前置到 TL;DR 旁；`examples/outputs/` 新增真实 workflow JSON 样例与渲染 HTML 样例；中文版本历史瘦身对齐英文（唯一完整历史=本文件）；清理历史条目中一处过时内部编号。
## v5.7.1 更新内容

- **样例脱敏**：随包样例文档文本中一处内网链接（examples/outputs/detect_sample.json）经卫生闸检出后脱敏。代码与引擎零变更——打分与 5.7.0 逐位一致；本版取代曾携带未脱敏样例的 ClawHub v5.7.0 包。

## v5.7.0 更新内容

- **发布完整性机制化改造（线上事故的机制级修复）**：v5.6.0 在 ClawHub 携带了 v5.5.0 旧文件（版本无关完成守卫误拦重打包+重试引用陈旧包）；v5.7.0 修机制：版本化完成守卫/链内打包后即时版本断言/构建器生成时归档旧守卫文件。
- **随包输出样例（`examples/outputs/`）**：检测/LLM 腔规范自查/改写建议的真实引擎 JSON 响应。
- **LLM 腔自查命中句定位**；CHANGELOG 快速上手横幅；SKILL.md 版本历史瘦身为最近三版（历史单一来源）。

## v5.6.0 更新内容

- **LLM 腔自查（第 7 查）**：中文输出高频 AI 腔三层检测（L1 隐喻滥用黑名单/L2 语气词/L3 句式模式），findings 附判例库「原句→改句」对照与医学语体白名单；跨线移植注明来源（免疫深读线判废复盘），摸底语料汇总随包 `eval/results/meddocs_20261014.json`。
- **诚实负结果**：引擎计分当日试当日回退（留出集人类 FPR@medium +1.5pt、当打代 AUROC −1pt）；检测器只报命中不计分，重试条件写入源码。

## v5.5.0 更新内容

- **术语一致性检查（`pp_style_norm.py` 第 5 查）**：同概念异写混用检测，词库 23 组（患者/病人、禁忌证/禁忌症、数据/资料、approximately/~…）；检测混用非对错，按组给统一建议；已并入 `pp_workflow` §9。
- **Findings Ledger（§10）**：workflow 报告每项检查标记 answered / partially / unresolved（混写判定恒 partially——校准即 triage 级）+ 预算说明。
- **文档**：子功能适用域矩阵补全；监督模型获取方式明示；性能表版本时代标注；深文档入口头；What's new 收敛入 CHANGELOG。

## v5.4.1 更新内容

- **图标版**：全新技能图标（家族扁平风：白底+钢蓝框+信号黄斜纹+特粗 AI% 徽章），随包 `assets/icon-512.png`。零代码变更。

## v5.4.0 更新内容

- **期刊口径 2.0——分学科语境**：期刊口径预检自动识别学科（`--discipline` 可覆盖）并给出分学科解读指引；20-25% 参考线不变，明示不虚构分学科数字。
- **指纹保鲜状态（`freshness_refresh.py --status`，或 `pp.py freshness`）**：最近执行/最新评测记录/四条已发布基线逐位漂移检查/到期提醒；`--json` 供管道，漂移 exit 1。
- **二进制输入护栏**：PDF/图片/zip 在任意文本入口得到明确解释与转存建议，不再静默乱码。

## v5.3.0 更新内容

- **Word 文档一等公民输入（`scripts/docx_text.py`）**：所有入口直读 .docx——单文件检测、`--batch` 自动收集、`pp_workflow`、`pp_fix_suggest`、`pp_style_norm`、`pp_rewrite_check`、`deai_gate` 与自查包命令。零依赖（标准库 zipfile+XML），按段落保留文本，解压炸弹防护。
- **投稿前自查包（`scripts/pp_report_bundle.py`，或 `pp.py bundle`）**：一条命令产出带时间戳自查目录——workflow 报告（MD+JSON）、段落归因 HTML、改写建议、规范自查 findings、README 清单。
- **文档**：子功能适用域矩阵（每个子工具的校准域与域外行为逐一明示）；FAQ 重组为分组编号章节。

## v5.2.0 更新内容

- **学术写作规范自查（`scripts/pp_style_norm.py`，或 `pp.py norm`）**：机械体例核对而非 AI 痕迹——全半角混用、数字用法一致性、缩写首次定义（含惯用豁免表）、单位格式（含 μ U+03BC/µ U+00B5 隐形混用）。仅输出带具体改法的 findings；不评分、无风险带，与 AI 率检测相互独立。已并入 `pp_workflow`（§9），SDK 暴露 `pp_api.style_norm()`。
- **`--batch --report` 直出**：`ai_detector --batch DIR --csv scores.csv --report report.html` 同一次跑完即渲染 HTML 汇总。
- **评测存档卫生**：`eval/results/archive/README.md` 解释 `STALE-cache-poisoned` 文件名标记——2026-10-02 缓存污染事故的作废结果（证据性保留；事故与结构性修复见 CHANGELOG v4.4.0）。

## v5.1.0 更新内容

- **改写效果回归验证（`scripts/pp_rewrite_check.py`，或 `pp.py rewrite-check`）**：引擎同源对比原稿与改稿——文档级分数与风险带迁移、段落级 difflib 对齐逐段 delta、七类特征清除/残留清单（与 pp_fix_suggest 同口径）、编辑幅度（字数比+段落替换率）。仅为本引擎口径下的相对参考，不构成任何机构判定。支持 `--json`、`--demo` 与 `pp_api.rewrite_check()`。
- **批量 HTML 汇总报告（`scripts/pp_batch_report.py`，或 `pp.py batch-report`）**：`--batch --csv` 产物渲染为单文件 HTML——总数/均分/风险分档卡片、分数分布直方图、按分数降序逐文件表（ERROR/unknown 置顶提示）。零依赖，不重跑引擎（只渲染既有 CSV）。
- **文档补全**：batch CSV 并发语义（v4.9.0 起原子写）与 `degraded_notice` 阅读指引显式入 FAQ。

## v5.0.0 更新内容

- **句子级改写建议（`scripts/pp_fix_suggest.py`，或 `pp.py fix`）**：分数之后的自然下一步——具体哪几句、因为什么、往哪个方向改。每个被标记的句子列出其具体特征（AI套话/填充短语/模板句式/模糊限定/连接词开头/破折号冒号习惯/均匀节律）并给出各类改写策略。只指位与策略、不代写不自动改写——改写决定权在作者本人。支持 `--json`、内置双样例演示（`--demo`），并已在 `pp_workflow` 报告中新增 `fix_suggest` 块。
- **随包单元测试套件（`tests/`，`pp.py test`）**：44 个标准库 unittest 用例，覆盖铁律（短文本/空输入/GBK）、报告字段契约、JSON 纯净性、门禁、工作流 Markdown 布局、数据文件与新工具——不装模型也能在自己机器上验证行为。
- **结构化零网络自证（`scripts/pp_verify.py`，或 `pp.py verify`）**：AST 级扫描全部脚本——网络 import/调用与 curl/wget 式子进程命令一律命中；报告页脚的 URL 字符串被正确视为数据（旧 grep 建议区分不了这两者）。exit 0=零网络调用。
- **语域感知 2.0**：文学叙事文本获得专门语域提示（该语域超出学术校准域；实测文学名篇在本引擎可达 high 档），结果请勿当作 AI 证据。仅披露，不改任何打分；全部已发布数字保持可复现。
- **打包**：`requirements.txt` 随包（核心零依赖；可选监督层依赖注释声明）；`pp.py quickstart` 零模型一键体验（detect → fix → doctor）；`pp_doctor` 新增最近留出集评测记录行；速查表补 quality_report 行。

## v4.9.0 更新内容

- **混写文档校准（收口 v4.7.0 backlog）**：段落级 hi/med/lo 阈值在可控混写基准（333 段逐段真值）上完成校准（最优工作点 ≥50 分：精度 0.60、覆盖 63%——诚实低于自动判定可用线，排序辅助）。校准口径中途修正：早先网格把中带剔出二分类导致 F1 虚高 0.85，按全带语义重算（真值 0.6131）。随包发布 `references/para_thresholds.json` 并在每次 `mixed_document` 评估中透出。
- **统一入口（`scripts/pp.py`）**：一条命令路由全部 11 个子命令——脚本导航成本清零。
- **可靠性**：批处理 CSV 改原子写（临时文件+改名，并发跑批安全）；门禁各层崩溃/超时先重试一次再兜底。

## v4.8.0 更新内容

- **测量与输出契约诚实版（第三方独立测试轮 13 项发现逐条核实，真缺陷全修，能力观察诚实披露）**：
  `run_eval.py` 缓存键纳入引擎档位（`:nosup` 后缀）——此前规则档评测会重放监督层缓存分致基础引擎数字不可复现；现已可复现且指纹+档位双绑定：纯规则老代 **0.8985** / 当打代 **0.7149**（随包语料）。
  `--profile journal --format json` 现输出**纯 JSON**（期刊口径以 `journal_precheck` 字段嵌入，双口径统计差异已内嵌解释）；每份报告透出 `risk_bands`（现行中/高风险带阈值+校准档位——监督档与规则档各自独立校准，跨档分带差异从此可解释）；`mixed_signal` 去噪（两端各 ≥25% 段占比才报混写）；单文件 >5MB 增加提示；`--batch` 目录要求写入报错信息。
- **诚实披露**：真实期刊论文（PDF 转文本）即使全档也可能评分偏高——段落归因才是可用信号；指纹归因为启发式参考（top-n 不进分），存在误归因可能。详见 FAQ。
- **文档精度**：随包语料口径澄清（抽样 1,304 vs 全量 5,251）；术语计数修正为加载 2,308 条；零网络验证命令改为 import 精确口径。

## v4.7.0 更新内容

- **混写文档专项**：构造带逐段真值的可控混写基准（54 篇合成文档，段落仅取自留出 test 半来源；`eval/build_mixed_bench.py`，结果 `eval/results/mixed_para_20261005.json`），把边界矩阵只能定性提示的局限定量化：**文档级 AUROC 0.52-0.54（平均原理性局限）vs 段落级 AUROC 0.69**——段落归因达到「人工复核定位」的 triage 质量而非自动判定。`pp_workflow.py` 新增 `mixed_document` 评估块（检测/AI 段占比估计/处置指引），混写文档在 Markdown 报告中醒目标注。
- **可发现性**：description 新增 Trigger on 路由词块；README 新增中国镜像（魔搭）链接。行为零变更。

## v4.6.0 更新内容

- **端到端工作流（`scripts/pp_workflow.py` / `pp_api.workflow()`）**：一条命令跑完全部自查——AI 率检测、段落级归因、四层门禁、术语保护、翻译腔、文体、质量报告、AIGC 标识自查——产出单一 Markdown 报告+完整 JSON。示例见 § 快速开始。
- **TL;DR 层与文档重构**：顶部新增 30 秒上手层；历史更新说明迁至 `CHANGELOG.md`；反模式集中成节；英文 FAQ 对齐中文版。
- **评测存档整理与错误可行动化**：过时评测产物移入 `eval/results/archive/`；pp_api/pp_setup 错误信息附带恢复建议。

## v4.5.0 更新内容

- **Python API（`scripts/pp_api.py`）**：引擎可直接 import。`detect_text(text)` 进程内跑完整检测（与 CLI 同一代码路径——已做同源校验），返回纯 JSON 兼容 dict；配套 `gate_text`、`term_report`、`smell_report`、`style_report`、`quality_report_file`、`attribution`、`model_fingerprint`、`doctor_summary`。零网络、零第三方依赖、非法输入抛异常不静默。程序化集成从此不必包装 subprocess。
- **一键装模（`scripts/pp_setup.py`）**：`--model <文件>` 取代多步手动放置。先按作者签发指纹注册表（`references/supervised_models.json`）校验 md5——未登记权重一律拒绝（exit 2）——再安装、推理金丝雀自检、GREEN 确认；`--check` 查看现状。模型依旧不随包、绝不联网下载（100% 本地契约不变）。

## v4.4.0 更新内容

- **头条数字在可信测量下重测——变了**：老代留出 AUROC **0.9998**（原以为 0.9022）、当打代 AUROC **0.9400**（原以为 0.6542）、人类误报@medium **2.3%**（原以为约 20%）。旧数字是测量伪象：评测分数缓存键不绑定模型（陈旧分跨版本复放）、部署模型二进制从未指纹化。两类故障自 v4.4.0 起结构性不可能：缓存键携带模型 md5（结果 JSON 带 `model_fp`）、pp_doctor 打印模型指纹供对账。
- **数据卫生审计叫停监督层再训练（负结果，数据闭环）**：原计划的 v36 再训练（7187 行旧数据+285 篇当打代新鲜样本）已部署、并一度测出近乎完美的分离度（老代 0.9994）——随即被本版新增的污染审计否决：**那 285 篇「新鲜样本」直接取自当打代评测集本身**（gen2026 评测集 64.6% 文档进入训练集、其中 154 篇属于留出半）。v36 全部数字作废；线上监督模型维持 **v35**（指纹 `2631df3d388b`，重导出已验证；污染审计显示 v35 训练数据与评测语料仅 1 篇留出集交集，其数字干净）。诚实的再训练需要新一轮采样（当前冻结）；`eval/check_leak.py` 从此把守每一次训练。
- **评测分数缓存绑定部署模型指纹**：`run_eval.py` 缓存键纳入模型 md5——换模型不再可能静默复用陈旧分（10-02 那份「位级 0.9022」的 v36 评测正是此故障；修复后 v36 的真实数字才浮出水面）。结果 JSON 携带 `model_fp`。
- **ONNX 导出自检 + 线程预算**：导出脚本在产出二进制前强制变长推理断言（transformers 4.57.6 回归会把动态轴烘焙成静态 seq=150——现在坏图在导出当场爆掉，不会流进生产）；`PP_ORT_THREADS` 限制 ONNX 线程池（默认自动）——56 vCPU 机器上不限线程会互踩（24.9 秒/篇 → 8 线程约 1 秒/篇）；`pp_doctor` 现打印模型 md5 指纹供对账。

## v4.3.0 更新内容

- **分代评测基础设施（首批数字）**：新增当打代评测集 `eval/corpora_small/eval_gen2026.jsonl`（312 篇当打代 AI×9 家族+131 篇人类留出=443 篇）；`run_eval.py --layer` 修复。**首批分代数字：老代语料 0.9022 vs 当打代 0.6542——代际退化首次量化**（此前 AUROC 混合老代样本，当打代检测力不可见）。
- **负结果×2 数据闭环**：谱 v2 混合与 L13 平滑度信号在当打代均无增益（逐位相同/方向不支持）——当打代补救唯一路径=监督层再训练（285 篇当打代样本已在手，规划中）。

## v4.2.0 更新内容

- **批处理递归**：`--batch 目录 --recursive` 遍历子目录，文件路径相对根目录呈现。
- **GitHub README**：仓库落地页现包含工具说明、快速开始、家族工具表与合规声明（skills add 发现渠道可见全貌）。
- **门禁层3 分布复核**：复活后 40 篇留出文档判定分布验证——零解析失败、无系统性偏移（数据入档）。

## v4.1.0 更新内容

- **平滑度层正式入融合（A/B 验证）**：L13 surprisal-variation 信号（各长度带 0.06 权重）纳入融合计分。留出集 A/B：**AUROC 与基线逐位相同（0.9022）、人类误报不变**——信号在当打代文本上触发时有真实影响力，评测语料零代价。
- **批处理 CSV 输出**：`--batch DIR --csv 路径` 逐文件结果落 CSV（UTF-8 BOM，Excel 友好）。
- **段落报告披露一致化**：HTML 归因报告现携带混写预警/语域提示/编码警示——与 JSON 报告一致。

## v4.0.0 更新内容

- **相关工具互引**：报告与文档在相邻环节出口处加入下一步工具提示（引用核验、深度调研、配图），并附 arXiv 幻觉引用禁投政策提醒。
- **任务词根全覆盖**：description 融入完整任务词根集（academic writing / polish / batch rewriting guidance / terminology），搜索可发现性对齐 cite-holmes 口径。
- **家族段整理**：docsor.cn 移至成员列表后；列表连续性修复（EN/ZH）。

## v3.12.0 更新内容

- **翻译腔层复活（实质性修复）**：deai_gate 层3 解析器期望 hits[] 数组，而 translation_smell --json 只输出 total_hits——schema 漂移以来该层一直静默走中性 50 兜底。已对齐 schema，翻译腔层首次真正参与融合计分。
- **诚信提示全报告覆盖**：term_check / quality_report / style_distance / translation_smell 输出现携带与 ai_detector/deai_gate 相同的学术诚信提示——"每份报告"的表述字面为真。
- **段落计数一致性**：quality_report 改用与 ai_detector 相同的空白/过短段过滤口径（尾随空行计数不一致修复）。
- 负结果入档：谱 v2 混合（新鲜代 0.15 配比）留出集逐位相同——不采纳；L13 中篇（300-800字）扩展经评估否决（人类可评样本过少、阈值下误报 2/10）。

## v3.11.0 更新内容

- **批处理检测（--batch 目录）**：一条命令打分目录内全部 .txt/.md 文件——逐文件分数+聚合统计（均分/最高/高风险文件数），确定性输出，>5MB 自动跳过。为论文级批量自查而生。
- **段落报告一致性**：HTML 归因报告头部加入与命令行报告相同的学术诚信提示。
- **负结果如实记录**：285 篇新鲜语料的跨家族 tier-2 n-gram 挖掘，守卫后只剩主题词噪声与两条已知标记——n-gram 召回扩展已到天花板（与 v3.0 重校准结论一致）。本轮指纹入册：无（质量门坚守）。

## v3.10.0 更新内容

- **指纹新鲜度第三期（当打模型覆盖）**：OpenCode Go 通道四家族新鲜采样 135 篇（kimi-k2.7 / minimax-m3 / deepseek-v4.1 / glm-5.3）；**kimi-k2.7 入册**（零误报模式，Kimi 族归因验证通过），主题词/跨家族污染候选按质量门回滚，glm-5.3 刷新无新模式。指纹库：13 家族。宁缺毋滥——每一笔入册都经归因验证。

## v3.9.0 更新内容

- **篇幅平滑度披露（L13，DivEye 思路本地化）**：新增 surprisal-variation 层——滑窗用词变化性刻画"AI 平滑、人类起伏"。留出集长文统计：独立信号 AUROC 0.8256、阈值 6 下检出 66/146、人类误报 1/14。**按"只报可复现的数字"铁律不进融合分**（单层信噪比不足）；以证据行形式出现在报告中（谱覆盖守卫 0.35 + 低覆盖证据折扣）。
- **报告层评测模式**：`python eval/run_eval.py --layer surprisal --split test`——给任何报告层一张可复现的 AUROC/检出/误报卡片（结果存 `eval/results/layer_*.json`）；正是这个框架让我们能诚实量化 L13，而不是凭信心把它融进分数。

## v3.8.0 更新内容

- **混写预警（mixed_signal）**：段落得分显著分化时如实提示"疑似人机混写、文档级分数不可单独采信"，并引导 `paragraph_report.py` 逐段归因——把能力边界矩阵中"混合文档 AUROC 0.38"的原理性局限变成引擎侧可操作指引（对齐学界混写检测方向：三分类人写/生成/润色与双向改写基准）。
- **语域提示（register_hint）**：检测到口语/叙事表达特征时提示"评分按学术语域校准、本场景仅供参考"——能力边界矩阵的引擎侧落地。
- **编码警示（encoding_warning）**：输入含大量不可解码字节（GBK/二进制）时提示结果可能失真。
- **门禁层间分歧披露**：deai_gate 在词级层与文体层方向显著矛盾（差 ≥30）时输出分歧说明（改写稿/语域混合常见）。
- **安全与行为声明节**：主动声明并可自主复核的本地运行/零上传/零凭证/无持久化承诺（平台审核趋势对齐）。
- **指纹新鲜度二轮**：qwen3.8 补齐均衡采样（35 篇）后无低误报模式过门槛——如实不入册（与 deepseek-v4 同处置）；kimi-k3 维持入册。

## v3.7.0 更新内容

- **篇章结构启发层（L12）**：新增自媒体式篇章级 AI 腔检测——八组模式（钩子/反转/口号/互动引导/排比三连/设问自答/口播收尾/情绪渲染）；≥2 组独立命中时按密度计分（8×组数+命中数，封顶 8，总封顶 30），单组命中仅记录不加分（学术零误伤），命中明细进报告。修复句层特征盲区：纯篇章结构文本此前仅得 21-32/低风险，现进入复核带；学术语料回归 AUROC 0.9022 逐位不变、零误伤。
- **FAQ 专节（评测驱动：C 维"缺少集中的常见问题解答章节"）**：10 条高频问题集中化——短文本为何不判定、医学文本为何偏高、监督层安装与确认、degraded_mode 含义、与知网/万方不可互换、层解析失败兜底、edit_extent 定位、英文支持边界、标识合规用法。
- **各脚本速查表（C 维"脚本用法说明可以更详细"）**：8 个入口的作用/关键参数/输出一表通览。
- **极端情况报错清晰化（R 维）**：style_distance 对无句边界/无正文段落场景给出具体原因与建议，替代原"文本过短"笼统提示。

## v3.6.0 更新内容

- **学术诚信护栏**：每份报告新增 `integrity_notice` 字段/提示行；新增「学术诚信」专节；定位明示——作者自查与写作质量改进、按规披露，不用于规避检测。
- **文档按平台政策加固**：英文文档（ClawHub 读取面）以质量口径措辞替换规避式表述；中文文档口径一致。

## v3.5.0 更新内容

- **降级模式披露（诚实工程）**：`ai_detector.py` 在监督层缺席/被 `PP_NO_SUP=1` 关闭/语言门控跳过时，JSON 与文本输出均带 `degraded_mode` + `degraded_notice`，并附医学语域高估警示（含留出集真实数字）。
- **铁律 2 落地**：不足 100 字的文本不再输出风险判定（`risk=unknown` + 提示）；此前只写在文档里、代码未实现——本版修复。`quality_report.py` 对短文本显示"无法判定"而非误导性的绿色。
- **`scripts/pp_doctor.py` 环境自检**：数据完整性、脚本可编译、可选依赖、模型在位与可加载、短文本/长文本/确定性探针、deai_gate 守卫，一条命令回答"能不能跑、跑的哪档"。
- **`deai_gate.py` 用法守卫与兜底闭环**：`--help`/缺失文件不再被当成文件名误跑门禁；层超时被捕获（中性 50）；翻译腔层解析失败改走中性 50 分而非 0 分（不再把垃圾输入推向 pass 带）；术语层失败不再把 Traceback 塞进 note。
- **中文 Windows 编码加固**：全部入口强制 UTF-8 输出并容错非 UTF-8（如 GBK）输入文件——zh-CN 默认控制台不再崩溃（多专家对抗测试发现）。
- 双语文档按诚实口径重建；触发词扩容（AI率/降AI/查AI率/论文AI率/降低AI率…）。
