---
name: paper-compare
description: Compare academic research papers side-by-side to identify similarities, differences, and research gaps. Use when user wants to compare 1-5 papers via DOIs, URLs, search queries, or PDF files. Supports mixed input types. Outputs both comparison table and detailed narrative summary.
version: 1.2.1
changelog: Added user_goal to history, clarified step structure
metadata: {"clawdbot":{"emoji":"📄","category":"research"}}
---

# Paper Compare

Compare academic papers side-by-side with structured tables and detailed narrative analysis.

---

## The Paper Comparison Reasoning Framework

```
┌─────────────────────────────────────────────────────────────┐
│  PAPER COMPARISON THINKING                                   │
├─────────────────────────────────────────────────────────────┤
│  1. INTERPRET  → What papers? What comparison goal?        │
│  2. RETRIEVE   → Fetch metadata, abstracts, full text     │
│  3. ANALYZE    → Extract across 10 dimensions              │
│  4. SYNTHESIZE → Build narrative, find gaps, score quality │
│  5. VALIDATE   → Check completeness, deliver              │
└─────────────────────────────────────────────────────────────┘
```

---

## Decision Tree: Input Processing

```
USER INPUT
    │
    ├── 1 paper ──→ Single Paper Summary
    │       └── Skip comparison, show full summary
    │
    ├── 2-5 papers ──→ Full Comparison
    │       └── Proceed with 10 dimensions
    │
    ├── >5 papers ──→ Ask to Narrow
    │       └── "Please narrow to 2-5 for meaningful comparison"
    │
    ├── DOI ──→ Fetch via crossref/semantic scholar
    │       └── https://api.crossref.org/works/{doi}
    │
    ├── URL ──→ Fetch via web_fetch
    │       └── Extract title, authors, abstract
    │
    ├── Search query ──→ Search first
    │       └── Use web_search, present top 3, CONFIRM before proceeding
    │
    └── PDF file ──→ Extract text first
            └── Use pdf skill, then extract metadata
```

---

## Decision Tree: Comparison Angle

```
WHAT IS THE COMPARISON ABOUT?
    │
    ├── Same topic, different methods ──→ 
    │       └── Focus: methodology differences, results comparison
    │
    ├── Same method, different domains ──→
    │       └── Focus: adaptation, performance across domains
    │
    ├── Evolution over time ──→
    │       └── Focus: improvements, what changed, SOTA progression
    │
    ├── Competing approaches ──→
    │       └── Focus: trade-offs, when to choose which
    │
    └── Complementary papers ──→
            └── Focus: how they combine, gaps each fills
```

**Self-Check: After Identifying Angle**
- [ ] Does my analysis focus on the right aspects?
- [ ] Will this help the user make a decision?

---

## Step 1: Interpret the Request

### What to Clarify

| Question | Why It Matters |
|----------|----------------|
| Which papers? | Need exact references |
| What goal? | Learning? Research? Writing? |
| What comparison angle? | Focus analysis appropriately |

### Self-Check: Before Starting

- [ ] Do I have all paper references?
- [ ] Do I understand what user wants to learn?
- [ ] Is the number of papers appropriate (1-5)?
- [ ] What's the comparison angle?

---

## Step 2: Retrieve Papers

### Retrieval Strategy

| Input Type | Method | Source |
|------------|--------|--------|
| DOI | API | crossref, semantic scholar |
| URL | web_fetch | arXiv, IEEE, PubMed |
| Search | web_search → web_fetch | Find, then confirm |
| PDF | pdf skill | Extract text |
| History | memory_search | Prior comparisons |

### Quality Priority

```
Must have:
├── Title
├── Authors
├── Year
├── Venue
├── Abstract (for methodology + results)

Nice to have:
├── Full text (for limitations)
├── Code/data links
├── Citation count (see below)
```

### Citation Count

Use Semantic Scholar API:
```
https://api.semanticscholar.org/graph/v1/paper/{doi}?fields=citationCount
```

### Self-Check: After Retrieval

- [ ] Did I get the abstract?
- [ ] Can I determine the methodology?
- [ ] Are there any papers with missing critical info?
- [ ] Did I get citation counts?

---

## Step 3: Analyze (10 Dimensions)

### Core Dimensions (Always Include)

| # | Dimension | What to Extract |
|---|-----------|-----------------|
| 1 | Title | Full title |
| 2 | Authors | All authors, first author highlighted |
| 3 | Year | Publication year |
| 4 | Venue | Journal/Conference |
| 5 | Research Question | What problem do they solve? |
| 6 | Methodology | Approach, techniques used |
| 7 | Dataset | What data did they use? |
| 8 | Results | Key findings with numbers |
| 9 | Limitations | What do they acknowledge? |
| 10 | Code & Data | Links to artifacts? |

### Decision: What If Missing?

```
Missing dimension:
    │
    ├── Abstract missing ──→ Note "Unable to analyze methodology"
    │
    ├── Results missing ──→ Note "Results not available in metadata"
    │
    ├── Limitations missing ──→ Note "Not specified" (don't infer)
    │
    └── Dataset unclear ──→ Note "Not clearly specified"
```

---

## Step 4: Synthesize

### Quality Scoring

Evaluate each paper:

| Factor | Score | Notes |
|--------|-------|-------|
| **Venue Quality** | | |
| - Top-tier (NeurIPS, ICML, ICLR, Nature, Science) | ⭐⭐⭐ | |
| - Good (AAAI, IJCAI, CVPR, EMNLP, IEEE) | ⭐⭐ | |
| - Other | ⭐ | |
| **Citations** | | |
| - 100+ | ⭐⭐⭐ | Highly cited |
| - 10-100 | ⭐⭐ | Well-known |
| - <10 | ⭐ | Recent or niche |
| **Code Available** | | |
| - Yes, official | ⭐⭐⭐ | |
| - Yes, community | ⭐⭐ | |
| - No | ⭐ | |
| **Data Available** | | |
| - Yes | ⭐⭐⭐ | |
| - No | ⭐ | |

**Overall Quality:** Sum stars (higher = more established)

### Comparison Table Structure

```
| Dimension | Paper A | Paper B | ... |
|-----------|---------|---------|-----|
| Title | ... | ... | ... |
| Authors | ... | ... | ... |
| Year | ... | ... | ... |
| Venue | ... | ... | ... |
| Research Question | ... | ... | ... |
| Methodology | ... | ... | ... |
| Dataset | ... | ... | ... |
| Results | ... | ... | ... |
| Limitations | ... | ... | ... |
| Code & Data | ... | ... | ... |
| Quality Score | [⭐⭐⭐] | [⭐⭐] | ... |
```

### Narrative Synthesis Template

**Structure:**
```
## Overview
[What problem each paper addresses - high-level]
[Comparison angle: what are we comparing?]

## Methodology Comparison
[Compare techniques - are they compression-based? architecture-based?
 What's the key algorithmic difference?
 How does the comparison angle affect this?]

## Results Analysis
[Quantitative results - specific numbers, metrics
 Performance comparison - trade-offs mentioned
 Which paper wins on what?]

## Limitations
[What each paper acknowledges - be honest about gaps]
[What's NOT covered that might matter]

## Research Gaps
[What's MISSING across ALL papers]
[What's not yet explored]
[Potential future directions]

## Quality Assessment
[Paper A: ⭐⭐⭐ - Why]
[Paper B: ⭐⭐ - Why]
[Note any concerns]
```

---

## Step 5: Structured Verdict

### Decision Matrix

### Decision Matrix

```
| If You Need... | Choose | Why |
|----------------|--------|-----|
| [Best performance] | Paper [X] | [Reason] |
| [Easiest to implement] | Paper [X] | [Reason] |
| [Latest method] | Paper [X] | [Reason] |
| [Most cited/reliable] | Paper [X] | [Reason] |
| [Code available] | Paper [X] | [Reason] |
```

### Final Recommendation

```markdown
## Verdict

**For [user's goal]:**

- **Best overall:** [Paper X] — [key reason]
- **Best for implementation:** [Paper Y] — [key reason]  
- **Best for research depth:** [Paper Z] — [key reason]

**My recommendation:** [Paper X] because [specific reason matching user's goal]

**If you're unsure:** Start with [Paper X] for [reason], then explore [Paper Y] if you need [different aspect].
```

### Self-Check: Before Delivering

- [ ] Did I answer the user's original question?
- [ ] Did I identify the comparison angle?
- [ ] Are all 10 dimensions covered?
- [ ] Is quality scored?
- [ ] Is verdict actionable?

---

## Step 6: Validate & Deliver

### For Single Paper (1 only)

**Output:**
```
## Paper Summary

**Title:** [title]
**Authors:** [authors]
**Year:** [year]
**Venue:** [venue]

### Research Question
[What problem they address]

### Methodology
[Brief description]

### Key Results
[With numbers]

### Limitations
[What they acknowledge]

### Code & Data
[Links or "Not specified"]

### Citation Count
[If available]

### Quality Score
[⭐⭐⭐]
```

### For Comparison (2-5 papers)

**Deliver:**
1. **Comparison Angle** — What we're comparing and why
2. **Comparison Table** — All 10 dimensions + quality
3. **Narrative Summary** — 6-section synthesis
4. **Quality Assessment** — Scored factors
5. **Structured Verdict** — Decision matrix + recommendation

### Edge Cases to Note

| Situation | How to Handle |
|-----------|---------------|
| Different fields | Warn: "Comparing CS vs Biology papers" |
| Very different years | Note: "2010 vs 2024 — comparison may be unfair" |
| Preprint | Note: "Preprint — not peer-reviewed" |
| Conflicting results | Note: "Paper A claims X, Paper B claims Y" |

---

## Error Handling

### If Retrieval Fails

```
FETCH FAILS
    │
    ├── DOI not found ──→ Check DOI format, try search
    │       └── "DOI not found. Did you mean...?"
    │
    ├── URL inaccessible ──→ Try alternative source
    │       └── e.g., arXiv → semantic scholar
    │
    ├── Search returns nothing ──→ Try different keywords
    │       └── "No papers found for [query]. Try...?"
    │
    └── PDF extraction fails ──→ Note "Unable to extract"
            └── Can still use metadata if available
```

---

## History (Persistence)

### Save After Comparison

```json
{
  "last_comparison": {
    "date": "2026-03-04",
    "user_goal": "[what user wanted to achieve - learning/research/writing/decision]",
    "papers": [
      {"title": "...", "doi": "10.xxxx/xxx"},
      {"title": "...", "url": "..."}
    ],
    "topic": "[what was compared]",
    "comparison_angle": "[same topic different methods / etc]",
    "verdict": "[which paper recommended]",
    "dimensions": {
      "methodology": "...",
      "key_difference": "..."
    }
  }
}
```

### Load History

- Read `memory/paper-compare-history.json` if exists
- Use `memory_search` to find prior comparisons

---

## Dependencies

| Skill | Use For |
|-------|---------|
| pdf | Extract text from uploaded PDFs |
| web_search | Find papers by query |
| web_fetch | Get paper content from URLs |

---

## Quick Reference

| Input | Action |
|-------|--------|
| 1 DOI | Single summary |
| 2 DOIs | Full comparison |
| arXiv URL | Fetch abstract |
| "search for X" | Search → confirm → proceed |
| Upload PDF | Extract → analyze |

---

## Summary Checklist

- [ ] Identify comparison angle
- [ ] Retrieve all papers (metadata + abstract)
- [ ] Extract 10 dimensions
- [ ] Score quality (venue, citations, code, data)
- [ ] Build comparison table
- [ ] Write narrative summary
- [ ] Create structured verdict
- [ ] Save to history

---

## Notes

- Always confirm before proceeding with search results
- Keep comparisons focused: 2-5 papers max
- Don't infer missing information — state "Not specified"
- Save to history for future reference
- Quality scoring helps users make informed decisions
