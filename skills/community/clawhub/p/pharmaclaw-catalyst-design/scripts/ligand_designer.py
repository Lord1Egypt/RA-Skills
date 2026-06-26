#!/usr/bin/env python3
"""Novel Ligand Designer for Organometallic Catalysts.

Uses RDKit to modify known ligand scaffolds and generate novel variants with
predicted properties. Applies bioisosteric replacements, steric tuning, and
electronic modifications.

Usage:
    python ligand_designer.py --scaffold "c1ccc(cc1)P(c1ccccc1)c1ccccc1" --strategy steric
    python ligand_designer.py --scaffold "PPh3" --strategy electronic --output designs.json
    python ligand_designer.py --scaffold "c1ccc(cc1)P(c1ccccc1)c1ccccc1" --strategy all --draw
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, Draw, rdMolDescriptors, rdmolops
    from rdkit.Chem import RWMol
except ImportError:
    print(json.dumps({"error": "RDKit not installed. Run: pip install rdkit", "status": "error"}))
    sys.exit(1)

# Known ligand name → SMILES shortcuts
LIGAND_ALIASES = {
    "PPh3": "c1ccc(cc1)P(c1ccccc1)c1ccccc1",
    "triphenylphosphine": "c1ccc(cc1)P(c1ccccc1)c1ccccc1",
    "PCy3": "C1(CCCCC1)P(C1CCCCC1)C1CCCCC1",
    "tricyclohexylphosphine": "C1(CCCCC1)P(C1CCCCC1)C1CCCCC1",
    "dppe": "c1ccc(cc1)P(CCP(c1ccccc1)c1ccccc1)c1ccccc1",
    "dppp": "c1ccc(cc1)P(CCCP(c1ccccc1)c1ccccc1)c1ccccc1",
    "NHC_IMes": "Cc1cc(C)cc(c1)N1C=CN(c2cc(C)cc(C)c2)C1",
    "NHC_IPr": "CC(C)c1cccc(C(C)C)c1N1C=CN(c2c(C(C)C)cccc2C(C)C)C1",
}

# Modification strategies
STERIC_MODS = [
    {"name": "ortho-methyl", "smarts_from": "[c:1][H]", "smarts_to": "[c:1]C", "description": "Add ortho-methyl for steric bulk", "positions": "ortho"},
    {"name": "ortho-isopropyl", "smarts_from": "[c:1][H]", "smarts_to": "[c:1]C(C)C", "description": "Add ortho-iPr for large cone angle"},
    {"name": "cyclohexyl-swap", "description": "Replace phenyl with cyclohexyl for increased donor strength and steric bulk"},
    {"name": "tert-butyl", "smarts_from": "[c:1][H]", "smarts_to": "[c:1]C(C)(C)C", "description": "Add t-Bu for maximum steric shielding"},
    {"name": "adamantyl", "description": "Replace aryl with adamantyl for extreme steric demand"},
]

ELECTRONIC_MODS = [
    {"name": "para-CF3", "smarts_from": "[c:1]([c:2])[H]", "smarts_to": "[c:1]([c:2])C(F)(F)F", "description": "Add p-CF3 (electron-withdrawing, σ-acceptor enhancement)"},
    {"name": "para-OMe", "smarts_from": "[c:1]([c:2])[H]", "smarts_to": "[c:1]([c:2])OC", "description": "Add p-OMe (electron-donating, increase σ-donor)"},
    {"name": "para-NMe2", "smarts_from": "[c:1]([c:2])[H]", "smarts_to": "[c:1]([c:2])N(C)C", "description": "Add p-NMe2 (strong electron-donor)"},
    {"name": "para-F", "smarts_from": "[c:1]([c:2])[H]", "smarts_to": "[c:1]([c:2])F", "description": "Add p-F (mild electron-withdrawing, metabolic stability)"},
    {"name": "para-NO2", "smarts_from": "[c:1]([c:2])[H]", "smarts_to": "[c:1]([c:2])[N+](=O)[O-]", "description": "Add p-NO2 (strong electron-withdrawing)"},
]

BIOISOSTERIC_MODS = [
    {"name": "P→As", "description": "Replace P with As (arsine ligand — softer donor, may activate different substrates)"},
    {"name": "P→N(sp3)", "description": "Replace phosphine with amine donor — cheaper, different trans influence"},
    {"name": "NHC-from-phosphine", "description": "Replace phosphine with NHC — stronger σ-donor, no π-acceptor"},
    {"name": "phenyl→pyridyl", "description": "Replace phenyl with 2-pyridyl — adds hemilabile N-donor site"},
    {"name": "phenyl→thienyl", "description": "Replace phenyl with thienyl — modifies electronics/sterics"},
]


def resolve_scaffold(scaffold: str) -> str:
    """Resolve ligand name alias to SMILES."""
    return LIGAND_ALIASES.get(scaffold, scaffold)


def compute_ligand_props(smiles: str) -> dict | None:
    """Compute properties relevant to ligand performance."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return {
        "smiles": Chem.MolToSmiles(mol),
        "MW": round(Descriptors.MolWt(mol), 2),
        "logP": round(Descriptors.MolLogP(mol), 2),
        "HBA": Descriptors.NumHAcceptors(mol),
        "HBD": Descriptors.NumHDonors(mol),
        "rotatable_bonds": Descriptors.NumRotatableBonds(mol),
        "aromatic_rings": rdMolDescriptors.CalcNumAromaticRings(mol),
        "heavy_atoms": mol.GetNumHeavyAtoms(),
        "has_phosphorus": any(a.GetSymbol() == "P" for a in mol.GetAtoms()),
        "has_nitrogen": any(a.GetSymbol() == "N" for a in mol.GetAtoms()),
        "num_stereocenters": len(Chem.FindMolChiralCenters(mol, includeUnassigned=True)),
    }


def generate_steric_variants(smiles: str) -> list[dict]:
    """Generate sterically modified ligand variants."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return []

    variants = []
    # Simple approach: enumerate substitution patterns on aromatic rings
    # For each aromatic H, try adding methyl, iPr, tBu
    substituents = {
        "methyl": "C",
        "isopropyl": "C(C)C",
        "tert-butyl": "C(C)(C)C",
    }

    for sub_name, sub_smi in substituents.items():
        # Use RDKit to find aromatic C-H positions
        try:
            mol_h = Chem.AddHs(mol)
            # Find aromatic carbons bonded to H
            aromatic_ch = []
            for atom in mol_h.GetAtoms():
                if atom.GetSymbol() == "C" and atom.GetIsAromatic():
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetSymbol() == "H":
                            aromatic_ch.append(atom.GetIdx())
                            break

            if aromatic_ch and len(aromatic_ch) > 0:
                # Modify first available position as example
                rw = RWMol(mol_h)
                target_idx = aromatic_ch[0]
                # Find the H bonded to this carbon
                for neighbor in rw.GetAtomWithIdx(target_idx).GetNeighbors():
                    if neighbor.GetSymbol() == "H":
                        h_idx = neighbor.GetIdx()
                        break
                else:
                    continue

                # Remove H and add substituent fragment
                sub_mol = Chem.MolFromSmiles(sub_smi)
                if sub_mol:
                    combined = Chem.RWMol(Chem.CombineMols(Chem.RemoveHs(mol), sub_mol))
                    # Bond the first atom of substituent to the target aromatic C
                    n_atoms_orig = mol.GetNumAtoms()
                    combined.AddBond(target_idx, n_atoms_orig, Chem.BondType.SINGLE)
                    try:
                        Chem.SanitizeMol(combined)
                        new_smi = Chem.MolToSmiles(combined)
                        props = compute_ligand_props(new_smi)
                        if props:
                            variants.append({
                                "modification": f"steric_{sub_name}",
                                "description": f"Added {sub_name} group to aromatic ring",
                                "strategy": "steric",
                                "properties": props,
                            })
                    except Exception:
                        pass
        except Exception:
            continue

    return variants


def generate_electronic_variants(smiles: str) -> list[dict]:
    """Generate electronically modified ligand variants."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return []

    variants = []
    substituents = {
        "para-OMe (e-donating)": "OC",
        "para-F (mild e-withdrawing)": "F",
        "para-CF3 (e-withdrawing)": "C(F)(F)F",
    }

    for sub_name, sub_smi in substituents.items():
        try:
            sub_mol = Chem.MolFromSmiles(sub_smi)
            if not sub_mol:
                continue

            # Find aromatic C not bonded to P (to modify para-position-like sites)
            aromatic_carbons = [a.GetIdx() for a in mol.GetAtoms()
                                if a.GetIsAromatic() and a.GetSymbol() == "C"
                                and not any(n.GetSymbol() == "P" for n in a.GetNeighbors())]

            if not aromatic_carbons:
                continue

            # Pick a representative position
            target = aromatic_carbons[-1]  # roughly para in simple rings
            combined = Chem.RWMol(Chem.CombineMols(mol, sub_mol))
            combined.AddBond(target, mol.GetNumAtoms(), Chem.BondType.SINGLE)

            try:
                Chem.SanitizeMol(combined)
                new_smi = Chem.MolToSmiles(combined)
                props = compute_ligand_props(new_smi)
                if props:
                    variants.append({
                        "modification": sub_name,
                        "description": f"Added {sub_name} to tune electronics",
                        "strategy": "electronic",
                        "properties": props,
                    })
            except Exception:
                pass
        except Exception:
            continue

    return variants


def generate_bioisosteric_suggestions(smiles: str) -> list[dict]:
    """Generate conceptual bioisosteric replacement suggestions."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return []

    suggestions = []
    has_P = any(a.GetSymbol() == "P" for a in mol.GetAtoms())
    has_aromatic = any(a.GetIsAromatic() for a in mol.GetAtoms())

    if has_P:
        suggestions.append({
            "modification": "P→NHC replacement",
            "description": "Replace phosphine with N-heterocyclic carbene (NHC). NHCs are stronger σ-donors with no π-acceptor character, often giving more active and stable catalysts. Well-proven in Pd, Ru, Au catalysis.",
            "strategy": "bioisosteric",
            "rationale": "NHC ligands form stronger M-C bonds vs M-P, resist oxidation, and provide tunable steric environment via N-substituents.",
            "literature": ["Chem. Rev. 2009, 109, 3612 (Díez-González et al.)"],
            "properties": None,
        })
        suggestions.append({
            "modification": "Phosphine → phosphite (P(OR)3)",
            "description": "Replace PR3 with P(OR)3. Phosphites are stronger π-acceptors, making the metal more electrophilic. Useful when oxidative addition is easy but reductive elimination is slow.",
            "strategy": "bioisosteric",
            "rationale": "Lower σ-donor / higher π-acceptor shifts the electronic balance. Good for electron-rich substrates.",
            "properties": None,
        })

    if has_aromatic:
        suggestions.append({
            "modification": "Phenyl → 2-pyridyl (hemilabile)",
            "description": "Replace one phenyl ring with 2-pyridyl to create a hemilabile coordination site. The pyridyl N can coordinate/dissociate dynamically, creating an open site for substrate binding.",
            "strategy": "bioisosteric",
            "rationale": "Hemilabile ligands improve catalyst longevity and substrate turnover in challenging reactions.",
            "properties": None,
        })
        suggestions.append({
            "modification": "Phenyl → mesityl (steric + electronic)",
            "description": "Replace phenyl with 2,4,6-trimethylphenyl (mesityl). Adds steric protection around the metal center while maintaining aromaticity.",
            "strategy": "bioisosteric",
            "rationale": "Mesityl groups prevent catalyst deactivation through dimerization and provide moderate electron donation.",
            "properties": None,
        })

    return suggestions


def design_ligands(scaffold: str, strategy: str = "all", draw: bool = False, output: str = None) -> dict:
    """Main design function."""
    smiles = resolve_scaffold(scaffold)
    base_props = compute_ligand_props(smiles)

    if base_props is None:
        return {
            "agent": "catalyst-design",
            "version": "1.0.0",
            "action": "design_ligand",
            "status": "error",
            "error": f"Could not parse scaffold SMILES: {smiles}",
        }

    variants = []
    if strategy in ("steric", "all"):
        variants.extend(generate_steric_variants(smiles))
    if strategy in ("electronic", "all"):
        variants.extend(generate_electronic_variants(smiles))
    if strategy in ("bioisosteric", "all"):
        variants.extend(generate_bioisosteric_suggestions(smiles))

    # Draw structures if requested
    viz_paths = []
    if draw and variants:
        drawable = [v for v in variants if v.get("properties") and v["properties"].get("smiles")]
        if drawable:
            mols = [Chem.MolFromSmiles(v["properties"]["smiles"]) for v in drawable[:8]]
            legends = [v["modification"] for v in drawable[:8]]
            mols = [m for m in mols if m is not None]
            if mols:
                out_path = output.replace(".json", "_grid.png") if output else "/tmp/ligand_designs.png"
                img = Draw.MolsToGridImage(mols, molsPerRow=4, subImgSize=(400, 300), legends=legends[:len(mols)])
                img.save(out_path)
                viz_paths.append(out_path)

    result = {
        "agent": "catalyst-design",
        "version": "1.0.0",
        "action": "design_ligand",
        "status": "success",
        "scaffold": {
            "input": scaffold,
            "smiles": smiles,
            "properties": base_props,
        },
        "variants": variants,
        "total_variants": len(variants),
        "viz": viz_paths,
        "recommend_next": ["catalyst_recommend", "chemistry-query", "ip-expansion"],
    }

    if output:
        with open(output, "w") as f:
            json.dump(result, f, indent=2)

    return result


def main():
    parser = argparse.ArgumentParser(description="Novel Ligand Designer")
    parser.add_argument("--scaffold", required=True, help="Ligand SMILES or name (PPh3, NHC_IMes, etc.)")
    parser.add_argument("--strategy", choices=["steric", "electronic", "bioisosteric", "all"], default="all",
                        help="Modification strategy")
    parser.add_argument("--draw", action="store_true", help="Generate 2D structure grid")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    result = design_ligands(args.scaffold, args.strategy, args.draw, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
