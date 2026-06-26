---
name: pharmaclaw-catalyst-design
description: Organometallic catalyst recommendation and novel ligand design for drug synthesis reactions. Recommends catalysts (Pd, Ru, Rh, Ir, Ni, Cu, Zr, Fe) for reaction types (Suzuki, Heck, Buchwald-Hartwig, metathesis, hydrogenation, click, etc.) from curated database with scoring. Designs novel ligand variants via RDKit (steric, electronic, bioisosteric modifications). Chains from chemistry-query/retrosynthesis (receives reaction type + substrate) and feeds into IP Expansion (novel ligands as patentable inventions). Triggers on catalyst, ligand, organometallic, cross-coupling catalyst, reaction conditions, catalyst selection, ligand design, cone angle, bite angle, phosphine, NHC, palladium catalyst, ruthenium catalyst.
---

# Catalyst Design Agent v1.0.0

## Overview

Recommends organometallic catalysts for drug synthesis steps and designs novel ligand modifications. Two core workflows: **recommend** (find the right catalyst) and **design** (create novel ligand variants).

## Quick Start

```bash
# Recommend catalysts for a Suzuki coupling
python scripts/catalyst_recommend.py --reaction suzuki

# Recommend with constraints (prefer cheap, earth-abundant)
python scripts/catalyst_recommend.py --reaction "C-N coupling" --constraints '{"prefer_earth_abundant": true, "max_cost": "medium"}'

# Design novel ligand variants from PPh3
python scripts/ligand_designer.py --scaffold PPh3 --strategy all --draw

# Full chain: reaction → catalyst → ligand optimization
python scripts/chain_entry.py --input-json '{"reaction": "suzuki", "context": "retrosynthesis"}'
```

## Scripts

### `scripts/catalyst_recommend.py`
Scores and ranks catalysts from curated database (12 catalysts, 28 reaction types).

```
--reaction <type>              Required. e.g., suzuki, metathesis, C-N coupling, hydrogenation
--substrate <SMILES>           Optional. Substrate context
--constraints <JSON>           Optional. {prefer_metal, max_cost, prefer_earth_abundant}
--enantioselective             Flag. Prioritize chiral catalysts
```

Scoring (0-100): reaction match (50), cost (15), metal preference (10), enantioselectivity (10), loading efficiency (5), advantages (5), earth-abundance (5).

### `scripts/ligand_designer.py`
Generates novel ligand variants via three strategies:

| Strategy | Method | Output |
|----------|--------|--------|
| steric | Add methyl/iPr/tBu to aromatic rings | Modified SMILES + properties |
| electronic | Add OMe/F/CF3 substituents | Modified SMILES + properties |
| bioisosteric | P→NHC, phenyl→pyridyl, phosphine→phosphite | Conceptual suggestions + rationale |

```
--scaffold <SMILES|name>       Required. PPh3, NHC_IMes, NHC_IPr, PCy3, dppe, dppp, or raw SMILES
--strategy <type>              steric|electronic|bioisosteric|all (default: all)
--draw                         Generate 2D grid PNG of variants
--output <path>                Save JSON results to file
```

### `scripts/chain_entry.py`
Standard PharmaClaw chain interface. Accepts JSON, routes to recommend/design/both.

Input keys: `reaction`, `scaffold`/`ligand`, `substrate`/`smiles`, `constraints`, `enantioselective`, `strategy`, `draw`, `context`

If only `reaction` is given, also auto-runs ligand optimization on the top recommended catalyst's ligand.

## Chaining

| From | Input | To | Output |
|------|-------|----|--------|
| Chemistry Query / Retrosynthesis | Reaction type needed for a synthesis step | **Catalyst Design** | Ranked catalysts + conditions |
| **Catalyst Design** | Top catalyst ligand SMILES | Ligand Designer | Novel ligand variants |
| **Catalyst Design** | Novel ligand SMILES | IP Expansion | Patent landscape check |
| **Catalyst Design** | Recommended conditions | Chemistry Query | Forward reaction simulation |

## Database

`references/catalyst_database.json` — 12 catalysts, 8 metals, 28 reaction types. Includes SMILES, conditions, loading ranges, cost ratings, advantages/limitations, and literature DOIs.

Expandable: add entries following the existing schema.

## Ligand Aliases

PPh3, PCy3, dppe, dppp, NHC_IMes, NHC_IPr — resolved automatically to SMILES.
