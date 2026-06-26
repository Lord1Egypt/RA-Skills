---
name: paper-impact-analyzer
description: "Analyze academic paper impact using multiple data sources (arXiv, GitHub, OpenAlex, Semantic Scholar). Input an arXiv ID and get a multi-dimensional impact assessment with graceful degradation when APIs are unavailable. Use when evaluating paper influence, comparing papers, or assessing whether a paper is worth reading."
version: "1.0.0"
allowed-tools: "Bash Read Write"
license: MIT-0
metadata:
  skill-author: haataa
  version: "1.0.0"
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python"]
---

# Paper Impact Analyzer

Multi-source, fault-tolerant academic paper impact analysis.

## When to Use

- Evaluating a paper's academic influence or community adoption
- Comparing impact across multiple papers
- Deciding whether a paper is worth reading based on external signals
- Checking GitHub stars, citation counts, venue acceptance for a paper
- Assessing author credibility (h-index) for a paper
- Batch-analyzing papers in a survey or literature review

## How to Use

### Single paper

Run the analysis script with an arXiv ID:

```bash
python scripts/analyze.py 2603.04948
```

### Multiple papers

Pass multiple arXiv IDs separated by spaces:

```bash
python scripts/analyze.py 2603.04948 2602.15922 2603.05488 2602.22661
```

### Output

The script prints a structured Markdown impact report for each paper, including:

| Dimension | Example |
|-----------|---------|
| Publication date | 2026-03-05 (20 days ago) |
| Venue acceptance | ICLR 2026 |
| GitHub repo | 2,263 stars / 214 forks |
| Citation count | 12 (OpenAlex) / 15 (S2) |
| Author h-index | First author h=23 |
| Affiliations | UC Berkeley, UT Austin |

Plus a synthesized overall rating (S/A/B/C/D) with confidence level and data completeness.

## Data Sources (Priority Order)

1. **arXiv API** — paper metadata, authors, abstract (always available)
2. **GitHub API** — repo stars, forks, issues (most reliable external signal)
3. **OpenAlex API** — citation count (free, no API key needed)
4. **Semantic Scholar API** — citations, influential citations, author h-index (rate-limited)

Each source fails independently. The script always produces output using whatever data is available.

## Design Philosophy

- **Graceful degradation**: Every API call is wrapped in try/except with timeouts. If Semantic Scholar returns 429, the report still includes arXiv + GitHub + OpenAlex data.
- **Age-aware scoring**: Papers < 3 months old are scored primarily on GitHub + venue + team. Papers > 1 year old are scored primarily on citations.
- **No API keys required**: All data sources used are free and keyless.
- **Single file**: The entire implementation is in `scripts/analyze.py` with zero external dependencies (stdlib only).
