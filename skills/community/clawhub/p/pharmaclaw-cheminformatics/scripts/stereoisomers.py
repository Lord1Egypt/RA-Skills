#!/usr/bin/env python3
"""Stereoisomer Enumeration.

Enumerates stereoisomers (E/Z, R/S) for molecules with stereocenters.
Identifies chiral centers, double bond geometries, and generates all
possible stereoisomers.

Usage:
    python stereoisomers.py --smiles "C(F)(Cl)Br" --action enumerate
    python stereoisomers.py --smiles "CC=CC" --action enumerate
    python stereoisomers.py --smiles "C(F)(Cl)Br" --action analyze
    python stereoisomers.py --smiles "OC(F)(Cl)Br" --action enumerate --max_isomers 32
"""

import argparse
import json
import sys

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
    from rdkit.Chem.EnumerateStereoisomers import (
        EnumerateStereoisomers,
        StereoEnumerationOptions
    )
except ImportError:
    print(json.dumps({"error": "RDKit not installed. pip install rdkit-pypi"}))
    sys.exit(1)


def validate_smiles(smiles: str):
    """Validate SMILES."""
    if not smiles or len(smiles) > 2000:
        return None
    return Chem.MolFromSmiles(smiles)


def analyze_stereo(smiles: str):
    """Analyze stereochemistry of a molecule without enumerating."""
    mol = validate_smiles(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES: {smiles}"}

    # Find chiral centers
    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True, useLegacyImplementation=False)

    # Find stereo double bonds
    stereo_bonds = []
    for bond in mol.GetBonds():
        stereo = bond.GetStereo()
        if stereo != Chem.BondStereo.STEREONONE:
            stereo_bonds.append({
                "bond_idx": bond.GetIdx(),
                "begin_atom": bond.GetBeginAtomIdx(),
                "end_atom": bond.GetEndAtomIdx(),
                "stereo": str(stereo),
                "bond_type": str(bond.GetBondType())
            })

    # Count potential stereocenters (including unassigned)
    num_chiral = len(chiral_centers)
    num_stereo_bonds = len(stereo_bonds)
    max_stereoisomers = 2 ** (num_chiral + num_stereo_bonds)

    return {
        "smiles": Chem.MolToSmiles(mol),
        "num_chiral_centers": num_chiral,
        "chiral_centers": [
            {"atom_idx": idx, "label": label}
            for idx, label in chiral_centers
        ],
        "num_stereo_double_bonds": num_stereo_bonds,
        "stereo_bonds": stereo_bonds,
        "max_possible_stereoisomers": max_stereoisomers,
        "note": f"Theoretical max = 2^{num_chiral + num_stereo_bonds} = {max_stereoisomers} (actual may be fewer due to symmetry/meso forms)"
    }


def enumerate_stereoisomers(smiles: str, max_isomers: int = 64,
                             unique: bool = True, only_unassigned: bool = False):
    """Enumerate all stereoisomers of a molecule."""
    mol = validate_smiles(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES: {smiles}"}

    # Configure enumeration options
    opts = StereoEnumerationOptions()
    opts.onlyUnassigned = only_unassigned
    opts.maxIsomers = max_isomers
    opts.unique = unique

    # Enumerate
    isomers = list(EnumerateStereoisomers(mol, options=opts))

    isomer_data = []
    for iso_mol in isomers:
        iso_smi = Chem.MolToSmiles(iso_mol)
        chiral = Chem.FindMolChiralCenters(iso_mol, includeUnassigned=False, useLegacyImplementation=False)

        isomer_data.append({
            "smiles": iso_smi,
            "chiral_assignments": [
                {"atom_idx": idx, "config": label}
                for idx, label in chiral
            ],
            "mw": round(Descriptors.MolWt(iso_mol), 2),
            "num_stereocenters_assigned": len(chiral)
        })

    # Check for meso compounds (identical despite chiral centers)
    unique_smiles = set(iso["smiles"] for iso in isomer_data)

    # Analysis of input
    analysis = analyze_stereo(smiles)

    return {
        "input_smiles": smiles,
        "canonical_smiles": Chem.MolToSmiles(mol),
        "analysis": {
            "num_chiral_centers": analysis.get("num_chiral_centers", 0),
            "num_stereo_double_bonds": analysis.get("num_stereo_double_bonds", 0),
            "max_theoretical": analysis.get("max_possible_stereoisomers", 0)
        },
        "enumeration": {
            "num_generated": len(isomer_data),
            "num_unique": len(unique_smiles),
            "has_meso_forms": len(unique_smiles) < analysis.get("max_possible_stereoisomers", 0),
            "max_isomers_setting": max_isomers,
            "only_unassigned": only_unassigned
        },
        "stereoisomers": isomer_data
    }


def compare_enantiomers(smiles: str):
    """Compare properties of stereoisomers (useful for drug development)."""
    result = enumerate_stereoisomers(smiles, max_isomers=64)
    if "error" in result:
        return result

    comparisons = []
    for iso in result["stereoisomers"]:
        mol = Chem.MolFromSmiles(iso["smiles"])
        if mol is None:
            continue

        comparisons.append({
            "smiles": iso["smiles"],
            "config": iso["chiral_assignments"],
            "properties": {
                "mw": round(Descriptors.MolWt(mol), 2),
                "logp": round(Descriptors.MolLogP(mol), 3),
                "tpsa": round(Descriptors.TPSA(mol), 2),
                "hbd": rdMolDescriptors.CalcNumHBD(mol),
                "hba": rdMolDescriptors.CalcNumHBA(mol),
                "rotatable_bonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
                "num_rings": rdMolDescriptors.CalcNumRings(mol)
            },
            "note": "2D properties are identical for enantiomers; 3D/binding differs"
        })

    return {
        "input_smiles": smiles,
        "num_stereoisomers": len(comparisons),
        "comparisons": comparisons,
        "drug_relevance": (
            "Stereoisomers can have drastically different biological activity, "
            "toxicity, and pharmacokinetics. FDA requires characterization of "
            "each stereoisomer for chiral drug candidates (e.g., thalidomide)."
        )
    }


def main():
    parser = argparse.ArgumentParser(description="Stereoisomer Enumeration")
    parser.add_argument("--smiles", required=True, help="Input SMILES")
    parser.add_argument("--action",
                        choices=["enumerate", "analyze", "compare"],
                        default="enumerate")
    parser.add_argument("--max_isomers", type=int, default=64)
    parser.add_argument("--only_unassigned", action="store_true",
                        help="Only enumerate unassigned stereocenters")

    args = parser.parse_args()

    if args.action == "analyze":
        result = analyze_stereo(args.smiles)
    elif args.action == "compare":
        result = compare_enantiomers(args.smiles)
    else:
        result = enumerate_stereoisomers(
            args.smiles,
            max_isomers=args.max_isomers,
            only_unassigned=args.only_unassigned
        )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
