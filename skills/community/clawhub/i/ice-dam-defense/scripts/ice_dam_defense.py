#!/usr/bin/env python3
"""ice-dam-defense: sidewalk/driveway de-icing planner + ice-dam risk assessor.

Pure-stdlib. Two tools:
  sidewalk  — area de-icing: melt-chemistry (NaCl eutectic -21C, MgCl2 -33C, CaCl2 -30C,
              blend availability), application rates by pavement temp band, spreader
              calibration, freeze-refreeze warning, corrosions/plant/pet warnings.
  roof      — ice-dam risk: attic insulation/ventilation/leak questionnaire scored 0-100,
              snow-load estimate (depth x density x area -> kg), snow-removal urgency,
              attic-rains/steam-caused damming explanation, safe removal ladder.

Usage:
  python3 ice_dam_defense.py sidewalk --area-sqm 60 --temp-c -8 --material rock-salt
  python3 ice_dam_defense.py sidewalk --area-sqm 100 --temp-c -18 --material mgcl2 --refreeze -3
  python3 ice_dam_defense.py roof --depth-cm 45 --roof-sqm 120 --insulation poor --recessed yes
  python3 ice_dam_defense.py demo
"""
from __future__ import annotations

import argparse
import sys

# ---------------------------------------------------------------- melt chemistry

# name: (min_effective_pavement_temp_C, eutectic_C, lbs_per_1000sqft_light,
#        lbs_per_1000sqft_heavy, corrosion, pet_hazard, plant_hazard, notes)
MATERIALS = {
    "rock-salt": {
        "min_temp_c": -9, "eutectic_c": -21,
        "rate_light": 12, "rate_heavy": 40,   # lbs per 1000 sq ft
        "corrosion": "high (steel/concrete rebar)",
        "pets": "irritates paws; licking causes GI upset",
        "plants": "soil sodium accumulation kills roadside plants",
        "notes": "Halite (NaCl). Cheapest, most available. Stops working as a MELTER below "
                 "-9C pavement temp even though eutectic is -21C (dissolution too slow).",
    },
    "mgcl2": {
        "min_temp_c": -15, "eutectic_c": -33,
        "rate_light": 10, "rate_heavy": 32,
        "corrosion": "moderate",
        "pets": "less paw irritation than NaCl but hygroscopic - can burn wet paws",
        "plants": "less damaging than NaCl",
        "notes": "Magnesium chloride, usually as flakes/pellets. Exothermic on dissolving "
                 "(releases heat) - works faster and colder than rock salt.",
    },
    "cacl2": {
        "min_temp_c": -25, "eutectic_c": -30,  # practical -25, eutectic around -30 at 30%
        "rate_light": 8, "rate_heavy": 28,
        "corrosion": "moderate-high",
        "pets": "hygroscopic; can burn paws - rinse after walks",
        "pets_extra": "at high concentration generates heat on wet skin",
        "plants": "moderate damage",
        "notes": "Calcium chloride. Most exothermic (- releases heat on contact with water) "
                 "so it melts fastest and coldest; often blended with NaCl to cut cost.",
    },
    "nacl-cacl2-blend": {
        "min_temp_c": -18, "eutectic_c": -31,
        "rate_light": 11, "rate_heavy": 36,
        "corrosion": "high",
        "pets": "same as rock salt",
        "ports_extra": "",
        "plants": "high damage",
        "notes": "Pre-wetted or blended products; CaCl2 portion kick-starts melting, NaCl "
                 "provides bulk at lower cost.",
    },
    "kac-acetate": {
        "min_temp_c": -25, "eutectic_c": -60,
        "rate_light": 9, "rate_heavy": 30,
        "corrosion": "negligible (chloride-free)",
        "pets": "safe for paws",
        "plants": "negligible damage; potassium is a nutrient",
        "notes": "Potassium acetate. Airport-grade, chloride-free, environmentally gentle - "
                 "and priced accordingly (5-10x salt).",
    },
    "cma": {
        "min_temp_c": -9, "eutectic_c": -21,  # CMA works to about -9 practically
        "rate_light": 15, "rate_heavy": 45,
        "corrosion": "negligible",
        "pets": "safe for paws",
        "plants": "negligible; biodegrades",
        "notes": "Calcium magnesium acetate. Chloride-free, gentle on concrete (ideal for "
                 "new concrete <1 y old) - but slower and needs more product.",
    },
    "sand-ash": {
        "min_temp_c": -99, "eutectic_c": None,
        "rate_light": 40, "rate_heavy": 100,
        "corrosion": "none (but clogs drains)",
        "pets": "safe",
        "plants": "safe",
        "notes": "No melting - traction only. The honest choice below -20C or on fresh "
                 "concrete; sweep up before spring rains or drains pay for it.",
    },
}

# ---------------------------------------------------------------- sidewalk tool

SQFT_PER_SQM = 10.7639
LB_PER_KG = 2.20462


def sidewalk_plan(area_sqm: float, temp_c: float, material: str, heavy: bool,
                  refreeze_c: float | None) -> dict:
    m = MATERIALS[material]
    sqft = area_sqm * SQFT_PER_SQM
    k_factor = sqft / 1000
    rate = m["rate_heavy"] if heavy else m["rate_light"]
    lbs = rate * k_factor
    kg = lbs / LB_PER_KG

    works = temp_c >= m["min_temp_c"]

    # pre-wet brine guidance: brine uses ~1/3 the salt of granular for anti-icing
    brine_gal = round(k_factor * (2.0 if heavy else 0.8), 1)  # gal per 1000 sqft rough

    out = {
        "area_sqm": area_sqm, "area_sqft": round(sqft, 1),
        "pavement_temp_c": temp_c, "material": material,
        "material_min_effective_c": m["min_temp_c"],
        "works_at_this_temp": works,
        "application_lbs": round(lbs, 1), "application_kg": round(kg, 2),
        "mode": "heavy ice/compacted snow" if heavy else "light ice / anti-ice pre-treat",
        "brine_alternative_gal": brine_gal,
        "warnings": [],
    }
    if not works:
        out["warnings"].append(
            f"{material} stops melting effectively below {m['min_effective_c' if False else 'min_temp_c']}C pavement temp "
            f"(you have {temp_c}C). Options: switch to cacl2/kac-acetate, or use sand-ash for traction and "
            "wait for sun/warmer hours.")
    if material in ("rock-salt", "nacl-cacl2-blend") and temp_c < -5:
        out["warnings"].append(
            "NaCl dissolution is slow below -5C even when it 'works' - expect 30+ min to bare pavement; "
            "CaCl2/MgCl2 act in minutes.")
    if refreeze_c is not None and refreeze_c < -2:
        out["warnings"].append(
            f"Refreeze forecast {refreeze_c}C tonight: melted brine WILL refreeze. Either apply early "
            "evening (anti-ice) or plan a second pass; slush pushed to edges becomes black ice.")
    if material == "sand-ash" and temp_c > 0:
        out["warnings"].append("Above 0C sand adds nothing - switch to melting or plain shoveling.")
    out["corrosion"] = m["corrosion"]
    out["pets"] = m["pets"]
    out["plants"] = m["plants"]
    out["notes"] = m["notes"]
    return out


def render_sidewalk(p: dict) -> str:
    L = []
    bar = "=" * 64
    L += [bar, "SIDEWALK / DRIVEWAY DE-ICING PLAN", bar]
    L.append(f"Area: {p['area_sqm']} m² ({p['area_sqft']} sq ft)   Pavement temp: {p['pavement_temp_c']}C")
    L.append(f"Material: {p['material']}   Mode: {p['mode']}")
    L.append("")
    L.append(f"APPLICATION: {p['application_kg']} kg  ({p['application_lbs']} lbs)")
    if p["works_at_this_temp"]:
        L.append(f"  {p['material']} is effective at {p['pavement_temp_c']}C "
                 f"(works to {p['material_min_effective_c']}C pavement temp).")
    else:
        L.append(f"  !! {p['material']} is BELOW its effective range at {p['pavement_temp_c']}C.")
    L.append(f"  Brine alternative (anti-ice, uses ~1/3 the salt): ~{p['brine_alternative_gal']} gal")
    L.append("")
    if p["warnings"]:
        L.append("WARNINGS:")
        for w in p["warnings"]:
            L.append(f"  ! {w}")
        L.append("")
    L.append("MATERIAL PROFILE:")
    L.append(f"  Corrosion: {p['corrosion']}")
    L.append(f"  Pets:      {p['pets']}")
    L.append(f"  Plants:    {p['plants']}")
    L.append(f"  {p['notes']}")
    L.append("")
    L.append("TECHNIQUE:")
    L.append("  1. SHOVEL FIRST. De-icer melts thin layers, not 5 cm of snow - scattering")
    L.append("     product on deep snow wastes it and concentrates chloride runoff.")
    L.append("  2. Spread evenly at the listed rate; more is NOT faster, just saltier.")
    L.append("     A coffee mug (~350 g) covers ~10 m² at light rate.")
    L.append("  3. Anti-icing (before the storm) beats de-icing: brine spray the evening")
    L.append("     before prevents the bond - needs ~1/3 the chemical.")
    L.append("  4. Fresh concrete (<1 year): chlorides + freeze-thaw pit the surface - use")
    L.append("     CMA or sand only.")
    L.append("  5. Pets: wipe paws after walks; booties for long ones.")
    return "\n".join(L)


# ---------------------------------------------------------------- roof tool

RISK_FACTORS = {
    # question key: (weight_if_yes, explanation)
    "insulation_poor": (25, "Thin/absent attic insulation lets house heat reach the roof deck."),
    "recessed_lights": (15, "Recessed ceiling lights leak warm air directly into the attic."),
    "bathroom_fan_vents_attic": (15, "Warm humid fan exhaust in the attic = frost + melt at the deck."),
    "attic_hatch_unsealed": (10, "An unsealed hatch is a chimney for warm air."),
    "flue_ducts_unsealed": (10, "Gaps around flues/duct chases dump heat into the attic."),
    "low_ventilation": (10, "Insufficient soffit+ridge ventilation can't flush attic heat."),
    "valleys_dormers": (10, "Valleys, dormers, and roof-wall joints trap snow and promote dams."),
    "gutters_frozen": (10, "Full/frozen gutters give meltwater a place to back up."),
    "past_dams": (20, "Previous ice dams are the single best predictor of future ones."),
    "deep_snow_on_roof": (10, "Deep snow on a warm roof = fuel for melting; heavy regardless."),
}

SNOW_DENSITY = {  # kg/m3
    "fresh": 70, "settled": 150, "packed": 250, "wet": 300, "ice_layered": 400,
}


def roof_risk(depth_cm: float, roof_sqm: float, answers: dict[str, bool],
              snow_type: str = "settled") -> dict:
    score = sum(w for k, (w, _x) in RISK_FACTORS.items() if answers.get(k))
    density = SNOW_DENSITY.get(snow_type, 150)
    snow_load_kg = depth_cm / 100 * roof_sqm * density
    # typical residential snow-load capacity: ~180 kg/m2 (varies by code/region)
    load_per_sqm = density * depth_cm / 100
    capacity = 180
    load_pct = load_per_sqm / capacity * 100

    if score >= 60:
        risk = "HIGH"
    elif score >= 35:
        risk = "MODERATE"
    else:
        risk = "LOW"

    urgency = "none"
    if load_pct >= 100:
        urgency = "structural-now"
    elif load_pct >= 75:
        urgency = "remove-priority"
    elif load_pct >= 50:
        urgency = "watch"

    return {
        "score": score, "risk": risk,
        "snow_load_kg": round(snow_load_kg), "load_per_sqm": round(load_per_sqm),
        "load_pct_of_typical": round(load_pct),
        "urgency": urgency, "factors_hit": [k for k in RISK_FACTORS if answers.get(k)],
    }


def render_roof(r: dict, depth_cm: float, roof_sqm: float, snow_type: str) -> str:
    L = []
    bar = "=" * 64
    L += [bar, "ROOF ICE-DAM RISK + SNOW LOAD", bar]
    L.append(f"Snow: {depth_cm} cm of {snow_type} snow on {roof_sqm} m² roof")
    L.append(f"Snow load: ~{r['snow_load_kg']:,} kg total  ({r['load_per_sqm']} kg/m² "
             f"= {r['load_pct_of_typical']}% of a typical 180 kg/m² residential capacity)")
    L.append(f"Risk score: {r['score']}/100  ->  {r['risk']} ice-dam risk")
    if r["factors_hit"]:
        L.append("Contributing factors:")
        for k in r["factors_hit"]:
            L.append(f"  x {k}: {RISK_FACTORS[k][1]}")
    L.append("")
    L.append("SNOW-REMOVAL URGENCY: ", )
    u = r["urgency"]
    if u == "structural-now":
        L.append("  !! STRUCTURAL: load exceeds typical capacity - remove snow now (roof rake")
        L.append("     from the ground; do NOT climb the roof). Watch for door jams, cracking,")
        L.append("     sagging. If those appear: leave and call a professional.")
    elif u == "remove-priority":
        L.append("  High load - rake the roof within 24 h, especially valleys and eaves.")
    elif u == "watch":
        L.append("  Moderate load - rake after the next snowfall; watch for added wet snow.")
    else:
        L.append("  Low load - no action needed for weight.")
    L.append("")
    L.append("ICE-DAM PLAYBOOK (how dams form: warm attic melts roof snow; water refreezes")
    L.append("at the cold eave and dams; backed water wicks under shingles):")
    L.append("  1. NOW: roof-rake the lower 1-1.5 m of roof + above valleys. From the ground.")
    L.append("  2. NEVER: axe/hammer the ice itself - you will crack shingles and the roof deck.")
    l3 = ("  3. Channels: if water is actively leaking, a professional can steam (not chip) a")
    L.append(l3)
    L.append("     channel through the dam. Filling a sock with calcium chloride and laying it")
    L.append("     across the dam melts a drain path (avoid pure NaCl - corrosive to fasteners).")
    L.append("  4. FIX THE CAUSE (before next winter): air-seal the attic (hatch, lights, flues),")
    L.append("     top up insulation to R-49+ / ~40 cm, verify soffit+ridge ventilation, extend")
    L.append("     bathroom/kitchen fans to the exterior, install heated eave cables if the")
    L.append("     attic can't be fixed (e.g., cathedral ceilings).")
    L.append("  5. INSIDE LEAK RESPONSE: catch water with buckets + plastic sheeting, poke a")
    L.append("     small drain hole in the bulging drywall if needed - relieving the water beats")
    L.append("     letting it spread. Then dry properly (mold in 48 h).")
    return "\n".join(L)


def demo() -> str:
    p = sidewalk_plan(60, -8, "rock-salt", heavy=False, refreeze_c=-12)
    r = roof_risk(45, 120, {
        "insulation_poor": True, "recessed_lights": True,
        "bathroom_fan_vents_attic": True, "past_dams": True,
        "valleys_dormers": True, "deep_snow_on_roof": True,
    }, snow_type="settled")
    return render_sidewalk(p) + "\n\n" + render_roof(r, 45, 120, "settled")


def main(argv=None):
    ap = argparse.ArgumentParser(description="De-icing planner + ice-dam risk assessor")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sidewalk", help="sidewalk/driveway de-icing plan")
    s.add_argument("--area-sqm", type=float, required=True)
    s.add_argument("--temp-c", type=float, required=True, help="PAVEMENT temp (not air)")
    s.add_argument("--material", default="rock-salt", choices=sorted(MATERIALS))
    s.add_argument("--heavy", action="store_true", help="compacted ice (vs light/anti-ice)")
    s.add_argument("--refreeze", type=float, dest="refreeze_c", help="overnight low, C")

    r = sub.add_parser("roof", help="ice-dam risk + snow load")
    r.add_argument("--depth-cm", type=float, required=True)
    r.add_argument("--roof-sqm", type=float, required=True)
    chemistry = r.add_argument("--snow-type", default="settled", choices=sorted(SNOW_DENSITY))
    for flag in RISK_FACTORS:
        r.add_argument(f"--{flag.replace('_', '-')}", dest=flag, action="store_true", default=False)
    r.add_argument("--demo", action="store_true")

    sub.add_parser("demo")

    args = ap.parse_args(argv)
    if args.cmd == "demo":
        print(demo())
        return
    if args.cmd == "sidewalk":
        print(render_sidewalk(sidewalk_plan(
            args.area_sqm, args.temp_c, args.material, args.heavy, args.refreeze_c)))
    if args.cmd == "roof":
        answers = {k: getattr(args, k) for k in RISK_FACTORS}
        rr = roof_risk(args.depth_cm, args.roof_sqm, answers, args.snow_type)
        print(render_roof(rr, args.depth_cm, args.roof_sqm, args.snow_type))


if __name__ == "__main__":
    main(sys.argv[1:])
