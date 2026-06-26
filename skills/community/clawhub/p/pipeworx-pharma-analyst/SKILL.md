# Pipeworx Pharma Analyst

Pharma Intel MCP — Compound tools that chain ClinicalTrials.gov,

## Setup

```json
{
  "mcpServers": {
    "pharma-intel": {
      "url": "https://gateway.pipeworx.io/mcp?task=pharma%20analysis"
    }
  }
}
```

## Compound tools (start here)

These combine multiple data sources into one call:

| Tool | Description |
|------|-------------|
| `pharma_drug_profile` | Complete drug dossier in one call — FDA approvals, drug labels, adverse events, RxNorm properties, d |
| `pharma_pipeline_scan` | Clinical trial pipeline analysis — by condition (e.g., "lung cancer", "Alzheimer") or by sponsor (e. |
| `pharma_safety_report` | Drug safety assessment — adverse event reports, top reaction types, recall history, and drug-drug in |

## Individual tools

For granular queries, these are also available:

| Tool | Description |
|------|-------------|
| `ct_search` | Search clinical trials by keyword, status, phase, or sponsor. Returns study count and array of match |
| `ct_get_study` | Get full study details for a clinical trial by its NCT ID. Returns the complete protocol section inc |
| `ct_count_by_condition` | Count the number of clinical trials for a condition or disease area. Useful for landscape analysis a |
| `ct_sponsor_trials` | List clinical trials run by a specific sponsor or pharmaceutical company. Useful for pipeline analys |
| `ct_recent_updates` | Get recently updated or posted clinical trials, sorted by last update date. Good for monitoring pipe |
| `fda_drug_events` | Search FDA Adverse Event Reporting System (FAERS) for drug adverse event reports. Supports OpenFDA s |
| `fda_drug_approvals` | Search FDA drug approval records (Drugs@FDA). Find approved drugs by brand name, generic name, appli |
| `fda_drug_labels` | Search FDA drug labeling (Structured Product Labeling). Returns drug label sections including indica |
| `fda_drug_recalls` | Search FDA drug recall and enforcement actions. Find recalls by drug name, classification level, or  |
| `fda_event_counts` | Count adverse events grouped by a specific field. Powerful for signal detection — e.g., find the top |
| `rxnorm_search` | Search for drugs by name (brand or generic). Returns concept groups with RxCUI identifiers, names, s |
| `rxnorm_get_properties` | Get properties for a drug by its RxCUI (RxNorm concept ID). Returns name, synonym, term type, langua |
| `rxnorm_related` | Get related concepts for a drug — brand names, generics, ingredients, and dose forms. Useful for map |
| `rxnorm_interactions` | Check drug-drug interactions for a given RxCUI. NOTE: The NIH retired this API in January 2024 — thi |
| `rxnorm_ndc` | Get NDC (National Drug Code) identifiers for a drug by its RxCUI. NDC codes uniquely identify drug p |

## Data sources

- **Clinicaltrials**: ClinicalTrials MCP — wraps ClinicalTrials.gov API v2 (free, no auth)
- **Openfda**: OpenFDA MCP — wraps the openFDA API (free, no auth required)
- **Rxnorm**: RxNorm MCP — wraps the NLM RxNav REST API (free, no auth)

## Tips

- Start with compound tools — they handle errors and combine data automatically
- Use `ask_pipeworx` if you're unsure which tool to use
- Use `remember`/`recall` to save intermediate findings
