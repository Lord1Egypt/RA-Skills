#!/usr/bin/env python3
"""Catalyst Recommendation Engine.

Recommends organometallic catalysts for a given reaction type, substrate, or synthesis step.
Searches curated database + optional PubChem/literature lookup.

Usage:
    python catalyst_recommend.py --reaction suzuki
    python catalyst_recommend.py --reaction "C-N coupling" --substrate "ClC1=CC=CC=C1" --constraints '{"prefer_metal":"Pd","max_cost":"high"}'
    python catalyst_recommend.py --reaction asymmetric_hydrogenation --enantioselective
"""

import argparse
import json
import os
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "references" / "catalyst_database.json"


def load_database():
    with open(DB_PATH) as f:
        return json.load(f)


def normalize_reaction(reaction_str: str, reaction_map: dict) -> list[str]:
    """Map user input to canonical reaction type keys."""
    r = reaction_str.strip().lower().replace("-", "_").replace(" ", "_")
    # Direct match
    if r in reaction_map:
        return [r]
    # Fuzzy match: check if input is substring of key or description
    matches = []
    for key, desc in reaction_map.items():
        if r in key or r in desc.lower():
            matches.append(key)
    # Common aliases
    aliases = {
        "c_n": ["buchwald_hartwig", "c_n_coupling"],
        "amination": ["buchwald_hartwig", "c_n_coupling"],
        "coupling": ["suzuki", "heck", "sonogashira", "negishi", "kumada", "stille"],
        "cross_coupling": ["suzuki", "heck", "sonogashira", "negishi", "kumada", "stille"],
        "metathesis": ["olefin_metathesis", "ring_closing_metathesis", "cross_metathesis"],
        "rcm": ["ring_closing_metathesis"],
        "click": ["click_CuAAC", "azide_alkyne_cycloaddition"],
        "hydrogenation": ["hydrogenation", "asymmetric_hydrogenation", "directed_hydrogenation"],
    }
    if r in aliases:
        matches.extend(aliases[r])
    return list(set(matches)) if matches else [r]


def score_catalyst(catalyst: dict, reaction_types: list[str], constraints: dict, enantioselective: bool) -> float:
    """Score a catalyst 0-100 based on match quality."""
    score = 0.0

    # Reaction type match (0-50 points)
    matched = set(catalyst["reaction_types"]) & set(reaction_types)
    if not matched:
        return 0.0
    score += 50.0 * len(matched) / len(reaction_types)

    # Cost preference (0-15 points)
    cost_scores = {"very_low": 15, "low": 12, "medium": 9, "high": 5, "very_high": 2}
    max_cost = constraints.get("max_cost", "very_high")
    cost_rank = list(cost_scores.keys())
    cat_cost = catalyst.get("cost_relative", "medium")
    if cost_rank.index(cat_cost) <= cost_rank.index(max_cost):
        score += cost_scores.get(cat_cost, 5)

    # Metal preference (0-10 points)
    if constraints.get("prefer_metal"):
        if catalyst["metal"].lower() == constraints["prefer_metal"].lower():
            score += 10

    # Earth-abundant bonus (0-5 points)
    if constraints.get("prefer_earth_abundant"):
        if catalyst["metal"] in ["Ni", "Cu", "Fe", "Zr"]:
            score += 5

    # Enantioselective bonus (0-10 points)
    if enantioselective:
        enantio_types = {"asymmetric_hydrogenation", "asymmetric_isomerization"}
        if set(catalyst["reaction_types"]) & enantio_types:
            score += 10
        elif "BINAP" in catalyst.get("ligand", "") or "chiral" in catalyst.get("name", "").lower():
            score += 5

    # Advantages count (0-5 points)
    score += min(5, len(catalyst.get("advantages", [])))

    # Low loading bonus (0-5 points)
    loading = catalyst.get("typical_loading_mol_pct", [5, 10])
    if loading[0] <= 1:
        score += 5
    elif loading[0] <= 2:
        score += 3

    return min(100.0, score)


def recommend(reaction: str, substrate: str = None, constraints: dict = None, enantioselective: bool = False) -> dict:
    """Main recommendation engine."""
    db = load_database()
    constraints = constraints or {}
    reaction_types = normalize_reaction(reaction, db["reaction_type_map"])

    results = []
    for cat in db["catalysts"]:
        score = score_catalyst(cat, reaction_types, constraints, enantioselective)
        if score > 0:
            results.append({
                "catalyst_id": cat["id"],
                "name": cat["name"],
                "abbreviation": cat["abbreviation"],
                "metal": cat["metal"],
                "ligand": cat["ligand"],
                "score": round(score, 1),
                "matched_reactions": sorted(set(cat["reaction_types"]) & set(reaction_types)),
                "conditions": cat["conditions"],
                "loading_mol_pct": cat["typical_loading_mol_pct"],
                "advantages": cat["advantages"],
                "limitations": cat["limitations"],
                "cost": cat["cost_relative"],
                "references": cat["references"],
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "agent": "catalyst-design",
        "version": "1.0.0",
        "action": "recommend",
        "query": {
            "reaction": reaction,
            "normalized_types": reaction_types,
            "substrate": substrate,
            "constraints": constraints,
            "enantioselective": enantioselective,
        },
        "results": results,
        "total_matches": len(results),
        "status": "success" if results else "no_matches",
        "suggestion": None if results else f"No catalysts found for '{reaction}'. Try broader terms like 'coupling' or 'hydrogenation'.",
    }


def main():
    parser = argparse.ArgumentParser(description="Catalyst Recommendation Engine")
    parser.add_argument("--reaction", required=True, help="Reaction type (e.g., suzuki, C-N coupling, metathesis)")
    parser.add_argument("--substrate", help="Substrate SMILES (for context)")
    parser.add_argument("--constraints", help="JSON constraints: {prefer_metal, max_cost, prefer_earth_abundant}")
    parser.add_argument("--enantioselective", action="store_true", help="Prioritize enantioselective catalysts")
    args = parser.parse_args()

    constraints = json.loads(args.constraints) if args.constraints else {}
    result = recommend(args.reaction, args.substrate, constraints, args.enantioselective)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
