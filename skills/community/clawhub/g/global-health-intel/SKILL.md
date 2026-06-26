---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_d43da77c5d8011f1abc85254006c9bbf
    ReservedCode1: egbWf4MUCtkwbvlfgC5AirwJyXZaMLsYInCI7asAwJ1Y0kNhKnIdy5LdaZ698nFDV+gUdgCIJSQcnDXRA2TvQauA2uO/QFEO0unCh63yR6irbJ04E4aLfdKehhlabnGp2mxQ56u09luMAM70w2mLsC136TTKV69bhxFyWSNvSBs6Nw+4sTo5/9SUywg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_d43da77c5d8011f1abc85254006c9bbf
    ReservedCode2: egbWf4MUCtkwbvlfgC5AirwJyXZaMLsYInCI7asAwJ1Y0kNhKnIdy5LdaZ698nFDV+gUdgCIJSQcnDXRA2TvQauA2uO/QFEO0unCh63yR6irbJ04E4aLfdKehhlabnGp2mxQ56u09luMAM70w2mLsC136TTKV69bhxFyWSNvSBs6Nw+4sTo5/9SUywg=
---



# Global Health & Biotech Intelligence

## Capabilities

| # | Capability | Input | Output |
|---|-----------|-------|--------|
| 1 | Disease Outbreak Surveillance | Country / pathogen / time range | Cases, R0, CFR, geographic spread, genomic variants, WHO/CDC advisories |
| 2 | Clinical Trial Intelligence | Drug / indication / phase / sponsor | Trial design, enrollment, endpoints, results, N sites, cross-referenced across CT.gov/EU-CTR |
| 3 | Drug Pipeline Analysis | Therapeutic area / mechanism / company | Phase progression, likelihood-of-approval, competitive landscape, patent expiry, market forecast |
| 4 | Health Systems Benchmarking | Countries (2-10) | Expenditure %GDP, UHC index, outcomes (LE/HALE), workforce density, hospital beds, digital maturity |
| 5 | Biomedical Literature Synthesis | Topic / PICOS query | Systematic review-style summary, strength-of-evidence grading, conflicting findings flagged |
| 6 | Regulatory & Reimbursement Landscape | Drug/device + jurisdiction | Approval pathway, HTA assessment, pricing & access, post-market surveillance requirements |
| 7 | Longevity & Aging Science Monitor | Intervention / pathway | Preclinical–clinical pipeline, mechanism-of-action, biomarker effects, safety signals |
| 8 | Digital Health & AI MedTech Radar | Category + region | Regulatory classification (SaMD), clinical evidence maturity, reimbursement status, competitive scan |
| 9 | Vaccine Development Dashboard | Pathogen / platform (mRNA/viral vector/etc) | Phase status, efficacy data, manufacturing capacity, cold-chain requirements, variant coverage |
| 10 | Health Policy Comparative Analysis | Policy area + countries | Legal framework, funding mechanism, implementation status, outcomes data, stakeholder positions |

## Workflow

```
User Query
  │
  ├─ [Step 1] Triage query → identify domain(s) from 9 disease categories + 4 analysis types
  │
  ├─ [Step 2] Execute parallel search across relevant sources:
  │   └─ Official sources (WHO GHO, CDC, NIH/FDA/EMA) for regulatory + epidemiological
  │   └─ Trial registries (CT.gov, EU-CTR) for clinical pipeline
  │   └─ Literature (PubMed, medRxiv) for evidence base
  │   └─ Analytics (IHME GBD, Our World in Data) for population-level metrics
  │
  ├─ [Step 3] Data fusion: cross-reference across sources, flag discrepancies
  │
  ├─ [Step 4] Quality assessment: GRADE framework for evidence, QC for data freshness (<30-day recency preferred)
  │
  ├─ [Step 5] Structured output generation per domain template
  │
  └─ [Step 6] Cite all sources with URLs, publish dates, and data vintage
```

## Output Formats

### Disease Outbreak Brief
| Field | Content |
|-------|---------|
| Pathogen/Syndrome | Name, taxonomy, known variants |
| Epidemiological Snapshot | Cases, deaths, CFR, R0/Rt, doubling time |
| Geographic Distribution | Affected regions, hot zones, importation risk |
| Countermeasures | Vaccines (available/in-development), therapeutics, diagnostics |
| Public Health Measures | WHO PHEIC status, travel advisories, NPIs |
| Sources | URLs + retrieval dates |

### Drug Pipeline Matrix
| Drug (Company) | Mechanism | Phase | Key Endpoints | PDUFA/Decision Date | LoA Est. | Notes |
|----------------|----------|-------|---------------|---------------------|----------|-------|
| ... | ... | ... | ... | ... | ... | ... |

### Health Systems Comparison Table
| Indicator | Country A | Country B | Country C | OECD Avg |
|-----------|-----------|-----------|-----------|----------|
| Health exp. %GDP | | | | |
| UHC Service Coverage Index | | | | |
| Life expectancy at birth | | | | |
| Physicians per 1,000 | | | | |
| Hospital beds per 1,000 | | | | |
| Out-of-pocket % health spend | | | | |

## Usage Guidelines

1. **Always query multiple sources** — no single database covers all needed dimensions
2. **Temporal context is critical** — include data vintage for all epidemiological and regulatory content
3. **Non-expert accessible** — translate medical terminology on first use; append glossary for complex topics
4. **Risk-appropriate framing** — distinguish between peer-reviewed consensus, preprints, and commercial forecasts
5. **Regulatory disclaimer** — this skill provides intelligence, not medical advice; include disclaimer for drug/device content
6. **Multi-language capability** — search and summarize across English, Chinese, Japanese, French, Spanish, German, Arabic

## Examples

### Example 1: Drug Pipeline Query
**User**: "What's the competitive landscape for GLP-1 receptor agonists beyond obesity?"
**Output**: Table of Phase 2/3 trials for cardiovascular, NASH/MASH, kidney disease, Alzheimer's, addiction indications; partnership/collaboration map; market size projections by indication.

### Example 2: Outbreak Intelligence
**User**: "Track the latest on H5N1 avian influenza in 2026"
**Output**: WHO/CDC case counts, mammal spillover events, vaccine stockpile status, genomic surveillance findings, pandemic risk assessment tier.

### Example 3: Health System Comparison
**User**: "Compare US, UK, and Singapore health systems on efficiency and outcomes"
**Output**: Multi-indicator comparison table; spending vs. outcomes scatter analysis; key structural differences (funding model, gatekeeping, provider payment).

---

**Data Base**: `references/health_sources.json` — 12 authoritative data sources, 9 disease domains, 8 health system countries, drug development phase reference data.
**Last Updated**: June 2026
**Free Tier**: Available. This skill aggregates public health intelligence; no proprietary data accessed.
*（内容由AI生成，仅供参考）*
