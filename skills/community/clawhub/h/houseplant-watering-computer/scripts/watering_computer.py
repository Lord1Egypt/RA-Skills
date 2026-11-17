#!/usr/bin/env python3
"""Houseplant watering computer — per-pot soil water balance.

Subcommands:
  compute       Dryout time + dose for one pot (substrate, geometry, demand)
  check         Interpret a moisture observation (finger test / meter / weight)
  symptoms      Route visual symptoms to over/under-watering + fixes
  selfwatering  Reservoir sizing for wick/cache pots (incl. vacation math)

Model: pot reservoir = substrate volume x WHC x usable fraction.
Demand = plant class base rate x light x VPD(temp,RH) x season.
Dryout days = reservoir / demand. Dose = ~20-25% of substrate volume.

Stdlib only. Offline. Numbers are starting points — verify with finger test.
"""
import argparse
import json
import math

# --- substrate table: (WHC mL per L substrate, usable fraction of that,
#     drainage class)
SUBSTRATES = {
    # name: (whc_ml_per_L, usable_frac, note)
    "peat-mix":      (500, 0.60, "standard potting mix (peat/coir based)"),
    "peat-perlite":  (400, 0.62, "50/50 mix, faster draining"),
    "cactus-mix":    (280, 0.65, "mineral-heavy, fast dryout"),
    "bark-aroid":    (220, 0.70, "chunky aroid/orchid-adjacent mix"),
    "leca":          (350, 0.55, "semi-hydro expanded clay, wick-fed"),
    "garden-soil":   (620, 0.45, "compacts in pots — replace with peat-mix"),
    "unknown":       (450, 0.55, "assumed typical potting mix — verify"),
}

# --- plant demand: base transpiration mL/day per L of substrate at baseline
#     (bright-indirect light, 22C, 45%RH, summer-ish)
PLANTS = {
    "small-foliage":  (22, "pothos cutting, small snake, 10-15cm pot plants"),
    "medium-foliage": (38, "typical pothos/philodendron/peace lily size"),
    "large-foliage":  (60, "monstera, ficus, bird of paradise, floor plants"),
    "succulent":      (10, "echeveria, haworthia, jade"),
    "cactus":         (7,  "desert cacti"),
    "fern":           (55, "maidenhair, boston — high transpiration"),
    "flowering":      (65, "in-bloom plants, high demand"),
}

LIGHT_MULT = {
    "low": 0.55,           # north window / deep room
    "medium-indirect": 0.8,
    "bright-indirect": 1.0,  # baseline
    "some-direct": 1.35,   # east/west window sun part of day
    "full-sun": 1.8,       # south window / outdoors
}

SEASON_MULT = {"summer": 1.15, "spring": 1.0, "fall": 0.85, "winter": 0.6}


def vpd_kpa(temp_c, rh):
    """Vapor pressure deficit (kPa) via Tetens."""
    es = 0.6108 * math.exp(17.27 * temp_c / (temp_c + 237.3))
    return es * (1 - rh / 100.0)


def vpd_mult(temp_c, rh):
    """Demand multiplier from VPD (1.0 at ~22C/45% => ~1.45 kPa)."""
    v = vpd_kpa(temp_c, rh)
    m = 0.6 + (v - 0.4) * (0.4 / 1.05)
    return max(0.4, min(2.0, m))


def pot_volume(args):
    """Substrate volume in L. Tapered pot = truncated cone; else cylinder."""
    if getattr(args, "pot_tapered", None):
        top, bot, h = [float(x) for x in args.pot_tapered.split(",")]
        r1, r2 = top / 2, bot / 2
        vol_cc = (math.pi * h / 3) * (r1 * r1 + r1 * r2 + r2 * r2)
    else:
        d, h = [float(x) for x in args.pot_cylinder.split(",")]
        r = d / 2
        vol_cc = math.pi * r * r * h
    # 15% of pot volume is root mass/roughness, not substrate
    return vol_cc / 1000.0 * 0.85


# ------------------------------------------------------------------ compute

def cmd_compute(a):
    if a.substrate not in SUBSTRATES:
        return {"error": f"unknown substrate {a.substrate}",
                "known": sorted(SUBSTRATES)}
    if a.plant not in PLANTS:
        return {"error": f"unknown plant class {a.plant}",
                "known": sorted(PLANTS)}
    vol_l = pot_volume(a)
    whc, usable, note = SUBSTRATES[a.substrate]
    reservoir_ml = vol_l * 1000 * whc / 1000 * usable  # mL usable water

    base, pdesc = PLANTS[a.plant]
    lm = LIGHT_MULT[a.light]
    vm = vpd_mult(a.temp, a.humidity)
    sm = SEASON_MULT[a.season]
    demand_ml_day = base * vol_l**0.85 * lm * vm * sm

    dryout_days = reservoir_ml / demand_ml_day
    dose_ml = vol_l * 1000 * 0.22  # 22% of substrate volume per watering

    v = vpd_kpa(a.temp, a.humidity)
    return {
        "pot": {
            "substrate_volume_L": round(vol_l, 2),
            "substrate": f"{a.substrate} ({note}), WHC {whc} mL/L, usable {usable:.0%}",
        },
        "water": {
            "usable_reservoir_ml": round(reservoir_ml),
            "dose_per_watering_ml": round(dose_ml),
            "dose_rule": "~20-25% of substrate volume, until slight runoff",
        },
        "demand": {
            "plant_class": f"{a.plant} ({pdesc})",
            "light": f"{a.light} x{lm}",
            "vpd": f"{v:.2f} kPa (T={a.temp}C RH={a.humidity}%) x{vm:.2f}",
            "season": f"{a.season} x{sm}",
            "total_ml_per_day": round(demand_ml_day, 1),
        },
        "answer": {
            "dryout_days": round(dryout_days, 1),
            "check_interval_days": max(1, round(dryout_days * 0.7)),
            "expected_interval_days": [max(1, round(dryout_days * 0.8)),
                                       max(1, round(dryout_days * 1.1))],
            "method": "Water when the top 2-4cm is dry (finger test) — the interval above is the physics, your finger is the truth.",
        },
        "warnings": [],
    }


# ------------------------------------------------------------------ check

def cmd_check(a):
    vol_l = pot_volume(a)
    whc, usable, _ = SUBSTRATES.get(getattr(a, "substrate", None) or "unknown",
                                    SUBSTRATES["unknown"])
    reservoir_ml = vol_l * whc * usable

    depth_map = {"shallow": "top 2-3cm", "mid": "5-7cm", "deep": "10+cm / bottom"}
    feels = a.feels.lower()
    if feels in ("dry", "dry-ish", "slightly-dry"):
        state, act = "DRY ZONE", "Water now with the computed dose; check drainage."
    elif feels == "moist":
        state, act = "USABLE MOISTURE", "Hold. Re-check in 1-2 days (small pots) / 2-4 days (large)."
    elif feels in ("wet", "soggy"):
        state, act = "SATURATED", "No water. If >10 days like this: root-rot risk — see `symptoms`."
    else:
        state, act = "UNKNOWN", "Describe feels as dry / moist / wet."

    out = {"observation": f"finger to {depth_map[a.finger_depth]}: {a.feels}",
           "zone": state, "action": act,
           "pot_reservoir_context": f"pot holds ~{reservoir_ml:.0f} mL usable; you sampled {depth_map[a.finger_depth]}",
           "weight_tip": "Pick the pot up right after watering and again at each check — weight is the fastest honest moisture meter."}
    if a.finger_depth == "shallow" and vol_l > 4:
        out["warning"] = (f"{vol_l:.0f}L substrate: the top can be dry while the "
                          "bottom is soaked. Use a bamboo skewer to the bottom, or weight.")
    return out


# ------------------------------------------------------------------ symptoms

SYMPTOM_ROUTER = {
    "wet": {
        "diagnosis": "OVERWATERED / root rot developing",
        "mechanism": "Saturated substrate excludes oxygen; roots suffocate and die; "
                     "dead roots can't take up water, so the plant wilts IN wet soil.",
        "actions": [
            "Stop watering. Move to brighter light if possible (raises demand).",
            "Check roots: unpot, smell (rot = swamp smell), trim black/mushy roots with sterile scissors.",
            "Repot in fresh airy mix (peat-perlite or bark-aroid); remove garden-soil pots entirely.",
            "Fungus gnats present? See the gnat protocol — same wet-soil cause.",
        ],
    },
    "dry-soil": {
        "diagnosis": "UNDERWATERED (or hydrophobic substrate)",
        "mechanism": "Demand exceeded supply; peat mixes go hydrophobic when fully dry "
                     "and shed water instead of absorbing it.",
        "actions": [
            "Bottom-soak: sit the pot in a water basin 20-30 min until it drinks.",
            "If water runs straight through: hydrophobic — soak + a drop of dish soap "
            "in the basin to break surface tension.",
            "Return to computed dose; increase check frequency in heat/VPD spikes.",
        ],
    },
}


def cmd_symptoms(a):
    out = {"inputs": {"yellowing": a.yellowing, "soil": a.soil,
                      "wilting": a.wilting, "gnats": a.gnats,
                      "brown_tips": a.brown_tips}}
    routing = SYMPTOM_ROUTER[a.soil]
    out["primary"] = {"diagnosis": routing["diagnosis"],
                      "mechanism": routing["mechanism"],
                      "actions": routing["actions"]}

    if a.soil == "wet" and a.wilting:
        out["classic_trap"] = ("Wilting + wet soil reads as 'needs water' — it's the "
                               "opposite: rotted roots can't drink. Watering more kills faster.")
    if a.gnats:
        out["fungus_gnats"] = {
            "cause": "Larvae eat fungus in constantly-wet topsoil; adults are the flying nuisance.",
            "protocol": [
                "1. Dry-out discipline: let top 3-4 cm dry between waterings (breaks the lifecycle).",
                "2. Bottom-water for 3 weeks: adults can't lay in dry topsoil.",
                "3. Yellow sticky traps for adults.",
                "4. Persistent: BTI (Bacillus thuringiensis israelensis) granules in the water — kills larvae, safe otherwise.",
                "5. Top-dress 1 cm of sand/grit: physical barrier to egg-laying.",
            ],
            "timeline": "Lifecycle ~3-4 weeks; expect adults gone in 2 generations if topsoil discipline holds.",
        }
    if a.yellowing == "lower" and a.soil == "wet":
        out["yellowing_read"] = "Lower/oldest leaves yellowing + wet soil = classic overwatering signature."
    elif a.yellowing == "lower" and a.soil == "dry":
        out["yellowing_read"] = "Lower yellowing + dry soil can be underwatering OR normal oldest-leaf senescence — check the dryout math."
    if a.brown_tips and a.soil == "dry":
        out["brown_tips_read"] = "Brown crispy tips + dry cycles: chronic underwatering or low humidity (VPD)."
    elif a.brown_tips and a.soil == "wet":
        out["brown_tips_read"] = "Brown tips + wet soil: overwatering root stress OR salt/fluoride accumulation — flush the pot with 2-3x volume water."
    return out


# ------------------------------------------------------------------ selfwatering

def cmd_selfwatering(a):
    vol_l = pot_volume(a)
    whc, usable, _ = SUBSTRATES[a.substrate]
    reservoir_ml = vol_l * whc * usable
    # assume medium demand, bright-indirect, baseline VPD if not given
    base, _ = PLANTS["medium-foliage"]
    demand = base * vol_l**0.85 * 1.0 * 1.0 * 1.0
    days_needed = a.away_days + 2  # margin
    needed_ml = demand * days_needed
    in_pot_ml = reservoir_ml * 0.8  # don't count on the last 20%

    gap_ml = max(0.0, needed_ml - in_pot_ml)
    return {
        "pot": {"substrate_volume_L": round(vol_l, 2),
                "in_pot_usable_ml": round(in_pot_ml)},
        "trip": {"days_with_margin": days_needed,
                 "total_need_ml": round(needed_ml),
                 "demand_assumed": "medium foliage, bright-indirect, baseline VPD — re-run compute() with real values for precision"},
        "external_reservoir_needed_ml": round(gap_ml),
        "reservoir_verdict": (
            f"A {gap_ml/1000:.1f} L external reservoir + wick delivers the gap. "
            if gap_ml > 0 else
            "The pot itself holds enough water for the trip — just saturate thoroughly before leaving. "),
        "wick_notes": [
            "Cotton rope wick, 6-10 mm diameter, buried 5+ cm in substrate, dangling to reservoir bottom.",
            "Wick rate self-regulates with demand roughly — but TEST it a week before the trip.",
            "Group pots: one reservoir per 3-4 pots, wick per pot.",
            "Rot-prone species (succulents, cacti, sansevieria): no wick — they'll survive the trip dry.",
        ],
        "cache_pot_warning": "Cache pots without drainage raise salt buildup — flush with clear water every 4-6 weeks.",
    }


# ------------------------------------------------------------------ cli

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("compute")
    sp.add_argument("--substrate", default="peat-mix", choices=sorted(SUBSTRATES))
    sp.add_argument("--pot-tapered", help="top_cm,bottom_cm,height_cm")
    sp.add_argument("--pot-cylinder", help="diameter_cm,height_cm")
    sp.add_argument("--plant", default="medium-foliage", choices=sorted(PLANTS))
    sp.add_argument("--light", default="bright-indirect", choices=sorted(LIGHT_MULT))
    sp.add_argument("--temp", type=float, default=22.0)
    sp.add_argument("--humidity", type=float, default=45.0)
    sp.add_argument("--season", default="summer", choices=sorted(SEASON_MULT))
    sp.set_defaults(fn=cmd_compute)

    sp = sub.add_parser("check")
    sp.add_argument("--finger-depth", choices=["shallow", "mid", "deep"], default="shallow")
    sp.add_argument("--feels", required=True, help="dry|moist|wet")
    sp.add_argument("--pot-tapered")
    sp.add_argument("--pot-cylinder")
    sp.add_argument("--substrate", choices=sorted(SUBSTRATES))
    sp.set_defaults(fn=cmd_check)

    sp = sub.add_parser("symptoms")
    sp.add_argument("--soil", required=True, choices=["wet", "dry"])
    sp.add_argument("--yellowing", choices=["lower", "overall", "none"], default="none")
    sp.add_argument("--wilting", action="store_true")
    sp.add_argument("--gnats", action="store_true")
    sp.add_argument("--brown-tips", action="store_true")
    sp.set_defaults(fn=cmd_symptoms)

    sp = sub.add_parser("selfwatering")
    sp.add_argument("--pot-tapered")
    sp.add_argument("--pot-cylinder")
    sp.add_argument("--substrate", default="peat-mix", choices=sorted(SUBSTRATES))
    sp.add_argument("--away-days", type=float, default=14.0)
    sp.set_defaults(fn=cmd_selfwatering)

    args = ap.parse_args()
    print(json.dumps(args.fn(args), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
