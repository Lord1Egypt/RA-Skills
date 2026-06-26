---
name: pharmaclaw-cheminformatics
description: Advanced cheminformatics agent for 3D molecular analysis, pharmacophore mapping, format conversion, RECAP fragmentation, and stereoisomer enumeration. The "senior cheminformatician" upgrade to Chemistry Query. Use for 3D conformer generation/ensembles (ETKDG + MMFF/UFF), pharmacophore feature extraction and fingerprints, molecular format conversion (SMILES/SDF/MOL/InChI/PDB/XYZ), RECAP retrosynthetic fragmentation for library design, stereoisomer enumeration (R/S, E/Z), and cheminformatics profiling. Chains from chemistry-query (receives SMILES) and feeds into pharmacology, catalyst-design, ip-expansion. Triggers on conformer, 3D structure, pharmacophore, SDF, MOL file, format conversion, RECAP, fragmentation, stereoisomer, chirality, enantiomer, cheminformatics, library design, building blocks, docking prep.
---

# Cheminformatics Agent v1.0.0

## Overview

Advanced cheminformatics toolkit for 3D molecular analysis and drug development workflows. Extends Chemistry Query (which handles 2D lookup/properties/visualization) with predictive and structural capabilities that require 3D reasoning.

**Chemistry Query** = "What is this molecule?" (2D, lookup, descriptors)
**Cheminformatics** = "What can this molecule become?" (3D, conformers, pharmacophores, fragments, stereoisomers)

## Scripts

### `scripts/conformer_gen.py`
3D conformer ensemble generation using ETKDG with MMFF/UFF optimization.

```
--smiles <SMILES> --action <generate|ensemble|best> [--num_confs N] [--optimize mmff|uff|none] [--energy_window F] [--prune_rms F] [--output file.sdf]
```

| Action | Description |
|--------|-------------|
| generate | Generate N conformers with energies and RMSD matrix |
| ensemble | Same as generate + write SDF file |
| best | Find lowest-energy conformer with 3D coordinates |

```bash
python scripts/conformer_gen.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --action generate --num_confs 20
python scripts/conformer_gen.py --smiles "CCO" --action best --output best.sdf
python scripts/conformer_gen.py --smiles "c1ccccc1" --action ensemble --num_confs 50 --output benzene_confs.sdf
```

Output includes: conformer energies (kcal/mol), relative energies, convergence status, RMSD matrix (top 20), SDF file.

### `scripts/format_converter.py`
Convert between molecular file formats.

```
--smiles <SMILES> | --input <file> --to <format> [--output file] [--batch] [--name label]
```

Supported formats: `smiles`, `sdf`, `mol`, `inchi`, `inchikey`, `pdb`, `xyz`

```bash
python scripts/format_converter.py --smiles "CCO" --to sdf --output ethanol.sdf
python scripts/format_converter.py --smiles "CCO" --to inchi
python scripts/format_converter.py --input mols.sdf --to smiles --batch
python scripts/format_converter.py --smiles "CCO" --to pdb --output ethanol.pdb
```

Batch mode reads multi-molecule SDF files. All 3D formats auto-generate and optimize conformers.

### `scripts/pharmacophore.py`
Pharmacophore feature extraction, fingerprints, and comparison.

```
--smiles <SMILES> --action <features|fingerprint|compare|map> [--target_smiles "smi1,smi2"] [--output file.png]
```

| Action | Description |
|--------|-------------|
| features | Extract 3D pharmacophoric features (HBD, HBA, aromatic, hydrophobic, ionizable) with coordinates |
| fingerprint | Generate Gobbi 2D pharmacophore fingerprint |
| compare | Pairwise pharmacophore similarity (Tanimoto) across multiple molecules |
| map | Generate color-coded pharmacophore PNG (green=donor, red=acceptor, yellow=aromatic, blue=hydrophobic) |

```bash
python scripts/pharmacophore.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --action features
python scripts/pharmacophore.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --action map --output pharm.png
python scripts/pharmacophore.py --target_smiles "CCO,CC(=O)O,c1ccccc1" --action compare
```

### `scripts/recap_fragment.py`
RECAP (Retrosynthetic Combinatorial Analysis Procedure) fragmentation at synthetically accessible bonds (amide, ester, amine, urea, ether, olefin, sulfonamide, etc.).

```
--smiles <SMILES> --action <fragment|leaves|tree|common_fragments> [--target_smiles "smi1,smi2"] [--max_depth N]
```

| Action | Description |
|--------|-------------|
| fragment | All RECAP fragments with metadata |
| leaves | Terminal building blocks only (for library design) |
| tree | Hierarchical decomposition tree |
| common_fragments | Shared fragments across multiple molecules (common scaffolds) |

```bash
python scripts/recap_fragment.py --smiles "CC(=O)Nc1ccc(O)cc1" --action fragment
python scripts/recap_fragment.py --smiles "CC(=O)Nc1ccc(O)cc1" --action leaves
python scripts/recap_fragment.py --target_smiles "CC(=O)Nc1ccc(O)cc1,CC(=O)Nc1ccccc1" --action common_fragments
```

Use case: Leaf fragments → building blocks for combinatorial library enumeration. Common fragments across a compound series → shared pharmacophoric scaffolds.

### `scripts/stereoisomers.py`
Stereoisomer enumeration and analysis (chiral centers R/S, double bond E/Z).

```
--smiles <SMILES> --action <enumerate|analyze|compare> [--max_isomers N] [--only_unassigned]
```

| Action | Description |
|--------|-------------|
| enumerate | Generate all stereoisomers with configurations |
| analyze | Count chiral centers and stereo bonds without enumerating |
| compare | Compare properties across all stereoisomers (drug dev relevance) |

```bash
python scripts/stereoisomers.py --smiles "C(F)(Cl)Br" --action enumerate
python scripts/stereoisomers.py --smiles "CC=CC" --action analyze
python scripts/stereoisomers.py --smiles "OC(F)(Cl)Br" --action compare
```

Drug relevance: FDA requires characterization of each stereoisomer for chiral drug candidates. Flags meso forms and provides R/S assignments.

### `scripts/chain_entry.py`
Standard agent chain interface. Runs all 5 modules on a SMILES input.

```bash
python scripts/chain_entry.py --input-json '{"smiles": "CC(=O)Nc1ccc(O)cc1", "context": "user"}'
python scripts/chain_entry.py --input-json '{"smiles": "CCO", "actions": ["conformers", "pharmacophore"]}'
```

Input JSON fields:
- `smiles` (required): Input SMILES
- `context`: Chain context string
- `actions`: Array to run subset — `["conformers", "pharmacophore", "recap", "stereoisomers", "formats"]`
- `output_dir`: Directory for SDF/PNG output files

Output schema:
```json
{
  "agent": "cheminformatics",
  "version": "1.0.0",
  "smiles": "<canonical>",
  "status": "success|error",
  "report": {
    "conformers": {...},
    "pharmacophore": {...},
    "recap": {...},
    "stereoisomers": {...},
    "formats": {...}
  },
  "risks": [],
  "warnings": [],
  "viz": ["path/to/file.sdf", "path/to/pharmacophore_map.png"],
  "recommend_next": ["pharmacology", "catalyst-design", "ip-expansion"],
  "confidence": 0.9,
  "timestamp": "ISO8601"
}
```

## Chaining

| From | To | What passes |
|------|----|-------------|
| Chemistry Query → | **Cheminformatics** | SMILES + basic properties |
| **Cheminformatics** → | Pharmacology | SMILES + pharmacophore profile for ADME context |
| **Cheminformatics** → | Catalyst Design | 3D conformer data for catalyst selection |
| **Cheminformatics** → | IP Expansion | Stereoisomers as patentable variants |
| **Cheminformatics** → | Toxicology | Fragment analysis for structural alerts |

## Dependencies

- Python ≥ 3.10
- rdkit-pypi
- Pillow (for pharmacophore map PNG)
- numpy
