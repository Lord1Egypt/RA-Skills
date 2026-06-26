---
name: review-paper-writing
description: |
  Literature review paper writing assistant — guides you through the full lifecycle:
  (1) Systematic search using PICO/Boolean/MeSH frameworks across arXiv, Semantic Scholar, OpenAlex, CrossRef & PubMed;
  (2) DOI & arXiv ID validation with cross-source conflict detection;
  (3) Multi-format citation output (APA 7th, MLA 9th, IEEE, BibTeX, RIS, Markdown);
  (4) Auto-generated structured literature review with timeline, keyword extraction & source-quality tagging.
  Use when drafting a review article, survey paper, or thesis background chapter — or when given a topic to compile references for.
---

# Review Paper Writing Skill

## Overview

This skill helps you write a thorough, well-structured literature review — from topic definition and systematic search to formatted citations and a polished markdown draft. It covers:

- **Topic framing** with PICO framework
- **Search strategy** (Boolean, MeSH, wildcards, proximity)
- **Multi-source academic search** (arXiv, Semantic Scholar, OpenAlex, CrossRef, PubMed)
- **DOI / arXiv ID validation** and conflict detection
- **Citation formatting** (APA, MLA, IEEE, BibTeX, RIS, Markdown)
- **Auto-generated literature review** in Markdown

## Quick Start

### 1. Run a Search

```bash
python3 scripts/lit_search.py "large language model education" -n 20 --sources arxiv openalex
```

### 2. Validate DOIs

```bash
python3 scripts/lit_search.py "machine learning" --validate
```

### 3. Format Citations

```bash
python3 scripts/lit_search.py "BERT" -n 10 -f apa      # APA 7th
python3 scripts/lit_search.py "transformer" -n 10 -f bibtex  # BibTeX
python3 scripts lit_search.py "attention" -n 10 -f ris     # RIS
```

### 4. Filter Results

| Flag | Effect |
|------|--------|
| `--published-only` | Exclude arXiv preprints |
| `--preprint-only` | Only arXiv preprints |
| `--min-year 2020` | Earliest publication year |
| `--min-citations 50` | Minimum citation count |
| `--conflicts` | Detect cross-source metadata conflicts |

### 5. Batch Mode (from file)

Create `papers.txt` with one DOI/PMID/arXiv ID per line:
```
10.48550/arXiv.2303.08774
10.48550/arXiv.2205.11916
PMID: 34567890
```
Then:
```bash
python3 scripts/lit_search.py file://papers.txt -f bibtex
```

## Search Strategy Framework

### PICO Framework

Use PICO to structure your research question:

| Element | Meaning | Example |
|---------|---------|---------|
| **P**opulation | Target group | high school students |
| **I**ntervention | Treatment or method | motivational interviewing |
| **C**omparator | Control group | no intervention |
| **O**utcome | Measurable result | academic performance |

Convert to search terms:
```
P: student*
I: "motivational interviewing"
O: "academic achievement"
→ "motivational interviewing" AND student* AND "academic achievement"
```

### Boolean Operators

```python
# AND: all terms must appear
"cognitive behavioral therapy" AND adolescent*

# OR: any term may appear
depression OR anxiety OR "mental health"

# NOT: exclude terms
animal NOT pet

# Parentheses for grouping
("cognitive behavioral therapy" OR CBT) AND adolescent*
```

### Wildcards & Truncation

```python
student*   → student, students, student's, students'
wom?n      → woman, women
```

### Proximity Search

```python
behavior N/2 change    # "behavior" within 2 words of "change"
"stress" ADJ3 "coping" # same sentence
```

### MeSH (PubMed)

```python
"Motor Activity"[Mesh]
"Depression"[Mesh] AND "Therapy"[Mesh:Subheading]
```

### Database-Specific Syntax

```python
# PubMed
"motivational interviewing"[Title/Abstract]
("Anxiety"[Mesh] OR "Anxiety Disorders"[Mesh]) AND 2020:2024[dp]

# PsycINFO (OVID)
exp Motivational Interviewing/
motivation interview*.tw

# Web of Science
TS=("motivational interviewing" AND school*)
PY=2020-2024
```

## Source Comparison

| Source | Type | API Key | Best For |
|--------|------|---------|---------|
| **arXiv** | Preprint | ❌ No | CS, ML, physics, stats |
| **Semantic Scholar** | Published + preprint | Optional | High-citation papers |
| **OpenAlex** | Published | ❌ No | Broad cross-disciplinary |
| **CrossRef** | Published | ❌ No | Authoritative DOI metadata |
| **PubMed** | Published (biomedical) | ❌ No | Medicine, health, biology |

**Recommended combinations:**
- `arxiv + semantic_scholar` → preprints + high-impact papers
- `openalex + pubmed` → comprehensive academic coverage
- `arxiv + openalex + pubmed` → full-spectrum search

## Quality Tags

| Source | Peer Reviewed | Tag |
|--------|--------------|-----|
| arXiv | ❌ No | `[arXiv]` |
| Journal / Conference | ✅ Yes | `[Published]` |
| PubMed | ✅ Yes | `[PubMed]` |

> ⚠️ arXiv papers are **preprints** — not peer-reviewed. Treat conclusions as provisional.

## Citation Formats

| Format | Style |
|--------|-------|
| `apa` | APA 7th Edition |
| `mla` | MLA 9th Edition |
| `ieee` | IEEE |
| `bibtex` | BibTeX (for LaTeX) |
| `ris` | RIS (for EndNote/Zotero) |
| `markdown` | Markdown with source tags |

## Search Workflow

```
1. Define topic → PICO framework
   ↓
2. Build search blocks → synonyms, MeSH terms, wildcards
   ↓
3. Run multi-source search (parallel API calls)
   ↓
4. Deduplicate by DOI / arXiv ID
   ↓
5. Validate IDs (HEAD request → doi.org)
   ↓
6. Detect cross-source conflicts (title, year, authors)
   ↓
7. Filter → year, citations, source type
   ↓
8. Format → APA / MLA / BibTeX / ...
   ↓
9. Generate literature review (timeline, keywords, summary)
```

## Configuration

Edit `scripts/lit_search.py` to add your Semantic Scholar API key:

```python
API_KEYS = {
    "semantic_scholar": "your-api-key"  # Get: https://www.semanticscholar.org/api-keys
}
```

Without a key, the free tier is used (1 req/sec). A key enables 1000 req/5 sec and avoids rate-limiting.

## Output Examples

**Markdown output (`-f markdown`):**
```
[1] **Attention Is All You Need**
* Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). *
arXiv: [1706.03762](https://arxiv.org/abs/1706.03762) [arXiv]
*Citations: 80000*

[2] **BERT: Pre-training of Deep Bidirectional Transformers**
* Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). NAACL-HLT 2019*
DOI: [10.48550/arXiv.1810.04805](https://doi.org/10.48550/arXiv.1810.04805) [Published]
*Citations: 70000*
```

**Generated review section:**
```
# Literature Review

## Statistics
- **Total Papers**: 20
- [arXiv]: 8
- [Published]: 10
- [PubMed]: 2

## Timeline
- 2024: 5 papers
- 2023: 8 papers
- 2022: 4 papers
- 2021: 3 papers
```

## Troubleshooting

| Problem | Solution |
|---------|---------|
| "Rate limit" from Semantic Scholar | Add API key, or switch to OpenAlex |
| No results | Try fewer / broader search terms |
| Too many results | Narrow date range, add AND filters |
| Invalid DOI | Check format; try CrossRef validation |
| arXiv ID not found | Use format `YYMM.NNNNN` (e.g., `2303.08774`) |
