---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100933ddd467852f87b5ebdb4953b1ad83302b35dee534d77c9e4d2b77aeb6a7030022100a178e4aa9a3853c3961db96cad80672d35170b204f72cd4d3c9bbe24276f4fab
    ReservedCode2: 3046022100c0c972b23489f556f68ca5ac3cf8aedf2c54ad9b217827b0a7d7bf00e0586246022100bd71c30ba6a59461229481fefd338f307110ccc6b600e7ab84a1db7f9ec136cf
---

# Lifescience Target Intelligence - Detailed Reference

## Pharma Intelligence MCP Server

**MCP Server ID**: `245f3ce8-79e4-4c2a-927c-e155c293f097`
**URL**: https://open.patsnap.com/marketplace/mcp-servers/245f3ce8-79e4-4c2a-927c-e155c293f097

This MCP server provides structured search, semantic vector search, and entity retrieval for drug intelligence analysis. Total of **27 tools** available.

## Complete Tool List (27 Tools)

### Search Tools

| Tool | Description |
|------|-------------|
| `ls_drug_search` | Search drug information by drug name, target, disease, organization, development phase, or milestone date |
| `ls_clinical_trial_search` | Search registered clinical trials by study drug, control drug, target, disease, sponsor, phase, or geography |
| `ls_clinical_trial_result_search` | Search published/indexed clinical trial results by drug, target, disease, sponsor, phase, or evaluation outcome |
| `ls_paper_search` | Search academic papers by drug, target, disease, organization, journal, author, or publication year |
| `ls_paper_vector_search` | Semantic similarity search for academic papers using natural language queries |
| `ls_news_vector_search` | Semantic similarity search for news content |
| `ls_clinical_guideline_vector_search` | Semantic similarity search for clinical guidelines |
| `ls_fda_label_vector_search` | Semantic similarity search for FDA drug labels |
| `ls_epidemiology_vector_search` | Semantic similarity search for epidemiology data |
| `ls_drug_deal_search` | Search licensing, collaboration, acquisition, or option deals |
| `ls_translational_medicine_search` | Search translational medicine records by drug, target, disease, sponsor, or translation stage |
| `ls_clinical_trial_vector_search` | Semantic similarity search for clinical trials |

### Fetch Tools

| Tool | Required Params | Description |
|------|----------------|-------------|
| `ls_drug_fetch` | `drug_ids` or `drug` | Batch fetch full drug detail records |
| `ls_clinical_trial_fetch` | `trial_ids` or `registration_number` | Batch fetch full clinical trial records |
| `ls_clinical_trial_result_fetch` | `result_ids` | Batch fetch full clinical trial result records |
| `ls_paper_fetch` | `paper_ids` | Batch fetch full academic paper records |
| `ls_patent_fetch` | `patent_ids` or `pn` | Batch fetch full patent records |
| `ls_news_fetch` | `news_ids` | Batch fetch full news records |
| `ls_drug_deal_fetch` | `drug_deal_ids` | Batch fetch full drug deal records |
| `ls_target_fetch` | `target_ids` or `target` | Batch fetch full target detail records |
| `ls_disease_fetch` | `disease_ids` or `disease` | Batch fetch full disease detail records |
| `ls_organization_fetch` | `organization_ids` or `organization` | Batch fetch full organization records |
| `ls_translational_medicine_fetch` | `translational_medicine_ids` | Batch fetch full translational medicine records |

## Detailed Search Examples

### PATH 1: Target Basic Information Retrieval

```python
# Retrieve EGFR target information
ls_target_fetch(
    target=["EGFR"]
)

# Retrieve by multiple target IDs
ls_target_fetch(
    target_ids=["uuid-1", "uuid-2"]
)
```

### PATH 2: Drug Development History Literature Search

```python
# Search for target review literature
ls_paper_search(
    target=["EGFR"],
    key_word=["drug review", "inhibitor"],
    limit=20
)

# Vector search for related literature
ls_paper_vector_search(
    query="EGFR tyrosine kinase inhibitor mechanism",
    lang="EN",
    top_k=20
)

# Fetch literature abstracts
ls_paper_fetch(
    paper_ids=["paper-uuid-1", "paper-uuid-2"]
)
```

### PATH 3: Drug Search

```python
# Condition search
ls_drug_search(
    target=["EGFR"],
    disease=["non-small cell lung cancer"],
    highest_phase=["approved"],
    limit=50
)

# Search by organization
ls_drug_search(
    organization=["Pfizer", "AstraZeneca"],
    highest_phase=["phase_3", "phase_2"],
    limit=50
)

# Search by drug type
ls_drug_search(
    drug_type=["monoclonal antibody", "small molecule"],
    disease=["breast cancer"],
    limit=30
)
```

### PATH 4: Clinical Trial Search

```python
# Search clinical trials
ls_clinical_trial_search(
    drug=["Osimertinib"],
    disease=["lung cancer"],
    phase=["phase_3", "phase_2"],
    country=["US", "CN"],
    limit=30
)

# Search by target
ls_clinical_trial_search(
    target=["PD-1", "PD-L1"],
    study_status=["recruiting", "active_not_recruiting"],
    limit=50
)

# Fetch trial details
ls_clinical_trial_fetch(
    trial_ids=["trial-uuid-1", "trial-uuid-2"]
)

# Or by registration number
ls_clinical_trial_fetch(
    registration_number=["NCT12345678", "NCT87654321"]
)

# Search trial results
ls_clinical_trial_result_search(
    drug=["Pembrolizumab"],
    disease=["melanoma"],
    phase=["phase_3"],
    general_evaluation=["positive", "superiority"],
    limit=20
)

# Fetch trial results
ls_clinical_trial_result_fetch(
    result_ids=["result-uuid-1"]
)
```

### PATH 5: Patent Search

```python
# Fetch patent details
ls_patent_fetch(
    pn=["US1234567A", "EP9876543B1"]
)

# Or by patent IDs
ls_patent_fetch(
    patent_ids=["patent-uuid-1", "patent-uuid-2"]
)
```

### PATH 6: Competitive Landscape Data Collection

```python
# Collect all relevant drugs
ls_drug_search(
    target=["EGFR"],
    limit=100
)

# Filter by development status
ls_drug_search(
    target=["EGFR"],
    dev_status=["approved", "clinical"],
    limit=100
)

# Search drug deals
ls_drug_deal_search(
    target=["KRAS"],
    deal_type=["license", "collaboration"],
    deal_date_from="2021-01-01",
    limit=20
)

# Get organization info
ls_organization_fetch(
    organization=["Roche", "Novartis"]
)

# Search news
ls_news_vector_search(
    query="EGFR inhibitor clinical trial results",
    lang="EN",
    top_k=10
)
```

### Additional Tools

```python
# Clinical Guidelines
ls_clinical_guideline_vector_search(
    query="EGFR targeted therapy guidelines",
    lang="EN",
    top_k=10
)

# FDA Labels
ls_fda_label_vector_search(
    query="EGFR inhibitor label warnings",
    lang="EN",
    top_k=10
)

# Epidemiology
ls_epidemiology_vector_search(
    query="EGFR mutation prevalence lung cancer",
    lang="EN",
    top_k=10
)

# Translational Medicine
ls_translational_medicine_search(
    target=["EGFR"],
    disease=["lung cancer"],
    translation_stage=["t2", "t3"],
    limit=20
)

# Disease Information
ls_disease_fetch(
    disease=["non-small cell lung cancer"]
)
```

## Important Parameter Guidelines

### Vector Search Parameters
- `query`: Natural-language search query. **Must NOT** include meta-words like "literature", "paper", "review", "report", "patent", "drug development". Only use biology, chemistry, and pharmaceutical-related terms.
- `lang`: Language code. Allowed values: `["CN", "EN"]`. Should match the language of the user's question.
- `top_k`: Maximum number of matched chunks to return. Defaults to 20.

### Condition Search Parameters
- Use `limit` to control page size (default: 20)
- Use `offset` for pagination
- Use `List[str]` format for multi-value filters: `target=["EGFR", "HER2"]`
- Use `YYYY-MM-DD` format for date parameters

### Development Phase Values
Allowed values for `highest_phase` and `dev_status`:
- `discovery`, `preclinical`, `ind_application`, `ind_approval`
- `clinical`, `early_phase_1`, `phase_1`, `phase_1_2`, `phase_2`, `phase_2_3`, `phase_3`
- `nda_bla`, `approved`, `phase_4`
- `discontinued`, `suspended`, `withdrawn`, `pending`, `unknown`

## EUREKA_REPORT Template

This skill always delivers in REPORT mode. The final answer must follow the system `<<<EUREKA_REPORT>>>` protocol:

1. A brief summary paragraph before the report wrapper (3-4 sentences covering core findings)

2. The report body inside `<<<EUREKA_REPORT>>>...<<<END_EUREKA_REPORT>>>`

3. H1 title as the first line inside the wrapper, followed by H2 sections

4. All factual claims must use inline `<refer e_id="..." e_type="..." />` tags per the system `<REFERENCE>` protocol

### Report Structure (H2 Sections)

#### H1: {Target Name} — Drug Development Intelligence

#### H2: Executive Summary

2-4 sentences: overall competitive dynamics — market concentration, dominant modalities, clinical progress pace, and high-level opportunity assessment.

#### H2: Target Rationale & Mechanism

- Biological function and disease association
- Synthetic lethality / pathway rationale (if applicable)
- Upstream → Target Engagement → Downstream signaling chain

#### H2: Pipeline Arena Map

Mermaid `graph TD` diagram showing player tiers and pipeline stages.

#### H2: Clinical Forensic Analysis

For failed/terminated trials, execute Four-Dimensional Audit (Target Engagement, Exposure Adequacy, Patient Stratification, Endpoint Design).

#### H2: Patent Landscape & Technology Trends

Mermaid visualizations: filing volume by year, modality distribution, key patent holders.

#### H2: Risk Assessment Matrix

| Risk Category | Risk Description | Confidence | Competitive Impact | Mitigation Strategy |
|:---|:---|:---:|:---:|:---|
| Clinical Translation | e.g., Biomarker improvement ≠ clinical benefit | High | High | Implement sensitive imaging endpoints |
| Commercial Access | e.g., Pricing too high → payer restrictions | Medium | Medium | Differentiated indication pricing strategy |
| Safety/Tolerability | e.g., Off-target toxicity | High | High | Enhanced biomarker screening protocols |
| Regulatory | e.g., Endpoint not accepted by FDA | Medium | Medium | Pre-IND meeting guidance |
| Patent Defense | e.g., Limited FTO coverage | Medium | High | Pursue formulation patents |

#### H2: Commercial Access & Pricing

- Pricing benchmarks (Web Search validated)
- Reimbursement landscape
- Patient compliance assessment

#### H2: Strategic Outlook & Three-Party Recommendations

**1. R&D Strategy (研发方向)**
- Identify technical "Dead Ends": Proven failed epitopes, molecular structures with unacceptable toxicity profiles
- Recommend next-generation improvements

**2. BD & Licensing (商务/并购)**
- Identify early-stage assets with Best-in-class potential
- Assess patent defense strength
- Evaluate fair value for licensing/acquisition transactions

**3. Investor Insight (投资建议)**
- Define "Value Catalysts": Next critical data readout milestones
- Compare market cap/valuation vs. clinical progress alignment
- Risk-adjusted opportunity assessment

## Completion Gates

All must pass before delivering the final report:

- [ ] Target identity confirmed (PATH 1 executed)
- [ ] Pipeline drugs identified and categorized by stage (PATH 3 executed)
- [ ] Key clinical trials fetched with efficacy and safety data (PATH 4 executed)
- [ ] Patent landscape analyzed with technology trend (PATH 5 executed)
- [ ] Report uses `<<<EUREKA_REPORT>>>` wrapper with H1 + H2 structure
- [ ] Pipeline Arena Map (mermaid graph) generated with stage-based color coding
- [ ] The report explicitly covers: target rationale, pipeline landscape, clinical analysis, patent trends, risk matrix, commercial assessment, strategic recommendations
- [ ] Evidence Hierarchy (Level A/B/C) applied to all claims
- [ ] Risk Assessment Matrix present with mitigation strategies
- [ ] Three-Party Recommendations (R&D/BD/Investor) included
- [ ] All factual claims carry inline `<refer e_id="..." e_type="..." />` tags
- [ ] Web Search validation executed for pricing/commercial data (PATH 7)
- [ ] Forensic Audit executed for any failed trials
- [ ] If evidence is insufficient for complete analysis, deliver "Evidence Gaps + Next Evidence-Gathering Directions" instead of forcing completeness

## Guardrails

- **Evidence Integrity**: Do NOT assign higher evidence level than data supports. Mark insufficient evidence as Level C.
- **No Fabrication**: Do not invent clinical data, patent details, or pricing information. If data unavailable, state "Data not available."
- **Patient Safety**: Do not recommend dosing regimens without supporting clinical data.
- **Competitive Neutrality**: Do not favor specific companies in recommendations — base all analysis on evidence.
- **Regulatory Awareness**: Do not suggest accelerated approval pathways unless data supports it.
- **Patent FTO**: Do not suggest market entry without noting FTO risks.
- **Evidence Timeliness**: Note patent publication delays and data currency date.
- **Report Format**: Use EUREKA_REPORT wrapper — do not deliver raw data dumps.
- **Recommendation Proportionality**: Strategic recommendations must be proportional to evidence strength.
