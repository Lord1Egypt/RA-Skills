#!/usr/bin/env python3
"""Mattress spec decoder — translate marketing into materials science.

Subcommands:
  recommend  Firmness band + type candidates for one sleeper
  couple     Two-sleeper compromise solving
  decode     Score a spec sheet (densities, coils, stack)
  compare    Two mattresses scored for YOUR profile
  warranty   Decode warranty terms (sag threshold, prorated schedule)
  sag        Verdict for a measured body impression

Stdlib only. Offline. No brand affiliations.
"""
import argparse
import json
import math
import sys

# ---------------------------------------------------------------- constants

# lb/ft3 density bands -> (verdict, expected usable years for comfort layers)
MEMORY_DENSITY = [
    (3.0, "JUNK", "Impressions likely within 1-2 years; avoid", 1.5),
    (4.0, "OK", "3-6 years of softening resistance", 4.5),
    (5.0, "GOOD", "5-8 years; the density sweet spot for memory foam", 6.5),
    (99.0, "EXCELLENT", "8-10+ years; dense, slow-responding, sleeps warmer", 9.0),
]
BASE_DENSITY = [
    (1.5, "JUNK", "Support layer will flatten first — this is where cheap beds cheat", 3.0),
    (1.8, "OK", "Acceptable; heavier bodies will outpace it", 5.5),
    (2.0, "GOOD", "6-8 years of support", 7.0),
    (99.0, "EXCELLENT", "8-10 years; heavy-body safe", 9.0),
]
LATEX_DENSITY = [
    (4.3, "LIGHT", "Softer all-latex; fine for lighter sleepers", 6.0),
    (5.3, "MID", "Dunlop mid density; very durable", 8.0),
    (99.0, "DENSE", "Firm, extremely durable; heavy and runs warm", 10.0),
]

POSITION_BASE_FIRMNESS = {
    "side": (4.0, "shoulder/hip pressure needs give"),
    "back": (6.0, "lumbar support with some contour"),
    "stomach": (7.5, "prevent hip sink pulling spine into extension"),
    "combo": (6.0, "compromise surface for shifting sleepers"),
}

BMI_SHIFT = [
    (19.0, -1.0, "light: softer surface so shoulders/hips sink"),
    (25.0, 0.0, "average band"),
    (30.0, 1.0, "overweight: firmer + denser support required"),
    (99.0, 2.0, "obese: high-density support non-negotiable (>=1.8 lb/ft3 base)"),
]

# queen-equivalent coil guidance
COIL_GUIDE = [
    (300, "JUNK", "Low count; innerspring from a bad era", 3.0),
    (480, "MINIMUM", "Acceptable budget bonnell/offset", 5.0),
    (900, "GOOD", "Pocketed-onc coil sweet spot", 7.0),
    (10**9, "MARKETING", "900+ is marketing above the knee of the curve", 7.5),
]

HEAVY_KG = 100  # ~220 lb


def band(value, table, label):
    prev = None
    for thresh, verdict, why, years in table:
        if value < thresh:
            return {
                "spec": label, "value": value, "band": verdict,
                "why": why, "years": years if prev is None else years,
            }
        prev = thresh
    return {"spec": label, "value": value, "band": "?", "why": "?", "years": 5.0}


def fmt_firmness(x):
    x = max(1.0, min(10.0, x))
    label = ("very soft" if x < 3.5 else "soft" if x < 4.75 else "medium"
             if x < 6.25 else "medium-firm" if x < 7.5 else "firm")
    return round(x, 1), label


# ---------------------------------------------------------------- profile

def parse_profile(s):
    pos, w, h = s.split(",")
    pos = pos.strip().lower()
    if pos not in POSITION_BASE_FIRMNESS:
        sys.exit(f"position must be one of {sorted(POSITION_BASE_FIRMNESS)}")
    return {"position": pos, "weight_kg": float(w), "height_cm": float(h)}


def bmi(p):
    m = p["height_cm"] / 100.0
    return p["weight_kg"] / (m * m)


def profile_firmness(p):
    base, why0 = POSITION_BASE_FIRMNESS[p["position"]]
    b = bmi(p)
    shift = sw = None
    for thresh, s, w in BMI_SHIFT:
        if b < thresh:
            shift, sw = s, w
            break
    f = base + shift
    f10, flabel = fmt_firmness(f)
    ild = 12 + (f - 4.0) * 2.2  # rough surface-ILD target
    out = {
        "position": p["position"],
        "weight_kg": p["weight_kg"],
        "bmi": round(b, 1),
        "bmi_note": sw,
        "firmness_10": f10,
        "firmness_label": flabel,
        "target_ild_range": [round(ild - 2), round(ild + 2)],
        "why": f"{why0}; BMI {b:.1f} -> shift {shift:+.0f}",
    }
    if p["weight_kg"] >= HEAVY_KG or b >= 30:
        out["hard_requirements"] = [
            "base foam >= 1.8 lb/ft3 (or high-gauge coils)",
            "avoid low-density memory comfort layers < 3 lb/ft3",
            "prefer hybrid or dense latex for support longevity",
        ]
    return out


def recommend(args):
    p = parse_profile(f"{args.position},{args.weight},{args.height}")
    r = profile_firmness(p)
    f = r["firmness_10"]
    types = []
    if r["position"] == "side":
        types.append("memory foam or pillow-top hybrid (pressure relief)")
    if r["position"] == "stomach" or (HEAVY_KG and p["weight_kg"] >= HEAVY_KG):
        types.append("hybrid with pocketed coils 13.5-14.5 gauge")
    if r["bmi"] >= 30:
        types.append("dense latex (5.3+) or firm hybrid")
    if r["position"] == "back":
        types.append("medium hybrid — zoned lumbar a plus")
    r["type_candidates"] = types or ["any well-spec'd hybrid"]
    r["warnings"] = []
    if r["bmi"] >= 30:
        r["warnings"].append("BMI >= 30: low-density foam will impress quickly — density beats brand.")
    if r["position"] == "stomach":
        r["warnings"].append("Stomach sleeping is the position most punished by a too-soft bed.")
    if r["bmi"] < 19:
        r["warnings"].append("Light body: very firm surfaces never contour — don't overshoot firmness.")
    return r


def couple(args):
    p1, p2 = parse_profile(args.p1), parse_profile(args.p2)
    r1, r2 = profile_firmness(p1), profile_firmness(p2)
    f_hi = max(r1["firmness_10"], r2["firmness_10"])
    f_lo = min(r1["firmness_10"], r2["firmness_10"])
    gap = f_hi - f_lo
    strat = []
    if gap <= 1.5:
        strat.append(f"Gap {gap:.1f}: one shared mattress at {fmt_firmness(f_hi)[0]}/10 "
                     "works — solve remaining pressure relief with a topper for the softer sleeper.")
    else:
        strat.append(f"Gap {gap:.1f} is large: split-core/dual-firmness mattress, or "
                     "'sleep number' style adjustable, or two Twin-XL cores under one king topper.")
    strat.append("Never average the firmness: the heavier sleeper's spine sets the core, "
                 "the lighter one gets comfort from the top layer.")
    if {r1["position"], r2["position"]} == {"side", "stomach"}:
        strat.append("side+stomach couple: medium core + removable soft topper each side.")
    return {
        "sleeper1": r1, "sleeper2": r2, "firmness_gap": round(gap, 1),
        "shared_core_firmness": fmt_firmness(f_hi),
        "strategy": strat,
        "motion_tip": "Pocketed coils + memory foam isolate motion best for different schedules.",
    }


# ---------------------------------------------------------------- decode

def decode_spec(spec):
    out = {"name": spec.get("name", "unnamed"), "type": spec.get("type", "unknown")}
    layers = []
    years = []
    if spec.get("memory_density"):
        b = band(float(spec["memory_density"]), MEMORY_DENSITY, "memory foam density (lb/ft3)")
        layers.append(b); years.append(b["years"])
    if spec.get("base_density"):
        b = band(float(spec["base_density"]), BASE_DENSITY, "base foam density (lb/ft3)")
        layers.append(b); years.append(b["years"])
    if spec.get("latex_density"):
        b = band(float(spec["latex_density"]), LATEX_DENSITY, "latex density (lb/ft3)")
        layers.append(b); years.append(b["years"])
    if int(spec.get("coils", 0)) > 0:
        c = int(spec["coils"])
        for thresh, verdict, why, cy in COIL_GUIDE:
            if c < thresh:
                layers.append({"spec": f"coil count (queen) = {c}", "value": c,
                               "band": verdict, "why": why, "years": cy})
                years.append(cy)
                break
        ct = spec.get("coil_type", "unknown")
        ct_note = {
            "pocketed": "best motion isolation + conformity",
            "offset": "traditional hinging feel, durable",
            "bonnell": "cheap, squeaky, transfers motion",
            "continuous": "durable but firm, poor conformity",
        }.get(ct, "ask which of: pocketed/offset/bonnell/continuous")
        layers.append({"spec": f"coil type = {ct}", "band": "INFO", "why": ct_note, "years": 6.0})
    if not layers:
        layers.append({"spec": "no quantified specs provided", "band": "OPAQUE",
                       "why": "Manufacturer hides densities — treat as junk until proven otherwise", "years": 2.0})
        years.append(2.0)
    worst = min(years)
    junk = [l for l in layers if l["band"] in ("JUNK", "OPAQUE")]
    out["layers"] = layers
    out["expected_lifespan_years"] = worst
    out["weakest_link"] = (junk[0]["spec"] if junk else
                           min(layers, key=lambda l: l["years"])["spec"])
    out["height_note"] = ("Total height is a marketing number — 14in of low-density foam "
                          "loses to 10in of high-density.")
    return out


def decode(args):
    spec = {"type": args.type}
    for k in ("memory_density", "base_density", "latex_density"):
        v = getattr(args, k)
        if v is not None:
            spec[k] = v
    if args.coils:
        spec["coils"] = args.coils
        spec["coil_type"] = args.coil_type
    return decode_spec(spec)


# ---------------------------------------------------------------- compare

def parse_kv(s):
    out = {}
    for part in s.split(","):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        try:
            out[k.strip()] = float(v)
        except ValueError:
            out[k.strip()] = v
    return out


def score_one(spec, prof):
    d = decode_spec(spec)
    f = prof["firmness_10"]
    score = 50.0
    notes = []
    # support fit
    if spec.get("type") == "hybrid":
        score += 10; notes.append("hybrid: good support generalist (+10)")
    if spec.get("type") == "foam" and prof["bmi"] >= 30:
        score -= 10; notes.append("all-foam at BMI>=30: durability risk (-10)")
    if spec.get("base_density", 0) >= 1.8:
        score += 10; notes.append("base >=1.8 lb/ft3: support lasts (+10)")
    elif spec.get("base_density"):
        score -= 8; notes.append("base <1.8 lb/ft3: will flatten (-8)")
    if spec.get("memory_density", 0) >= 4.0:
        score += 8; notes.append("memory >=4.0 lb/ft3 (+8)")
    elif spec.get("memory_density", 0) and spec.get("memory_density") < 3.0:
        score -= 10; notes.append("memory <3.0 lb/ft3: impressions (-10)")
    if spec.get("coils", 0) >= 480 and spec.get("coil_type") == "pocketed":
        score += 10; notes.append("pocketed coils >=480 (+10)")
    if prof["position"] == "side" and spec.get("type") in ("foam", "hybrid") and spec.get("memory_density", 0) >= 3.0:
        score += 6; notes.append("side sleeper + conforming memory (+6)")
    if prof["position"] == "stomach" and spec.get("type") == "foam" and spec.get("memory_density", 0) >= 4.0:
        score -= 4; notes.append("stomach + dense memory: can hammock (-4)")
    # durability normalized per year of expected life
    score += (d["expected_lifespan_years"] - 5.0) * 2
    price = spec.get("price")
    cpyn = None
    if price:
        cpyn = price / max(d["expected_lifespan_years"], 1)
        notes.append(f"cost per good year: ${cpyn:.0f}")
    return {"name": d["name"], "score": round(score, 1), "notes": notes,
            "lifespan_years": d["expected_lifespan_years"], "cost_per_year": cpyn}


def compare(args):
    prof = profile_firmness(parse_profile(args.profile))
    a, b = score_one(parse_kv(args.a), prof), score_one(parse_kv(args.b), prof)
    winner = max((a, b), key=lambda x: x["score"])
    return {"your_profile": {k: prof[k] for k in
                             ("position", "bmi", "firmness_10", "firmness_label")},
            "a": a, "b": b,
            "verdict": f"{winner['name']} wins for your body "
                       f"(score {winner['score']}; reasoning above, marketing excluded)"}


# ---------------------------------------------------------------- warranty

def warranty(args):
    out = {"stated_years": args.years, "prorated": args.prorated,
           "sag_threshold_in": args.sag_threshold}
    if args.prorated:
        out["real_coverage"] = ("Full refund/replacement typically only years 1-"
                                f"{max(1, args.years // 5)}; after that YOU pay a % "
                                "that grows yearly (prorated schedule) + often shipping both ways.")
        out["year10_cost_example"] = ("By year 10 you may pay 50-80% of original price "
                                      "for a replacement of a bed you already dislike.")
    else:
        out["real_coverage"] = "Non-prorated full term — genuinely good if it exists; verify in writing."
    t = args.sag_threshold
    out["sag_math"] = (f"Coverage requires visible sag > {t}in with NO load, measured "
                       "with a string across the mattress + ruler. Normal body impressions "
                       "under your weight do NOT count.")
    out["voids"] = ["stains (use a protector from night one)",
                    "wrong foundation/frame (keep the receipt)",
                    "no rotating (rotate head-to-foot 2-4x/year, log it)",
                    "removed law tag"]
    if t >= 1.5:
        out["threshold_verdict"] = (f"{t}in is the industry-standard loophole: foam "
                                    "comfort impressions (the thing that actually ruins "
                                    "sleep) usually measure 0.75-1.5in — below threshold.")
    else:
        out["threshold_verdict"] = f"{t}in threshold is tighter than the 1.5in norm — better than average."
    return out


def sag(args):
    covered = args.measured > args.threshold
    why = (f"{args.measured}in {'>' if covered else '<='} {args.threshold}in threshold "
           "(no-load, string-measured)")
    out = {"measured_in": args.measured, "threshold_in": args.threshold,
           "years_owned": args.years_owned, "covered": covered, "why": why}
    if covered:
        out["steps"] = [
            "photograph with the string + ruler in frame, straight-on",
            "find the claim page: photos, receipt, law tag photo",
            "cite the warranty clause verbatim in your claim letter",
        ]
    else:
        out["steps"] = [
            "measure again properly: no bedding, no load, string across surface",
            "if still under: impressions this shallow are 'normal softening' to them — "
            "a firm topper or rotated use is your real remedy",
        ]
    if args.years_owned >= 8:
        out["reality_check"] = "8+ years is at/past expected life — replacement usually beats a claim fight."
    return out


# ---------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("recommend")
    sp.add_argument("--position", required=True, choices=sorted(POSITION_BASE_FIRMNESS))
    sp.add_argument("--weight", type=float, required=True, help="kg")
    sp.add_argument("--height", type=float, required=True, help="cm")
    sp.set_defaults(fn=recommend)

    sp = sub.add_parser("couple")
    sp.add_argument("--p1", required=True, help="position,weight_kg,height_cm")
    sp.add_argument("--p2", required=True)
    sp.set_defaults(fn=couple)

    sp = sub.add_parser("decode")
    sp.add_argument("--type", required=True, choices=["foam", "hybrid", "innerspring", "latex"])
    sp.add_argument("--memory-density", type=float)
    sp.add_argument("--base-density", type=float)
    sp.add_argument("--latex-density", type=float)
    sp.add_argument("--coils", type=int)
    sp.add_argument("--coil-type", choices=["pocketed", "offset", "bonnell", "continuous"])
    sp.set_defaults(fn=decode)

    sp = sub.add_parser("compare")
    sp.add_argument("--profile", required=True, help="position,weight_kg,height_cm")
    sp.add_argument("--a", required=True, help="k=v,k=v (name,type,memory_density,base_density,coils,coil_type,price)")
    sp.add_argument("--b", required=True)
    sp.set_defaults(fn=compare)

    sp = sub.add_parser("warranty")
    sp.add_argument("--years", type=int, default=10)
    sp.add_argument("--prorated", action="store_true")
    sp.add_argument("--sag-threshold", type=float, default=1.5)
    sp.set_defaults(fn=warranty)

    sp = sub.add_parser("sag")
    sp.add_argument("--measured", type=float, required=True)
    sp.add_argument("--threshold", type=float, default=1.5)
    sp.add_argument("--years-owned", type=float, default=3.0)
    sp.set_defaults(fn=sag)

    args = ap.parse_args()
    print(json.dumps(args.fn(args), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
