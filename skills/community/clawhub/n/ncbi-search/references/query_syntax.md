# PubMed Query Syntax Guide

## Quick Reference

| Field | Syntax | Example |
|-------|--------|---------|
| Title | `[Title]` or `[ti]` | `Alzheimer[ti]` |
| Abstract | `[Abstract]` or `[ab]` | `treatment[ab]` |
| Title/Abstract | `[Title/Abstract]` or `[tiab]` | `dementia[tiab]` |
| MeSH | `[MeSH]` or `[mh]` | `"Cerebrovascular Circulation"[mh]` |
| Author | `[Author]` or `[au]` | `Smith J[au]` |
| Journal | `[Journal]` or `[ta]` | `Nature[ta]` |
| Year | `[PDat]` | `2020:2025[PDat]` |
| PMID | `[PMID]` | `12345678[PMID]` |
| DOI | `[DOI]` | `10.1038/s12345[DOI]` |

## Boolean Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `AND` | Both must appear | `Alzheimer AND dementia` |
| `OR` | Either may appear | `Alzheimer OR dementia` |
| `NOT` | Exclude term | `Alzheimer NOT review` |

**Operator Precedence**: NOT > AND > OR

Use parentheses to group: `(Alzheimer OR dementia) AND treatment`

## Date Filters

### Publication Date Range
```
2020:2025[PDat]        # 2020 to 2025
2024/01/01:2024/12/31[PDat]  # Specific date range
```

### Relative Dates (use script options)
```bash
--years 5    # Last 5 years
--years 1    # Last 1 year
```

## Article Type Filters

| Type | Query Syntax |
|------|-------------|
| Review | `Review[pt]` |
| Clinical Trial | `Clinical Trial[pt]` |
| Randomized Controlled Trial | `Randomized Controlled Trial[pt]` |
| Meta-Analysis | `Meta-Analysis[pt]` |
| Case Report | `Case Reports[pt]` |
| Editorial | `Editorial[pt]` |
| Letter | `Letter[pt]` |
| Practice Guideline | `Practice Guideline[pt]` |

**Use `--type` option for convenience:**
```bash
--type review
--type clinical_trial
```

## MeSH Terms

MeSH (Medical Subject Headings) are controlled vocabulary terms assigned by NLM indexers.

### Search MeSH Terms
```
"Cerebrovascular Circulation"[MeSH]
"Alzheimer Disease"[MeSH]
```

### MeSH Subheadings
```
"Alzheimer Disease/therapy"[MeSH]
"Alzheimer Disease/pathology"[MeSH]
```

### MeSH Qualifiers
| Qualifier | Use |
|-----------|-----|
| `/therapy` | Treatment approaches |
| `/diagnosis` | Diagnostic methods |
| `/pathology` | Disease mechanisms |
| `/etiology` | Causes |
| `/epidemiology` | Population studies |
| `/genetics` | Genetic aspects |

## Author Search

### Last Name Only
```
Smith[Author]
```

### Last Name + Initial
```
Smith J[Author]
```

### Multiple Authors
```
Smith J[Author] OR Jones K[Author]
```

## Journal Search

### Journal Name
```
"Nature Medicine"[Journal]
```

### Journal Abbreviation
```
JAMA[Journal]
```

## Advanced Examples

### Recent Reviews on Topic
```
"Alzheimer disease"[MeSH] AND Review[pt] AND 2022:2025[PDat]
```

### Clinical Trials for a Condition
```
"Alzheimer disease"[MeSH] AND "Clinical Trial"[pt]
```

### Gene-Disease Association
```
APOE[Title/Abstract] AND "Alzheimer disease"[MeSH]
```

### Specific Author in Specific Journal
```
Smith J[Author] AND Nature[Journal]
```

### Exclude Article Types
```
"Alzheimer disease"[MeSH] NOT (Review[pt] OR Editorial[pt])
```

### Free Full Text Available
```
"Alzheimer disease"[MeSH] AND "free full text"[sb]
```

## Search Field Descriptions

| Tag | Full Name | Description |
|-----|-----------|-------------|
| `[ti]` | Title | Article title |
| `[ab]` | Abstract | Article abstract |
| `[tiab]` | Title/Abstract | Combined title and abstract |
| `[mh]` | MeSH Terms | Controlled vocabulary |
| `[au]` | Author | Author names |
| `[ta]` | Journal | Journal title/abbreviation |
| `[pt]` | Publication Type | Article type |
| `[dp]` | Date of Publication | Publication date |
| `[edat]` | Entrez Date | Date added to PubMed |
| `[pmid]` | PMID | PubMed ID |
| `[doi]` | DOI | Digital Object Identifier |

## Wildcards

### Truncation (`*`)
```
diabet*    # diabetes, diabetic, diabetology
```

### Phrase Search (quotes)
```
"Alzheimer disease"
```

## Tips for Better Searches

1. **Start broad, then narrow** - Begin with simple keywords, add filters as needed
2. **Use MeSH terms** - More precise than keyword searching
3. **Combine with Boolean** - Use AND/OR/NOT strategically
4. **Check synonyms** - Different authors use different terms
5. **Use parentheses** - Group related terms: `(Alzheimer OR dementia)`
6. **Limit by date** - Recent literature for current knowledge
7. **Limit by type** - Reviews for overview, trials for evidence

## Common Search Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `Alzheimer disease` | Searches all fields | `"Alzheimer disease"[Title/Abstract]` |
| `Smith` (author) | Too common | `Smith J[Author]` |
| `2024` | Searches all fields | `2024[PDat]` |
| `review` | Searches for word | `Review[pt]` |

## Resources

- PubMed Help: https://pubmed.ncbi.nlm.nih.gov/help/
- MeSH Browser: https://meshb.nlm.nih.gov/
- PubMed Advanced Search Builder: https://pubmed.ncbi.nlm.nih.gov/advanced/