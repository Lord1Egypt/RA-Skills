# QC Report Template & Output Contract

Version 1.4.0 | 2026-10-11

---

## Output Contract (four elements; all mandatory)

Borrowed from the detect-only pattern, every finding must contain:

| # | Element | Requirement |
|:--:|---|---|
| 1 | **Named rule** | Must cite a named rule code from this skill (e.g. RZ-01, RZE-07, D2.4, C1). **Unnamed vague accusations are invalid** |
| 2 | **Verbatim excerpt** | Must give a specific location (page/line/section) + verbatim excerpt |
| 3 | **Proposed fix** | State how to fix (or state "requires user input") |
| 4 | **Consequence of not fixing** | Must-Fix items only. No consequence = doesn't belong in Must Fix |

**Three hard prohibitions**:

- ❌ **No rewriting** — the report stage never touches the original; edits require user confirmation
- ❌ **No author attribution** — never judge "was this written by AI"; only judge "can this be delivered"
- ❌ **No fabrication** — no adding numbers, quotes, or cases

---

## ★ Three Report Format Rules (mandatory since v1.2)

> In a flat item-by-item report, the user must read 15 entries to see the whole picture. **Overview first, details second.**

| # | Rule | Notes |
|:--:|---|---|
| **1** | **Group by tier** | Issues in the same tier are **grouped into one table** — never listed flat. 🔴 one table, 🟡 one table, ⚪ one table, ✅ one table |
| **2** | **Counts first** | The report's **first screen** must show per-tier **counts** plus the per-dimension distribution. The user should know "how many problems, where they cluster" without reading details |
| **3** | **Tables first** | Details always in **tables**, one row per item. Only Must-Fix items may append a "consequence of not fixing" note below the table |

**Bar chart (plain text; renders in any Markdown environment)**:

```
bar length = round(tier count / max tier count × 12), minimum 1 █
```

Example: Must Fix 2 / Should Fix 4 / Unverified 1 → max 4 → Must Fix `██████` (6), Should Fix `████████████` (12), Unverified `███` (3)

> **Count consistency (computable, mandatory)**: every count shown must be derivable from the tables beneath it — `Passed = row count of the Passed table`, `Total = Must + Should + Unverified + Passed`. A mismatched count is itself a consistency defect and has caused real findings in this project's own QC history.

> **⚠️ When rendering to HTML/PDF, do NOT copy `█` or emoji verbatim** (a pit we hit ourselves):
> - `█` character bars become **solid black blocks** in the HTML→PDF print pipeline (especially when one tier far exceeds the baseline and its bar is stretched); HTML/PDF editions must use **CSS bars** instead: `<span class="bar"><i style="width:…%"></i></span>`.
> - Emoji (🔴🟡⚪✅) degrade to **bitmap glyphs** in PDF and blur when zoomed; use **CSS dots** instead (the `dotEmoji()` helper emits `<span>` dots).
> - **Never apply `font-weight:700` to fonts without true bold** (Songti/Heiti/FangSong etc.): the browser synthesizes bold and stores it as a **Type3 bitmap** → the whole paragraph blurs. For emphasis, either use a font with true bold (Microsoft YaHei) or use color/borders instead of bolding.
> - All of the above are already built into `assets/report.html`; do not regress when editing the template. Verification: the PDF's **bitmap Type3 count must be 0**.

---

## Master Template (Markdown)

````markdown
# ontoAI Quality Inspector · QC Report

| | |
|---|---|
| **Artifact** | <filename or description> |
| **Modality** | <A–H, multiple allowed> | **Scenario** <S1–S7> | **Rule level** <RL1–RL4 · L1–L7> |
| **Verdict** | <🟢 Ship / 🔵 Ship after minor tweaks / 🟡 Ship after revisions / 🔴 Recommend redo> |

## 1. Overview

| Tier | Count | Distribution | Meaning | What you should do |
|---|:--:|---|---|---|
| 🔴 Must Fix | 2 | `██████` | Do not ship unfixed | Fix, then ship |
| 🟡 Should Fix | 4 | `████████████` | Better fixed; shippable as-is | Optional |
| ⚪ Unverified | 1 | `███` | Beyond my judgment | Needs your confirmation |
| ✅ Passed | 6 | — | Inspected, no issues | — |
| **Total** | **13** | | | |

## 2. Distribution (by dimension)

| Dimension | 🔴 | 🟡 | ⚪ | Subtotal | Distribution |
|---|:--:|:--:|:--:|:--:|---|
| Residue D1 | 2 | 3 | 0 | 5 | `████████████` |
| Factual integrity D2 | 0 | 0 | 1 | 1 | `██` |
| Consistency D3 | 0 | 0 | 0 | 0 | — |
| Completeness D4 | 0 | 0 | 0 | 0 | — |
| Compliance D5 | 0 | 0 | 0 | 0 | — |
| Fitness D6 | 0 | 1 | 0 | 1 | `██` |
| **Total** | **2** | **4** | **1** | **7** | |

> This table answers "where do the problems cluster" — in this example, **Residue**: controllable formatting issues, not factual defects.

## 3. 🔴 Must Fix (2) — do not ship unfixed

| # | Location | Issue | Rule | Excerpt | Consequence of not fixing | How to fix |
|:--:|---|---|---|---|---|---|
| 1 | Final paragraph | Dialogue tail residue | RZ-01 | "需要我帮你生成其他版本吗？" | Readers spot AI output instantly; credibility of the whole piece drops to zero; media and clients return it | Delete the sentence |
| 2 | Paragraph 2 | Unfilled placeholder | RZ-03 | "缩短至 [待补充] 分钟" | Brackets in a public release is a major release incident, and this metric is the core selling point | Fill in the measured value (**I will not fill it in for you**) |

## 4. 🟡 Should Fix (4) — better fixed; shippable as-is

| # | Location | Issue | Rule | Advice |
|:--:|---|---|---|---|
| 1 | Paragraph 1 | Grand-context opener | RZ-12 | Delete; no substantive connection to the body |
| 2 | Paragraph 1 | Symmetric skeleton | RZ-15 | Rewrite as plain statement of fact |
| 3 | Paragraphs 1–2 | Two rule-of-three triads | RZ-16 | Keep the three content items, drop the parallel shell |
| 4 | End of paragraph 2 | Unsupported uplift | RZ-13 | Delete; no independent information |

## 5. ⚪ Unverified (1) — beyond my judgment; please confirm

| # | Location | Question | Why I cannot verify | How to treat until confirmed |
|:--:|---|---|---|---|
| 1 | Paragraph 2 | "据行业研究表明…提升显著" cited without source | No matching study found; source and magnitude unverifiable | Treat as unsourced: add a real citation or delete |

## 6. ✅ Passed (6 items) — these I checked

| Dimension | Check & conclusion | Result |
|---|---|:--:|
| Residue | No prompt residue, no AI self-reference, no marker leakage | ✅ |
| Factual integrity | The 60% and 45% figures are internally consistent | ✅ |
| Consistency | Terminology unified; no person/voice shifts | ✅ |
| Completeness | Structure complete; no truncation, no empty sections | ✅ |
| Compliance | No superlatives, no leaked secrets, no private data | ✅ |
| Fitness | Length fits the press-release spec | ✅ |

## 7. Next step

> Shall I apply the Must-Fix revisions? (Only these 2 spots; nothing else touched. The placeholder value must come from you.)
````

---

## Full Example

````markdown
# ontoAI Quality Inspector · QC Report

| | |
|---|---|
| **Artifact** | 2026Q3-product-launch.docx |
| **Modality** | H1 text+image / W1 Word | **Scenario** S2 public release | **Rule level** RL1–RL3 · L1–L2 |
| **Verdict** | 🟡 Ship after revisions |

## 1. Overview

| Tier | Count | Distribution | Meaning | What you should do |
|---|:--:|---|---|---|
| 🔴 Must Fix | 2 | `████████` | Do not ship unfixed | Fix, then ship |
| 🟡 Should Fix | 3 | `████████████` | Better fixed; shippable as-is | Optional |
| ⚪ Unverified | 1 | `████` | Beyond my judgment | Needs your confirmation |
| ✅ Passed | 7 | — | Inspected, no issues | — |
| **Total** | **13** | | | |

## 2. Distribution (by dimension)

| Dimension | 🔴 | 🟡 | ⚪ | Subtotal | Distribution |
|---|:--:|:--:|:--:|:--:|---|
| Residue D1 | 1 | 2 | 0 | 3 | `████████████` |
| Factual integrity D2 | 1 | 0 | 1 | 2 | `████████` |
| Consistency D3 | 0 | 1 | 0 | 1 | `████` |
| Completeness D4 | 0 | 0 | 0 | 0 | — |
| Compliance D5 | 0 | 0 | 0 | 0 | — |
| Fitness D6 | 0 | 0 | 0 | 0 | — |
| **Total** | **2** | **3** | **1** | **6** | |

## 3. 🔴 Must Fix (2) — do not ship unfixed

| # | Location | Issue | Rule | Excerpt | Consequence of not fixing | How to fix |
|:--:|---|---|---|---|---|---|
| 1 | Final paragraph, p.8 | Dialogue tail residue | RZ-01 | "需要我帮你生成其他版本吗？" | Readers spot AI output instantly; the whole piece's credibility drops to zero — equivalent to admitting "no human review"; clients or publishers return it outright | Delete the sentence; if a closer is needed, write a substantive one |
| 2 | Paragraph 2, p.3 | Uncited quotation | D2.4 | "据 2025 年行业统计，市场规模增长了 37%" | Unanswerable under questioning; in bidding or publishing contexts this is a factual error and may constitute misrepresentation | Add a real source (publisher + year + page), or delete and restate qualitatively |

## 4. 🟡 Should Fix (3) — better fixed; shippable as-is

| # | Location | Issue | Rule | Advice |
|:--:|---|---|---|---|
| 1 | Page 2 | Three consecutive rule-of-three triads | RZ-16 | Merge into substantive description |
| 2 | Page 4 | Two buzzwords: "赋能", "闭环" | RZ-17 | Replace with concrete actions |
| 3 | Figure 3 | Inconsistent with body's framing | D3.7 | Unify to "同比" (year-over-year) |

## 5. ⚪ Unverified (1) — beyond my judgment; please confirm

| # | Location | Question | Why I cannot verify | How to treat until confirmed |
|:--:|---|---|---|---|
| 1 | Page 5 | Cites "XX Industry White Paper" | Report not found; existence unverifiable | Treat as unusable; this item clears once you confirm it exists |

## 6. ✅ Passed (7 items) — these I checked

| Dimension | Check & conclusion | Result |
|---|---|:--:|
| Residue | No prompt residue, no placeholders, no AI self-reference (except the one above) | ✅ |
| Factual integrity | All 23 figures cross-checked consistent (except the one above) | ✅ |
| Consistency | Terminology unified throughout; no person/voice shifts | ✅ |
| Completeness | All sections present, no truncation, all figure captions present | ✅ |
| Compliance | No superlatives, no leaked secrets, no private data | ✅ |
| Fitness | Length fits the WeChat-official-account spec; image sizes compliant | ✅ |
| **Cross-modal** | **All 5 images match the body text (anchor alignment 11/11)** | ✅ |

## 7. Next step

> Shall I apply the Must-Fix revisions? (Only these 2 spots; nothing else touched.)
````

---

## "Recommend Redo" Report (Must-Fix > 5 items)

Do not expand detail tables — **when the whole fails, itemized detail is meaningless**.

````markdown
| | |
|---|---|
| **Artifact** | XXX |
| **Verdict** | 🔴 **Recommend redo** |

## 1. Overview

| Tier | Count | Distribution |
|---|:--:|---|
| 🔴 Must Fix | 9 | `████████████` |
| 🟡 Should Fix | 4 | `█████` |
| ⚪ Unverified | 2 | `███` |
| ✅ Passed | 6 | — |

> 9 Must-Fix items exceed the patching threshold (5). The problem is not "fix a bit" but "nothing was verified overall."

## 2. Top 3 by impact score

| # | Location | Issue | Rule | Impact |
|:--:|---|---|---|:--:|
| 1 | Chapter 3 | Fabricated quote | D2.3 | 25 |
| 2 | Throughout | Missing data sources | D2.4 | 20 |
| 3 | Chapter 5 | Figure/text number contradiction | H2 | 20 |

## 3. Redo direction

> First settle the data sources and citation list, then rewrite chapters 2–4. Patching item by item costs more than redoing.
````

---

## Minimal Report (no issues)

````markdown
# ontoAI Quality Inspector · QC Report

| | |
|---|---|
| **Artifact** | weekly-1010.md | **Modality** A3 text | **Scenario** S7 internal doc |
| **Verdict** | 🟢 Ship |

| Tier | Count |
|---|:--:|
| 🔴 Must Fix | 0 |
| 🟡 Should Fix | 0 |
| ⚪ Unverified | 0 |
| ✅ Passed | 6 |

| Dimension | Check & conclusion | Result |
|---|---|:--:|
| Residue | No dialogue tails, no placeholders | ✅ |
| Completeness | No truncation, no empty sections | ✅ |
| Consistency | No contradictions | ✅ |
| Factual integrity | 3 figures consistent | ✅ |
| Compliance | Nothing abnormal | ✅ |
| Fitness | Fits internal-doc spec | ✅ |

Not activated: L2–L4 style rules (internal-doc scenario).
````

---

## Layout & Delivery Forms (HTML / PDF)

Generate a report file when the user **explicitly asks** for "a report file / let me see charts / export / a PDF", or when the artifact is complex
(**≥8 findings, multi-modal, or batch files**).

### Four Layouts (same DATA; switch by one field)

**There is only one template**: `assets/report.html`. All four layouts' CSS and render functions live inside the file,
selected by the `DATA.style` field — no need to maintain four files.

| Layout | `DATA.style` | Character | Use for |
|---|---|---|---|
| **A · Official Inspection Report** | `"a"` (default) | Official-document style: serif body, red header line, conclusion box, seal slot, prepared/reviewed/approved signature rows, declaration clauses | Formal external delivery, client submission, archival |
| **B · Third-Party Lab** | `"b"` | Laboratory style: dark-blue table headers, verdict badge, numbered sections, declaration clauses | Commissioned inspection; conveying institutional neutrality |
| **C · Modern Charts** | `"c"` | SaaS style: count cards, bar charts, donut chart | On-screen reading, quick internal review |
| **D · Academic / Publishing** | `"d"` | Journal style: serif, three-line tables, table titles & notes, abstract block | Books, papers, publication proofing |

**Switching** (priority high to low):

1. URL parameter: `report.html?style=b` (temporary preview; file untouched)
2. The `DATA.style` field (for formal reports)
3. **Quick switcher (default)**: double-clicking the HTML shows a floating style bar at the top-left — 4 style buttons + a collapse button (collapsing restores the clean formal look). Click to switch, no typing needed.
4. Full comparison: `report.html?picker=1` (titled bar with per-style descriptions and print tips; optional)
5. Clean formal delivery: `report.html?formal=1` (hides every UI shell — what a recipient should see)

The switcher never appears in printed/PDF output (`@media print` strips all shell elements), so double-click preview and formal delivery share one file safely.

**Default strategy**: the Markdown report is the primary deliverable; when a file is requested — **on-screen reading → Style C; print/PDF → Style A**
(A is A4 official-document layout: the most stable and the most "official, rigorous" for external delivery).

**Four rendered samples**: `evals/samples/` (each with .html and .pdf; open in a browser to compare).
After editing `report.html`, run `node assets/gen-samples.js` to regenerate all HTML+PDF samples in one go (the script deletes the old PDF before printing, to avoid mistaking a stale file for success).

### Two Delivery Forms

| Form | Notes |
|---|---|
| **HTML** | Single file, zero external dependencies, works offline. All charts rendered with native CSS — no external chart libraries |
| **PDF** | Printed from the HTML edition, for archiving, sending, and stamping. The HTML embeds `@page A4` and background-preservation rules |

**PDF generation**: `node assets/make-pdf.js <input.html> [output.pdf]`
Uses the local Edge/Chrome headless print pipeline — **no puppeteer / wkhtmltopdf dependency**, works offline.
Fallback without a browser: open the HTML → Ctrl+P → destination "Save as PDF" → enable "Background graphics".

> **Hard constraint**: the HTML, PDF, and Markdown editions **must carry identical content**. Layout is presentation only; findings must never be added or dropped.

### Language Switching (DATA.lang = zh / en)

The report UI supports a Chinese/English chrome switch, controlled by `DATA.lang` (`"zh"` default, `"en"` for English chrome).

- **Scope**: switches only the report's own **UI labels** — page title, layout headline, section headings, table column headers (Location/Issue/Rule/Excerpt/Dimension/Result/Count/Distribution/Tier/Meaning/Handling…), the four-tier legend phrases ("do not ship unfixed" / "better fixed" / "beyond my judgment" / "inspected, no issues"…), declaration clauses, signature rows, typographic punctuation (`。「」｜` → `"` `.` `|`), plus Style B's English pass-rate line — **about 120 strings**. **The artifact's own text, verbatim excerpts (`quote`), rule codes (RZ-xx / RZE-xx), and dimension names stay in their original language** — Chinese artifacts get Chinese reports, English artifacts get English reports; no translation migration (avoids introducing new facts / changing meaning).
- **Implementation**: `assets/report.html` uses a **render-then-localize** pattern — the 4 skin render functions stay untouched; the assembled HTML string passes through `localize()` inside `show()` for longest-match substitution (`ZH2EN` dictionary + sorted `split/join`). Zero risk; no skin logic rewritten.
- **Font switching**: in `en` mode `<html>` gets the `.lang-en` class — headings/emphasis switch to **Arial / Georgia** (both with true bold, avoiding synthetic-bold Type3 bitmap degradation); Latin body text uses Arial with a `Songti SC / SimSun` CJK fallback so any embedded Chinese doesn't garble.
- **PDF verification (extra hard constraints in English mode)**: English Latin fonts must be **vector Type0 (embedded subsets)**, never falling back to synthetic-bold Type3 bitmaps; verification must confirm the English PDF has **bitmap Type3 count = 0** and **no residual Chinese in UI labels** (Product Inspected / Inspection Conclusion / Total / Must Fix…).
- **English sample**: `evals/samples/style-a-en.html` / `.pdf` (Style-A official report · English UI), generated together by `node assets/gen-samples.js`.

### Usage

Replace only the `DATA` object in the top `<script>` of the file; **change nothing else**.
`DATA.publisher` takes the publisher/copyright holder's full name (default: 天津市微数人工智能科技有限责任公司).

```js
const DATA = {
  publisher: "天津市微数人工智能科技有限责任公司",
  lang: "zh",                           // Report UI language: "zh" Chinese chrome (default) / "en" English chrome
  reportNo: "ontoAI-QC-20261011-001",   // Report number; shown in styles A/B/D
  date: "2026-10-11",                   // Inspection date
  basis: "ontoAI QC Specification v1.2 · Universal dimensions D1–D6",  // Inspection basis; shown in A/B/D
  product: "2026Q3-product-launch.docx",
  modality: "H1 text+image / W1 Word",
  scenario: "S2 public release",
  ruleLevel: "RL1–RL3 · L1–L2",
  verdict: { code: "modify", label: "修改后放行", emoji: "🟡",
             note: "Ship after fixing the 2 Must-Fix items" },
  // Four tier counts (overview and charts computed automatically)
  counts: { must: 2, should: 3, doubt: 1, pass: 7 },
  // Per-dimension cross stats (stacked bars rendered automatically)
  byDimension: [
    { dim: "残留度 D1", must: 1, should: 2, doubt: 0 },
    { dim: "真实性 D2", must: 1, should: 0, doubt: 1 },
    { dim: "一致性 D3", must: 0, should: 1, doubt: 0 },
    { dim: "完整性 D4", must: 0, should: 0, doubt: 0 },
    { dim: "合规性 D5", must: 0, should: 0, doubt: 0 },
    { dim: "适配性 D6", must: 0, should: 0, doubt: 0 }
  ],
  must:   [{ no:1, loc:"第 8 页末段", issue:"结尾残留对话尾巴", rule:"RZ-01",
             quote:"需要我帮你生成其他版本吗？",
             consequence:"读者一眼看出是 AI 输出，全文可信度归零",
             fix:"删除该句" }],
  should: [{ no:1, loc:"第 2 页", issue:"三连排比", rule:"RZ-16", advice:"合并为实质描述" }],
  doubt:  [{ no:1, loc:"第 5 页", point:"《XX 产业白皮书》未检索到",
             reason:"无法确认是否真实存在", action:"按不可用处理" }],
  passed: [{ dim:"真实性", item:"全文 23 处数字交叉核对一致" }],
  next:   "是否由我执行必改项的修改？（只改这 2 处，其余不动）"
};
```

Note: the values inside `must` / `should` / `doubt` / `passed` / `verdict.label` are **artifact content** — keep them in the artifact's language (Chinese artifact → Chinese values; English artifact → English values). Only the chrome around them is localized by `DATA.lang`.

**Chart elements**: ① tier count cards ② tier distribution horizontal bars ③ dimension × tier stacked bars ④ pass-rate donut.
All rendered with native CSS — **no external chart libraries** (guarantees offline use).

> **Note**: the HTML report and the Markdown report **must carry identical content**; HTML is presentation only — findings must never be added or dropped.

---

## Report-Writing Negative List

| ❌ Banned | Why | ✅ Instead |
|---|---|---|
| Flat item-by-item listing ([1][2][3]…) | Takes 15 reads to see the whole picture | Group same-tier items into one table, one row each |
| Details without counts | User can't tell how many problems | First screen shows overview + distribution tables |
| "Feels very AI" | Cannot guide a fix | "Paragraph 3 contains a rule-of-three triad (RZ-16); suggest merging" |
| "Doesn't read human" | Subjective, unactionable | Point to the concrete excerpt and rule code |
| "Suggest polishing" | Zero information | Give specific location and fix |
| "Might be a problem" | Uncertain | Send to Unverified with the reason it can't be verified |
| "Overall quite good, but…" | Pleasantry | Give the verdict and items directly |
| Self-scores, "73% AI content" | Fake precision | Use impact scores and rule codes; never percentage content |
| 20 Must-Fix items | Nobody will read them | Over 5 → verdict "Recommend redo" |

**A report's value = the user glances once and knows how many problems, where they cluster, and what to do.** A report that fails this is worse than no report.
