---
name: pharmaclaw-market-intel-agent
description: |
  Fetches and analyzes FAERS (FDA Adverse Event Reporting System) data from openFDA API.
  Supports drug names and SMILES (resolves via PubChem).
  Generates: events list, yearly trends (counts), top reactions/outcomes as JSON + matplotlib bar chart PNGs.
triggers: ['faers', 'adverse event', 'safety report', 'drug side effect', 'post-market surveillance', 'reaction trend', 'clinical trial', 'clinicaltrials', 'trial pipeline', 'recruiting trial']
---

# Pharma Market Intel Agent - FAERS Query Skill

## Overview
Query real-world post-market safety data for drugs. Useful for market intel on safety profiles, emerging risks, competitor analysis.

Key outputs:
- JSON summaries (trends, top reactions/outcomes)
- PNG bar charts (yearly reports, top 10 reactions/outcomes)
- Sample recent events

**Rate limits**: openFDA ~240 req/min. Counts are fast (no full data).

## Chemistry-Query Structure
Parse user queries into this model for standardized chaining:

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ChemistryQuery:
    drug: str  # Drug name or SMILES
    query_type: str = 'faers'  # 'faers', 'pubchem', etc.
    metrics: Optional[List[str]] = None  # ['yearly_trends', 'top_reactions', 'top_outcomes', 'events']
    limit_events: int = 20
```

Example:
```json
{
  \"drug\": \"aspirin\",  // or \"CC(=O)OC1=CC=CC=C1C(=O)O\"
  \"query_type\": \"faers\",
  \"metrics\": [\"yearly_trends\", \"top_reactions\"]
}
```

## Quick Start / Workflows

### 1. Basic Query (All Metrics)
```
exec skills/pharma-market-intel-agent/scripts/query_faers.py --drug aspirin --output ./aspirin_faers
```
Generates:
- aspirin_faers/aspirin_summary.json
- *.png plots
- Recent events JSON

### 2. SMILES Input
```
exec ... --drug \"CC(=O)OC1=CC=CC=C1C(=O)O\"  # Aspirin SMILES
```
Auto-resolves to name via PubChem.

### 3. Custom Limit
```
exec ... --drug ozempic --limit-events 50 --output ozempic_analysis
```

## Chaining Examples
- **With chemistry-query**: Resolve/validate SMILES first, then FAERS.
- **pharma-tox-agent**: Feed top reactions for tox prediction.
- **pharma-ip-expansion-agent**: Check safety for IP expansion targets.
- **traction-agent**: Market risk scoring from FAERS trends.

```
# Agent workflow:
1. Parse ChemistryQuery
2. Resolve SMILES if needed (pubchempy or query_faers handles)
3. Run query_faers.py
4. Read PNGs/JSONs into response
5. Chain if metrics require
```

---

## ClinicalTrials.gov Integration

Query clinical trial data from ClinicalTrials.gov API v2. Search by drug, condition, phase, and status. No API key needed.

### Quick Start

```bash
# Search by drug
exec skills/pharma-market-intel-agent/scripts/query_trials.py --drug "sotorasib" --output ./sotorasib_trials

# Search by condition + filters
exec ... --condition "breast cancer" --phase PHASE3 --status RECRUITING --limit 10 --output ./bc_trials

# Search by both
exec ... --drug "pembrolizumab" --condition "NSCLC" --output ./pembro_trials

# SMILES input (auto-resolves via PubChem)
exec ... --drug "CC(=O)OC1=CC=CC=C1C(=O)O" --output ./aspirin_trials
```

### Outputs
- `{drug}_trials_summary.json` — Full structured summary with trials list and aggregate stats
- `{drug}_trials_by_phase.png` — Bar chart by phase
- `{drug}_trials_by_status.png` — Bar chart by status
- `{drug}_trials_timeline.png` — Timeline of trial start dates

### JSON Summary Structure
```json
{
  "drug": "sotorasib",
  "total_found": 45,
  "trials": [{"nct_id": "NCT...", "title": "...", "phase": "PHASE3", "sponsor": "Amgen", ...}],
  "stats": {"by_phase": {...}, "by_status": {...}, "top_sponsors": [...], "top_conditions": [...]}
}
```

### Chaining Examples
- **Chemistry Query → Market Intel**: Resolve SMILES, then query trials for competitive landscape
- **FAERS + Trials**: Run both scripts for a drug to get safety profile + development pipeline
- **chain_entry.py**: Use `--metrics trials` or `--metrics faers,trials` to run both in one call

---

## References
- [faers_fields.md](./references/faers_fields.md): Key FAERS fields & search syntax
- [clinicaltrials_fields.md](./references/clinicaltrials_fields.md): ClinicalTrials.gov API fields & enums
- [openFDA Drug Event API](https://open.fda.gov/apis/drug/event/)
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)

## Resources
- **scripts/query_faers.py**: FAERS query executable
- **scripts/query_trials.py**: ClinicalTrials.gov query executable
- **scripts/chain_entry.py**: Unified entry point (faers + trials)
- **assets/**: Store generated PNGs here for reuse
