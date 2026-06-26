#!/usr/bin/env python3
"""3D Conformer Generation & Ensemble Analysis.

Generates 3D conformer ensembles using RDKit's ETKDG method with MMFF/UFF
force field optimization. Outputs energies, RMSD matrix, and SDF files.

Usage:
    python conformer_gen.py --smiles "CCO" --num_confs 10 --action generate
    python conformer_gen.py --smiles "CCO" --num_confs 50 --action ensemble --output confs.sdf
    python conformer_gen.py --smiles "CCO" --action best --output best.sdf
"""

import argparse
import json
import sys
import os
import numpy as np

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, rdMolDescriptors, rdMolAlign
    from rdkit.Chem import rdDistGeom
except ImportError:
    print(json.dumps({"error": "RDKit not installed. pip install rdkit-pypi"}))
    sys.exit(1)


def validate_smiles(smiles: str):
    """Validate and return RDKit mol from SMILES."""
    if not smiles or len(smiles) > 2000:
        return None
    mol = Chem.MolFromSmiles(smiles)
    return mol


def generate_conformers(smiles: str, num_confs: int = 10, seed: int = 42,
                        optimize: str = "mmff", energy_window: float = None,
                        prune_rms: float = 0.5):
    """Generate 3D conformer ensemble with ETKDG."""
    mol = validate_smiles(smiles)
    if mol is None:
        return {"error": f"Invalid SMILES: {smiles}"}

    mol = Chem.AddHs(mol)

    # ETKDG parameters
    params = rdDistGeom.ETKDGv3()
    params.randomSeed = seed
    params.pruneRmsThresh = prune_rms
    params.numThreads = 0  # use all cores

    # Generate conformers
    conf_ids = rdDistGeom.EmbedMultipleConfs(mol, numConfs=num_confs, params=params)

    if len(conf_ids) == 0:
        return {"error": "Failed to generate conformers. Molecule may be too constrained."}

    # Optimize with force field
    energies = []
    converged = []
    if optimize == "mmff":
        results = AllChem.MMFFOptimizeMoleculeConfs(mol, maxIters=500)
        for conv, energy in results:
            converged.append(conv == 0)
            energies.append(round(energy, 4))
    elif optimize == "uff":
        results = AllChem.UFFOptimizeMoleculeConfs(mol, maxIters=500)
        for conv, energy in results:
            converged.append(conv == 0)
            energies.append(round(energy, 4))
    else:
        energies = [None] * len(conf_ids)
        converged = [None] * len(conf_ids)

    # Filter by energy window if specified
    if energy_window and energies[0] is not None:
        min_energy = min(energies)
        mask = [e - min_energy <= energy_window for e in energies]
    else:
        mask = [True] * len(conf_ids)

    # Build conformer data
    conformers = []
    for i, cid in enumerate(conf_ids):
        if not mask[i]:
            continue
        conf = mol.GetConformer(cid)
        rel_energy = round(energies[i] - min(energies), 4) if energies[i] is not None else None
        conformers.append({
            "conf_id": int(cid),
            "energy_kcal": energies[i],
            "relative_energy_kcal": rel_energy,
            "converged": converged[i],
        })

    # Sort by energy
    if conformers and conformers[0]["energy_kcal"] is not None:
        conformers.sort(key=lambda c: c["energy_kcal"])

    # RMSD matrix for top conformers (max 20 for performance)
    rmsd_confs = [c["conf_id"] for c in conformers[:20]]
    rmsd_matrix = []
    if len(rmsd_confs) > 1:
        for i, ci in enumerate(rmsd_confs):
            row = []
            for j, cj in enumerate(rmsd_confs):
                if i == j:
                    row.append(0.0)
                elif j < i:
                    row.append(rmsd_matrix[j][i])  # symmetric
                else:
                    rmsd = rdMolAlign.GetBestRMS(mol, mol, ci, cj)
                    row.append(round(rmsd, 4))
            rmsd_matrix.append(row)

    return {
        "smiles": Chem.MolToSmiles(Chem.RemoveHs(mol)),
        "num_requested": num_confs,
        "num_generated": len(conformers),
        "force_field": optimize,
        "prune_rms_threshold": prune_rms,
        "energy_window_kcal": energy_window,
        "conformers": conformers,
        "rmsd_matrix": rmsd_matrix if rmsd_matrix else None,
        "mol": mol  # keep for SDF writing
    }


def write_sdf(mol, conformers, output_path: str):
    """Write conformers to SDF file."""
    writer = Chem.SDWriter(output_path)
    for conf_data in conformers:
        cid = conf_data["conf_id"]
        mol.SetProp("ConformerID", str(cid))
        if conf_data["energy_kcal"] is not None:
            mol.SetProp("Energy_kcal", str(conf_data["energy_kcal"]))
            mol.SetProp("RelativeEnergy_kcal", str(conf_data["relative_energy_kcal"]))
        writer.write(mol, confId=cid)
    writer.close()


def get_best_conformer(smiles: str, optimize: str = "mmff"):
    """Get the lowest-energy conformer."""
    result = generate_conformers(smiles, num_confs=50, optimize=optimize,
                                  prune_rms=0.35)
    if "error" in result:
        return result

    best = result["conformers"][0]
    mol = result["mol"]
    conf = mol.GetConformer(best["conf_id"])

    # Get 3D coordinates
    coords = []
    for i in range(mol.GetNumAtoms()):
        pos = conf.GetAtomPosition(i)
        atom = mol.GetAtomWithIdx(i)
        coords.append({
            "atom": atom.GetSymbol(),
            "idx": i,
            "x": round(pos.x, 4),
            "y": round(pos.y, 4),
            "z": round(pos.z, 4)
        })

    return {
        "smiles": result["smiles"],
        "best_conformer": best,
        "total_generated": result["num_generated"],
        "coordinates": coords
    }


def main():
    parser = argparse.ArgumentParser(description="3D Conformer Generation")
    parser.add_argument("--smiles", required=True, help="Input SMILES string")
    parser.add_argument("--action", choices=["generate", "ensemble", "best"],
                        default="generate", help="Action to perform")
    parser.add_argument("--num_confs", type=int, default=10, help="Number of conformers")
    parser.add_argument("--optimize", choices=["mmff", "uff", "none"], default="mmff")
    parser.add_argument("--energy_window", type=float, default=None,
                        help="Energy window in kcal/mol (filter high-energy confs)")
    parser.add_argument("--prune_rms", type=float, default=0.5,
                        help="RMSD threshold for pruning similar conformers")
    parser.add_argument("--output", type=str, default=None, help="Output SDF file path")
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if args.action == "best":
        result = get_best_conformer(args.smiles, optimize=args.optimize)
        if "error" not in result and args.output:
            # For best, regenerate to get mol object
            full = generate_conformers(args.smiles, num_confs=50, optimize=args.optimize)
            if "error" not in full:
                write_sdf(full["mol"], [full["conformers"][0]], args.output)
                result["sdf_file"] = args.output
        print(json.dumps({k: v for k, v in result.items() if k != "mol"}, indent=2))

    elif args.action in ("generate", "ensemble"):
        result = generate_conformers(
            args.smiles, num_confs=args.num_confs, seed=args.seed,
            optimize=args.optimize, energy_window=args.energy_window,
            prune_rms=args.prune_rms
        )
        if "error" not in result and args.output:
            write_sdf(result["mol"], result["conformers"], args.output)
            result["sdf_file"] = args.output

        # Remove mol object before JSON serialization
        output = {k: v for k, v in result.items() if k != "mol"}
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
