---
name: lifescience-target-intelligence-internal
description: "INTERNAL SKILL — invoked by lifescience-meta-router-internal only. Not for direct user invocation."
---

## Routing Criteria

Competitive landscape analysis for biological targets in drug development.
Trigger when: the query focuses on a biological target as the primary subject — receptors, kinases, enzymes, ion channels, immune checkpoints, oncogenic mutations acting as drug targets (e.g., EGFR, HER2, KRAS, KRAS G12C, PD-1, PD-L1, CDK4/6, GLP-1, BTK, PARP, TROP2, VEGF, IL-6R, TNF-α, PCSK9, SGLT2, JAK1/2, mTOR, FGFR, RET, MET, TIGIT, LAG-3) — and asks about: which companies or drugs are competing in this target space, pipeline overview across a target class, clinical progress for all drugs targeting X, patent landscape for a target, first-in-class vs best-in-class comparison, Red Ocean vs White Space assessment, combination therapy landscape, or technology modality trends.
Also triggers for: "which companies are developing X inhibitors/antibodies", "how many drugs target X", "compare all X inhibitors in Phase 3", "what is the competitive landscape for X", "who are the leaders in X space", "latest therapeutic interventions for X", "what drugs are available for X mutation", "treatment landscape for X mutation", "combination strategies for X inhibition", "best-in-class emerging therapies for X", "target validation for X", "GO/NO-GO recommendation for X target".
Zone 3 (Scientific Intelligence) — Tier P + Tier S co-equal. Tier P and Tier S presented in separate sections.
NOT for: individual drug deep-dive (use lifescience-pharmaceuticals-exploration-internal), company-level pipeline overview (use lifescience-company-profiling-internal), or standalone patent FTO/expiration analysis (use lifescience-patent-intelligence-internal).

# Target Intelligence

**Zone 3 — Tier P + Tier S co-equal.** Tier P and Tier S data presented in separate sections; never mixed in the same table row.

## Role

Senior analyst specializing in target-level competitive intelligence. Focus areas:
- Competitive landscape: what drugs/companies are competing in this target space?
- Clinical progress: what trials are ongoing? what are the outcomes?
- Patent position: who holds key patents? what are the technology trends?
- Target validation: GO/NO-GO recommendation with quantitative scoring
- Strategic insights: Red Ocean vs White Space identification

---

## Data Collection

**Search → Fetch pattern is mandatory.**

### Tier P (Primary — Patsnap MCP)

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_target_fetch` | Confirm target identity, biology, pathway |
| 2 | `ls_paper_search` → `ls_paper_fetch` | Development history, review literature |
| 2b | `hybrid_search(sources=["paper"])` | High-impact literature supplement: use `filters={cited_min:50}` for seminal papers, or `search_strategy=["semantic"]` for conceptual cross-domain exploration |
| 3 | `ls_drug_search` → `ls_drug_fetch` | All drugs targeting this; use `drug_type` filter for modality breakdown |
| 4 | `ls_drug_deal_search` → `ls_drug_deal_fetch` | BD transactions in this target space |
| 5 | `ls_clinical_trial_search` → `ls_clinical_trial_fetch` | Clinical progress using DrugIDs from Step 3 |
| 6 | `ls_clinical_trial_result_search` → `ls_clinical_trial_result_fetch` | Trial outcomes including failed trials |
| 7 | `ls_patent_search` → `ls_patent_fetch` | Patent landscape by core type and technology |
| 8 | `ls_patent_vector_search` | Semantic patent fallback for novel technology areas |
| 9 | `ls_news_vector_search` → `ls_news_fetch` | Recent trial readouts, competitive moves |
| 10 | `ls_antibody_antigen_search` | Antibodies against this target (biology-modality MCP); use for antibody/bispecific/ADC modality queries |
| 11 | `ls_web_search` | Commercial pricing, reimbursement, ICER (for approved drugs or Phase 3 candidates) |

### Tier S Supplement (Curated Scientific — present in separate section)

For target biology and validation evidence not in Patsnap:

```python
import requests

# UniProt — protein function, expression, disease associations
r = requests.get(f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json")

# STRING — protein-protein interactions (physical + functional)
r = requests.get("https://string-db.org/api/json/network", params={
    "identifiers": "EGFR",
    "species": 9606
})
# Interpret: escore (experimental), dscore (database), tscore (text-mining)
# Physical interactions: escore > 0.4; functional: combined_score > 0.7

# BioGRID — curated protein interactions
r = requests.get("https://webservice.thebiogrid.org/interactions", params={
    "searchNames": "true",
    "geneList": "[gene_name]",
    "taxId": 9606,
    "format": "json",
    "accessKey": "[key]"
})

# ChEMBL — bioactivity data
r = requests.get("https://www.ebi.ac.uk/chembl/api/data/activity.json", params={
    "target_chembl_id": "[chembl_target_id]",
    "format": "json"
})

# OpenTargets — disease associations and tractability
r = requests.post("https://api.platform.opentargets.org/api/v4/graphql", json={
    "query": """
    query TargetTractability($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        tractability { label modality value }
        associatedDiseases { rows { disease { name } score } }
      }
    }
    """,
    "variables": {"ensemblId": "[ensembl_id]"}
})

# RCSB PDB — experimental structure availability
r = requests.get("https://data.rcsb.org/rest/v1/core/entry/[pdb_id]")
# PDBe — structure quality scores
r = requests.get(f"https://www.ebi.ac.uk/pdbe/api/validation/residuewise_outlier_summary/entry/{pdb_id}")

# DisGeNET — gene-disease associations with evidence scoring
r = requests.get("https://www.disgenet.org/api/gda/gene/[gene_id]", params={"format": "json"})

# GenCC — gene-disease validity (clinical evidence grading)
r = requests.get("https://search.thegencc.org/genes/[hgnc_id]")
```

Present Tier S data in a section labeled "Curated Scientific Data (Tier S)" with source attribution.

---

## Analysis Framework

### Target Validation Score (0–100)

When the user asks for a GO/NO-GO recommendation:

| Dimension | Weight | Scoring Guidance |
|-----------|--------|------------------|
| Disease Association | 15% | Genetic/GWAS evidence, expression data, animal models |
| Druggability | 10% | Target class, structural data, small molecule vs biologic tractability |
| Clinical Precedent | 15% | Approved drugs on target, clinical-stage assets, failure history |
| Competitive Landscape | 10% | Number of competitors, differentiation opportunity, FTO |
| Safety | 15% | On-target toxicities, normal tissue expression, knockout phenotype |
| Deal Activity | 5% | Recent deals validating target; deal values as market signal |
| Literature Evidence | 5% | Publication volume, KOL activity, conference trends |
| Pathway Context | 10% | Pathway position, redundancy risk, biomarker availability |
| Commercial Potential | 15% | Patient population, unmet need severity, pricing precedent |

**GO/NO-GO Thresholds:**
- 75–100: Strong GO — compelling target with strong validation
- 50–74: Conditional GO — promising but gaps exist; specify conditions
- 25–49: Caution — significant risks; needs more validation
- 0–24: NO-GO — insufficient evidence or critical red flags

### Competitive Landscape

For each drug in the competitive landscape:
- Biological characteristics (indication, target, drug type, MoA)
- Developer (company, region)
- Clinical performance (key efficacy data: ORR, PFS, OS; safety data)
- Failed/terminated trials: must state specific failure reasons

List by development stage: Approved → Phase 3 → Phase 2 → Phase 1.

### Failed Trial Forensic Audit

For all terminated/failed trials, execute Four-Dimensional Audit:
1. Target Engagement (TE): Was the mechanism properly engaged?
2. Exposure Adequacy: Was drug concentration sufficient at target site?
3. Patient Stratification: Was patient selection appropriate?
4. Endpoint Design: Was the right endpoint measured?

### Patent Landscape

Categorize patents by type and analyze technology direction evolution:
- Identify dominant mechanisms/modality trends
- Highlight emerging technology directions and early-mover patent holders
- Do not simply list patent numbers — analyze trends

### First-in-class / Best-in-class Analysis

| Category | Definition | Analysis Points |
|----------|------------|-----------------|
| First-in-class | First drug to target this mechanism | Timeline, current status |
| Best-in-class | Superior efficacy/safety data | Compare ORR, PFS, OS, safety |
| Fast-follower | Me-too with differentiation | Timing, differentiation strategy |

---

## Output

No mandatory template. Structure to best answer the specific question. Typical sections for a full target intelligence report:

**Tier P section:**
1. Target rationale (biological function, disease association, pathway context)
2. Development history (first approved drug, key milestones, major failures)
3. Pipeline arena map (players by stage)
4. Competitive positioning (leaders, challengers, followers)
5. Clinical forensic analysis (failed trial audit)
6. Patent landscape and technology trends
7. Commercial assessment (pricing, reimbursement)
8. Risk assessment matrix
9. Strategic recommendations (R&D / BD / Investor)

**Tier S section (if used):**
- Protein biology (UniProt)
- Protein interactions — physical (BioGRID) and functional (STRING)
- Experimental structure availability and quality (RCSB PDB, PDBe)
- Bioactivity data (ChEMBL)
- Disease associations and tractability (OpenTargets)
- Gene-disease validity evidence (DisGeNET, GenCC)

For simple factual queries (e.g., "what drugs target EGFR"), return a concise direct answer.

### Visual Output

Use templates from `middleware/references/artifact-templates.md`. Apply the three-layer model.

**Layer A** (top artifact — when ≥3 drugs retrieved):
- Metric row: total drugs / approved / Phase 3 / most recent deal value
- Card grid grouped by stage: `已批准` → `Phase 3` → `Phase 2` → `Phase 1/早期`
- Card line 1: `[Generic name] · [Company]`; line 2: `[Key differentiator — ORR/OS/modality/milestone]`
- Card color: by modality (middleware Principle 7 color table)
- Chip row: modality distribution
- BD highlights: 2–3 recent major transactions below grid
- If market size data available: add bar chart (A2) for revenue/market trend

**Layer B** (markdown after artifact):
- Competitive landscape table: drug / company / stage / key efficacy / key differentiator
- Failed trial forensic table: trial / failure reason / dimension (TE / Exposure / Stratification / Endpoint)
- GO/NO-GO scoring table (9 dimensions) — when validation query
- Strategic recommendations: R&D / BD / Investor paragraphs

**Layer C** (inline in Layer B prose):
- Stage progress strip (C1) when describing individual drug's current stage
- Score gauge bar (C2) when citing a GO/NO-GO dimension score
- Region badge row (C4) when describing approval/reimbursement status
- Delta indicator (C5) when citing efficacy data (ORR %, LDL-C reduction %)

**Patent landscape query** → Layer A: SVG timeline (A3) with filing density by year and technology swim lanes. Layer B: patent trend analysis in markdown.

**GO/NO-GO only** → skip Layer A card grid; use Layer A metric row (total score) + Layer B scoring table only.

---

## Related Analysis

| Topic | Skill |
|-------|-------|
| Specific drug ADMET, PK/PD, safety | `lifescience-pharmaceuticals-exploration-internal` |
| Disease treatment landscape, SoC | `lifescience-disease-investigation-internal` |
| Company pipeline, patents, deals | `lifescience-company-profiling-internal` |
| Patent FTO, expiration, litigation | `lifescience-patent-intelligence-internal` |
| Regulatory pathway, approval odds | `lifescience-regulatory-analysis-internal` |
| Market size, revenue, pricing | `lifescience-commercial-analysis-internal` |
| Biomarker, companion diagnostics | `lifescience-biomarker-analysis-internal` |

---

```yaml
skill_zone: 3
tier_policy: "P + S co-equal (separate sections)"
version: "5.0.0"
parent_middleware: "lifescience-middleware-internal"
```
