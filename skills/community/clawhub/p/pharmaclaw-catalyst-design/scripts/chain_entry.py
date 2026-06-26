#!/usr/bin/env python3
"""Chain Entry Point for Catalyst Design Agent.

Standard interface for PharmaClaw agent chaining. Accepts JSON input and routes
to recommendation or ligand design workflows.

Usage:
    python chain_entry.py --input-json '{"reaction": "suzuki", "context": "retrosynthesis"}'
    python chain_entry.py --input-json '{"scaffold": "PPh3", "strategy": "all", "context": "optimization"}'
    python chain_entry.py --input-json '{"reaction": "C-N coupling", "substrate": "ClC1=CC=CC=C1", "enantioselective": true}'
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))

from catalyst_recommend import recommend
from ligand_designer import design_ligands


def chain_run(input_data: dict) -> dict:
    """Route input to appropriate catalyst design workflow."""
    context = input_data.get("context", "user")
    results = {}

    # Determine what to run
    has_reaction = "reaction" in input_data or "reaction_type" in input_data
    has_scaffold = "scaffold" in input_data or "ligand" in input_data

    # 1. Catalyst recommendation
    if has_reaction:
        reaction = input_data.get("reaction") or input_data.get("reaction_type")
        substrate = input_data.get("substrate") or input_data.get("smiles")
        constraints = input_data.get("constraints", {})
        enantio = input_data.get("enantioselective", False)
        results["recommendation"] = recommend(reaction, substrate, constraints, enantio)

    # 2. Ligand design
    if has_scaffold:
        scaffold = input_data.get("scaffold") or input_data.get("ligand")
        strategy = input_data.get("strategy", "all")
        draw = input_data.get("draw", False)
        results["ligand_design"] = design_ligands(scaffold, strategy, draw)

    # 3. If both reaction and scaffold given, also suggest ligand modifications for top catalyst
    if has_reaction and not has_scaffold and results.get("recommendation", {}).get("results"):
        top = results["recommendation"]["results"][0]
        if top.get("abbreviation"):
            # Try to get ligand SMILES from the recommendation
            from catalyst_recommend import load_database
            db = load_database()
            for cat in db["catalysts"]:
                if cat["id"] == top["catalyst_id"] and cat.get("ligand_smiles"):
                    results["ligand_optimization"] = design_ligands(
                        cat["ligand_smiles"], "all", draw=False
                    )
                    break

    # Build unified output
    status = "success" if results else "error"
    recommend_next = set()
    if results.get("recommendation", {}).get("results"):
        recommend_next.update(["chemistry-query", "pharmacology"])
    if results.get("ligand_design", {}).get("variants"):
        recommend_next.update(["ip-expansion", "chemistry-query"])

    return {
        "agent": "catalyst-design",
        "version": "1.0.0",
        "context": context,
        "status": status,
        "report": results,
        "recommend_next": sorted(recommend_next),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Catalyst Design Agent - Chain Entry")
    parser.add_argument("--input-json", required=True, help="JSON input string")
    args = parser.parse_args()

    try:
        input_data = json.loads(args.input_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"agent": "catalyst-design", "status": "error", "error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    result = chain_run(input_data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
