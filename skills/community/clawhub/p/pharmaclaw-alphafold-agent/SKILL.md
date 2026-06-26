---
name: pharmaclaw-alphafold-agent
description: Compliant AlphaFold Agent for protein structure retrieval, ESMFold prediction, binding site detection, and RDKit ligand docking. Fetches public PDB/AlphaFold DB structures, predicts folds via ESMFold (HuggingFace), identifies binding pockets, and performs basic molecular docking. Chains from Chemistry Query (receives SMILES for docking) and feeds into IP Expansion and Catalyst Design. Triggers on alphafold, fold, PDB, docking, structure, protein, binding site, pocket, UniProt, KRAS, target.
---

# PharmaClaw AlphaFold Agent

## Overview
Protein structure retrieval and ligand docking agent for the PharmaClaw drug discovery pipeline. Fetches experimental structures from RCSB PDB and predicted structures from AlphaFold DB, detects binding sites, and performs conformer-based docking with RDKit.

## Quick Start

```bash
# Fetch structure and dock a ligand
python scripts/alphafold_agent.py '{"uniprot": "P01116", "smiles": "CC(=O)Nc1ccc(O)cc1"}'

# Structure retrieval only
python scripts/alphafold_agent.py '{"uniprot": "P01116"}'
```

## Capabilities

| Feature | Method | Source |
|---------|--------|--------|
| Structure Fetch | RCSB Search API + AlphaFold DB | Public PDB files |
| Fold Prediction | ESMFold via HuggingFace | Sequence → 3D structure |
| Binding Sites | Pocket detection | Residue-level pockets |
| Ligand Docking | RDKit conformer generation | SMILES → affinity score |

## Decision Tree
- **UniProt ID provided?** → Fetch from RCSB PDB / AlphaFold DB
- **FASTA sequence provided?** → Predict fold via ESMFold
- **SMILES provided?** → Dock ligand into detected binding pocket
- **No structure found?** → Fall back to ESMFold prediction

## Input Format

```json
{
  "uniprot": "P01116",
  "smiles": "CC(=O)Nc1ccc(O)cc1",
  "fasta": "path/to/sequence.fasta"
}
```

## Output Format

```json
{
  "pdb": "1abc.pdb",
  "sites": [{"res": "G12", "pocket_vol": 150}],
  "docking": {"affinity": -15.2, "viz": "docked.png"},
  "compliance": "Public AlphaFold 2 DB/ESMFold (commercial OK)"
}
```

## Chain Integration
- **Receives from:** Chemistry Query (SMILES for docking), Literature (target proteins)
- **Feeds into:** IP Expansion (novel binding modes), Catalyst Design (structure-guided synthesis)

## Dependencies
- `rdkit-pypi` — Conformer generation and molecular descriptors
- `biopython` — PDB parsing and FASTA sequence handling
- `requests` — API calls to RCSB and AlphaFold DB

## Compliance
Uses only publicly available protein structures (RCSB PDB, AlphaFold DB) and open-source prediction (ESMFold). All data sources are commercially permissible. No proprietary AlphaFold 3 server calls.

## Scripts
- `scripts/alphafold_agent.py` — Main agent: fetch, predict, detect sites, dock

## Limitations
- Docking uses RDKit conformer scoring (not full physics-based docking like Vina)
- ESMFold prediction requires significant compute for large proteins
- Binding site detection is simplified; production use should integrate fpocket or P2Rank
