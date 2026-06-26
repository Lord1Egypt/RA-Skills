# Medical Literature Search — PubMed

Search and synthesize biomedical literature using the NCBI PubMed E-utilities API (free, no API key required).

## Quick Search

Search for papers on a topic:
```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=YOUR_QUERY&retmax=10&retmode=json&sort=relevance"
```

## Common Medical Search Patterns

| Pattern | Example Query |
|---------|---------------|
| Drug efficacy | `(oseltamivir OR tamiflu) AND (influenza) AND (randomized controlled trial[pt])` |
| Treatment guidelines | `diabetes type 2 management guideline[tiab]` |
| Adverse drug reactions | `metformin AND (lactic acidosis OR adverse effects[sh])` |
| Meta-analyses | `(aspirin) AND (meta-analysis[pt]) AND (cardiovascular)` |
| Clinical trials | `immunotherapy AND (cancer) AND (clinical trial[pt])` |
| COVID-19 research | `covid-19 OR sars-cov-2 AND (treatment OR therapy)` |

## Evidence Quality Assessment

- 🟢 **RCT / Meta-analysis** — 高质量随机对照试验或荟萃分析
- 🔵 **Cohort study** — 队列研究
- 🟡 **Case-control** — 病例对照研究
- ⚠️ **Case report / Expert opinion** — 个案报道或专家意见

## Usage

Triggered by: `search literature`, `find papers`, `PubMed`, `查文献`, `搜论文`, `找临床研究`, `药物证据`