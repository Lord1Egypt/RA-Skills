#!/usr/bin/env python3
"""Laundry dry forecaster: hours-to-dry, humidity dumped into the room, cost.

Engine: E = k_class * VPD(T,RH) kg/h per 4 kg spread load; two-phase drying
(1.45x W/E); coupled room-RH hourly simulation with ventilation removal;
peak-RH condensation warning; method cost table.

Calibration anchors (4 kg cotton, 1400 rpm = 2.0 kg water, 20C):
  still room 50%RH ~18h, fan ~10h, dehumidifier ~5h. See references/.
"""
import argparse
import json
import math

RHO = 1.2           # air kg/m3
P_ATM = 101.3       # kPa

SPIN_RM = [(800, 0.70), (1000, 0.62), (1200, 0.55), (1400, 0.50), (1600, 0.45)]
# kg water/h per kPa VPD per 4kg load; (local temp boost, effective RH cap)
AIRFLOW = {
    "still":        (0.14, 0.0, None),
    "fan":          (0.28, 0.0, None),
    "heated-airer": (0.38, 6.0, None),
    "dehumidifier": (0.55, 0.0, 45.0),
    "outdoor-light": (0.30, 0.0, None),
    "outdoor-breezy": (0.55, 0.0, None),
}
DEHUMID_EXTRACTION = 0.45   # kg water/h capacity of a ~20L/day domestic unit
FALLING_RATE_AFTER = 0.70   # fraction of water after which rate drops to 0.4x


def residual_moisture(spin):
    spins = [s for s, _ in SPIN_RM] + [spin]
    rm = dict(SPIN_RM)
    if spin in rm:
        return rm[spin]
    lo = max(s for s in spins if s <= spin)
    hi = min(s for s in spins if s >= spin)
    if lo == hi:
        return rm[lo]
    f = (spin - lo) / (hi - lo)
    return rm[lo] * (1 - f) + rm[hi] * f


def e_sat(t):
    """Saturation vapor pressure kPa (Tetens)."""
    return 0.6108 * math.exp(17.27 * t / (t + 237.3))


def vpd(t, rh):
    return e_sat(t) * (1 - min(max(rh, 5), 99) / 100.0)


def x_sat(t):
    """Saturation humidity ratio kg/kg."""
    e = e_sat(t)
    return 0.622 * e / (P_ATM - e)


def simulate(kg_dry, spin, t, rh, airflow, room_m3, ach, hours_cap=48):
    k, dT, rh_cap = AIRFLOW[airflow]
    water = kg_dry * residual_moisture(spin)
    x = x_sat(t) * rh / 100.0          # current room humidity ratio
    x_out = x_sat(t) * 0.35            # winter outdoor air warmed up (~35% equiv)
    evap_total, peak_rh, t_dry = 0.0, rh, None
    per_hour = []
    for h in range(1, hours_cap + 1):
        rh_room = 100 * x / x_sat(t)
        rate = k * vpd(t + dT, rh_room) * (kg_dry / 4.0)
        # falling-rate phase: fiber-interior diffusion limits the tail
        if evap_total > FALLING_RATE_AFTER * water:
            rate *= 0.4
        rate = max(min(rate, max(water - evap_total, 0.0)), 1e-6)
        evap_total += rate
        x += rate / (room_m3 * RHO) if room_m3 else 0.0
        # sinks: ventilation, then the dehumidifier's rate-limited pump
        if room_m3:
            x -= ach * (x - x_out)
        if rh_cap:
            x_tank = x_sat(t) * rh_cap / 100.0
            mass_room = room_m3 * RHO if room_m3 else 1.0
            extract = min(DEHUMID_EXTRACTION * (kg_dry / 4.0),
                          max(0.0, (x - x_tank)) * mass_room)
            x -= extract / mass_room
        # physics: RH can't exceed 100% (surfaces condense the excess)
        x = min(x, x_sat(t))
        x = max(x, x_out * 0.9)
        rh_room = 100 * x / x_sat(t)
        peak_rh = max(peak_rh, rh_room)
        per_hour.append({"hour": h, "evap_kg": round(rate, 3),
                         "rh_room": round(rh_room, 1)})
        if evap_total >= water - 1e-4:
            t_dry = h
            break
    return water, evap_total, t_dry, peak_rh, per_hour


def cost_table(price_kwh):
    """Per 4kg load, ~2.0 kg water. kWh figures from references §5."""
    rows = [
        ("rack (heat comes from your heating)", 1.30, "adds 2 kg water to room air"),
        ("rack + dehumidifier (closed room)", 0.55, "water to tank; heat stays in room"),
        ("heated airer 230W", 1.50, "adds water to room air"),
        ("condenser tumble dryer", 2.20, "heat+moisture to room unless plumbed"),
        ("heat-pump tumble dryer", 0.75, "appliance benchmark"),
        ("outdoor line", 0.0, "zero indoor moisture (weather permitting)"),
    ]
    return [{"method": m, "kwh": e, "cost": round(e * price_kwh, 2), "note": n}
            for m, e, n in rows]


def main():
    ap = argparse.ArgumentParser(description="Laundry drying time & humidity calculator")
    ap.add_argument("--kg", type=float, default=4.0, help="dry weight of load, kg")
    ap.add_argument("--spin", type=int, default=1200, help="washer spin rpm")
    ap.add_argument("--tin", type=float, default=20.0, help="room temp °C")
    ap.add_argument("--rh", type=float, default=55.0, help="room RH %%")
    ap.add_argument("--airflow", default="still", choices=list(AIRFLOW))
    ap.add_argument("--room-m3", type=float, default=40.0, help="room volume m3")
    ap.add_argument("--vent-ach", type=float, default=1.0,
                    help="air changes per hour (closed bath 0.5, open room 1-2)")
    ap.add_argument("--hang-hour", type=int, default=None, help="hour you hang it (0-23)")
    ap.add_argument("--deadline", type=int, default=None,
                    help="hour you need it dry (0-23)")
    ap.add_argument("--window-threshold", type=float, default=55.0,
                    help="your coldest glazing condensation RH%% (see windowfog)")
    ap.add_argument("--price", type=float, default=0.25, help="electricity $/kWh")
    ap.add_argument("--compare", action="store_true", help="method cost table")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    water, evap, t_dry, peak_rh, per_hour = simulate(
        a.kg, a.spin, a.tin, a.rh, a.airflow, a.room_m3, a.vent_ach)

    warn = peak_rh >= a.window_threshold

    out = {
        "load_kg_dry": a.kg,
        "residual_water_kg": round(water, 2),
        "spin_rpm": a.spin,
        "room": f"{a.tin:.0f}C {a.rh:.0f}%RH, {a.room_m3:.0f}m3 @ {a.vent_ach} ACH",
        "hours_to_dry": t_dry if t_dry else f">{len(per_hour)}",
        "peak_room_rh": round(peak_rh, 1),
        "condensation_warning": warn,
    }

    if a.hang_hour is not None and t_dry:
        dry_at = (a.hang_hour + t_dry)
        need = ((a.deadline or 24) - a.hang_hour) % 24 or 24
        out["dry_by"] = f"hour {(dry_at) % 24:02d}:00 (+{t_dry}h from hang)"
        out["meets_deadline"] = bool(t_dry <= need)

    if a.compare:
        out["cost_per_load"] = cost_table(a.price)

    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print(f"Load {a.kg:.1f} kg dry @ {a.spin} rpm spin -> {water:.1f} kg water to remove")
    print(f"Room: {out['room']}, airflow: {a.airflow}")
    if t_dry:
        print(f"DRY in ~{t_dry} h")
    else:
        print(f"NOT DRY within {len(per_hour)} h in these conditions")
    if "dry_by" in out:
        print(f"  {out['dry_by']}"
              + ("  -> MEETS deadline" if out["meets_deadline"] else "  -> MISSES deadline"))
    print(f"Peak room RH during drying: {peak_rh:.0f}%")
    if warn:
        print(f"  WARNING: exceeds window condensation threshold {a.window_threshold:.0f}% "
              "-> expect fogging; use dehumidifier mode or burst-ventilate")
    if a.compare:
        print(f"\nMethod cost per ~4kg load (${a.price:.2f}/kWh):")
        print(f"{'method':<38}{'kWh':>6}{'cost':>7}  note")
        for r in out["cost_per_load"]:
            print(f"{r['method']:<38}{r['kwh']:>6.2f}{r['cost']:>7.2f}  {r['note']}")


if __name__ == "__main__":
    main()
