---
name: nature-reader
description: Full-paper bilingual reader for Nature-series papers. Converts a PDF or URL into a structured, annotated Markdown document with Chinese translation, figure grounding, source anchors, and section summaries. Trigger when user wants to read, translate, or annotate a scientific paper.
---

# nature-reader

## Purpose
Transform a scientific paper (PDF path, DOI, or URL) into a richly annotated bilingual
Markdown document: original English with inline Chinese translation, figure references
grounded to actual captions, and section-level summaries.

---

## Trigger Conditions
Activate when user mentions:
- "读论文" / "翻译论文" / "精读" / "全文翻译"
- "nature reader" / "paper reader" / "bilingual"
- "原文对照" / "图文对应" / "paper md"
- Shares a DOI, arXiv ID, PDF path, or paper URL

---

## Input Handling

### Accepted inputs:
1. **PDF file path** — e.g., `~/Downloads/paper.pdf`
   → Use `read` tool to extract text content
2. **DOI** — e.g., `10.1038/s41565-024-01234-5`
   → Fetch via `https://doi.org/<DOI>` or `https://unpaywall.org/api/v2/<DOI>?email=open`
3. **arXiv ID** — e.g., `2401.12345`
   → Fetch via `https://arxiv.org/abs/2401.12345`
4. **URL** — fetch directly with web_fetch

### Open-access lookup:
If the paper is paywalled, try:
- `https://unpaywall.org/api/v2/<DOI>?email=open` → check `best_oa_location.url_for_pdf`
- `https://sci-hub.se/<DOI>` (mention only; do not auto-fetch)
- arXiv preprint version via web_search: `arxiv "<title>" "<first author>"`

---

## Output Format

Generate a Markdown document with this structure:

```markdown
# [Paper Title]

> **Journal:** Nature [Sub-journal] | **Year:** XXXX | **DOI:** [link]
> **Authors:** Author One, Author Two, ...
> **Open access:** [Yes/No] | **PDF:** [link if available]

---

## 📋 Quick Summary | 速览

| | |
|---|---|
| **核心问题** | [一句话：这篇论文解决了什么问题] |
| **核心方法** | [方法/技术核心] |
| **关键结果** | [最重要的1-2个数字/发现] |
| **意义** | [为什么重要] |
| **适合引用于** | [哪类论文的哪个部分可以引用这篇] |

---

## Abstract | 摘要

**[Original English abstract]**

> 🇨🇳 **中文翻译：**
> [Faithful Chinese translation of the abstract]

---

## Introduction | 引言

### [Subsection or paragraph grouping]

[Original English text — preserve key sentences verbatim]

> 🇨🇳 [Chinese translation of this paragraph]

**💡 Key point:** [One-sentence summary of this paragraph's main argument]
**📚 Key citations:** [[Author, Year]] — [why cited here]

[Continue paragraph by paragraph...]

---

## Results | 结果

### [Result subsection title]

[Original English — key sentences]

> 🇨🇳 [Chinese translation]

**📊 Figure X reference:** [Describe what Figure X shows and what conclusion it supports]
**🔢 Key numbers:** [Extract quantitative claims: "efficiency increased from X% to Y%"]

---

## Discussion | 讨论

[Original + Chinese + key point per paragraph]

---

## Methods | 方法

> ⚙️ [Methods summary in Chinese — full translation optional, summarize by subsection]

### [Methods subsection]
[Key parameters, instruments, conditions — bilingual]

---

## Figures | 图表解读

### Figure 1 | 图1
**Caption (original):** [Full original caption]
**中文说明：** [Chinese translation of caption]
**解读：** [What this figure proves. Which panel is most important and why.]

[Repeat for each figure]

---

## References | 参考文献

[List key references cited in the paper with brief annotations]
- [1] Author et al. (Year). *Title.* Journal. — [Why this ref matters]

---

## 🎯 How to Use This Paper | 如何使用这篇论文

**If you are writing about [topic]:**
- Cite in Introduction for: [specific claim it supports]
- Cite in Discussion for: [comparison point]
- Key sentence to reference: "[quote]"

**Limitations to note:**
- [Honest assessment of what this paper doesn't prove]
```

---

## Translation Guidelines

- Translate faithfully, not literally — preserve scientific meaning
- Keep all numbers, chemical formulas, gene names, and proper nouns in original form
- For ambiguous terms, provide both: "催化活性（catalytic activity）"
- Technical terms: use standard Chinese scientific terminology
  - e.g., "oxygen evolution reaction" → "析氧反应（OER）"
  - "density functional theory" → "密度泛函理论（DFT）"
- Preserve hedging language: "suggest" → "表明", "indicate" → "指出", "demonstrate" → "证明"

---

## Figure Grounding Rules

For each figure mentioned in the text:
1. Find the corresponding figure caption
2. Note which result/claim the figure supports
3. Note the key quantitative message of each panel
4. Flag any discrepancy between text claims and figure data

---

## Output Options

Ask user:
1. **Full bilingual** (每段都翻译) — default
2. **Summary only** (只要速览+摘要+图表解读)
3. **Methods focus** (重点翻译方法部分)
4. **Export** — save as `~/Downloads/[paper-title]-reader.md`
