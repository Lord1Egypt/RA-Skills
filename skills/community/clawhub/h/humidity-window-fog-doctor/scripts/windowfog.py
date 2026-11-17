#!/usr/bin/env python3
"""Window fog doctor: will the inside of the glass collect water tonight?

T_s(inner pane) from U-value + film resistances; condensation iff T_s <= dew
point (Magnus). Threshold RH table across outdoor temps for the glazing;
curtain-cavity chilling; moisture-source audit; fix ladder.

Pure stdlib.
"""
import argparse
import json
import math

R_I, R_O = 0.13, 0.04  # film resistances m2K/W (indoor still air / outdoor)
GLAZING = {   # center-of-glass U, W/m2K
    "single": 5.4,
    "double": 2.9,
    "double-low-e": 1.6,
    "triple": 0.9,
}
CURTAIN_R = 0.15  # extra room-side resistance from closed curtains


def dew_point(t, rh):
    g = math.log(max(rh, 0.1) / 100.0) + 17.62 * t / (243.12 + t)
    return 243.12 * g / (17.62 - g)


def surface_temp(tin, tout, u, curtains=False):
    """Inner pane surface temp via resistance chain.

    R_total = R_room(+curtain cavity) + R_glazing + R_outdoor, where the
    glazing stack resistance is backed out of the rated U-value.
    """
    r_room = R_I + (CURTAIN_R if curtains else 0.0)
    r_glaz = max(1.0 / u - R_I - R_O, 0.005)
    r_total = r_room + r_glaz + R_O
    return tin - (tin - tout) * r_room / r_total


def threshold_rh(tin, tout, u, curtains=False):
    """Indoor RH (%) at which dew point equals pane surface temp."""
    ts = surface_temp(tin, tout, u, curtains)
    # RH* = 100 * exp( 17.62*ts/(243.12+ts) - 17.62*tin/(243.12+tin) )
    x = (17.62 * ts / (243.12 + ts)) - (17.62 * tin / (243.12 + tin))
    return 100.0 * math.exp(x)


def main():
    ap = argparse.ArgumentParser(description="Inside-glass condensation verdict")
    ap.add_argument("--tin", type=float, default=21.0, help="indoor temp °C")
    ap.add_argument("--rh", type=float, default=50.0, help="indoor RH %%")
    ap.add_argument("--tout", type=float, required=True, help="outdoor min temp °C")
    ap.add_argument("--glazing", default="double", choices=list(GLAZING))
    ap.add_argument("--curtains", action="store_true",
                    help="closed curtains at night (colder pane)")
    ap.add_argument("--margin", type=float, default=5.0,
                    help="safety margin in RH points for target")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    u = GLAZING[a.glazing]
    ts = surface_temp(a.tin, a.tout, u, a.curtains)
    td = dew_point(a.tin, a.rh)
    rh_star = threshold_rh(a.tin, a.tout, u, a.curtains)
    delta = a.rh - rh_star

    if ts <= td:
        klass = "CONDENSATION (or frost if pane < 0°C)"
    elif delta < a.margin:
        klass = "MARGINAL - fogs in the coldest hour (4-7am)"
    else:
        klass = "DRY"

    table = {f"{t:+d}C": round(threshold_rh(a.tin, t, u, a.curtains))
             for t in [0, -5, -10, -15, -20]}

    target = rh_star - a.margin
    if target < 35:
        fix_side = ("GLASS-SIDE FIX required: target RH %.0f%% is below the ~35%% "
                    "comfort floor. Ladder rung 3-4: interior storm film/panel or "
                    "low-e glazing upgrade; ventilating further just dries the house."
                    % target)
    else:
        fix_side = ("Target indoor RH <= %.0f%% keeps this glazing dry at %+.0f°C out "
                    "(threshold %.0f%% minus %.0f margin). Reachable with behavior: "
                    "burst ventilation + source control." % (target, a.tout, rh_star, a.margin))

    out = {
        "glazing": a.glazing, "u": u, "curtains": a.curtains,
        "pane_surface_c": round(ts, 1),
        "dew_point_c": round(td, 1),
        "threshold_rh_pct": round(rh_star),
        "your_rh_pct": a.rh,
        "margin_rh_points": round(-delta),
        "verdict": klass,
        "threshold_by_outdoor": table,
        "target_rh": round(max(target, 0)),
        "fix": [fix_side,
                "Free levers: laundry out of living space (1.5-3 kg water/day), "
                "kill unflued gas heating (1.6 kg water per kg gas), 10-min burst "
                "ventilation after shower/cooking and on waking.",
                "Curtains: leave 2-3 cm gaps top+bottom if you have fog behind them "
                "(closed cavity chills the pane further)."] +
               (["Tonight's culprit may be the curtains: pane is %.1f°C colder with "
                 "them closed." % (surface_temp(a.tin, a.tout, u, False) - ts)]
                if a.curtains else []),
        "sources_g": {"shower_10min": 150, "family_cooking": 500,
                      "2_sleepers_per_night": 500, "laundry_load_indoors": 2000,
                      "unflued_gas_heater_per_kg_fuel": 1600},
    }

    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print(f"Glazing: {a.glazing} (U={u}), indoor {a.tin:.0f}°C @ {a.rh:.0f}% RH "
          f"(dew point {td:.1f}°C), outdoor min {a.tout:+.0f}°C"
          + (", curtains closed" if a.curtains else ""))
    print(f"Inner pane surface: {ts:.1f}°C   threshold RH: {rh_star:.0f}%")
    print(f"VERDICT: {klass}")
    print(f"\nThreshold RH by outdoor temp ({a.glazing}):")
    for k, v in table.items():
        mark = "  <- tonight" if int(k[:-1]) == int(a.tout) else ""
        print(f"  {k:>6}: {v:>3}%{mark}")
    print("\nFix ladder:")
    for i, f in enumerate(out["fix"], 1):
        print(f"{i}. {f}")
    print("\nMoisture sources for audit (g water):")
    for k, v in out["sources_g"].items():
        print(f"  {k}: ~{v}")


if __name__ == "__main__":
    main()
