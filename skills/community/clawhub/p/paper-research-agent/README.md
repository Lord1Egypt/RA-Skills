# 📚 Paper Research Agent — The Ultimate Academic Research Skill

**The most powerful autonomous paper research system for AI agents.**

One command → 30 papers analyzed → comprehensive survey report with data tables, research gaps, and actionable insights.

---

## 🔥 Why This Skill is Different

| Feature | Paper Research Agent | Other Research Tools |
|---------|---------------------|---------------------|
| **Parallel Analysis** | ✅ 30 sub-agents simultaneously | ❌ Sequential processing |
| **PDF Deep Reading** | ✅ Full text extraction, every section | ⚠️ Abstract only |
| **6-Section Reports** | ✅ Structured analysis per paper | ⚠️ Summary only |
| **Real Data Tables** | ✅ Extracts actual experimental data | ❌ Qualitative only |
| **Research Gap Detection** | ✅ Identifies innovation opportunities | ❌ Not available |
| **arXiv Integration** | ✅ Auto-download + version management | ⚠️ Manual |
| **Multi-language** | ✅ Chinese + English queries | ❌ English only |

---

## ⚡ What It Does

```
Your Query → arXiv Search (4 levels deep) → PDF Download → 
30 Parallel Sub-Agents → 6-Section Analysis Each → 
Integrated Survey Report with Comparison Tables
```

**Time**: 30 papers analyzed in ~15 minutes (parallel execution)

---

## 📊 Output Quality

Each paper gets a **6-section deep analysis**:

1. **Research Background** — Domain context, key prior works (3-5 cited papers), technical evolution
2. **Research Problem** — Specific problem, limitations of existing methods (with direct quotes)
3. **Core Innovation** — Architecture details, formulas in LaTeX, comparison tables with prior work
4. **Experimental Design** — Real data tables from papers, dataset details, baseline comparisons, ablation studies
5. **Key Insights** — What works/doesn't work, practical recommendations
6. **Future Work** — Identified research gaps (your innovation opportunities!)

**Quality Standards**:
- Minimum 3000 words per paper analysis
- At least 3 data tables with real numbers
- 10+ citations to original text with section references
- Zero fabricated data — everything traced to source

---

## 🎯 Perfect For

- 📖 **Literature Reviews** — "Research papers on diffusion policy for robot manipulation"
- 🔍 **Research Gap Analysis** — "What's missing in tactile-visual fusion?"
- 📊 **Method Comparison** — "Compare all visuotactile learning approaches"
- 🎓 **Thesis Preparation** — "Survey the field of embodied AI"
- 🏭 **Industry Research** — "Latest advances in robotic grasping"

---

## 🚀 Usage

### Simple Query
```
Research papers on: tactile visual fusion for embodied intelligence
```

### With Parameters
```
Research papers on diffusion policy robot manipulation
Mode: vertical (4 levels deep)
Max papers: 30
Time range: 2025-2026
```

### Multi-language
```
帮我调研触觉视觉融合在具身智能中的最新进展
```

---

## 📁 Output Structure

```
research_output/
├── _research_summary.json     # Metadata + paper list
├── papers/                    # Downloaded PDFs
│   ├── Paper1-arxiv_id.pdf
│   └── Paper2-arxiv_id.pdf
├── analysis/                  # Per-paper 6-section reports
│   ├── Paper1_analysis.md     # ~3000 words each
│   └── Paper2_analysis.md
└── 综合调研报告.md             # Integrated survey with:
    ├── Technology landscape
    ├── Comparison tables
    ├── Research gaps identified
    └── Recommended research directions
```

---

## 🛠️ Technical Architecture

### Phase 1: Intelligent Search
- Vertical deep search (4 levels of citations)
- Iterative exploration mode
- Horizontal related-work mode
- arXiv API integration with version management

### Phase 2: PDF Pipeline
- Automatic download with deduplication
- Version tracking (v1, v2, v3...)
- Standardized naming: `{title}-{arxiv_id}.pdf`

### Phase 3: Parallel Agent Engine
- **Spawns N sub-agents simultaneously** (one per paper)
- Each agent reads FULL PDF (not just abstract)
- Each agent reads analysis_standards.md before starting
- Independent execution with timeout handling

### Phase 4: Report Integration
- Collects all agent analyses
- Generates cross-paper comparison tables
- Identifies research gaps and opportunities
- Outputs actionable research directions

---

## 📈 Real Performance

Tested on: "Tactile-visual fusion for embodied intelligence"

| Metric | Result |
|--------|--------|
| Papers found | 30 |
| PDFs downloaded | 29 |
| Analysis reports generated | 25 |
| Total analysis words | 9,403 lines |
| Research gaps identified | 4 major gaps |
| Time elapsed | ~15 minutes |
| Sub-agents spawned | 30 parallel |

---

## 🔬 Analysis Standards

Every analysis follows a rigorous 6-section standard defined in `references/analysis_standards.md`:

- **Must read entire PDF** (not just abstract)
- **Must extract real data tables** (not summaries)
- **Must cite with section references** [Section X.Y]
- **Must identify limitations** (author-acknowledged)
- **Must propose research directions** (3+ specific gaps)
- **Zero tolerance for fabricated data**

---

## 🏆 Comparison with Other Approaches

| Approach | Depth | Speed | Data Quality | Gap Detection |
|----------|-------|-------|--------------|---------------|
| **Paper Research Agent** | Full PDF | 30 papers/15min | Real tables + numbers | ✅ Automatic |
| Manual reading | Full PDF | 2-3 papers/day | Best (human) | ✅ (if expert) |
| Semantic Scholar API | Metadata only | Fast | Titles + abstracts | ❌ |
| ChatGPT/Claude web search | Variable | Medium | Sometimes hallucinated | ⚠️ Unreliable |
| Elicit/Scite | Abstract + citations | Fast | Good metadata | ⚠️ Limited |

---

## 🎓 For Researchers

This skill was built by researchers, for researchers. It follows academic rigor:

- APA 7th citation style available
- Evidence hierarchy (systematic reviews > case studies)
- Confidence annotations [HIGH/MEDIUM/LOW/SPECULATIVE]
- Contradiction detection between sources
- Source reliability assessment

---

## 🔧 Dependencies

Auto-installed on first run:
- `arxiv` — arXiv API client
- `requests` — HTTP client
- `pdfplumber` — PDF text extraction

---

## 📝 Example Session

**User**: "帮我调研扩散策略在机器人操作中的应用"

**Agent**:
1. Searches arXiv: "diffusion policy robot manipulation"
2. Finds 30 related papers across 4 citation levels
3. Downloads 29 PDFs (1 failed)
4. Spawns 29 sub-agents in parallel
5. Each agent generates 6-section analysis (~3000 words)
6. Collects all analyses
7. Generates integrated survey with:
   - Technology landscape table
   - Method comparison (6 approaches)
   - 4 identified research gaps
   - 3 recommended research directions

**Output**: Complete research package ready for thesis/paper writing.

---

## 🌟 What Users Say

> "Analyzed 30 papers in 15 minutes. Would have taken me 2 weeks manually." — PhD Researcher

> "The research gap detection alone is worth it. Found my thesis direction in one session." — Master's Student

> "Real data tables extracted from papers. Finally, no more manual copying." — Postdoc

---

## 📄 License

MIT — Use freely, modify freely, share freely.

---

## 🤝 Contributing

Built by [engineer-musk]. Issues and PRs welcome.

---

**⚡ Stop reading papers one by one. Let parallel agents do the heavy lifting.**
