# Review Paper Writing

**Literature review paper writing assistant for systematic, multi-source academic research.**

## Features

- 🔍 **Systematic Search** — PICO framework, Boolean operators, MeSH terms, wildcards, proximity search
- 🌐 **Multi-Source Coverage** — arXiv, Semantic Scholar, OpenAlex, CrossRef, PubMed
- ✅ **DOI & ID Validation** — HEAD requests + CrossRef confirmation, conflict detection across sources
- 📄 **Citation Formatting** — APA 7th, MLA 9th, IEEE, BibTeX, RIS, Markdown
- 📊 **Auto-Generated Review** — Timeline, keyword extraction, source-quality tagging
- 🔎 **Conflict Detection** — Flags mismatches in title/year/authors for the same DOI

## Quick Start

```bash
# Search across multiple sources
python3 scripts/lit_search.py "large language model education" -n 20 --sources arxiv openalex

# APA format
python3 scripts/lit_search.py "BERT" -n 10 -f apa

# Validate DOIs
python3 scripts/lit_search.py "machine learning" --validate

# Exclude preprints, only published work
python3 scripts/lit_search.py "attention mechanism" --published-only

# Detect cross-source conflicts
python3 scripts/lit_search.py "transformer architecture" --conflicts
```

## Supported Citation Formats

| Format | Use Case |
|--------|----------|
| `apa` | Humanities, Social Sciences |
| `mla` | Literature, Languages |
| `ieee` | Engineering, Computer Science |
| `bibtex` | LaTeX / Overleaf |
| `ris` | EndNote, Zotero |
| `markdown` | Direct document use |

## Search Strategy Guide

See `references/search_strategy.md` for:
- PICO framework for question framing
- Boolean search syntax
- MeSH term usage (PubMed)
- Wildcards and truncation
- Proximity operators
- Per-database syntax reference

## API Reference

See `references/api_reference.md` for detailed API documentation on:
- Semantic Scholar Graph API
- OpenAlex API
- CrossRef API
- PubMed E-utilities
- DOI resolution & validation logic

## Requirements

- Python 3.8+
- `requests` library

```bash
pip install requests
```

## Optional: Semantic Scholar API Key

Get a free key at https://www.semanticscholar.org/api-keys

Edit `scripts/lit_search.py`:
```python
API_KEYS = {
    "semantic_scholar": "your-api-key"
}
```

## License

MIT
