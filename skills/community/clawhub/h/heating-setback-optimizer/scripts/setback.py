#!/usr/bin/env python3
"""Heating setback optimizer: does turning the thermostat down pay, and by how much?

Physics: Q = K*(Tin-Tout); savings = K*dT*hours minus recovery costs.
System rules: furnace free / heat-pump strips cap / radiant floor 1C max /
resistance always pays. Scan mode ranks setback depths 0-6C.

Pure stdlib.
"""
import argparse
import json

# effective thermal capacity kWh/K by construction class
C_EFF = {"light": 3.0, "medium": 6.0, "heavy": 12.0}
# oversizing factor: burner capacity vs design heat loss
OVERSIZE = {"furnace": 2.5, "boiler": 2.0, "heat-pump": 1.15,
            "resistance": 1.3, "radiant": 1.2}
EFF = {"furnace": 0.90, "boiler": 0.88, "heat-pump": 3.0,   # COP seasonal
       "resistance": 1.0, "radiant": 0.92}
STRIP_CAPS = {"heat-pump": 2.0}      # max setback °C before strips eat savings
MIN_WINDOW_H = {"light": 3.0, "medium": 5.0, "heavy": 8.0}  # setback >= this
MAX_SETBACK = {"radiant": 1.0}


def season_energy(k, tin, tout_avg, days):
    """Heating energy, kWh_th, for constant hold."""
    dt = tin - tout_avg
    return k * dt * 24.0 * days / 1000.0


def setback_savings(k, depth, hours, days, c_eff, system, q_design,
                    tin, tout_avg):
    """Net season saving kWh_th of one daily setback window, after recovery.

    Recovery cost model: bringing the mass back up needs C*dT energy; if the
    system excess capacity is small, part of recovery runs on strips (COP 1)
    -> for heat-pump we price the recovery penalty as efficiency loss.
    Realization factor: setback shorter than tau -> mass floats the air,
    savings realized fraction ~ min(1, hours / tau).
    """
    tau = c_eff / (k / 1000.0)                 # hours
    realize = min(1.0, hours / (0.25 * tau))   # light houses realize fast
    ideal = k * depth * hours * days / 1000.0  # kWh_th
    saved = ideal * realize
    # recovery: energy = C*depth (same kWh_th either way), penalty is only
    # the efficiency split for heat pumps whose recovery exceeds compressor
    penalty_kwh = 0.0
    if system == "heat-pump" and depth > STRIP_CAPS[system]:
        frac_strip = min(1.0, (depth - STRIP_CAPS[system]) / 3.0)
        # strip fraction of recovery energy at COP1 vs compressor COP
        rec_energy = c_eff * depth            # kWh_th per recovery
        cop = EFF[system]
        penalty_kwh = rec_energy * frac_strip * (1.0 - 1.0 / cop) * days * 0.5
        saved -= penalty_kwh
    return max(0.0, saved), penalty_kwh


def ramp_minutes(depth, c_eff, system, q_design, k, tin, tout_design):
    """Minutes to climb back 'depth' degrees at design outdoor temp."""
    q_x = OVERSIZE.get(system, 1.5) * q_design - k * (tin - tout_design)
    q_x = max(q_x, 0.5 * q_design)            # floor to avoid div0 absurdity
    hours = c_eff * depth / (q_x / 1000.0)
    return hours * 60.0


def verdict(system, depth, hours, mass):
    notes = []
    if system in MAX_SETBACK and depth > MAX_SETBACK[system]:
        notes.append(f"DEPTH EXCEEDS {system} limit {MAX_SETBACK[system]:.0f}C - "
                     "slab recovery takes 6-12h; house stays cold all day.")
    if system in STRIP_CAPS and depth > STRIP_CAPS[system]:
        notes.append(f"Depth >{STRIP_CAPS[system]:.0f}C on strip-equipped heat pump: "
                     "morning recovery fires resistive strips (COP 1) and eats savings. "
                     "Use smart/gradual recovery or cap depth.")
    if hours < MIN_WINDOW_H[mass]:
        notes.append(f"Setback window {hours:.0f}h < minimum {MIN_WINDOW_H[mass]:.0f}h for "
                     f"{mass} mass - savings ~0, cycling wear up. Extend the window.")
    if not notes:
        notes.append("OK: depth and window compatible with system and mass.")
    return notes


def main():
    ap = argparse.ArgumentParser(description="Thermostat setback savings calculator")
    ap.add_argument("--k", type=float, default=180.0,
                    help="heat-loss coefficient W/K (or derive: --fuel-kwh --hdd)")
    ap.add_argument("--fuel-kwh", type=float, default=None,
                    help="season fuel use kWh (to derive K with --hdd)")
    ap.add_argument("--hdd", type=float, default=None, help="heating degree days base 18C")
    ap.add_argument("--eta", type=float, default=None,
                    help="system efficiency/COP override (else by --system)")
    ap.add_argument("--tin", type=float, default=21.0, help="hold setpoint °C")
    ap.add_argument("--tout-avg", type=float, default=0.0, help="season avg outdoor °C")
    ap.add_argument("--tout-design", type=float, default=-15.0, help="design outdoor °C")
    ap.add_argument("--depth", type=float, default=3.0, help="setback depth °C")
    ap.add_argument("--hours", type=float, default=8.0, help="setback hours/day")
    ap.add_argument("--days", type=float, default=210.0, help="heating season days")
    ap.add_argument("--system", default="furnace",
                    choices=list(OVERSIZE), help="heating system type")
    ap.add_argument("--mass", default="medium", choices=list(C_EFF))
    ap.add_argument("--price", type=float, default=0.10,
                    help="fuel price per kWh_fuel (gas ~0.10, electric ~0.25)")
    ap.add_argument("--scan", action="store_true",
                    help="rank setback depths for your setup")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    k = a.k
    derived = None
    if a.fuel_kwh and a.hdd:
        k = a.fuel_kwh * (a.eta or EFF[a.system]) / (a.hdd * 24.0) * 1000.0
        derived = round(k, 1)
    eff = a.eta if a.eta is not None else EFF[a.system]
    c_eff = C_EFF[a.mass]
    q_design = k * (a.tin - a.tout_design)         # W at design temp

    base = season_energy(k, a.tin, a.tout_avg, a.days)     # kWh_th constant hold
    saved, penalty = setback_savings(k, a.depth, a.hours, a.days, c_eff,
                                     a.system, q_design, a.tin, a.tout_avg)
    saved_fuel = saved / eff
    base_fuel = base / eff
    pct = 100.0 * saved / base if base else 0.0
    ramp = ramp_minutes(a.depth, c_eff, a.system, q_design, k,
                        a.tin, a.tout_design)
    notes = verdict(a.system, a.depth, a.hours, a.mass)

    out = {
        "k_w_per_k": round(k, 1), "k_derived_from_bill": derived,
        "q_design_w": round(q_design),
        "system": a.system, "mass": a.mass, "eff_or_cop": eff,
        "season_heating_kwh_th": round(base),
        "season_fuel_kwh": round(base_fuel),
        "setback": {"depth_c": a.depth, "hours": a.hours},
        "saved_kwh_th": round(saved), "recovery_penalty_kwh_fuel": round(penalty),
        "saved_fuel_kwh": round(saved_fuel),
        "saved_pct_of_heating": round(pct, 1),
        "saved_money": round(saved_fuel * a.price, 2),
        "recovery_ramp_min_at_design": round(ramp),
        "verdict": notes,
    }

    if a.scan:
        rows = []
        for depth in [0, 1, 1.5, 2, 3, 4, 5, 6]:
            if a.system in MAX_SETBACK and depth > MAX_SETBACK[a.system]:
                continue
            s, p = setback_savings(k, depth, a.hours, a.days, c_eff,
                                   a.system, q_design, a.tin, a.tout_avg)
            sf = s / eff
            rows.append({"depth_c": depth,
                         "saved_fuel_kwh": round(sf),
                         "saved_money": round(sf * a.price, 2),
                         "pct": round(100.0 * s / base, 1) if base else 0,
                         "strip_penalty": round(p)})
        rows.sort(key=lambda r: -r["saved_fuel_kwh"])
        out["scan_ranked"] = rows
        out["scan_note"] = ("Savings flatten where strip penalty appears "
                            "(heat pump) or depth exceeds realization; pick "
                            "the top row whose comfort you accept.")

    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print(f"House: K={out['k_w_per_k']} W/K"
          + (f" (derived from bill: {derived})" if derived else "")
          + f", design loss {out['q_design_w']} W, mass={a.mass}, system={a.system}")
    print(f"Season (constant {a.tin:.0f}C hold): {out['season_heating_kwh_th']} kWh_th "
          f"= {out['season_fuel_kwh']} kWh fuel")
    print(f"\nSetback {a.depth:.1f}C x {a.hours:.0f}h/day:")
    print(f"  saves {out['saved_fuel_kwh']} kWh fuel "
          f"({out['saved_pct_of_heating']}% of heating) "
          f"= ${out['saved_money']}/season")
    if penalty:
        print(f"  (includes recovery penalty {out['recovery_penalty_kwh_fuel']} kWh "
              "from strip usage)")
    print(f"  morning recovery ramp at design temp: ~{out['recovery_ramp_min_at_design']} min "
          f"to full-mass warmth (air feels warm in ~{max(5, out['recovery_ramp_min_at_design'] // 3)} min)")
    print("\nVerdict:")
    for n in notes:
        print(f"  - {n}")
    if a.scan:
        print(f"\nScan (depth ranked by net saving, {a.hours:.0f}h window):")
        print(f"{'depth':>6} {'saved kWh':>10} {'% heat':>8} {'$/season':>9} {'strip pen':>9}")
        for r in out["scan_ranked"]:
            print(f"{r['depth_c']:>6} {r['saved_fuel_kwh']:>10} {r['pct']:>8} "
                  f"{r['saved_money']:>9} {r['strip_penalty']:>9}")


if __name__ == "__main__":
    main()
