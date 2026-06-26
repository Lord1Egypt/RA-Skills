#!/usr/bin/env python3
"""
diagnose.py — 3D print failure diagnosis tool.

Usage:
  diagnose.py --symptoms "stringing,warping"
  diagnose.py --description "my print has lots of hair between parts and the corners lifted"
  diagnose.py --symptoms "stringing" --description "also some zits on the surface"
  diagnose.py --symptoms "stringing" --json  # JSON output only
"""

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Failure knowledge base (matches failure-types.md)
# ---------------------------------------------------------------------------

FAILURES = [
    {
        "id": "stringing",
        "name": "Stringing / Oozing",
        "keywords": ["stringing", "oozing", "hair", "cobweb", "wisp", "thread", "spider", "hairs", "webbing", "strings"],
        "causes": [
            "Retraction distance too short",
            "Retraction speed too slow",
            "Print temperature too high",
            "Travel speed too slow",
            "Wet/moisture-laden filament (especially PETG/Nylon)",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Retraction length: 2–4 mm (direct drive: 0.5–1.5 mm)",
                "Retraction speed: 45–60 mm/s",
                "Minimum travel after retraction: 2 mm",
                "Enable 'Wipe before retract'",
                "Reduce nozzle temperature by 5–10°C (e.g. PLA 200→190°C)",
            ],
            "Cura": [
                "Retraction distance: 5–7 mm (Bowden) / 1–2 mm (direct drive)",
                "Retraction speed: 45–55 mm/s",
                "Minimum retraction travel: 1.5–2 mm",
                "Combing mode: All",
                "Travel speed: 150–200 mm/s",
            ],
            "OrcaSlicer": [
                "Retraction length: 1–2 mm (direct drive) / 4–6 mm (Bowden)",
                "Retraction speed: 35–60 mm/s",
                "Travel distance threshold: 2 mm",
                "Enable 'Wipe on loops'",
                "Reduce temperature 5°C and test",
            ],
        },
        "reference": "failure-types.md → Stringing, slicer-fixes.md → Stringing",
    },
    {
        "id": "warping",
        "name": "Warping / Bed Adhesion Failure",
        "keywords": ["warping", "warp", "lifting", "corner lift", "peel", "adhesion", "detach", "pop off", "unstuck", "lift", "corners up"],
        "causes": [
            "Bed not level or Z offset too high",
            "Bed temperature too low",
            "No brim",
            "Cooling too aggressive on first layers",
            "Wrong bed surface for material",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Brim width: 8–12 mm, brim offset: 0 mm",
                "Bed temp: PLA 60–65°C, ABS 100–110°C, PETG 75–85°C",
                "Fan speed for first 3 layers: 0%",
                "Enable draft shield for ABS/ASA",
            ],
            "Cura": [
                "Build plate adhesion: Brim, width 8–12 mm",
                "Initial layer temperature: +5°C above print temp",
                "Bed temp: PLA 60–65°C, ABS 100–110°C, PETG 80°C",
                "Fan speed first layer: 0%",
            ],
            "OrcaSlicer": [
                "Brim: Mouse ear or outer brim, width 8 mm",
                "First layer bed temp: PLA 65°C, PETG 80°C, ABS 110°C",
                "First layer speed: 20 mm/s",
                "Chamber temp for ABS/ASA: 40–50°C if enclosed",
            ],
        },
        "reference": "failure-types.md → Warping, slicer-fixes.md → Warping",
    },
    {
        "id": "layer_adhesion",
        "name": "Layer Adhesion / Delamination",
        "keywords": ["layer adhesion", "delamination", "layer split", "layer separation", "weak layers", "splitting", "cracking", "fracture", "delaminate", "crack", "brittle", "breaks at layer"],
        "causes": [
            "Print temperature too low",
            "Layer height too tall relative to nozzle diameter",
            "Print speed too fast",
            "Cooling too aggressive",
            "Old or wet filament",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Nozzle temperature: increase by 5–10°C",
                "Layer height: max 0.3 mm for 0.4 mm nozzle (75% rule)",
                "Print speed: reduce to 40–50 mm/s",
                "Fan speed: reduce by 20–30%",
            ],
            "Cura": [
                "Print temperature: increase 5–10°C",
                "Layer height: reduce to 0.2 mm for 0.4 mm nozzle",
                "Print speed: 40 mm/s",
                "Fan speed: 30–50% for PLA; 0–20% for ABS/PETG",
            ],
            "OrcaSlicer": [
                "Nozzle temp: increase 5–10°C",
                "Max layer height: 75% of nozzle diameter",
                "Perimeter speed: reduce to 40 mm/s",
                "Fan: reduce by 20%",
            ],
        },
        "reference": "failure-types.md → Layer Adhesion, slicer-fixes.md → Layer Adhesion",
    },
    {
        "id": "under_extrusion",
        "name": "Under-Extrusion",
        "keywords": ["under extrusion", "underextrusion", "gaps", "sparse", "weak", "thin layers", "missing material", "incomplete", "holes in walls", "translucent", "not enough filament"],
        "causes": [
            "Extruder steps/mm not calibrated",
            "Nozzle partial clog",
            "Print speed too fast for flow rate",
            "Temperature too low for filament",
            "Flow rate too low in slicer",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Extrusion multiplier: increase 1.00 → 1.05 (5% steps, max ~1.15)",
                "Temperature: increase 5°C",
                "Speed: reduce to 40 mm/s overall",
                "Calibrate extruder E-steps (100 mm commanded = 100 mm extruded)",
            ],
            "Cura": [
                "Flow rate: increase to 105% (test up to 115%)",
                "Print temperature: increase 5°C",
                "Print speed: reduce to 40 mm/s",
            ],
            "OrcaSlicer": [
                "Filament flow ratio: increase 0.02–0.05",
                "Temperature: increase 5°C",
                "Outer wall speed: reduce to 35 mm/s",
                "Max volumetric speed: verify not too high (PLA max ~11 mm³/s)",
            ],
        },
        "reference": "failure-types.md → Under-Extrusion, slicer-fixes.md → Under-Extrusion",
    },
    {
        "id": "over_extrusion",
        "name": "Over-Extrusion / Blobbing",
        "keywords": ["over extrusion", "overextrusion", "blob", "bulge", "zit", "seam bump", "rough surface", "too much material", "fat lines", "blobby", "lumpy"],
        "causes": [
            "Flow rate (extrusion multiplier) too high",
            "Extruder steps/mm miscalibrated",
            "Temperature too high (low viscosity)",
            "Retraction insufficient",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Extrusion multiplier: reduce 1.00 → 0.95 (5% steps)",
                "Temperature: reduce 5°C",
                "Retraction: increase by 0.5 mm",
            ],
            "Cura": [
                "Flow rate: reduce to 95%",
                "Print temperature: reduce 5°C",
            ],
            "OrcaSlicer": [
                "Flow ratio: reduce by 0.03–0.05",
                "Temperature: reduce 5°C",
                "Run pressure advance calibration",
            ],
        },
        "reference": "failure-types.md → Over-Extrusion, slicer-fixes.md → Over-Extrusion",
    },
    {
        "id": "elephant_foot",
        "name": "Elephant Foot",
        "keywords": ["elephant foot", "flared base", "first layer squish", "wide base", "bottom flare", "splayed", "flare at bottom", "base too wide"],
        "causes": [
            "Z offset too low (nozzle too close to bed)",
            "First layer flow rate too high",
            "Bed temperature too high",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Elephant foot compensation: 0.1–0.3 mm (Print Settings → Advanced)",
                "First layer height: 0.2 mm minimum",
                "First layer extrusion width: 100–120% max",
                "Z offset: raise by 0.05 mm increments",
            ],
            "Cura": [
                "Initial layer horizontal expansion: -0.1 to -0.2 mm",
                "First layer flow: reduce to 95%",
                "Z offset: raise nozzle slightly",
            ],
            "OrcaSlicer": [
                "Elephant foot compensation: 0.1–0.2 mm",
                "First layer flow: 95%",
                "Z offset: increase by 0.05 mm and observe",
            ],
        },
        "reference": "failure-types.md → Elephant Foot, slicer-fixes.md → Elephant Foot",
    },
    {
        "id": "layer_shifting",
        "name": "Layer Shifting / Skipping",
        "keywords": ["layer shift", "layer skip", "offset", "misaligned layers", "shifted", "staircase", "x shift", "y shift", "axis skip", "slipped", "off center"],
        "causes": [
            "Print speed too fast for belt tension",
            "Loose belt (X or Y axis)",
            "Acceleration too high",
            "Print head collision with model",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Print speed: reduce to 60 mm/s (from 80–100)",
                "Acceleration: reduce to 500–800 mm/s² (from 1000–2000)",
                "Note: also check belt tension — not slicer-fixable alone",
            ],
            "Cura": [
                "Print speed: reduce to 50–60 mm/s",
                "Acceleration: 500 mm/s² (enable Acceleration Control)",
                "Jerk control: enable, set 8 mm/s for X/Y",
            ],
            "OrcaSlicer": [
                "Speed: reduce to 60 mm/s",
                "Acceleration: 500 mm/s²",
                "Jerk: reduce to 8 mm/s",
            ],
        },
        "reference": "failure-types.md → Layer Shifting, slicer-fixes.md → Layer Shifting",
    },
    {
        "id": "bridging",
        "name": "Poor Bridging",
        "keywords": ["bridging", "bridge", "sag", "drooping", "hanging", "span", "overhang droop", "bridge failure", "bridge sag"],
        "causes": [
            "Bridge speed too slow (filament spends more time hot)",
            "Cooling insufficient on bridges",
            "Temperature too high",
            "Bridge flow too high",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Bridging speed: 20–30 mm/s",
                "Bridging fan speed: 100%",
                "Bridging flow: 0.9–0.95",
                "Enable 'Detect bridging perimeters'",
            ],
            "Cura": [
                "Bridge speed: 20–30 mm/s",
                "Bridge fan speed: 100%",
                "Bridge wall flow: 90%",
            ],
            "OrcaSlicer": [
                "Bridge speed: 25 mm/s",
                "Bridge fan speed: 100%",
                "Bridge flow ratio: 0.90",
            ],
        },
        "reference": "failure-types.md → Bridging, slicer-fixes.md → Bridging",
    },
    {
        "id": "overhang",
        "name": "Overhang Quality Issues",
        "keywords": ["overhang", "drooping", "curling", "overhang failure", "cantilever", "curl up", "overhang quality", "overhang bad", "curled edges"],
        "causes": [
            "Overhang angle exceeds material capability (>45–50°)",
            "Cooling insufficient",
            "Temperature too high",
            "Print speed too high on overhangs",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Fan speed: 100% for overhangs (PLA)",
                "Overhang speed: reduce to 15–25 mm/s for steep angles",
                "Extra perimeters if needed: enabled",
                "Support threshold: 45–50° for PLA, 40° for PETG/ABS",
            ],
            "Cura": [
                "Fan speed: 100% on overhangs",
                "Speed for 50–89% overhang: 20 mm/s",
                "Support angle threshold: 50° (PLA), 45° (PETG)",
            ],
            "OrcaSlicer": [
                "Overhang speed: 20 mm/s at 50%+ overhang",
                "Fan: 100% for overhangs",
                "Support threshold: 40–50°",
            ],
        },
        "reference": "failure-types.md → Overhang, slicer-fixes.md → Overhang",
    },
    {
        "id": "clog",
        "name": "Clogged Nozzle / Grinding",
        "keywords": ["clog", "clogged", "grinding", "clicking", "extruder skip", "stripped filament", "no extrusion", "jam", "clicking sound", "skipping", "no flow"],
        "causes": [
            "Nozzle partially blocked by burnt filament or debris",
            "Temperature too low for material",
            "Print speed too fast for flow rate",
            "PTFE tube degraded/melted",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Temperature: PLA ≥ 200°C, PETG ≥ 230°C, ABS ≥ 240°C",
                "Max volumetric speed: reduce to 8 mm³/s for PLA",
                "Note: perform cold pull to clear clog (manual fix required)",
            ],
            "Cura": [
                "Print temperature: ensure minimum (PLA 200°C, PETG 235°C)",
                "Max flow rate: reduce by 10–15%",
                "Note: perform cold pull (manual)",
            ],
            "OrcaSlicer": [
                "Nozzle temperature: at minimum for material",
                "Reduce max volumetric speed by 10%",
                "Use nozzle purge before print start",
            ],
        },
        "reference": "failure-types.md → Clogged Nozzle, slicer-fixes.md → Clogged Nozzle",
    },
    {
        "id": "pillowing",
        "name": "Pillowing / Poor Top Surface",
        "keywords": ["pillowing", "top surface", "holes on top", "bulging top", "wavy top", "pockmarks", "top layer gap", "top holes", "top infill gap"],
        "causes": [
            "Top solid layers count too low",
            "Infill percentage too low",
            "Cooling insufficient on top layers",
            "Top layer speed too fast",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Top solid layers: 5–7 (increase from 3)",
                "Top surface pattern: Monotonic or Concentric",
                "Top infill speed: 30–40 mm/s",
                "Fan speed top layer: 100% (PLA)",
                "Infill: minimum 20–25%",
            ],
            "Cura": [
                "Top layers: 5–7",
                "Top surface skin layers: +1–2 additional",
                "Top/bottom speed: 30–40 mm/s",
                "Infill density: 20% minimum",
            ],
            "OrcaSlicer": [
                "Top shell layers: 5–7",
                "Top surface pattern: Monotonic",
                "Top speed: 30 mm/s",
                "Enable ironing for smooth top surface",
            ],
        },
        "reference": "failure-types.md → Pillowing, slicer-fixes.md → Pillowing",
    },
    {
        "id": "ringing",
        "name": "Ringing / Ghosting",
        "keywords": ["ringing", "ghosting", "vibration", "ripple", "echo", "resonance", "wave pattern", "surface ripple", "wavy walls", "artifact"],
        "causes": [
            "Print speed too high",
            "Acceleration/jerk settings too high",
            "Mechanical looseness (belts, gantry)",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Perimeter speed: reduce to 40–60 mm/s",
                "Acceleration: reduce to 500–700 mm/s²",
                "If running Klipper: enable input shaper",
            ],
            "Cura": [
                "Print speed: reduce to 50 mm/s",
                "Acceleration: 500 mm/s² (enable Acceleration Control)",
                "Jerk: 8 mm/s (enable Jerk Control)",
            ],
            "OrcaSlicer": [
                "Outer wall speed: reduce to 40 mm/s",
                "Acceleration: 500 mm/s²",
                "Jerk: 8 mm/s",
                "Run input shaper calibration if supported",
            ],
        },
        "reference": "failure-types.md → Ringing, slicer-fixes.md → Ringing",
    },
    {
        "id": "z_banding",
        "name": "Z-Banding / Inconsistent Layer Height",
        "keywords": ["z banding", "z wobble", "inconsistent layers", "screw artifact", "vertical lines", "banding", "ribbing", "periodic lines", "wavy vertical"],
        "causes": [
            "Z lead screw bent or misaligned",
            "Z coupler loose or eccentric",
            "Z steps/mm slightly off",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Z speed: reduce to 10 mm/s",
                "Use step-aligned layer heights: 0.1, 0.15, 0.2, 0.25, 0.3 mm",
                "Note: primarily a mechanical fix (check Z coupler, lead screw)",
            ],
            "Cura": [
                "Z speed: reduce",
                "Use step-aligned layer heights",
            ],
            "OrcaSlicer": [
                "Use step-aligned layer heights",
                "Z hop speed: reduce to 5–8 mm/s",
            ],
        },
        "reference": "failure-types.md → Z-Banding, slicer-fixes.md → Z-Banding",
    },
    {
        "id": "seam",
        "name": "Seam / Zit Visibility",
        "keywords": ["seam", "zit", "seam line", "visible seam", "layer start", "blob on seam", "seam artifact", "vertical line", "seam visible"],
        "causes": [
            "Seam placement not optimized",
            "Retraction settings not dialed in",
            "Pressure advance not tuned",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Seam position: Aligned or Rear",
                "Use seam painting to place on back/concave feature",
                "Wipe: enabled, length 1.5–2 mm",
                "Tune Pressure Advance (Klipper) or Linear Advance (Marlin)",
            ],
            "Cura": [
                "Seam corner preference: Smart hiding or Sharpest corner",
                "Z seam alignment: Back",
                "Coasting: enable, volume 0.064 mm³ (0.4 mm nozzle, 0.2 mm layer)",
            ],
            "OrcaSlicer": [
                "Seam: Aligned or Back",
                "Wipe on loops: enabled",
                "Scarf seam: enable (blends seam over a distance)",
                "Tune pressure advance",
            ],
        },
        "reference": "failure-types.md → Seam, slicer-fixes.md → Seam",
    },
    {
        "id": "supports",
        "name": "Support Issues",
        "keywords": ["support stuck", "support won't come off", "support mark", "support failure", "support didn't work", "support over-adhesion", "support too strong", "support left marks"],
        "causes": [
            "Support Z distance too small (over-adhesion) or too large (failure)",
            "Support interface layers missing",
            "Support density incorrect",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Support Z distance: 0.15–0.2 mm",
                "Support interface layers: 2–3",
                "Interface density: 80–100%",
                "Pattern: Rectilinear or Gyroid for easier removal",
            ],
            "Cura": [
                "Support Z distance: 0.15–0.2 mm",
                "Support interface: enable, thickness 0.6–1.0 mm",
                "Interface density: 33–50% for easy removal",
                "Support type: Tree for organic shapes",
            ],
            "OrcaSlicer": [
                "Support top Z distance: 0.2 mm",
                "Support interface: 2 layers",
                "Interface density: 50%",
                "Enable tree supports for complex geometry",
            ],
        },
        "reference": "failure-types.md → Support Issues, slicer-fixes.md → Supports",
    },
    {
        "id": "first_layer",
        "name": "First Layer Issues",
        "keywords": ["first layer", "adhesion problem", "first layer gap", "first layer squish", "bed level", "not sticking", "peeling off bed", "first layer bad"],
        "causes": [
            "Z offset incorrect",
            "Bed not level",
            "Bed surface contaminated",
            "First layer speed too high",
        ],
        "fixes": {
            "PrusaSlicer": [
                "First layer height: 0.2 mm (or 50–75% of layer height)",
                "First layer speed: 15–25 mm/s",
                "First layer extrusion width: 120–150%",
                "Z offset: paper test — slight drag",
                "Bed temp: PLA 60°C, PETG 80°C, ABS 100°C",
            ],
            "Cura": [
                "Initial layer height: 0.2–0.3 mm",
                "Initial layer speed: 20 mm/s",
                "Initial layer flow: 100%",
                "Enable skirt/brim for priming",
            ],
            "OrcaSlicer": [
                "First layer height: 0.2 mm",
                "First layer speed: 20 mm/s",
                "First layer width: 120%",
                "Run built-in Z offset calibration print",
                "Clean bed with IPA before each print",
            ],
        },
        "reference": "failure-types.md → First Layer, slicer-fixes.md → First Layer",
    },
    {
        "id": "wet_filament",
        "name": "Wet Filament / Moisture Damage",
        "keywords": ["wet filament", "moisture", "bubbling", "popping", "hissing", "crackling", "steam", "rough from moisture", "snapping", "crackling sound", "popping sound"],
        "causes": [
            "Filament stored without desiccant",
            "Humidity above 40–50% RH during printing",
            "Hygroscopic material (PETG, Nylon, TPU, PVA) exposed to air",
        ],
        "fixes": {
            "PrusaSlicer": [
                "Dry filament first — slicer cannot fix moisture",
                "Temperature: increase 5–10°C (forces moisture out faster)",
                "Speed: reduce by 20%",
                "Dry times: PLA 45°C/4–6h, PETG 55°C/6–8h, Nylon 70–80°C/8–12h",
            ],
            "Cura": [
                "Dry filament first",
                "Temperature: increase 5–10°C",
                "Speed: reduce 20%",
                "Print a purge line before print",
            ],
            "OrcaSlicer": [
                "Dry filament first",
                "Temperature: increase 5–10°C",
                "Speed: reduce 20%",
                "Use filament dryer box while printing",
            ],
        },
        "reference": "failure-types.md → Wet Filament, slicer-fixes.md → Wet Filament",
    },
]


# ---------------------------------------------------------------------------
# Scoring logic
# ---------------------------------------------------------------------------

def normalize(text):
    """Lowercase and strip punctuation for matching."""
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


def score_failure(failure, tokens):
    """Return a match score (0–100) for a failure given input tokens."""
    score = 0
    matched_keywords = []
    norm_tokens = " ".join(tokens)

    for kw in failure["keywords"]:
        norm_kw = normalize(kw)
        # Exact keyword phrase match
        if norm_kw in norm_tokens:
            score += 20
            matched_keywords.append(kw)
            continue
        # Partial word overlap
        kw_words = norm_kw.split()
        for word in kw_words:
            if len(word) >= 4 and word in norm_tokens:
                score += 8
                if kw not in matched_keywords:
                    matched_keywords.append(kw)
                break

    return min(score, 100), matched_keywords


def confidence_label(score):
    if score >= 60:
        return "high"
    elif score >= 30:
        return "medium"
    elif score > 0:
        return "low"
    return "none"


def diagnose(symptoms_list=None, description=None):
    """Run diagnosis and return sorted list of results."""
    tokens = []

    if symptoms_list:
        for s in symptoms_list:
            tokens.extend(normalize(s).split())
    if description:
        tokens.extend(normalize(description).split())

    if not tokens:
        return []

    results = []
    for failure in FAILURES:
        score, matched = score_failure(failure, tokens)
        if score > 0:
            results.append({
                "failure_type": failure["name"],
                "failure_id": failure["id"],
                "confidence": confidence_label(score),
                "confidence_score": score,
                "matched_symptoms": matched,
                "causes": failure["causes"],
                "fixes": failure["fixes"],
                "reference": failure["reference"],
            })

    results.sort(key=lambda x: x["confidence_score"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_human(results, symptoms_input, description_input):
    """Print human-readable diagnosis."""
    print("\n" + "=" * 60)
    print("  3D Print Failure Diagnosis")
    print("=" * 60)

    if symptoms_input:
        print(f"Symptoms: {', '.join(symptoms_input)}")
    if description_input:
        print(f"Description: {description_input}")
    print()

    if not results:
        print("No matching failure types found.")
        print("Try describing symptoms like: stringing, warping, layer adhesion,")
        print("under extrusion, elephant foot, layer shifting, clogged, etc.")
        return

    # Only show results with a meaningful score
    shown = [r for r in results if r["confidence_score"] >= 10]
    if not shown:
        shown = results[:3]

    for i, r in enumerate(shown[:5], 1):
        conf = r["confidence"].upper()
        print(f"{'─' * 60}")
        print(f"#{i} {r['failure_type']}  [{conf} confidence]")
        print(f"    Matched: {', '.join(r['matched_symptoms'])}")
        print()

        print("  Likely Causes:")
        for cause in r["causes"]:
            print(f"    • {cause}")
        print()

        print("  Recommended Fixes:")
        for slicer, fix_list in r["fixes"].items():
            print(f"    [{slicer}]")
            for fix in fix_list:
                print(f"      → {fix}")
        print()
        print(f"  Reference: {r['reference']}")
        print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Diagnose 3D print failures from symptoms or description."
    )
    parser.add_argument(
        "--symptoms", "-s",
        help='Comma-separated symptom list (e.g. "stringing,warping,poor adhesion")',
    )
    parser.add_argument(
        "--description", "-d",
        help="Free-text description of the failure",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        dest="json_output",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--top", "-n",
        type=int,
        default=5,
        help="Number of results to show (default: 5)",
    )

    args = parser.parse_args()

    if not args.symptoms and not args.description:
        parser.print_help()
        print("\nError: provide --symptoms and/or --description")
        sys.exit(1)

    symptoms_list = [s.strip() for s in args.symptoms.split(",")] if args.symptoms else []
    description = args.description or None

    results = diagnose(symptoms_list, description)
    top_results = results[: args.top]

    if args.json_output:
        output = {
            "input": {
                "symptoms": symptoms_list,
                "description": description,
            },
            "results": top_results,
        }
        print(json.dumps(output, indent=2))
    else:
        print_human(top_results, symptoms_list, description)


if __name__ == "__main__":
    main()
