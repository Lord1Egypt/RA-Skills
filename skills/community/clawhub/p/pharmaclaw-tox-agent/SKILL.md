---
name: pharmaclaw-tox-agent
description: Toxicology Agent for pharma drug safety profiling from SMILES. Computes RDKit ADMET descriptors (logP, TPSA, MW, HBD, HBA, rotatable bonds), Lipinski Rule of Five violations, Veber rule checks, QED drug-likeness score, and PAINS substructure alerts. Outputs risk classification (Low/Medium/High) with full property report. Chains from Chemistry Query (receives SMILES) and feeds into IP Expansion for safer derivative suggestions. Triggers on tox, toxicology, safety, ADMET, hepatotox, carcinogen, risk, PAINS, drug safety, Lipinski, Veber, QED.
---

# PharmaClaw Toxicology Agent

## Overview
Predictive toxicology and drug safety profiling agent for the PharmaClaw pipeline. Screens drug candidates via RDKit descriptors, rule-based filters (Lipinski Ro5, Veber), QED scoring, and PAINS alerts to flag safety risks early in the discovery process.

## Quick Start

```bash
# Analyze a compound
python scripts/tox_agent.py "CC(=O)Nc1ccc(O)cc1"

# Default (ethanol)
python scripts/tox_agent.py
```

## Capabilities

| Check | Method | Threshold |
|-------|--------|-----------|
| Lipinski Ro5 | MW, LogP, HBD, HBA | MW>500, LogP>5, HBD>5, HBA>10 |
| Veber Rules | TPSA, Rotatable Bonds | TPSA>140, RotB>10 |
| QED Score | RDKit QED module | 0-1 (higher = more drug-like) |
| PAINS Alerts | Substructure matching | Known assay interference patterns |
| Ring Analysis | Aromatic/total ring count | Complexity indicator |

## Decision Tree
- **SMILES input** → RDKit descriptor calculation → Rule-based screening
- **Lipinski violations = 0 AND PAINS = 0** → Risk: Low
- **Any violations or PAINS hits** → Risk: Medium/High
- **High risk flagged** → Recommend analogs via Chemistry Query / IP Expansion

## Output Format

```json
{
  "lipinski_viol": 0,
  "veber_viol": 0,
  "qed": 0.737,
  "pains": 0,
  "risk": "Low",
  "props": {
    "mw": 151.2,
    "logp": 1.02,
    "tpsa": 49.3,
    "hbd": 2,
    "hba": 2,
    "rotb": 1,
    "rings": 1,
    "arom": 1
  }
}
```

## Risk Classification
- **Low:** No Lipinski violations, no PAINS alerts, QED > 0.5
- **Medium:** 1-2 Lipinski violations OR low QED
- **High:** 3+ Lipinski violations, PAINS hits, or multiple Veber violations

## Chain Integration
- **Receives from:** Chemistry Query (SMILES), Pharmacology (ADME flags)
- **Feeds into:** IP Expansion (safer derivative suggestions), Synthesis (avoid toxic intermediates)
- **Cross-references:** Market Intel (FAERS adverse events for similar structures)

## Dependencies
- `rdkit-pypi` — Molecular descriptors, QED, substructure matching

## Scripts
- `scripts/tox_agent.py` — Main agent: ToxAgent class with `analyze(smiles)` method

## Limitations
- PAINS screening uses simplified substructure set (production should use full PAINS catalog)
- No Ames mutagenicity or hERG channel prediction (descriptor-based proxies planned)
- LD50 estimation not yet implemented (QSAR model planned for future version)
