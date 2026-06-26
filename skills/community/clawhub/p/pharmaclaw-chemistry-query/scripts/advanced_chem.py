#!/usr/bin/env python3
"""
Advanced cheminformatics features for PharmaClaw Chemistry Query Agent v2.0.0
Features: standardize, descriptors, scaffold, mcs, mmpa, chemspace
"""

import argparse
import json
import sys
import os
import re
import warnings
warnings.filterwarnings("ignore")

from rdkit import Chem
from rdkit.Chem import (
    Descriptors, AllChem, Draw, BRICS,
    rdFMCS, rdMMPA,
    rdMolDescriptors, Scaffolds, QED,
    rdRGroupDecomposition
)
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.Chem import RDConfig
from rdkit import DataStructs
import numpy as np


def _sanitize_input(value, label="input", max_len=2000):
    if not isinstance(value, str):
        raise ValueError(f"Invalid {label}: expected string")
    if '\x00' in value:
        raise ValueError(f"Invalid {label}: null bytes not allowed")
    if len(value) > max_len:
        raise ValueError(f"Invalid {label}: exceeds {max_len} character limit")
    return value.strip()


def _sanitize_output_path(path, allowed_dir=None):
    path = os.path.normpath(path)
    if '..' in path.split(os.sep):
        raise ValueError("Invalid output path: path traversal not allowed")
    if os.path.isabs(path):
        if allowed_dir:
            real_path = os.path.realpath(path)
            real_allowed = os.path.realpath(allowed_dir)
            if not real_path.startswith(real_allowed + os.sep) and real_path != real_allowed:
                raise ValueError(f"Invalid output path: must be within {allowed_dir}")
        else:
            raise ValueError("Invalid output path: absolute paths not allowed without allowed_dir")
    _, ext = os.path.splitext(path)
    if ext.lower() not in ('.png', '.svg', '.json', '.xyz', '.txt', '.csv', ''):
        raise ValueError(f"Invalid output extension: {ext}")
    return path


def get_mol(smiles):
    smiles = _sanitize_input(smiles, "SMILES")
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    return mol


def parse_smiles_list(smiles_str):
    """Parse comma-separated SMILES into list of (smiles, mol) tuples."""
    smiles_str = _sanitize_input(smiles_str, "SMILES list", max_len=50000)
    smiles_list = [s.strip() for s in smiles_str.split(',') if s.strip()]
    if len(smiles_list) < 1:
        raise ValueError("Need at least 1 SMILES")
    results = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {smi}")
        results.append((Chem.MolToSmiles(mol), mol))
    return results


# ============================================================
# 1. STANDARDIZE - Molecular Standardization & Tautomers
# ============================================================
def action_standardize(smiles):
    mol = get_mol(smiles)
    canonical = Chem.MolToSmiles(mol, isomericSmiles=True)

    # Largest fragment (strip salts)
    lfc = rdMolStandardize.LargestFragmentChooser()
    parent = lfc.choose(mol)
    parent_smi = Chem.MolToSmiles(parent, isomericSmiles=True)

    # Uncharger - neutralize
    uncharger = rdMolStandardize.Uncharger()
    neutralized = uncharger.uncharge(parent)

    # Normalize
    normalizer = rdMolStandardize.Normalizer()
    standardized = normalizer.normalize(neutralized)
    standardized_smi = Chem.MolToSmiles(standardized, isomericSmiles=True)

    # Tautomer enumeration
    enumerator = rdMolStandardize.TautomerEnumerator()
    tautomers = list(enumerator.Enumerate(standardized))
    tautomer_smiles = list(set(
        Chem.MolToSmiles(t, isomericSmiles=True) for t in tautomers
    ))[:20]  # cap at 20

    # Canonical tautomer
    canon_taut = enumerator.Canonicalize(standardized)
    canon_taut_smi = Chem.MolToSmiles(canon_taut, isomericSmiles=True)

    # Stereochemistry info
    chiral_centers = Chem.FindMolChiralCenters(standardized, includeUnassigned=True)
    charge = Chem.GetFormalCharge(standardized)

    return {
        "action": "standardize",
        "input_smiles": smiles,
        "canonical_smiles": canonical,
        "parent_smiles": parent_smi,
        "standardized_smiles": standardized_smi,
        "canonical_tautomer": canon_taut_smi,
        "tautomers": sorted(tautomer_smiles),
        "num_tautomers": len(tautomer_smiles),
        "chiral_centers": [{"atom_idx": c[0], "chirality": c[1]} for c in chiral_centers],
        "num_chiral_centers": len(chiral_centers),
        "formal_charge": charge,
        "num_atoms": standardized.GetNumAtoms(),
        "num_heavy_atoms": standardized.GetNumHeavyAtoms()
    }


# ============================================================
# 2. DESCRIPTORS - Extended Molecular Descriptors (200+)
# ============================================================
def action_descriptors(smiles, descriptor_set="all"):
    mol = get_mol(smiles)
    canonical = Chem.MolToSmiles(mol, isomericSmiles=True)

    # Calculate all RDKit descriptors
    all_descs = {}
    for name, func in Descriptors.descList:
        try:
            val = func(mol)
            if val is not None and not (isinstance(val, float) and (np.isnan(val) or np.isinf(val))):
                all_descs[name] = round(val, 6) if isinstance(val, float) else val
        except Exception:
            pass

    # Categorize descriptors
    physical_keys = [
        'ExactMolWt', 'MolWt', 'HeavyAtomMolWt', 'MolLogP', 'MolMR',
        'TPSA', 'LabuteASA', 'NumValenceElectrons', 'MaxPartialCharge',
        'MinPartialCharge', 'MaxAbsPartialCharge', 'MinAbsPartialCharge',
        'FpDensityMorgan1', 'FpDensityMorgan2', 'FpDensityMorgan3'
    ]
    druglike_keys = [
        'MolLogP', 'MolWt', 'TPSA', 'NumHDonors', 'NumHAcceptors',
        'NumRotatableBonds', 'NumAromaticRings', 'RingCount',
        'FractionCSP3', 'HeavyAtomCount', 'NHOHCount', 'NOCount',
        'NumAliphaticCarbocycles', 'NumAliphaticHeterocycles',
        'NumAliphaticRings', 'NumAromaticCarbocycles',
        'NumAromaticHeterocycles', 'NumHeteroatoms',
        'NumSaturatedCarbocycles', 'NumSaturatedHeterocycles',
        'NumSaturatedRings'
    ]
    topological_keys = [
        'BertzCT', 'Chi0', 'Chi0n', 'Chi0v', 'Chi1', 'Chi1n', 'Chi1v',
        'Chi2n', 'Chi2v', 'Chi3n', 'Chi3v', 'Chi4n', 'Chi4v',
        'HallKierAlpha', 'Ipc', 'Kappa1', 'Kappa2', 'Kappa3',
        'BalabanJ'
    ]

    def filter_descs(keys):
        return {k: all_descs[k] for k in keys if k in all_descs}

    # QED and SA Score
    try:
        qed_score = round(QED.qed(mol), 4)
    except Exception:
        qed_score = None

    try:
        from rdkit.Chem import RDConfig
        sa_path = os.path.join(RDConfig.RDContribDir, 'SA_Score', 'sascorer.py')
        if os.path.exists(sa_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location("sascorer", sa_path)
            sascorer = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(sascorer)
            sa_score = round(sascorer.calculateScore(mol), 4)
        else:
            sa_score = None
    except Exception:
        sa_score = None

    # Lipinski rules
    lipinski = {
        "mw_le_500": all_descs.get('MolWt', 0) <= 500,
        "logp_le_5": all_descs.get('MolLogP', 0) <= 5,
        "hbd_le_5": all_descs.get('NumHDonors', 0) <= 5,
        "hba_le_10": all_descs.get('NumHAcceptors', 0) <= 10,
        "violations": sum([
            all_descs.get('MolWt', 0) > 500,
            all_descs.get('MolLogP', 0) > 5,
            all_descs.get('NumHDonors', 0) > 5,
            all_descs.get('NumHAcceptors', 0) > 10,
        ]),
        "passes": sum([
            all_descs.get('MolWt', 0) > 500,
            all_descs.get('MolLogP', 0) > 5,
            all_descs.get('NumHDonors', 0) > 5,
            all_descs.get('NumHAcceptors', 0) > 10,
        ]) <= 1
    }

    # Veber rules
    veber = {
        "tpsa_le_140": all_descs.get('TPSA', 0) <= 140,
        "rotb_le_10": all_descs.get('NumRotatableBonds', 0) <= 10,
        "passes": all_descs.get('TPSA', 0) <= 140 and all_descs.get('NumRotatableBonds', 0) <= 10
    }

    if descriptor_set == "druglike":
        descriptors = filter_descs(druglike_keys)
    elif descriptor_set == "physical":
        descriptors = filter_descs(physical_keys)
    elif descriptor_set == "topological":
        descriptors = filter_descs(topological_keys)
    else:
        descriptors = all_descs

    return {
        "action": "descriptors",
        "smiles": canonical,
        "descriptor_set": descriptor_set,
        "num_descriptors": len(descriptors),
        "total_rdkit_descriptors": len(all_descs),
        "descriptors": descriptors,
        "scores": {
            "qed": qed_score,
            "sa_score": sa_score
        },
        "rules": {
            "lipinski": lipinski,
            "veber": veber
        }
    }


# ============================================================
# 3. SCAFFOLD - Murcko Scaffold & R-Group Analysis
# ============================================================
def action_scaffold(smiles_input, target_smiles=None, rgroup_core=None):
    """Scaffold analysis for single or multiple molecules."""

    # Determine input source
    if target_smiles:
        mol_list = parse_smiles_list(target_smiles)
    elif smiles_input:
        # Could be single or comma-separated
        if ',' in smiles_input:
            mol_list = parse_smiles_list(smiles_input)
        else:
            mol_list = parse_smiles_list(smiles_input)
    else:
        raise ValueError("Need --smiles or --target_smiles")

    scaffolds = []
    for smi, mol in mol_list:
        try:
            core = MurckoScaffold.GetScaffoldForMol(mol)
            core_smi = Chem.MolToSmiles(core, isomericSmiles=True)
            generic = MurckoScaffold.MakeScaffoldGeneric(core)
            generic_smi = Chem.MolToSmiles(generic, isomericSmiles=True)

            # Side chains (atoms not in scaffold)
            core_match = mol.GetSubstructMatch(core)
            all_atoms = set(range(mol.GetNumAtoms()))
            side_chain_atoms = all_atoms - set(core_match) if core_match else set()

            scaffolds.append({
                "smiles": smi,
                "murcko_scaffold": core_smi,
                "generic_scaffold": generic_smi,
                "scaffold_atoms": len(core_match) if core_match else 0,
                "total_atoms": mol.GetNumAtoms(),
                "side_chain_atoms": len(side_chain_atoms),
                "num_rings": mol.GetRingInfo().NumRings()
            })
        except Exception as e:
            scaffolds.append({
                "smiles": smi,
                "error": str(e)
            })

    # Diversity analysis for multiple molecules
    unique_scaffolds = list(set(s.get("murcko_scaffold", "") for s in scaffolds if "murcko_scaffold" in s))
    unique_generic = list(set(s.get("generic_scaffold", "") for s in scaffolds if "generic_scaffold" in s))

    # Most common scaffold
    scaffold_counts = {}
    for s in scaffolds:
        sc = s.get("murcko_scaffold", "")
        if sc:
            scaffold_counts[sc] = scaffold_counts.get(sc, 0) + 1
    most_common = max(scaffold_counts, key=scaffold_counts.get) if scaffold_counts else None

    result = {
        "action": "scaffold",
        "num_molecules": len(mol_list),
        "scaffolds": scaffolds,
        "unique_murcko_scaffolds": len(unique_scaffolds),
        "unique_generic_scaffolds": len(unique_generic),
        "diversity_ratio": round(len(unique_scaffolds) / max(len(mol_list), 1), 4),
        "most_common_scaffold": most_common,
        "scaffold_list": unique_scaffolds
    }

    # R-Group Decomposition if core provided
    if rgroup_core:
        rgroup_core = _sanitize_input(rgroup_core, "rgroup_core")
        core_mol = Chem.MolFromSmarts(rgroup_core)
        if core_mol is None:
            core_mol = Chem.MolFromSmiles(rgroup_core)
        if core_mol is None:
            result["rgroup_error"] = f"Invalid core SMARTS/SMILES: {rgroup_core}"
        else:
            try:
                mols = [mol for _, mol in mol_list]
                decomp = rdRGroupDecomposition.RGroupDecomposition(core_mol)
                for mol in mols:
                    decomp.Add(mol)
                decomp.Process()
                columns = decomp.GetRGroupsAsColumns()

                rgroups = {}
                for col_name, col_mols in columns.items():
                    rgroups[col_name] = [
                        Chem.MolToSmiles(m, isomericSmiles=True) if m else None
                        for m in col_mols
                    ]
                result["rgroup_decomposition"] = {
                    "core": rgroup_core,
                    "rgroups": rgroups,
                    "num_rgroups": len(rgroups)
                }
            except Exception as e:
                result["rgroup_error"] = str(e)

    return result


# ============================================================
# 4. MCS - Maximum Common Substructure
# ============================================================
def action_mcs(target_smiles):
    mol_list = parse_smiles_list(target_smiles)
    if len(mol_list) < 2:
        raise ValueError("MCS requires at least 2 molecules")

    mols = [mol for _, mol in mol_list]

    # Find MCS
    mcs_result = rdFMCS.FindMCS(
        mols,
        atomCompare=rdFMCS.AtomCompare.CompareElements,
        bondCompare=rdFMCS.BondCompare.CompareOrder,
        ringMatchesRingOnly=True,
        completeRingsOnly=False,
        timeout=60
    )

    mcs_smarts = mcs_result.smartsString
    mcs_mol = Chem.MolFromSmarts(mcs_smarts) if mcs_smarts else None

    # Coverage per molecule
    coverage = []
    for smi, mol in mol_list:
        if mcs_mol:
            match = mol.GetSubstructMatch(mcs_mol)
            matched = len(match)
        else:
            matched = 0
        total = mol.GetNumAtoms()
        coverage.append({
            "smiles": smi,
            "matched_atoms": matched,
            "total_atoms": total,
            "coverage_pct": round(matched / max(total, 1) * 100, 1)
        })

    # Try to get a valid SMILES from the MCS SMARTS
    mcs_smiles = None
    if mcs_mol:
        try:
            # Use first molecule's match to extract MCS as SMILES
            first_mol = mols[0]
            match = first_mol.GetSubstructMatch(mcs_mol)
            if match:
                edit = Chem.RWMol(first_mol)
                atoms_to_remove = sorted(
                    set(range(first_mol.GetNumAtoms())) - set(match),
                    reverse=True
                )
                for idx in atoms_to_remove:
                    edit.RemoveAtom(idx)
                try:
                    Chem.SanitizeMol(edit)
                    mcs_smiles = Chem.MolToSmiles(edit, isomericSmiles=True)
                except Exception:
                    mcs_smiles = None
        except Exception:
            mcs_smiles = None

    return {
        "action": "mcs",
        "mcs_smarts": mcs_smarts,
        "mcs_smiles": mcs_smiles,
        "num_mcs_atoms": mcs_result.numAtoms,
        "num_mcs_bonds": mcs_result.numBonds,
        "molecules_compared": len(mol_list),
        "canceled": mcs_result.canceled,
        "coverage": coverage
    }


# ============================================================
# 5. MMPA - Matched Molecular Pair Analysis
# ============================================================
def action_mmpa(target_smiles):
    mol_list = parse_smiles_list(target_smiles)
    if len(mol_list) < 2:
        raise ValueError("MMPA requires at least 2 molecules")

    # Fragment each molecule
    fragments = {}
    for smi, mol in mol_list:
        try:
            frags = rdMMPA.FragmentMol(mol)
            fragments[smi] = []
            for core, chains in frags:
                core_smi = Chem.MolToSmiles(core, isomericSmiles=True) if core else ""
                chains_smi = Chem.MolToSmiles(chains, isomericSmiles=True) if chains else ""
                fragments[smi].append({
                    "core": core_smi,
                    "chains": chains_smi
                })
        except Exception as e:
            fragments[smi] = [{"error": str(e)}]

    # Find matched pairs (same core, different R-groups)
    pairs = []
    smiles_list = [smi for smi, _ in mol_list]
    for i in range(len(smiles_list)):
        for j in range(i + 1, len(smiles_list)):
            smi1, smi2 = smiles_list[i], smiles_list[j]
            frags1 = fragments.get(smi1, [])
            frags2 = fragments.get(smi2, [])

            for f1 in frags1:
                if "error" in f1 or not f1.get("core"):
                    continue
                for f2 in frags2:
                    if "error" in f2 or not f2.get("core"):
                        continue
                    if f1["core"] == f2["core"] and f1["chains"] != f2["chains"]:
                        pairs.append({
                            "mol1": smi1,
                            "mol2": smi2,
                            "core": f1["core"],
                            "transformation": {
                                "from": f1["chains"],
                                "to": f2["chains"]
                            }
                        })

    # Unique transformations
    unique_transforms = list(set(
        f"{p['transformation']['from']}->{ p['transformation']['to']}"
        for p in pairs
    ))

    return {
        "action": "mmpa",
        "molecules_analyzed": len(mol_list),
        "pairs": pairs[:100],  # cap output
        "num_pairs": len(pairs),
        "unique_transformations": len(unique_transforms),
        "transformations_list": unique_transforms[:50],
        "fragments_per_molecule": {
            smi: len(frags) for smi, frags in fragments.items()
        }
    }


# ============================================================
# 6. CHEMSPACE - Chemical Space Visualization
# ============================================================
def action_chemspace(target_smiles=None, input_file=None, method="pca", output="chemspace.png"):
    # Collect SMILES
    smiles_list = []
    if input_file:
        input_file = _sanitize_input(input_file, "input_file", max_len=500)
        if not os.path.exists(input_file):
            raise ValueError(f"File not found: {input_file}")
        with open(input_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    smiles_list.append(line.split()[0])  # first column
    elif target_smiles:
        target_smiles = _sanitize_input(target_smiles, "SMILES list", max_len=100000)
        smiles_list = [s.strip() for s in target_smiles.split(',') if s.strip()]
    else:
        raise ValueError("Need --target_smiles or --input_file")

    if len(smiles_list) < 2:
        raise ValueError("Need at least 2 molecules for chemical space visualization")

    # Generate fingerprints
    valid_smiles = []
    fps = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            gen = AllChem.GetMorganGenerator(radius=2, fpSize=2048)
            fp = gen.GetFingerprintAsNumPy(mol)
            fps.append(fp)
            valid_smiles.append(Chem.MolToSmiles(mol, isomericSmiles=True))

    if len(valid_smiles) < 2:
        raise ValueError("Need at least 2 valid molecules")

    X = np.array(fps)

    # Dimensionality reduction
    if method == "pca":
        from sklearn.decomposition import PCA
        reducer = PCA(n_components=2, random_state=42)
        coords = reducer.fit_transform(X)
        explained_var = reducer.explained_variance_ratio_.tolist()
    elif method == "tsne":
        from sklearn.manifold import TSNE
        perplexity = min(30, max(2, len(valid_smiles) - 1))
        reducer = TSNE(n_components=2, random_state=42, perplexity=perplexity)
        coords = reducer.fit_transform(X)
        explained_var = None
    elif method == "umap":
        try:
            import umap
            n_neighbors = min(15, max(2, len(valid_smiles) - 1))
            reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=n_neighbors)
            coords = reducer.fit_transform(X)
            explained_var = None
        except ImportError:
            # Fallback to t-SNE
            from sklearn.manifold import TSNE
            method = "tsne (umap unavailable, fallback)"
            perplexity = min(30, max(2, len(valid_smiles) - 1))
            reducer = TSNE(n_components=2, random_state=42, perplexity=perplexity)
            coords = reducer.fit_transform(X)
            explained_var = None
    else:
        raise ValueError(f"Unknown method: {method}. Use pca, tsne, or umap.")

    # Plot
    output = _sanitize_output_path(output)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    scatter = ax.scatter(coords[:, 0], coords[:, 1], c=range(len(valid_smiles)),
                         cmap='viridis', s=80, alpha=0.8, edgecolors='black', linewidths=0.5)
    ax.set_xlabel(f"Component 1", fontsize=12)
    ax.set_ylabel(f"Component 2", fontsize=12)
    ax.set_title(f"Chemical Space ({method.upper()}) — {len(valid_smiles)} molecules", fontsize=14)
    plt.colorbar(scatter, label="Molecule Index")

    # Annotate points with truncated SMILES
    for i, smi in enumerate(valid_smiles):
        label = smi[:20] + "..." if len(smi) > 20 else smi
        ax.annotate(label, (coords[i, 0], coords[i, 1]), fontsize=6,
                    xytext=(5, 5), textcoords='offset points', alpha=0.7)

    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()

    # Build coordinates list
    coord_list = []
    for i, smi in enumerate(valid_smiles):
        coord_list.append({
            "smiles": smi,
            "x": round(float(coords[i, 0]), 6),
            "y": round(float(coords[i, 1]), 6)
        })

    result = {
        "action": "chemspace",
        "method": method,
        "num_molecules": len(valid_smiles),
        "num_invalid_skipped": len(smiles_list) - len(valid_smiles),
        "plot_path": output,
        "coordinates": coord_list
    }
    if explained_var:
        result["explained_variance"] = [round(v, 4) for v in explained_var]

    return result


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Advanced cheminformatics (PharmaClaw)")
    parser.add_argument("--action", required=True,
                        choices=["standardize", "descriptors", "scaffold", "mcs", "mmpa", "chemspace"],
                        help="Action to perform")
    parser.add_argument("--smiles", help="Single SMILES string")
    parser.add_argument("--target_smiles", help="Comma-separated SMILES for multi-molecule actions")
    parser.add_argument("--descriptor_set", choices=["all", "druglike", "physical", "topological"],
                        default="all", help="Descriptor category filter")
    parser.add_argument("--rgroup_core", help="SMARTS/SMILES core for R-group decomposition")
    parser.add_argument("--method", choices=["pca", "tsne", "umap"], default="pca",
                        help="Dimensionality reduction method for chemspace")
    parser.add_argument("--input_file", help="File with SMILES (one per line) for chemspace")
    parser.add_argument("--output", default="chemspace.png", help="Output file for plots")
    args = parser.parse_args()

    try:
        if args.action == "standardize":
            if not args.smiles:
                raise ValueError("--smiles required for standardize")
            result = action_standardize(args.smiles)

        elif args.action == "descriptors":
            if not args.smiles:
                raise ValueError("--smiles required for descriptors")
            result = action_descriptors(args.smiles, args.descriptor_set)

        elif args.action == "scaffold":
            result = action_scaffold(args.smiles, args.target_smiles, args.rgroup_core)

        elif args.action == "mcs":
            if not args.target_smiles:
                raise ValueError("--target_smiles required for mcs (comma-separated, 2+ molecules)")
            result = action_mcs(args.target_smiles)

        elif args.action == "mmpa":
            if not args.target_smiles:
                raise ValueError("--target_smiles required for mmpa (comma-separated, 2+ molecules)")
            result = action_mmpa(args.target_smiles)

        elif args.action == "chemspace":
            result = action_chemspace(args.target_smiles, args.input_file, args.method, args.output)

        print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
