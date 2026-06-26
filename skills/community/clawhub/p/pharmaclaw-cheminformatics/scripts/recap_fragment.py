#!/usr/bin/env python3
"""RECAP Fragmentation — Retrosynthetic Combinatorial Analysis Procedure.

Fragments molecules at synthetically accessible bonds using RECAP rules
(11 bond types: amide, ester, amine, urea, etc.). Generates fragment trees,
leaf nodes for combinatorial library design, and reconstruction suggestions.

Usage:
    python recap_fragment.py --smiles "CC(=O)Nc1ccc(O)cc1" --action fragment
    python recap_fragment.py --smiles "CC(=O)Nc1ccc(O)cc1" --action leaves
    python recap_fragment.py --target_smiles "smi1,smi2" --action common_fragments
    python recap_fragment.py --smiles "CC(=O)Nc1ccc(O)cc1" --action tree
"""

import argparse
import json
import sys

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors
    from rdkit.Chem import Recap as RECAP
except ImportError:
    print(json.dumps({"error": "RDKit not installed. pip install rdkit-pypi"}))
    sys.exit(1)


# RECAP bond types for reference
RECAP_BOND_TYPES = {
    "amide": "C(=O)-N",
    "ester": "C(=O)-O",
    "amine": "C-N (not amide)",
    "urea": "N-C(=O)-N",
    "ether": "C-O-C",
    "olefin": "C=C",
    "quaternary_nitrogen": "N+ bonds",
    "aromatic_nitrogen_aliphatic_carbon": "nAr-C",
    "lactam_nitrogen_aliphatic_carbon": "N(lactam)-C",
    "aromatic_carbon_aromatic_carbon": "cAr-cAr",
    "sulfonamide": "S(=O)(=O)-N"
}


def validate_smiles(smiles: str):
    """Validate SMILES."""
    if not smiles or len(smiles) > 2000:
        return None
    return Chem.MolFromSmiles(smiles)


def fragment_molecule(smiles: str):
    """Fragment molecule using RECAP rules. Return all fragments with metadata."""
    mol = validate_smiles(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES: {smiles}"}

    recap_tree = RECAP.RecapDecompose(mol)

    if recap_tree is None:
        return {
            "smiles": Chem.MolToSmiles(mol),
            "num_fragments": 0,
            "fragments": [],
            "note": "No RECAP-cleavable bonds found"
        }

    # Get all nodes (fragments)
    all_nodes = recap_tree.GetAllChildren()
    leaves = recap_tree.GetLeaves()

    fragments = []
    for smi, node in all_nodes.items():
        frag_mol = Chem.MolFromSmiles(smi)
        if frag_mol is None:
            continue

        # Clean up dummy atoms for display
        clean_smi = smi
        mw = round(Descriptors.MolWt(frag_mol), 2) if frag_mol else None

        is_leaf = smi in leaves

        fragments.append({
            "smiles": smi,
            "is_leaf": is_leaf,
            "mw": mw,
            "num_atoms": frag_mol.GetNumHeavyAtoms() if frag_mol else None
        })

    # Sort by MW
    fragments.sort(key=lambda f: f.get("mw", 0) or 0, reverse=True)

    return {
        "smiles": Chem.MolToSmiles(mol),
        "parent_mw": round(Descriptors.MolWt(mol), 2),
        "num_fragments": len(fragments),
        "num_leaves": len(leaves),
        "recap_bond_types": RECAP_BOND_TYPES,
        "fragments": fragments
    }


def get_leaves(smiles: str):
    """Get only leaf fragments (terminal, non-decomposable)."""
    mol = validate_smiles(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES: {smiles}"}

    recap_tree = RECAP.RecapDecompose(mol)
    if recap_tree is None:
        return {
            "smiles": Chem.MolToSmiles(mol),
            "num_leaves": 0,
            "leaves": [],
            "note": "No RECAP-cleavable bonds found"
        }

    leaves = recap_tree.GetLeaves()
    leaf_data = []

    for smi, node in leaves.items():
        frag_mol = Chem.MolFromSmiles(smi)
        mw = round(Descriptors.MolWt(frag_mol), 2) if frag_mol else None
        leaf_data.append({
            "smiles": smi,
            "mw": mw,
            "num_atoms": frag_mol.GetNumHeavyAtoms() if frag_mol else None
        })

    leaf_data.sort(key=lambda f: f.get("mw", 0) or 0, reverse=True)

    return {
        "smiles": Chem.MolToSmiles(mol),
        "num_leaves": len(leaf_data),
        "leaves": leaf_data,
        "use_case": "These leaf fragments are building blocks for combinatorial library design"
    }


def get_tree(smiles: str, max_depth: int = 5):
    """Get hierarchical RECAP tree structure."""
    mol = validate_smiles(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES: {smiles}"}

    recap_tree = RECAP.RecapDecompose(mol, minFragmentSize=2)
    if recap_tree is None:
        return {"smiles": Chem.MolToSmiles(mol), "tree": None}

    def node_to_dict(node, depth=0):
        if depth > max_depth:
            return {"smiles": node.smiles, "truncated": True}

        children = []
        for child_smi, child_node in node.children.items():
            children.append(node_to_dict(child_node, depth + 1))

        result = {
            "smiles": node.smiles,
            "num_children": len(children)
        }
        if children:
            result["children"] = children
        return result

    return {
        "smiles": Chem.MolToSmiles(mol),
        "tree": node_to_dict(recap_tree),
        "max_depth": max_depth
    }


def common_fragments(smiles_list: list):
    """Find common RECAP fragments across multiple molecules."""
    all_fragments = {}
    mol_data = []

    for smi in smiles_list:
        smi = smi.strip()
        mol = validate_smiles(smi)
        if mol is None:
            continue

        canonical = Chem.MolToSmiles(mol)
        recap_tree = RECAP.RecapDecompose(mol)
        if recap_tree is None:
            mol_data.append({"smiles": canonical, "fragments": set()})
            continue

        leaves = recap_tree.GetLeaves()
        frags = set(leaves.keys())
        mol_data.append({"smiles": canonical, "fragments": frags})

        for frag_smi in frags:
            if frag_smi not in all_fragments:
                all_fragments[frag_smi] = {"count": 0, "in_molecules": []}
            all_fragments[frag_smi]["count"] += 1
            all_fragments[frag_smi]["in_molecules"].append(canonical)

    # Find shared fragments (in 2+ molecules)
    shared = {smi: data for smi, data in all_fragments.items() if data["count"] >= 2}

    # Sort by frequency
    shared_list = [
        {"smiles": smi, "count": data["count"], "in_molecules": data["in_molecules"]}
        for smi, data in sorted(shared.items(), key=lambda x: x[1]["count"], reverse=True)
    ]

    return {
        "num_molecules": len(mol_data),
        "total_unique_fragments": len(all_fragments),
        "num_shared_fragments": len(shared_list),
        "shared_fragments": shared_list,
        "use_case": "Shared fragments indicate common pharmacophoric scaffolds or synthetic building blocks"
    }


def main():
    parser = argparse.ArgumentParser(description="RECAP Fragmentation")
    parser.add_argument("--smiles", type=str, help="Input SMILES")
    parser.add_argument("--target_smiles", type=str,
                        help="Comma-separated SMILES for common fragment analysis")
    parser.add_argument("--action",
                        choices=["fragment", "leaves", "tree", "common_fragments"],
                        default="fragment")
    parser.add_argument("--max_depth", type=int, default=5, help="Max tree depth")

    args = parser.parse_args()

    if args.action == "common_fragments":
        smiles_list = []
        if args.target_smiles:
            smiles_list = args.target_smiles.split(",")
        elif args.smiles:
            smiles_list = args.smiles.split(",")
        if len(smiles_list) < 2:
            print(json.dumps({"error": "Need at least 2 SMILES for common_fragments"}))
            sys.exit(1)
        result = common_fragments(smiles_list)

    elif args.action == "tree":
        if not args.smiles:
            print(json.dumps({"error": "Provide --smiles"}))
            sys.exit(1)
        result = get_tree(args.smiles, args.max_depth)

    elif args.action == "leaves":
        if not args.smiles:
            print(json.dumps({"error": "Provide --smiles"}))
            sys.exit(1)
        result = get_leaves(args.smiles)

    else:  # fragment
        if not args.smiles:
            print(json.dumps({"error": "Provide --smiles"}))
            sys.exit(1)
        result = fragment_molecule(args.smiles)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
