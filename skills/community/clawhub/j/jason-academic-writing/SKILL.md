---
name: jason-academic-writing
description: "Complete academic paper writing pipeline with integrity checks and multi-agent review system. Optimized prompts for Methods/Results/Discussion sections. Features self-counterargument framework, bias matrix, and overclaim self-audit. Use when writing research papers, need citation verification, anti-hallucination checks, multi-perspective review, or auditable process records."
version: 1.0.1
requires:
  env:
    - OPENAI_API_KEY
    - OPENAI_BASE_URL
---

# Academic Writing Pipeline

End-to-end academic paper production with built-in quality gates and multi-agent review.

## Pipeline Overview

```
Research → Write → Integrity Check → Review → Revise → Summary
```

Each stage has defined inputs/outputs and quality gates. The pipeline is **non-linear**: stages may loop (Review → Revise → Re-Review) until quality threshold met.

## Stage Details

### Stage 1: Research

**Goal**: Gather and organize evidence.

**Actions**:
1. Literature search via Semantic Scholar API
2. Filter by relevance score ≥ 0.5
3. Grade evidence level (A: meta-analysis, B: RCT, C: observational, D: opinion)
4. Output: `research/evidence.json`

**Script**: `scripts/research.py`

### Stage 2: Write

**Goal**: Generate structured manuscript.

**Actions**:
1. Build argument chain from evidence
2. Generate sections: Abstract, Introduction, Methods, Results, Discussion
3. Track citation markers for each claim
4. Output: `draft/manuscript.md`

**Script**: `scripts/write.py`

### Stage 3: Integrity Check (CRITICAL)

**Goal**: Anti-hallucination verification.

**Check types**:
- **Citation verification**: DOI exists? Authors match? Year correct?
- **Data verification**: Numbers match tables/figures?
- **Claim verification**: Evidence supports assertion?

**Threshold**: Must pass 100% of checks to proceed.

**Script**: `scripts/integrity_check.py`

**APIs used**:
- Semantic Scholar (`https://api.semanticscholar.org`)
- CrossRef DOI (`https://api.crossref.org/works/`)

### Stage 4: Review (5-Person Panel)

**Agents**:
| Role | Focus | Score Weight |
|------|-------|--------------|
| Editor-in-Chief | Contribution, journal fit | 30% |
| Methodology | Methods, stats, reproducibility | 25% |
| Domain Expert | Related work, theory | 20% |
| Devil's Advocate | Strongest counter-arguments | 15% |
| Synthesizer | Merge opinions, roadmap | 10% |

**Decision mapping**:
- ≥80: Accept
- 65-79: Minor Revision
- 50-64: Major Revision
- <50: Reject

**Script**: `scripts/review.py`

### Stage 5: Revise

**Goal**: Address reviewer feedback.

**Actions**:
1. Parse Synthesizer roadmap
2. Generate revision plan with priorities
3. Rewrite affected sections
4. Re-run Integrity Check

**Script**: `scripts/revise.py`

### Stage 6: Process Summary

**Goal**: Auditable record.

**Output**: `summary.json` containing:
- Timeline of each stage
- Decision points and scores
- Integrity check results
- Reviewer scores and comments
- Revision history

**Script**: `scripts/summary.py`

## Configuration

Edit `config.yaml` for:
- Model selection (default: `qwen3.5-plus`)
- Temperature (default: 0.3 for stability)
- Review thresholds
- API keys

## Usage

```bash
# Full pipeline
python scripts/main.py --topic "your research topic"

# Single stage
python scripts/main.py --stage integrity-check --input draft/manuscript.md

# With custom config
python scripts/main.py --config custom_config.yaml
```

## Quality Gates

| Gate | Requirement | Action on Fail |
|------|-------------|----------------|
| Evidence | ≥5 Grade A/B sources | Return to Research |
| Integrity | 100% verification | Return to Write |
| Review | ≥65 score | Loop Revise |
| Final Integrity | 100% verification | Block submission |

## Key Principles

1. **Integrity First**: Citation verification is non-negotiable
2. **Quantified Review**: Scores enable objective decisions
3. **Loopable Pipeline**: Revision cycles until threshold met
4. **Auditable Output**: Process Summary for journal submission

## Reference Files

- `references/review_rubric.md` - Detailed scoring criteria
- `references/evidence_levels.md` - Evidence grading standards
- `references/citation_styles.md` - Journal formatting guides