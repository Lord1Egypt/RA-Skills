#!/usr/bin/env python3
"""Pharmacophore Mapping & Feature Extraction.

Identifies pharmacophoric features (HBD, HBA, hydrophobic, aromatic, pos/neg ionizable)
from 3D conformers. Generates pharmacophore fingerprints and feature maps.

Usage:
    python pharmacophore.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --action features
    python pharmacophore.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --action fingerprint
    python pharmacophore.py --target_smiles "smi1,smi2" --action compare
    python pharmacophore.py --smiles "CCO" --action map --output pharm.png
"""

import argparse
import json
import sys
import os

try:
    from rdkit import Chem, RDConfig
    from rdkit.Chem import AllChem, rdMolDescriptors, Draw
    from rdkit.Chem.Pharm2D import Gobbi_Pharm2D, Generate
    from rdkit.Chem import ChemicalFeatures
    from rdkit import DataStructs
except ImportError:
    print(json.dumps({"error": "RDKit not installed. pip install rdkit-pypi"}))
    sys.exit(1)

# Load feature factory
FDEF_FILE = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')
FEATURE_FACTORY = ChemicalFeatures.BuildFeatureFactory(FDEF_FILE)

# Pharmacophore feature families
FEATURE_FAMILIES = [
    "Donor",           # Hydrogen bond donor
    "Acceptor",        # Hydrogen bond acceptor
    "Aromatic",        # Aromatic ring
    "Hydrophobe",      # Hydrophobic group
    "PosIonizable",    # Positive ionizable
    "NegIonizable",    # Negative ionizable
    "LumpedHydrophobe" # Lumped hydrophobic
]


def validate_smiles(smiles: str):
    """Validate SMILES."""
    if not smiles or len(smiles) > 2000:
        return None
    return Chem.MolFromSmiles(smiles)


def get_3d_mol(smiles: str):
    """Generate 3D conformer for a molecule."""
    mol = validate_smiles(smiles)
    if mol is None:
        return None
    mol = Chem.AddHs(mol)
    result = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    if result == -1:
        return None
    try:
        AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
    except Exception:
        pass
    return mol


def extract_features(smiles: str):
    """Extract pharmacophoric features with 3D coordinates."""
    mol = get_3d_mol(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES or failed 3D embedding: {smiles}"}

    features = FEATURE_FACTORY.GetFeaturesForMol(mol)

    feature_list = []
    family_counts = {}

    for feat in features:
        family = feat.GetFamily()
        feat_type = feat.GetType()
        pos = feat.GetPos()
        atom_ids = list(feat.GetAtomIds())

        family_counts[family] = family_counts.get(family, 0) + 1

        feature_list.append({
            "family": family,
            "type": feat_type,
            "atom_ids": atom_ids,
            "position": {
                "x": round(pos.x, 4),
                "y": round(pos.y, 4),
                "z": round(pos.z, 4)
            }
        })

    return {
        "smiles": Chem.MolToSmiles(Chem.RemoveHs(mol)),
        "num_features": len(feature_list),
        "family_counts": family_counts,
        "features": feature_list,
        "summary": {
            "HBD": family_counts.get("Donor", 0),
            "HBA": family_counts.get("Acceptor", 0),
            "aromatic": family_counts.get("Aromatic", 0),
            "hydrophobic": family_counts.get("Hydrophobe", 0) + family_counts.get("LumpedHydrophobe", 0),
            "pos_ionizable": family_counts.get("PosIonizable", 0),
            "neg_ionizable": family_counts.get("NegIonizable", 0)
        }
    }


def pharmacophore_fingerprint(smiles: str):
    """Generate 2D pharmacophore fingerprint (Gobbi)."""
    mol = validate_smiles(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES: {smiles}"}

    try:
        fp = Generate.Gen2DFingerprint(mol, Gobbi_Pharm2D.factory)
        on_bits = list(fp.GetOnBits())
        return {
            "smiles": Chem.MolToSmiles(mol),
            "fingerprint_type": "Gobbi_Pharm2D",
            "num_bits": fp.GetNumBits(),
            "num_on_bits": len(on_bits),
            "on_bits": on_bits[:100],  # cap for readability
            "density": round(len(on_bits) / fp.GetNumBits(), 6)
        }
    except Exception as e:
        return {"error": f"Fingerprint generation failed: {str(e)}"}


def compare_pharmacophores(smiles_list: list):
    """Compare pharmacophore fingerprints between molecules."""
    mols = []
    fps = []
    valid_smiles = []

    for smi in smiles_list:
        mol = validate_smiles(smi.strip())
        if mol is None:
            continue
        try:
            fp = Generate.Gen2DFingerprint(mol, Gobbi_Pharm2D.factory)
            mols.append(mol)
            fps.append(fp)
            valid_smiles.append(Chem.MolToSmiles(mol))
        except Exception:
            continue

    if len(fps) < 2:
        return {"error": "Need at least 2 valid molecules for comparison"}

    # Pairwise Tanimoto similarity on pharmacophore fingerprints
    comparisons = []
    for i in range(len(fps)):
        for j in range(i + 1, len(fps)):
            sim = DataStructs.TanimotoSimilarity(fps[i], fps[j])
            comparisons.append({
                "mol_a": valid_smiles[i],
                "mol_b": valid_smiles[j],
                "pharmacophore_similarity": round(sim, 4)
            })

    # Feature comparison
    feature_profiles = []
    for smi in valid_smiles:
        feat = extract_features(smi)
        if "error" not in feat:
            feature_profiles.append({
                "smiles": smi,
                "summary": feat["summary"]
            })

    return {
        "num_molecules": len(valid_smiles),
        "smiles": valid_smiles,
        "pairwise_similarity": comparisons,
        "feature_profiles": feature_profiles
    }


def pharmacophore_map(smiles: str, output_path: str = None):
    """Generate a 2D pharmacophore feature map as PNG."""
    mol = validate_smiles(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES: {smiles}"}

    try:
        from rdkit.Chem import Draw
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return {"error": "PIL/Pillow not installed for image generation"}

    # Get features on 2D mol
    features = FEATURE_FACTORY.GetFeaturesForMol(Chem.AddHs(mol))

    # Color map for feature families
    colors = {
        "Donor": (0, 0.8, 0),       # green
        "Acceptor": (0.8, 0, 0),     # red
        "Aromatic": (0.8, 0.8, 0),   # yellow
        "Hydrophobe": (0, 0, 0.8),   # blue
        "PosIonizable": (0.8, 0, 0.8),  # magenta
        "NegIonizable": (0, 0.8, 0.8),  # cyan
        "LumpedHydrophobe": (0.4, 0.4, 0.8)  # light blue
    }

    # Highlight atoms by feature type
    atom_highlights = {}
    for feat in features:
        family = feat.GetFamily()
        color = colors.get(family, (0.5, 0.5, 0.5))
        for aid in feat.GetAtomIds():
            if aid < mol.GetNumAtoms():
                atom_highlights[aid] = color

    highlight_atoms = list(atom_highlights.keys())
    highlight_colors = {k: v for k, v in atom_highlights.items()}

    img = Draw.MolToImage(mol, size=(500, 500),
                          highlightAtoms=highlight_atoms,
                          highlightAtomColors=highlight_colors)

    if output_path:
        img.save(output_path)
        return {
            "smiles": Chem.MolToSmiles(mol),
            "image": output_path,
            "legend": {family: f"rgb{colors[family]}" for family in colors},
            "num_features_highlighted": len(highlight_atoms)
        }

    return {
        "smiles": Chem.MolToSmiles(mol),
        "num_features_highlighted": len(highlight_atoms),
        "note": "Provide --output to save PNG"
    }


def main():
    parser = argparse.ArgumentParser(description="Pharmacophore Mapping")
    parser.add_argument("--smiles", type=str, help="Input SMILES")
    parser.add_argument("--target_smiles", type=str,
                        help="Comma-separated SMILES for comparison")
    parser.add_argument("--action",
                        choices=["features", "fingerprint", "compare", "map"],
                        default="features")
    parser.add_argument("--output", type=str, default=None, help="Output file path")

    args = parser.parse_args()

    if args.action == "features":
        if not args.smiles:
            print(json.dumps({"error": "Provide --smiles"}))
            sys.exit(1)
        result = extract_features(args.smiles)

    elif args.action == "fingerprint":
        if not args.smiles:
            print(json.dumps({"error": "Provide --smiles"}))
            sys.exit(1)
        result = pharmacophore_fingerprint(args.smiles)

    elif args.action == "compare":
        smiles_list = []
        if args.target_smiles:
            smiles_list = args.target_smiles.split(",")
        elif args.smiles:
            smiles_list = args.smiles.split(",")
        result = compare_pharmacophores(smiles_list)

    elif args.action == "map":
        if not args.smiles:
            print(json.dumps({"error": "Provide --smiles"}))
            sys.exit(1)
        result = pharmacophore_map(args.smiles, args.output)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
