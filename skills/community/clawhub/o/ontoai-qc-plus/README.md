# ontoAI Quality Inspector (ontoAI 质检官)

> ## The Final Gate Before Delivery ｜ 交付前最后一道关

Factory-grade quality inspection for AI-generated artifacts. **It does not ask "was this written by AI?" — it asks "can this be delivered?"**

Covers 8 modality categories and 52 artifact types: text, code, data, documents, images, web UI, audio/video, and combined artifacts.
Outputs a four-tier graded QC report: **Must Fix / Should Fix / Unverified / Passed**.

[中文说明 → README.zh-CN.md](README.zh-CN.md)

---

## Why It Exists

A generating AI cannot catch its own errors — it is steeped in its own retrieval context and remembers "why I wrote it this way," so a fabricated quote "looks true" within its context.

> **Generation writes forward; inspection reads backward. The same model cannot do both well in the same conversational context.**

The real-world cost: a book about how AI destroys truth was itself found to contain 6+ fabricated quotes; a $300 university textbook reportedly printed ChatGPT's own words — "If you'd like, I can also explain…" — in its body text (viral screenshots reported in May 2026; wording varies by source).

---

## Core Design

| Design | Notes |
|---|---|
| **Four iron rules** | Report only, never edit · Never fabricate · Language-driven rule loading · Under-report rather than over-report |
| **Independent-invocation constraints** | Read the artifact, never the generation process · Start from suspicion · Facts verified externally |
| **Six universal dimensions** | Residue · Factual integrity · Consistency · Completeness · Compliance · Fitness-for-purpose |
| **Impact model** | Impact = Exposure × Severity × Certainty |
| **Four-tier report** | 🔴 Must Fix (≤5 items, each with its consequence) ｜ 🟡 Should Fix ｜ ⚪ Unverified ｜ ✅ Passed |
| **Seven scenarios** | Publishing / public release / marketing / bidding / launch / academic / internal — exposure drives strictness |
| **Five noise-control rules** | Certainty threshold · Must-Fix quota ≤5 · Consequence-driven · Style preferences banned · Passed items mandatory |
| **Conflict arbitration ladder** | One excerpt hit by multiple rules yields one finding: tier → harm → coverage → structure>vocabulary |
| **Visual engine** | 9-grid enumeration → three-element evidence → verdict; anchor alignment for cross-modal contradictions; no external vision tools needed |
| **Three report-format rules** | Group by tier (one table per tier) · Counts first (overview + per-dimension distribution) · Tables first (flat listing forbidden) |
| **Four report layouts** | Single template `assets/report.html`; switch via `DATA.style`: A Official Inspection Report · B Third-Party Lab · C Modern Charts · D Academic/Publishing. **Double-clicking the HTML shows a floating style switcher** (4 buttons + collapse) — no parameters needed; `?formal=1` hides it for clean delivery, and it never appears in printed/PDF output |
| **Self-QC (dogfooding)** | Inspected itself in **2 independent-session full rounds** (v1.4.1, v1.4.2); all findings repaired in the next release — real reports included in [`evals/qc-reports/`](evals/qc-reports/) |
| **Data evidence anchored** | The residue rule-library dataset completed a platform data-evidence deposit **before open-sourcing** (No. `CZ20260215641694`, content hash + timestamp anchored 2026-10-11, 数据通 data-IP platform) |
| **HTML / PDF dual form** | HTML is a single offline file; PDF is produced by `assets/make-pdf.js` using local Edge/Chrome headless printing — no third-party dependencies |
| **Bilingual artifacts & reports** | Chinese rule pack (RZ-xx) + English rule pack (RZE-xx) loaded by artifact language; report UI localizes via `DATA.lang` (≈120 strings) |

---

## Installation

Copy into your agent's skill directory:

```bash
# WorkBuddy
cp -r ontoAI-qc ~/.workbuddy/skills/

# Claude Code
cp -r ontoAI-qc ~/.claude/skills/

# Codex
cp -r ontoAI-qc ~/.codex/skills/
```

Restart your agent to take effect.

---

## Usage

### Trigger phrases

> QC this ｜ quality check ｜ ontoAI QC ｜ pre-delivery check ｜ factory check
> can I deliver this ｜ can I ship this ｜ check this for problems ｜ is this ready to publish

### Examples

```
QC this product launch draft; scenario: public release
```

```
Run the inspection on everything under /code
```

```
Can I send this deck to the client? Check it.
```

### Specifying a scenario (optional)

If unspecified, defaults to the "public release" preset (strictest). Naming the scenario yields sharper tiering:

```
This is an internal weekly report — QC it.
```

---

## Language Support

| Layer | Chinese artifacts | English artifacts |
|---|---|---|
| Residue rule pack | `references/rules-residue-zh.md` (RZ-xx, 32 rules — written in Chinese by design) | `references/rules-residue-en.md` (RZE-xx, 30 rules) |
| Compliance | L1 Chinese Advertising Law superlatives | L7 FTC truth-in-advertising superlatives |
| L2–L4 (secrets/privacy/copyright) | language-agnostic regex | language-agnostic regex |
| Report UI chrome | `DATA.lang: "zh"` (default) | `DATA.lang: "en"` (≈120 localized strings, zero residual Chinese, verified) |
| Agent-facing docs | `docs/SKILL.zh-CN.md` (mirror) | `SKILL.md` (primary) |
| Mixed CN/EN artifacts | both packs in parallel, findings reported separately | same |

---

## Directory Structure

```
ontoAI-qc/
├── SKILL.md                      Main skill file (8-step workflow + iron rules + modality routing) — English primary
├── README.md                     This file (English primary)
├── README.zh-CN.md               Chinese mirror
├── CHANGELOG.md                  Release notes (English primary)
├── LICENSE                       Commercial EULA (proprietary, paid product)
├── requirements.txt              Python deps for verify-samples.py (PyMuPDF)
├── ontoAI_512x512.png            Skill icon
├── references/
│   ├── rules-residue-zh.md       L1 Chinese residue rule pack (32 rules + protection boundaries + arbitration ladder; Chinese by design)
│   ├── rules-residue-en.md       English residue rule pack (RZE-xx, 30 rules)
│   ├── dimensions.md             6 universal dimensions + 8 modality-specific dimensions
│   ├── multimodal-engine.md      Visual & cross-modal inspection engine (E 9-grid + H anchor alignment)
│   ├── scenarios.md              7 scenario presets and strictness levels
│   ├── compliance.md             Compliance checks (L1 CN ad law / L2 secrets / L3 privacy / L4 copyright / L5 industry claims / L6 sensitive / L7 FTC)
│   ├── artifact-types.md         Inspection config for 52 artifact types
│   ├── report-template.md        Four-tier report template & output contract
│   └── scoring.md                Impact model and four-tier verdicts
├── assets/
│   ├── report.html               Report template (4 layouts in one file; switch via DATA.style; bilingual UI via DATA.lang)
│   ├── make-pdf.js               HTML → PDF generator (uses local Edge/Chrome headless print)
│   └── gen-samples.js            Sample regeneration script (4 Chinese + 1 English)
├── docs/                         Chinese mirrors of primary docs (non-normative)
│   ├── SKILL.zh-CN.md
│   ├── report-template.zh-CN.md
│   └── compliance.zh-CN.md
├── verify-samples.py             PDF contract verification (bitmap Type3 = 0, emoji = 0, █ = 0, EN chrome Chinese-free)
└── evals/
    ├── cases.md                  Test case set (SF/SNF/TC, 37 cases)
    ├── selftest-demo.md          Self-test demo (Markdown-edition real output)
    ├── selftest-report.html      Self-test report sample (Style C; open in browser)
    ├── selftest-report.pdf       Self-test report sample (PDF)
    ├── qc-reports/               **Real self-QC reports** (2 independent-session rounds; findings all fixed — see its README)
    └── samples/                  Layout samples (.html + .pdf each), incl. style-a-en (English chrome)
```

### Report layouts

| Layout | `DATA.style` | Use for |
|---|:--:|---|
| A · Official Inspection Report | `"a"` default | Formal external delivery, client submission, archival (A4 official style; most stable) |
| B · Third-Party Lab | `"b"` | Commissioned inspection; institutional neutrality |
| C · Modern Charts | `"c"` | On-screen reading, quick internal review |
| D · Academic / Publishing | `"d"` | Books, papers, publication proofing |

**PDF output**: `node assets/make-pdf.js <input.html> [output.pdf]`
→ uses local Edge/Chrome headless printing; no puppeteer/wkhtmltopdf dependency; works offline.
Fallback without a browser: open the HTML → Ctrl+P → Save as PDF → enable "Background graphics".

**Regenerating samples** after editing the template: `node assets/gen-samples.js`, then verify with `python verify-samples.py` (needs PyMuPDF: `pip install -r requirements.txt`).

---

## License

Released under the [Commercial End User License](LICENSE) — Copyright (c) 2026 天津市微数人工智能科技有限责任公司 (Tianjin Weishu Artificial Intelligence Technology Co., Ltd.). All rights reserved. This is proprietary, paid software; redistribution, resale, or repackaging without written consent is prohibited.

## How It Differs From Similar Projects

| | Similar projects (humanizer / no-ai-slop / deslop etc.) | ontoAI Quality Inspector |
|---|---|---|
| Modality coverage | 99% text-only | 8 categories, 52 types — incl. images, code, data, combined artifacts |
| What it checks | Language style (does it look good) | Facts, common sense, logic, compliance (is it right) |
| Output | Rewritten text | Four-tier graded QC report + verdict |
| Edits? | Rewrites directly | **Report only**; edits require confirmation |
| Languages | Mostly English (Chinese versions are translations) | Bilingual rule packs rebuilt for each language's AI patterns |
| Combined artifacts | Unsupported | **Cross-modal contradiction detection** |

**In one line**: competitors manage "does it look good"; we manage "can it be delivered."

---

## Adjudication Skeleton Sources

The **method skeleton** draws on these open-source projects; all rules and lexicons were rebuilt natively for each language context, not translated across:

- [qu-ai-wei](https://github.com/LifelongLazyLearner/qu-ai-wei) (five-part pattern method: skeleton/trigger/protection/action/rescan)
- [Humanizer-zh](https://github.com/op7418/Humanizer-zh) (preservation boundaries and false-positive guards)
- [no-ai-slop](https://github.com/petergyang/no-ai-slop) (detect-only output contract)
- [ai-slop-detector-skill](https://github.com/asabirov/ai-slop-detector-skill) (rule grading, density gating, severity mapping)
- [kill-ai-slop](https://github.com/yetone/kill-ai-slop) (visual trope checklist and false positives)
- [shuorenhua](https://github.com/MrGeDiao/shuorenhua) (scenario routing and test-case format)
- [human-writing](https://github.com/KKKKhazix/human-writing) (five concreteness tests)
- [ai-office-director-skill](https://github.com/qierkang/ai-office-director-skill) (Office-file editability contract)

Local indexes of the referenced projects are archived separately with development materials and are **not** distributed with this skill package (this package contains no third-party source text).

---

## Release Notes

See [CHANGELOG.md](CHANGELOG.md).

---

**Publisher / Copyright**: 天津市微数人工智能科技有限责任公司 (Tianjin Weishu Artificial Intelligence Technology Co., Ltd.)

Version 1.4.3 | 2026-10-11 | English-primary edition
