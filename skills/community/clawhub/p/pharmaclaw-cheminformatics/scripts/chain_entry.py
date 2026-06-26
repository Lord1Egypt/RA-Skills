#!/usr/bin/env python3
"""Cheminformatics Agent — Chain Entry Point.

Standard agent chain interface for the PharmaClaw cheminformatics agent.
Accepts SMILES input and runs a comprehensive cheminformatics profile:
conformers, pharmacophores, RECAP fragmentation, stereoisomer analysis,
and format conversion.

Usage:
    python chain_entry.py --input-json '{"smiles": "CC(=O)Nc1ccc(O)cc1", "context": "user"}'
    python chain_entry.py --input-json '{"smiles": "CC(=O)Nc1ccc(O)cc1", "actions": ["conformers", "pharmacophore"]}'
"""

import argparse
import json
import sys
import os
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Import modules
sys.path.insert(0, SCRIPT_DIR)

try:
    from rdkit import Chem
except ImportError:
    print(json.dumps({"error": "RDKit not installed. pip install rdkit-pypi"}))
    sys.exit(1)


def run_module(module_name: str, func_name: str, **kwargs):
    """Dynamically import and run a module function."""
    try:
        mod = __import__(module_name)
        func = getattr(mod, func_name)
        return func(**kwargs)
    except Exception as e:
        return {"error": f"{module_name}.{func_name} failed: {str(e)}"}


def validate_smiles(smiles: str):
    """Validate SMILES input."""
    if not smiles or len(smiles) > 2000:
        return None
    mol = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(mol) if mol else None


def run_chain(input_data: dict):
    """Run full cheminformatics chain on a SMILES input."""
    smiles = input_data.get("smiles", "")
    context = input_data.get("context", "chain")
    actions = input_data.get("actions", None)
    output_dir = input_data.get("output_dir", None)

    # Validate
    canonical = validate_smiles(smiles)
    if canonical is None:
        return {
            "agent": "cheminformatics",
            "version": "1.0.0",
            "status": "error",
            "error": f"Invalid SMILES: {smiles}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    # Default: run all actions
    all_actions = ["conformers", "pharmacophore", "recap", "stereoisomers", "formats"]
    if actions:
        run_actions = [a for a in actions if a in all_actions]
    else:
        run_actions = all_actions

    report = {}
    risks = []
    warnings = []
    viz = []

    # 1. Conformer generation
    if "conformers" in run_actions:
        conf_result = run_module("conformer_gen", "generate_conformers",
                                  smiles=smiles, num_confs=20, optimize="mmff")
        if "error" not in conf_result:
            # Write SDF if output dir specified
            if output_dir:
                sdf_path = os.path.join(output_dir, "conformers.sdf")
                try:
                    mol = conf_result.get("mol")
                    if mol:
                        from conformer_gen import write_sdf
                        write_sdf(mol, conf_result["conformers"], sdf_path)
                        viz.append(sdf_path)
                except Exception:
                    pass
            # Remove mol object for serialization
            conf_result = {k: v for k, v in conf_result.items() if k != "mol"}
        report["conformers"] = conf_result

    # 2. Pharmacophore features
    if "pharmacophore" in run_actions:
        pharm_result = run_module("pharmacophore", "extract_features", smiles=smiles)
        report["pharmacophore"] = pharm_result

        # Flag low feature count
        if "error" not in pharm_result:
            summary = pharm_result.get("summary", {})
            if summary.get("HBD", 0) == 0 and summary.get("HBA", 0) == 0:
                warnings.append("No hydrogen bond donors or acceptors detected")

        # Generate pharmacophore map if output dir specified
        if output_dir and "error" not in pharm_result:
            map_path = os.path.join(output_dir, "pharmacophore_map.png")
            map_result = run_module("pharmacophore", "pharmacophore_map",
                                    smiles=smiles, output_path=map_path)
            if "error" not in map_result:
                viz.append(map_path)

    # 3. RECAP fragmentation
    if "recap" in run_actions:
        recap_result = run_module("recap_fragment", "fragment_molecule", smiles=smiles)
        report["recap"] = recap_result

        if "error" not in recap_result:
            num_frags = recap_result.get("num_fragments", 0)
            if num_frags == 0:
                warnings.append("No RECAP-cleavable bonds found — molecule may be a simple building block")

    # 4. Stereoisomer enumeration
    if "stereoisomers" in run_actions:
        stereo_result = run_module("stereoisomers", "enumerate_stereoisomers",
                                    smiles=smiles, max_isomers=32)
        report["stereoisomers"] = stereo_result

        if "error" not in stereo_result:
            num_iso = stereo_result.get("enumeration", {}).get("num_generated", 0)
            if num_iso > 1:
                risks.append(f"Molecule has {num_iso} stereoisomers — each must be characterized for drug development (FDA requirement)")

    # 5. Format conversion summary
    if "formats" in run_actions:
        format_result = run_module("format_converter", "convert_mol",
                                    mol=Chem.MolFromSmiles(canonical),
                                    to_format="inchi")
        report["formats"] = {
            "canonical_smiles": canonical,
            "inchi": format_result.get("value") if "error" not in format_result else None,
            "available_conversions": ["smiles", "sdf", "mol", "inchi", "inchikey", "pdb", "xyz"]
        }

    # Determine recommendations for next agent
    recommend_next = []
    if "pharmacophore" in report and "error" not in report.get("pharmacophore", {}):
        recommend_next.append("pharmacology")  # ADME profiling
    if "conformers" in report and "error" not in report.get("conformers", {}):
        recommend_next.append("catalyst-design")  # 3D info useful for catalyst selection
    if "stereoisomers" in report:
        stereo = report.get("stereoisomers", {})
        if stereo.get("enumeration", {}).get("num_generated", 0) > 1:
            recommend_next.append("ip-expansion")  # Stereoisomers = patentable variants

    return {
        "agent": "cheminformatics",
        "version": "1.0.0",
        "smiles": canonical,
        "status": "success",
        "context": context,
        "report": report,
        "risks": risks,
        "warnings": warnings,
        "viz": viz,
        "recommend_next": recommend_next,
        "confidence": 0.9,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def main():
    parser = argparse.ArgumentParser(description="Cheminformatics Agent Chain Entry")
    parser.add_argument("--input-json", required=True, help="JSON input string")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Directory for output files (SDF, PNG)")

    args = parser.parse_args()

    try:
        input_data = json.loads(args.input_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {str(e)}"}))
        sys.exit(1)

    if args.output_dir:
        input_data["output_dir"] = args.output_dir

    result = run_chain(input_data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
