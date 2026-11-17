# Changelog

## [2.1.2] - 2026-10-13

### Added (multi-channel distribution & plugin-less payment fallback)

- **402 responses now include `code_url`**: the gateway attaches a WeChat Native scan-to-pay link to every payment-required response, so any environment — including ones without the WeChat Pay plugin (GitHub, ClawHub, …) — can complete payment.
- **Plugin-less QR-payment branch in the contract**: step 3 now branches on plugin availability — with the plugin, use `weixinpay_pay`; without it, **never** give up or ask the user to install anything — render the `code_url` as a QR code so the user can pay the same order by WeChat scan, then resend the request unchanged.
- **Mandatory execution path updated accordingly**: in plugin-less environments the agent must present the code_url QR first; the ban on locally recomputing reports remains unchanged.
- **License upgraded**: LICENSE.md changed from MIT to the Licensor's own commercial End User License (a paid product is no longer published under an open-source license); frontmatter `license: Commercial`.
- Gateway side: when AI pre-order fails, the gateway now degrades to pure code_url scan mode instead of interrupting payment.

## [2.1.1] - 2026-10-12

### Changed (billing switched to the real self-hosted backend)

- **Payment contract now points to the real backend**: the placeholder local-payment description is replaced by the live WeChat Pay X402 gateway at `https://www.ontoagent.net/qc402/api/resource` — a request without an order number returns HTTP 402 (headers `WeixinPay-Required` + `X-Out-Trade-No`); after completing the CNY 1.9 payment via the `weixinpay_pay` plugin (with an availability pre-check: if the plugin is missing/disabled, tell the user explicitly and pause — never fail silently), the agent **resends the original request unchanged** with the `X-Out-Trade-No` header to receive the full QC report. End-to-end verified with a real CNY 1.9 payment (order, callback, fulfillment, idempotency).
- **New `"lang": "en"` request field** for the English edition: the WeChat payment order shows the English product description (ontoAI QC Inspector·Last gate before delivery·…).
- **Payment order description refreshed to the brand copy** (checks AI residue / content errors / logic / compliance), no longer echoing the user's submitted content.

### Fixed (server-side QC rule engine)

- Extended Advertising-Law superlative coverage: range-qualified superlatives such as "全国第一 / 行业第一 / 销量第一" (No.1 nationwide / in the industry / in sales) are now detected (the old rule only matched "第一品牌/名/家").
- Added strong-marketing-signal detection (扫码/加微信/抢购/秒杀/限时/优惠, i.e. scan-QR / add-WeChat / flash-sale style CTAs): prohibited superlatives in customer-facing marketing copy are correctly escalated to 🔴 Must Fix, with zero false positives on legitimate uses ("第一时间 / 第一人称 / 第一季度").

## [2.1.0] - 2026-10-11

### Added (SkillHub Plus edition)

- Rebranded PRO -> Plus for the SkillHub distribution; per-call billing CNY 1.9 (pricing declared in frontmatter, settled by the platform).
- Added SkillHub frontmatter fields (slug/displayName/summary/license/tags/pricing).
- Slimmed package for the SkillHub file-type whitelist (no extensionless files, no nested archives/PDFs; LICENSE -> LICENSE.md, VERSION folded into frontmatter).

# Changelog

All notable changes to **ontoAI Quality Inspector (ontoai-qc)** are documented here.
Format inspired by [Keep a Changelog](https://keepachangelog.com/); versions are dated by release day.

---

## [1.4.3] — 2026-10-11 · Second Independent QC Round Repairs

Second independent-session inspection (candidate for GitHub release): 4 Must-Fix, 4 Should-Fix, 2 Unverified — all adjudicated and repaired.

### Must-Fix repairs

1. **Residue grading renamed L1–L4 → RL1–RL4** in both residue packs (`rules-residue-zh.md`, `rules-residue-en.md`), plus `scenarios.md`, `dimensions.md`, `SKILL.md`, and all `DATA.ruleLevel` examples (`"RL1–RL3 · L1–L2"`) — the third and final instance of the code-collision family: the residue **grading** levels no longer collide with the **compliance** codes L1–L7. Compliance references (Chinese Advertising Law L1) are untouched.
2. **Product-ID vs check-code collision declared** in `artifact-types.md`: the left "product ID" column (A1–H4) is documented as row-localization only, same shape as modality check codes but different meaning; **reports cite check codes only**.
3. **Threshold precedence rule added** to `scoring.md`: dimension rules mandating unconditional Unverified (D2.4 no-source data, RZ-32 S3) **override the impact-score cutoff** — impact < 5 no longer silently passes such findings. `cases.md` TC-02 expectation rewritten accordingly.
4. **Full-Example distribution bars corrected** (6/9/3 → 8/12/4) in `report-template.md` and its Chinese mirror — the example now satisfies the very count-consistency rule v1.4.1 introduced.

### Should-Fix repairs

1. `DATA.verdict.label` wrapped in `PROTECT()` (4 render sites) — the last product field exposed to EN-mode punctuation substitution.
2. `cases.md` SF-02 mis-citation fixed: RZ-07 (markdown-marker leak) cannot hit a plain sentence; now cites RZ-02 only.
3. Phantom `basis` citations ("质检规范 v1.2" / "Spec v1.3") replaced with the real basis: `ontoAI Quality Inspector SKILL.md v1.4.3 · D1–D6` (report.html + gen-samples.js).
4. Both READMEs now link the 8 upstream skeleton-source repositories (URLs extracted from the locally archived indexes, not guessed).

### Unverified resolved

1. PDF hard contract re-run after this round: `verify-samples.py` all green (bitmap Type3 = 0 / emoji = 0 / █ = 0 / EN chrome Chinese-free across 6 PDFs).
2. Chinese mirror `docs/SKILL.zh-CN.md` description wording aligned with the English primary ("overlay-load", not "optional overlay"); mirror otherwise stays frozen per its banner.

### Added (same release)

- **Self-QC reports included**: both real independent-session inspection reports shipped in `evals/qc-reports/` with a versioned index README (round 1 → v1.4.1, Style C HTML; round 2 → v1.4.2, Style A HTML+PDF). Findings kept verbatim for authenticity; each maps to its fix in the corresponding release notes. READMEs also gained a Self-QC (dogfooding) highlight row and bilingual main titles.
- **Data evidence deposit anchored before open-sourcing**: the residue rule-library dataset (RZ-32 + RZE-30 + compliance triggers + 37 cases) completed a data-evidence deposit on the 数据通 data-IP platform — deposit No. `CZ20260215641694`, content hash + timestamp anchored 2026-10-11. Both READMEs carry a "Data evidence anchored" row.

---

## [1.4.2] — 2026-10-11 · Always-Visible Style Switcher

### Changed

- **Report template (`assets/report.html`)**: double-clicking the HTML now shows a floating **quick style switcher** at the top-left — 4 style buttons + a collapse button. Click to switch layouts, no URL parameter typing required. Collapsing restores the clean formal look.
- **New URL mode `?formal=1`**: hides every UI shell for clean formal delivery (previously this was the undocumented default).
- `?picker=1` full comparison mode unchanged.
- Documented all three modes in `references/report-template.md` (EN primary) and its Chinese mirror.

### Fixed

- Switcher (and all preview shells) are stripped from printed/PDF output by `@media print`; verified zero leakage across all 6 sample PDFs.

---

## [1.4.1] — 2026-10-11 · First Independent QC Round Repairs

The package ran its own full pre-delivery inspection in an **independent session** (as its own iron rules require); 5 Must-Fix, 6 Should-Fix, and 3 Unverified items were adjudicated and repaired.

### Must-Fix repairs

1. **Stale code D7 → W7** in `references/scenarios.md` (S6 academic scenario) — a leftover from the v1.2.1 code-collision overhaul; a full-package grep confirmed no other stale codes.
2. **LICENSE added** (MIT; copyright the publisher company) + license declared in both READMEs — without it, the "copy and use" installation instructions were legally self-contradictory for an open-source release.
3. **Passed-count contradictions unified** in `references/report-template.md` (master template 11/7/6 → 6 everywhere; full example 14/7 → 7) and mirrored in the Chinese mirror and the sample DATA (`counts.pass: 14 → 7`). Added an explicit **count-consistency rule** (every count must be computable from the tables beneath it).
4. **L1–L6 → L1–L7** in `dimensions.md` (×2), `artifact-types.md`, and the Chinese compliance mirror — the v1.4.0 FTC layer was invisible to the prefix-convention validators, which would have silently skipped English-artifact FTC checks.
5. **localize() verbatim-quote protection** (`assets/report.html`) — the EN chrome's global punctuation substitution (`。「」｜` → `"."|`) previously rewrote product excerpts too, violating the verbatim-excerpt contract for mixed artifacts. Product fields are now wrapped in `PROTECT()` markers; `localize()` stashes marker content, localizes chrome only, then restores. Unit-tested: quotes containing `。「」｜` and chrome-word collisions pass through byte-identical while chrome still localizes. (The unit test also caught and fixed a fatal `P` naming collision with the pass-count constant that would have broken rendering entirely; `localize()` now reads `DATA.lang` at call time instead of a load-time cache.)

### Should-Fix repairs

6. Both READMEs' directory trees redrawn to the actual v1.4.0 file list (added `rules-residue-en.md`, `gen-samples.js`, `verify-samples.py`, `docs/`, `CHANGELOG.md`, `LICENSE`, `requirements.txt`, icon, selftest PDF); compliance described as 7 categories; install commands unified to the real directory name `ontoAI-qc`.
7. `requirements.txt` added (PyMuPDF) and verification instructions now state the install step.
8. `docs/SKILL.zh-CN.md` banner now states it is frozen at v1.3.0.
9. `rules-residue-en.md` RZE-22 garbled title fixed (虚技术超级lative → 虚技术极限词 tech superlatives).
10. `assets/make-pdf.js`: file URL now encodes each path segment with `encodeURIComponent` (fixes truncation on `#`/`?`/`%` paths; Windows drive colon preserved); headless mode tries `--headless=new` first and falls back to `--headless=old` for older browsers.

### Unverified items handled

11. The "$300 textbook" anecdote now carries "reportedly" (both READMEs) with wording-variance disclosure.
12. L7's legal basis rewritten: **FTC Act §5** as the core authority; 16 CFR Part 255 repositioned as the Endorsement Guides (applicable to endorsement/testimonial-style claims), not as a superlative rule.

### Process hardening

13. SKILL.md step 7 now fixes the **delivery contract**: Markdown edition always; HTML/PDF per conditions; external-release default = Style-A PDF; report chrome language follows the conversation language; one HTML file carries all four layouts.

## [1.4.0] — 2026-10-11 · International (GitHub) Release, English-Primary

1. **SKILL.md converted to the English primary document** — for international distribution; the original Chinese edition is archived at `docs/SKILL.zh-CN.md` (non-normative mirror).
2. **Reference docs converted to English primary** — `references/report-template.md` and `references/compliance.md` are now English-primary documents (Chinese mirrors archived under `docs/`; L1 keeps the Chinese statute citation and Chinese trigger regexes — they govern Chinese artifacts by design).
3. **Rule packs partitioned by artifact language (status formalized)** — `rules-residue-zh.md` (RZ-xx, for Chinese artifacts; kept in Chinese with an English usage header) + `rules-residue-en.md` (RZE-xx, for English artifacts); mixed artifacts load both packs in parallel and report findings separately.
4. **Bilingual README** — this file and the English `README.md` are primary; `README.zh-CN.md` is the Chinese mirror; release notes moved here.
5. **Bilingual report UI (landed across v1.3.x)** — `DATA.lang = "zh"/"en"` switches ≈120 UI strings; English sample `evals/samples/style-a-en.html/.pdf` (zero residual Chinese, pure vector fonts); PDF verification script `verify-samples.py`.
6. Compliance: added **L7 · FTC truth-in-advertising / superlatives** (the English counterpart of L1 Chinese Advertising Law).

## [1.3.x] — 2026-10-11 · Four Layouts, PDF Form, Bilingual Report UI

### [1.3.1/1.3.2] — English-chrome hardening

1. **`ZH2EN` localization table expanded to ≈120 strings** — an early check of only 10 chrome words masked a real gap: 30 Chinese runs survived in the EN PDF (table column headers, four-tier legend phrases, declaration/signature rows, typographic punctuation). All table headers (Location/Issue/Rule/Excerpt/Dimension/Result/Count/Distribution/Tier/Meaning/Handling…), legend phrases, and punctuation (`。「」｜` → `"` `.` `|`) are now localized. Verified: EN sample PDF Chinese residue = **0**.
2. **`<title>` localized** in EN mode.
3. **`verify-samples.py`** — reusable PyMuPDF verification: hard contract bitmap-Type3 = 0 / color-emoji = 0 / `█` = 0 across all samples; EN-specific checks (no residual Chinese, key English labels present, Latin fonts vector Type0).

### [1.3.0] — Four report layouts + PDF delivery

1. **Report layouts expanded from one to four selectable styles** — the single chart style read like an internet product, not a formal report. Built-in styles:
   - **A Official Inspection Report** (default): official-document layout — serif body, red header line, conclusion box, seal slot, prepared/reviewed/approved signature rows, declaration clauses
   - **B Third-Party Lab**: dark-blue headers, verdict badge, numbered sections, declaration clauses
   - **C Modern Charts**: count cards + bar charts + donut chart (the original style)
   - **D Academic / Publishing**: serif, three-line tables, table titles & notes, abstract block
2. **Four styles in one template** — all CSS and render functions live in `assets/report.html`, switched by `DATA.style` (`a`/`b`/`c`/`d`); URL params `?style=b` (preview) and `?picker=1` (side-by-side). One file maintained; one DATA edit updates all four.
3. **PDF delivery form added** — `assets/make-pdf.js` drives local Edge/Chrome headless printing; no puppeteer/wkhtmltopdf; offline; built-in A4 page rules and background preservation. DATA gained `reportNo` / `date` / `basis` fields (shown in styles A/B/D).
4. Four rendered samples in `evals/samples/` (each .html + .pdf); the self-test report regenerated on the new template.

## [1.2.1] — 2026-10-11 · The Inspector Inspects Itself

A full QC pass (independent invocation + suspicion stance) was run on this skill package itself; 5 Must-Fix and 5 Should-Fix findings repaired:

1. **Internal traces removed** — client names in the release notes (2 spots) deleted; full-package scan confirmed no "AI-assisted" declarations, no internal code-name signatures.
2. **Publisher/copyright added** — unified as 天津市微数人工智能科技有限责任公司 (README, SKILL.md metadata, HTML report footer `DATA.publisher`).
3. **Artifact count corrected** — actual count is **52 types** (A15/B8/C5/D5/E6/F5/G4/H4); the previous external figure of 48 was corrected in 6 places.
4. **Code-collision fixed** (a consistency defect that would send execution to the wrong dimension) — compliance codes `C1–C6` → **`L1–L6`**; document codes `D1–D9` → **`W1–W9`**. Universal dimensions remain `D1–D6`; data codes remain `C1–C8`. Both prefix conventions documented at the top of `dimensions.md` and `artifact-types.md`.
5. **Test-case count corrected** — `cases.md` header 36 → 37 cases (v1.2 added TC-09).
6. Should-Fix: report example "passed 11/14 items" mismatched its 7-row table → unified to 7; `artifact-types.md` version synced to 1.2.0; TC-01 severity aligned with `scoring.md`; a README reference to an external dev-workspace path rewritten to be self-contained.

## [1.2.0] — 2026-10-11 · Report Format Overhaul + HTML Chart Edition

1. **Report format redesigned** — the original report listed findings flatly and read tediously. Now:
   - **Group by tier**: same-tier issues in one table each (🔴/🟡/⚪/✅), no flat lists
   - **Counts first**: the first screen shows per-tier counts + per-dimension distribution — one glance yields "how many, where they cluster"
   - **Tables first**: one row per finding; bars rendered as plain-text `█` (any Markdown environment)
2. **HTML chart report added** (`assets/report.html`) — single file, zero dependencies, offline, printable to PDF. Replace only the top `DATA` object. Includes: tier count cards, tier distribution bars, dimension × tier stacked bars, pass-rate donut, four detail tables. **Content must match the Markdown edition**; HTML is presentation only.
3. Self-test samples updated; chart-edition sample produced at `evals/selftest-report.html`.

## [1.1.0] — 2026-10-11 · Arbitration Ladder + Visual Engine

1. **Rule-conflict arbitration ladder** — four-step arbitration (tier → harm → coverage → structure>vocabulary) + a 9-pair common-conflict verdict table, plus a dedicated four-case ruling for RZ-12 × RZ-17 (A/B/C merge into one finding, D reports each). One excerpt yields one reported item; other hits demote to "incidental" — fixing verbose, formulaic reports.
2. **New rule RZ-32: unbased quantification & vague degree adverbs** — "significantly improved", "improved by 40%" with no baseline. Types S1/S2/S3; Must Fix only when the missing element can be named; marketing scenarios hand off to L1 compliance.
3. **Visual & cross-modal inspection engine added** (`references/multimodal-engine.md`) — Category-E 9-grid observation order, five false-positive red lines, visual certainty assignment rules, Category-H anchor-alignment four-step flow. **No external vision tools or specialized detection models needed** — the host model's native multimodal capability is the executor; this engine supplies the adjudication protocol that converges capability into evidence-backed verdicts.
4. Test-case set grown to 36 cases (added unbased quantification, image-text, art-style exemption, rule de-duplication, visual certainty gate).

## [1.0.0] — 2026-10-11 · Initial Complete Release

SKILL.md + 31 Chinese residue rules + 6 universal dimensions + 8 modality dimensions + 7 scenarios + four-tier report + 24 test cases.
