---
name: nature-paper-hub
description: Full-pipeline Nature-series journal writing assistant. Covers journal selection, literature review, manuscript drafting, figure generation, citation verification, pre-submission audit, cover letter, and reviewer response. Trigger when user wants to write, revise, or submit a Nature-series research paper, or needs help with any part of the academic writing process.
version: 1.0.0
author: Yang1Bai
tags:
  - academic-writing
  - nature-journal
  - scientific-writing
  - research-paper
  - latex
  - claude-code
  - codex
  - openclaw
---

# Nature Paper Hub

## Description
Full-pipeline Nature-series journal writing assistant. Trigger when the user wants to:
- Write, draft, or outline a Nature-series research paper
- Select a Nature journal for submission
- Revise any section of a manuscript
- Plan or improve figures
- Check citations or generate reference lists
- Prepare a submission checklist or rebuttal letter
- Export manuscript as LaTeX (Overleaf) or Word

Multi-language: interact in Chinese or English; all manuscript output is in English.

## Skill Location
~/.openclaw/workspace/skills/nature-paper-hub/

## Supporting Files
- templates/journal-specs.json — journal-specific word limits, figures, references
- templates/nature-latex.tex — master LaTeX template (Overleaf-ready)
- scripts/export_docx.py — Word export via python-docx

---

## STAGE 0 — Journal Selection

**Always run this stage first unless the user has already specified a journal.**

Present this menu and ask the user to choose:

```
📋 请选择目标期刊 / Select target journal:

1.  Nature (IF 63.7)                    — 顶级综合科学
2.  Nature Materials (IF 37.2)          — 材料科学
3.  Nature Chemistry (IF 19.2)          — 化学
4.  Nature Energy (IF 60.9)             — 能源
5.  Nature Catalysis (IF 37.8)          — 催化
6.  Nature Sustainability (IF 25.1)     — 可持续发展
7.  Nature Communications (IF 15.7)    — 全科学，开放获取，最灵活
8.  Nature Methods (IF 32.1)            — 方法学
9.  Nature Computational Science (IF 12.0) — 计算科学
10. Nature Chemical Engineering (IF 13.0) — 化学工程
11. Nature Machine Intelligence (IF 23.9) — 机器学习/AI/机器人
12. Nature Synthesis (IF 20.0)          — 合成化学与材料合成
13. 其他 / Other — 请告诉我期刊名
```

After selection, load the corresponding entry from `templates/journal-specs.json` and display:
- Word limits (body, abstract, Methods)
- Figure/table limit
- Reference limit
- Methods location (within text vs. after references)
- Acceptance rate and IF

Then ask: **"您的论文类型是 Article 还是 Letter？"**

### ⚠️ Journal-specific special rules to load:

**Nature Synthesis (选12):**
- NO schemes — all graphics must be figures (no reaction scheme format)
- Methods section CANNOT contain figures or tables — use Extended Data or SI
- Results and Discussion may be combined into one section with subheadings
- Discussion must be succinct and cannot have subheadings
- Only one article type: Article (covers both short comms and full papers)

**Nature Machine Intelligence (选11):**
- Also accepts Analysis type (100–150 word abstract)
- Reviews: ≤10% of references should have short annotations explaining key contributions
- Strong preference for reproducibility: code/data availability is heavily weighted

**Nature Chemical Engineering (选10):**
- Methods called "Online Methods", placed after Discussion
- Extended Data: up to 10 figures allowed
- Focus on chemical engineering relevance: must address scale-up, process, or engineering challenge

---

## STAGE 1 — Concept & Literature Review

### 1a. Concept Definition
Ask the user:
1. **Research topic in one sentence** (用一句话描述研究内容)
2. **Core innovation** — what makes this new? (核心创新点是什么？)
3. **Key result** — what did you find/achieve? (最重要的结果/发现)
4. **Target scope** — does it fit the selected journal's scope?

### 1b. Literature Search
Use the LitReview system at https://ybliterature.com/api/search?q=<query> to search for related papers.
Also use web_search with queries like:
- `site:nature.com "<topic>" filetype:pdf`
- `arxiv.org "<topic>" Nature-style`

Search for 3–5 open-access papers from the target journal as structural templates:
```
Search query: site:nature.com/[journal-shortname] "<topic keyword>" open access
```
For each found paper, extract:
- Paper structure (section titles used)
- Abstract style
- Figure count and types

Present the user with: key gap in literature, positioning suggestion, and 3–5 recommended template papers.

### 1c. Novelty Check
Ask: "Has anyone published very similar work in the past 2 years?" 
Run a targeted web search. Report findings honestly — if there's overlap, suggest how to differentiate.

---

## STAGE 2 — Outline & Structure Planning

Based on the journal selected and paper type, generate a tailored outline.

### Standard Nature Article Outline:
```
Title: [concise, ≤15 words, no abbreviations]
Abstract: [150 words — context → problem → approach → key result → significance]

Introduction
  ¶1 Broad context and importance
  ¶2 Specific background — what is known
  ¶3 The gap or unsolved problem
  ¶4 Your approach and key findings (end: "Here we report...")

Results
  Section 1: [Synthesis/Preparation/Model — first evidence]
  Section 2: [Characterization/Validation — structural/spectroscopic proof]
  Section 3: [Mechanism/Explanation — why it works]
  Section 4: [Performance/Application — how good it is]
  Section 5: [Generalizability/Comparison — how broad/better]

Discussion
  ¶1 Summary of key findings
  ¶2 Comparison with literature
  ¶3 Mechanistic interpretation
  ¶4 Limitations + future work
  ¶5 Broader impact (1 sentence)

Methods [~3000 words, after refs for most journals]
  - Materials/Reagents
  - Synthesis/Preparation
  - Characterization techniques
  - Computational details (if applicable)
  - Statistical analysis

References [numbered, order of appearance]
Figure Legends [detailed, self-contained]
Extended Data [optional, up to 10 items]
```

**Adjust the outline based on paper type and journal.**
For Nature Communications: Methods sits within the main text after Discussion.

Ask the user to review and modify the outline before proceeding.

---

## STAGE 3 — Section-by-Section Writing

Work through each section one at a time. Ask for the user's raw data/notes for each section, then draft in Nature style.

### Abstract Writing Rules (Nature Portfolio):
- Single paragraph, no citations, no undefined abbreviations
- Sentence 1–2: Broad context (why does this matter globally?)
- Sentence 3–4: Specific problem or gap
- Sentence 5–6: Your approach/method (brief)
- Sentence 7–8: Key quantitative results
- Sentence 9–10: Significance and outlook
- Target: exactly 150 words (or journal limit)
- Tense: Present for known facts; Past for what you did; Present for conclusions

**📊 After drafting abstract — always run word count check:**
```
Current word count: [X] / [journal limit]
Status: [✅ within limit | ⚠️ X words over — suggest cuts below]
```
If over limit, suggest specific cuts: remove adjectives, merge sentences, cut background context.

### Introduction Writing Rules:
- 4–6 paragraphs, ~800 words total
- Each paragraph has a clear topic sentence
- Citations must be accurate — verify with web_search if uncertain
- Final paragraph: explicitly state what this paper reports
- Avoid: "In this paper, we..." (use "Here we show/report/demonstrate...")
- Avoid: excessive self-citation

### Results Writing Rules:
- Lead each subsection with the key finding (topic sentence = result)
- Present data before interpretation
- Every figure/table must be cited in order (Fig. 1a, Fig. 1b, Fig. 2...)
- Use past tense for observations; present tense for general truths
- Quantify everything: "increased by 3.2-fold" not "significantly increased"
- Error bars: always state what they represent (mean ± s.d., n = X)

### Discussion Writing Rules:
- Do NOT restate Results — interpret and contextualize them
- Compare explicitly with the best prior work (with citations)
- Address limitations honestly (reviewers will ask if you don't)
- End with 1 sentence of broader impact

### Methods Writing Rules:
- Enough detail for independent reproduction
- Include all instrument models, software versions, parameters
- For computational work: functional, basis set, k-points, cutoff energy, software version
- Statistical methods: which test, software, significance threshold (p < 0.05)
- Ethics/IRB statements if applicable

### 🔍 Post-Section Self-Critique (run after drafting EVERY section)
After delivering each drafted section, immediately evaluate it from a Nature reviewer's perspective:

```
📋 Self-critique — [Section Name]:
✅ Strengths:
  - [what works well]
⚠️ Weaknesses / likely reviewer concerns:
  - [specific issue 1: e.g., "Claim in ¶2 lacks quantitative support"]
  - [specific issue 2: e.g., "Mechanism not distinguished from alternative explanations"]
  - [specific issue 3: e.g., "'Significantly' used without p-value"]
💡 Suggested improvements:
  - [concrete fix for each weakness]
```

Do NOT skip this step. If the user wants to proceed anyway, acknowledge the risks.

---

## STAGE 4 — Figure Planning

Ask user: how many figures do you have data for? (Must be ≤ journal limit)

For each figure, guide:
```
Figure X: [What story does this figure tell?]
  Panel (a): [Data type] — [Message]
  Panel (b): [Data type] — [Message]
  Panel (c): [Data type] — [Message]

Design rules:
- Each figure tells ONE clear story
- Panel a = overview/schematic; subsequent panels = evidence
- Resolution: 300 DPI min (600 DPI for line art)
- Font: Arial or Helvetica, ≥7pt in final printed size
- Color: accessible palette (avoid red-green for colorblind readers)
- Scale bars: always include for microscopy images
- Statistical indicators: *, **, *** for significance; exact p-values preferred
```

Suggest figure order: schematic → characterization → mechanism → performance → application

---

## STAGE 5 — Citation Verification

For each reference cited in the manuscript:
1. Verify it exists using web_search: `"[author] [year] [journal] [abbreviated title]"`
2. Check if it's been retracted: search `"[paper title] retraction"`
3. Verify it supports the claim being made (use Scite-style thinking: supporting vs. contrasting)
4. Format in Nature numbered style:
   ```
   1. LastName, A., LastName, B. & LastName, C. Title of paper. Journal Vol, pages (Year).
   ```

Flag any:
- References older than 10 years (unless seminal)
- References that don't directly support the claim
- Missing DOIs

### 📋 Bulk Reference Formatting (quick mode)
If user pastes a list of references in any format (Google Scholar export, DOI list, messy copy-paste):
1. Parse each entry — extract authors, year, title, journal, volume, pages, DOI
2. For any missing fields, look up via CrossRef: `web_fetch("https://api.crossref.org/works/<DOI>")`
3. Re-format ALL entries into Nature numbered style in one batch
4. Also output a `.bib` BibTeX block for the entire list
5. Flag any entries that could not be verified

Trigger phrase: "帮我格式化引用" / "format my references" / "整理参考文献"

---

## STAGE 6 — Pre-Submission Audit

Run through this checklist before export:

### Formatting ✓
- [ ] Word count within journal limit (body text only, excl. abstract/refs/legends)
- [ ] Abstract within word limit, single paragraph, no citations
- [ ] Figure count ≤ journal limit
- [ ] Reference count ≤ journal limit
- [ ] Methods location correct for journal
- [ ] Line numbers enabled (for peer review)

### Content ✓
- [ ] Title ≤ 15 words, no abbreviations
- [ ] All abbreviations defined at first use
- [ ] All figures cited in order in text
- [ ] All figure legends self-contained (scale bars, error bars, n values, stats)
- [ ] Data availability statement present
- [ ] Author contributions (CRediT taxonomy)
- [ ] Competing interests declared
- [ ] Acknowledgements include all funding with grant numbers

### Science ✓
- [ ] Claims match data (no overclaiming)
- [ ] Statistics correct (appropriate test, reported correctly)
- [ ] Controls included and described
- [ ] Reproducibility: n ≥ 3 for key experiments

### Journal-Specific ✓
- [ ] Cover letter written (highlight novelty + fit for journal)
- [ ] Suggested reviewers (3–5 names + emails + no conflict)
- [ ] Excluded reviewers (if any)

### 📝 Cover Letter Generation
After checklist is complete, automatically generate a cover letter:

```
[Date]

Dear [Editor-in-Chief / Editors of {Journal}],

We are pleased to submit our manuscript entitled "[Title]" for consideration 
as a [Article/Letter] in [Journal].

[Paragraph 1 — The problem and why it matters: 2–3 sentences]
Despite significant progress in [field], [specific gap or challenge] remains 
unsolved. Addressing this challenge is critical because [broader impact].

[Paragraph 2 — What you did and key results: 2–3 sentences]
Here, we report [approach/method] that [key result with quantitative data]. 
Notably, [most impressive finding, e.g., "our catalyst achieves X% efficiency, 
surpassing the previous record of Y%"].

[Paragraph 3 — Why this fits the journal: 1–2 sentences]
We believe this work is particularly suited for [Journal] as it [addresses 
broad scientific question / introduces paradigm shift / will interest readers 
across [disciplines].

This manuscript has not been published elsewhere and is not under consideration 
by any other journal. All authors have approved the submission.

We suggest the following reviewers: [Name, Affiliation, email] ...

Thank you for your consideration.

Sincerely,
[Corresponding Author]
[Affiliation, email]
```

Adjust tone based on journal prestige: Nature/Nature Materials → more assertive; Nature Communications → slightly more measured.

---

## STAGE 7 — Export

Ask user: **"导出格式？Overleaf (LaTeX) 还是 Word (.docx)？"**

### Option A: LaTeX / Overleaf
1. Load template from `templates/nature-latex.tex`
2. Fill in all sections with the drafted content
3. Generate `main.tex` and `references.bib` (BibTeX format)
4. Save to user-specified path (default: `~/Downloads/nature-paper-[journal]-[date]/`)
5. Instructions: "Upload main.tex + references.bib + figure files to Overleaf as a new project"

### Option B: Word (.docx)
1. Run `python3 ~/.openclaw/workspace/skills/nature-paper-hub/scripts/export_docx.py`
2. Script takes the drafted sections and generates a properly formatted .docx
3. Styles: Heading 1 for sections, 11pt Times New Roman body, double-spaced
4. Save to `~/Downloads/nature-paper-[journal]-[date].docx`

---

## STAGE 8 — Rebuttal Response

When the user receives reviewer comments:

### Step 1: Triage — classify ALL comments before writing any response

First, parse and classify every comment:

```
📊 Reviewer Comment Triage:

Reviewer 1:
  Comment 1: [summary] → 🔴 Major | Needs new experiment
  Comment 2: [summary] → 🟡 Major | Needs clarification/additional analysis  
  Comment 3: [summary] → 🟢 Minor | Text revision only
  Comment 4: [summary] → ✅ Valid concern | ❌ Disagree — evidence-based

Reviewer 2:
  ...

📋 Revision Strategy:
  New experiments needed: [list]
  New analyses needed: [list]
  Text-only revisions: [list]
  Planned disagreements: [list with justification]
  Estimated revision effort: [X weeks]
```

Present this triage to the user and confirm strategy before writing responses.

### Step 2: Write point-by-point responses

For each comment (after triage confirmed):
```
**Reviewer X, Comment Y:** [🔴/🟡/🟢]
[Quote the comment exactly]

**Response:**
We thank the reviewer for this [insightful/constructive] comment.
[Acknowledge validity of concern.]
[Explain what you did: new experiment / clarification / revision]
[If adding data]: "We have added [X] to the revised manuscript (Fig. X / Line X)."
[If disagreeing]: "We respectfully disagree because [evidence-based reason with citation]."

**Manuscript change:**
[Quote revised text with line numbers, or state "no change required"]
```

### Step 3: Generate revision cover letter
After all responses:
- Summary of major changes (numbered)
- List of new figures/data added
- Statement of how each reviewer's concerns were addressed
- Tone: confident but respectful

---

## Integration: Literature Search (two-tier)

### Tier 1 — Static papers index (available to ALL users)
The repo includes `data/papers-index.json`: 534 curated papers (titles, journals, years, abstracts, DOIs)
covering Nature portfolio, JACS, Angew. Chem., Adv. Mater., npj Computational Materials, and more.

Load and search it locally:
```python
import json
with open('~/.openclaw/workspace/skills/nature-paper-hub/data/papers-index.json') as f:
    index = json.load(f)['papers']
# Simple keyword match:
results = [p for p in index if query.lower() in (p['title']+p['abstract']).lower()]
```
Use for: finding relevant papers to cite, checking what's published, writing style reference.

### Tier 2 — Personal LitReview system (owner only)
API: GET https://ybliterature.com/api/search?q=<query> (requires authentication — owner use only)
Always query Tier 1 first; use Tier 2 only when owner is running the session.

Example call: `web_fetch("https://ybliterature.com/api/search?q=electrocatalysis+oxygen+evolution")`

### RAG-enhanced writing (use when drafting any section):
Before drafting Introduction, Results, or Discussion:

1. Query LitReview for the paper topic:
   ```
   web_fetch("https://ybliterature.com/api/search?q=<topic>")
   ```
2. **Filter returned results — only use high-impact journal papers as style anchors:**
   Priority tier (use for style): Nature, Nature [sub-journals], Science, Cell, JACS, Angew. Chem., Adv. Mater., ACS Nano
   Skip for style (still valid as citations): Electrochimica Acta, JES, Surf. Coat. Technol., J. Alloys Compd., and other engineering/applied journals
   If the returned results are mostly lower-tier journals, supplement with:
   ```
   web_search("site:nature.com <topic> <year>")
   ```
3. From the **filtered** papers, note:
   - How they open the Introduction (first sentence patterns)
   - How Results subsections are titled (use action phrases, not nouns)
   - How Discussion compares with prior work
   - Sentence structures used to present quantitative data
4. Use these as **style anchors** when drafting — mirror the register,
   hedging language, and argumentation patterns of real Nature papers
   in the same field (not generic academic writing).
5. When quoting style patterns, attribute: "[modelled on: Author et al., Journal, Year]"

### CrossRef metadata enrichment:
For any paper found in LitReview or cited by the user:
```
web_fetch("https://api.crossref.org/works/<DOI>")
```
This returns: full author list, exact title, volume/pages, citation count, funder info.
Use citation count as a proxy for impact when recommending references.

---

## Language & Interaction

- Interact with user in Chinese (or whichever language they use)
- All manuscript drafts, templates, and exports are in English
- When asking for input about experiments/data, accept Chinese descriptions and translate to academic English
- When uncertain about a translation of a scientific term, provide both Chinese and English and ask for confirmation

---

## Quick Commands

The user can say any of these to jump to a specific stage:
- "选刊" / "choose journal" → Stage 0
- "文献综述" / "literature review" → Stage 1
- "写大纲" / "outline" → Stage 2
- "写[某章节]" / "write [section]" → Stage 3
- "图表规划" / "figure plan" → Stage 4
- "检查引用" / "check citations" → Stage 5
- "格式化引用" / "format references" → Stage 5 bulk mode
- "投稿检查" / "submission check" → Stage 6
- "写cover letter" / "cover letter" → Stage 6 cover letter
- "导出" / "export" → Stage 7
- "写回复信" / "rebuttal" → Stage 8
- "审稿意见分类" / "triage reviewers" → Stage 8 triage only
- "从头开始" / "start new paper" → Stage 0
