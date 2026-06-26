#!/usr/bin/env python3
"""Molecular Format Conversion — SDF, MOL, SMILES, InChI, PDB, XYZ.

Converts between chemical file formats using RDKit. Handles single molecules
and multi-molecule SDF files.

Usage:
    python format_converter.py --input mol.sdf --to smiles
    python format_converter.py --smiles "CCO" --to sdf --output ethanol.sdf
    python format_converter.py --smiles "CCO" --to mol --output ethanol.mol
    python format_converter.py --smiles "CCO" --to inchi
    python format_converter.py --input mols.sdf --to smiles --batch
    python format_converter.py --smiles "CCO" --to pdb --output ethanol.pdb
"""

import argparse
import json
import sys
import os

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, inchi, rdmolfiles
except ImportError:
    print(json.dumps({"error": "RDKit not installed. pip install rdkit-pypi"}))
    sys.exit(1)


SUPPORTED_FORMATS = ["smiles", "sdf", "mol", "inchi", "inchikey", "pdb", "xyz", "mol2"]


def _sanitize_path(path: str) -> str:
    """Basic path sanitization."""
    if not path or len(path) > 500:
        return None
    if "\x00" in path:
        return None
    # Block path traversal
    norm = os.path.normpath(path)
    if ".." in norm.split(os.sep):
        return None
    return path


def mol_from_file(filepath: str):
    """Read molecule(s) from file based on extension."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".sdf" or ext == ".sd":
        suppl = Chem.SDMolSupplier(filepath, removeHs=False)
        mols = [m for m in suppl if m is not None]
        return mols
    elif ext == ".mol":
        mol = Chem.MolFromMolFile(filepath, removeHs=False)
        return [mol] if mol else []
    elif ext == ".pdb":
        mol = Chem.MolFromPDBFile(filepath, removeHs=False)
        return [mol] if mol else []
    elif ext == ".mol2":
        mol = Chem.MolFromMol2File(filepath, removeHs=False)
        return [mol] if mol else []
    else:
        return []


def mol_from_smiles(smiles: str):
    """Create mol from SMILES."""
    if not smiles or len(smiles) > 2000:
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return mol


def convert_mol(mol, to_format: str, output_path: str = None, mol_name: str = ""):
    """Convert a single mol to target format."""
    if mol is None:
        return {"error": "Invalid molecule"}

    result = {"format": to_format}

    if to_format == "smiles":
        result["value"] = Chem.MolToSmiles(mol)

    elif to_format == "inchi":
        inchi_str = inchi.MolToInchi(mol)
        result["value"] = inchi_str

    elif to_format == "inchikey":
        inchi_str = inchi.MolToInchi(mol)
        if inchi_str:
            result["value"] = inchi.InchiToInchiKey(inchi_str)
        else:
            result["error"] = "Could not generate InChI"

    elif to_format == "mol":
        mol_3d = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol_3d, AllChem.ETKDGv3())
        try:
            AllChem.MMFFOptimizeMolecule(mol_3d, maxIters=200)
        except Exception:
            pass
        mol_block = Chem.MolToMolBlock(mol_3d)
        if output_path:
            safe_path = _sanitize_path(output_path)
            if safe_path:
                with open(safe_path, "w") as f:
                    f.write(mol_block)
                result["file"] = safe_path
        result["value"] = mol_block

    elif to_format == "sdf":
        mol_3d = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol_3d, AllChem.ETKDGv3())
        try:
            AllChem.MMFFOptimizeMolecule(mol_3d, maxIters=200)
        except Exception:
            pass
        if output_path:
            safe_path = _sanitize_path(output_path)
            if safe_path:
                writer = Chem.SDWriter(safe_path)
                if mol_name:
                    mol_3d.SetProp("_Name", mol_name)
                writer.write(mol_3d)
                writer.close()
                result["file"] = safe_path
        result["value"] = Chem.MolToMolBlock(mol_3d)

    elif to_format == "pdb":
        mol_3d = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol_3d, AllChem.ETKDGv3())
        try:
            AllChem.MMFFOptimizeMolecule(mol_3d, maxIters=200)
        except Exception:
            pass
        pdb_block = Chem.MolToPDBBlock(mol_3d)
        if output_path:
            safe_path = _sanitize_path(output_path)
            if safe_path:
                with open(safe_path, "w") as f:
                    f.write(pdb_block)
                result["file"] = safe_path
        result["value"] = pdb_block

    elif to_format == "xyz":
        mol_3d = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol_3d, AllChem.ETKDGv3())
        try:
            AllChem.MMFFOptimizeMolecule(mol_3d, maxIters=200)
        except Exception:
            pass
        conf = mol_3d.GetConformer()
        lines = [str(mol_3d.GetNumAtoms()), mol_name or Chem.MolToSmiles(Chem.RemoveHs(mol_3d))]
        for i in range(mol_3d.GetNumAtoms()):
            pos = conf.GetAtomPosition(i)
            atom = mol_3d.GetAtomWithIdx(i)
            lines.append(f"{atom.GetSymbol():2s}  {pos.x:12.6f}  {pos.y:12.6f}  {pos.z:12.6f}")
        xyz_str = "\n".join(lines)
        if output_path:
            safe_path = _sanitize_path(output_path)
            if safe_path:
                with open(safe_path, "w") as f:
                    f.write(xyz_str)
                result["file"] = safe_path
        result["value"] = xyz_str

    else:
        result["error"] = f"Unsupported format: {to_format}"

    return result


def batch_convert(input_path: str, to_format: str, output_path: str = None):
    """Convert multi-molecule file."""
    mols = mol_from_file(input_path)
    if not mols:
        return {"error": f"No valid molecules found in {input_path}"}

    results = []
    for i, mol in enumerate(mols):
        name = mol.GetProp("_Name") if mol.HasProp("_Name") else f"mol_{i}"
        r = convert_mol(mol, to_format, mol_name=name)
        r["index"] = i
        r["name"] = name
        results.append(r)

    # If SDF output, write all to one file
    if to_format == "sdf" and output_path:
        safe_path = _sanitize_path(output_path)
        if safe_path:
            writer = Chem.SDWriter(safe_path)
            for mol in mols:
                mol_3d = Chem.AddHs(mol)
                AllChem.EmbedMolecule(mol_3d, AllChem.ETKDGv3())
                try:
                    AllChem.MMFFOptimizeMolecule(mol_3d, maxIters=200)
                except Exception:
                    pass
                writer.write(mol_3d)
            writer.close()

    return {
        "input_file": input_path,
        "to_format": to_format,
        "num_molecules": len(results),
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(description="Molecular Format Converter")
    parser.add_argument("--smiles", type=str, help="Input SMILES")
    parser.add_argument("--input", type=str, help="Input file (SDF, MOL, PDB)")
    parser.add_argument("--to", required=True, choices=SUPPORTED_FORMATS, help="Target format")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    parser.add_argument("--batch", action="store_true", help="Batch convert multi-mol file")
    parser.add_argument("--name", type=str, default="", help="Molecule name")

    args = parser.parse_args()

    if not args.smiles and not args.input:
        print(json.dumps({"error": "Provide --smiles or --input file"}))
        sys.exit(1)

    if args.batch and args.input:
        result = batch_convert(args.input, args.to, args.output)
    elif args.input:
        mols = mol_from_file(args.input)
        if not mols:
            print(json.dumps({"error": f"Could not read molecule from {args.input}"}))
            sys.exit(1)
        result = convert_mol(mols[0], args.to, args.output, args.name)
    else:
        mol = mol_from_smiles(args.smiles)
        if mol is None:
            print(json.dumps({"error": f"Invalid SMILES: {args.smiles}"}))
            sys.exit(1)
        result = convert_mol(mol, args.to, args.output, args.name)

    # Truncate long values for JSON display
    output = {}
    for k, v in result.items():
        if k == "value" and isinstance(v, str) and len(v) > 5000:
            output[k] = v[:2000] + f"\n... [{len(v)} chars total, written to file]"
        else:
            output[k] = v
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
