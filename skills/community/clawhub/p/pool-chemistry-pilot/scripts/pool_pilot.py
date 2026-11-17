#!/usr/bin/env python3
"""pool_pilot.py — residential pool/spa chemistry dosing calculator & diagnostician.

Offline, stdlib-only. State: pool_state.json beside the script (or --state).
Commands: setup | log | status | plan | slam | history
Chemistry-first: generic chemical names, no brands. Not for public-pool compliance.
"""
import argparse
import json
import math
import sys
from datetime import date, datetime
from pathlib import Path

DEFAULT_STATE = Path(__file__).resolve().parent / "pool_state.json"

# slam FC by CYA (rounded interpolation of the TFP table)
SLAM_TABLE = [(0, 10), (10, 10), (20, 10), (30, 12), (40, 16), (50, 20),
              (60, 24), (70, 28), (80, 31), (90, 35), (100, 35)]


def slam_fc(cya):
    if cya is None:
        return None
    if cya >= 100:
        return 35
    lo, hi = 0, len(SLAM_TABLE) - 1
    for i in range(len(SLAM_TABLE) - 1):
        c0, f0 = SLAM_TABLE[i]
        c1, f1 = SLAM_TABLE[i + 1]
        if c0 <= cya <= c1:
            if c1 == c0:
                return f0
            return f0 + (f1 - f0) * (cya - c0) / (c1 - c0)
    return 35


def load(state):
    if Path(state).exists():
        return json.loads(Path(state).read_text())
    return {"pool": {}, "tests": []}


def save(st, state):
    Path(state).write_text(json.dumps(st, indent=2))


def latest(st):
    merged = {}
    for t in st["tests"]:
        for k, v in t.items():
            merged[k] = v  # most recent wins
    return merged


# ------------------------------------------------------------------ dosing
# amounts to change 1 ppm in 10,000 L
DOSE = {
    "fc_liquid12": 83,     # mL of 12% sodium hypochlorite per +1 ppm FC per 10 m3
    "fc_liquid10": 100,    # mL of 10%
    "fc_dichlor": 18,      # g 56% available chlorine
    "fc_calhypo": 15,      # g 68%
    "fc_trichlor": 11,     # g 90%
    "ta_baking_soda": 16.7,   # g per +1 ppm TA
    "ch_calcium_chloride": 12,  # g 77% per +1 ppm CH
    "cya_stabilizer": 8.3,     # g pure cyanuric per +1 ppm CYA
    "salt_nacl": 10,        # g per +1 ppm salt
    "borate_boric": 11,     # g per +1 ppm borates
}
# muriatic 31.45%: mL per 10,000 L to drop pH by ~0.2 at given TA (pH 7.8->7.6-ish)
ACID_ph = {60: 70, 70: 80, 80: 90, 100: 105, 120: 120}


def acid_ml_per_ph02(vol_l, ta):
    """mL of 31.45% muriatic acid to lower pH by 0.2 in vol_l liters at given TA."""
    base = ACID_ph.get(min(ACID_ph, key=lambda t: abs(t - ta)), 90)
    return base * (vol_l / 10000)


def fmt(amount, unit):
    if unit == "g":
        return f"{amount / 1000:.2f} kg" if amount >= 1000 else f"{amount:.0f} g"
    return f"{amount / 1000:.2f} L" if amount >= 1000 else f"{amount:.0f} mL"


# ------------------------------------------------------------------ CSI
def csi(ph, temp_c, ch, ta, cya, tds=900):
    """Langelier saturation index: pH - pHs, pHs = (9.3+A+B) - (C+D)."""
    if None in (ph, temp_c, ch, ta) or ch <= 0 or ta <= 0:
        return None
    a = (math.log10(tds) - 1.0) / 10.0
    b = -13.12 * math.log10(temp_c + 273.15) + 34.55
    c = math.log10(ch) - 0.4
    adj_ta = max(ta - (cya or 0) * 0.33, 5)
    d = math.log10(adj_ta)
    phs = (9.3 + a + b) - (c + d)
    return round(ph - phs, 2)


# ------------------------------------------------------------------ commands
def cmd_setup(a, st, state):
    vol = a.liters
    if not vol and a.gallons:
        vol = a.gallons * 3.78541
    if not vol and a.shape:
        if a.shape == "rect":
            vol = a.length * a.width * a.avg_depth * 1000
        elif a.shape == "round":
            vol = math.pi * (a.diameter / 2) ** 2 * a.avg_depth * 1000
        if a.unit == "us":
            vol *= 3.78541
    if not vol or vol <= 0:
        sys.exit("need --liters / --gallons / or --shape with dimensions")
    st["pool"] = {"liters": round(vol), "surface": a.surface, "sanitizer": a.sanitizer}
    save(st, state)
    print(f"pool: {round(vol):,} L ({vol / 3.78541:,.0f} gal) | surface={a.surface} | sanitizer={a.sanitizer}")
    print("volume is the #1 dosing error source — verify by salt-rise if unsure.")


def cmd_log(a, st, state):
    t = {"date": a.date or date.today().isoformat()}
    for k in ("fc", "cc", "ph", "ta", "ch", "cya", "salt", "borates", "temp"):
        v = getattr(a, k)
        if v is not None:
            t[k] = v
    if len(t) == 1:
        sys.exit("nothing to log")
    st["tests"].append(t)
    save(st, state)
    print(f"logged {t['date']}: " + ", ".join(f"{k}={v}" for k, v in t.items() if k != "date"))


def _targets(st):
    swg = st["pool"].get("sanitizer") == "swg"
    surf = st["pool"].get("surface", "plaster")
    return {
        "fc": (3.0, 7.5 if swg else 7.0),
        "cc": (0.0, 0.5),
        "ph": (7.2, 7.8),
        "ta": ((60, 80) if surf != "plaster" else (70, 90)),
        "ch": ((150, 250) if surf != "plaster" else (250, 450)),
        "cya": ((30, 80) if swg else (30, 50)),
        "salt": ((3000, 4000) if swg else (0, 2000)),
        "borates": (0, 50),
    }


def cmd_status(a, st, state):
    if not st["pool"]:
        sys.exit("run setup first")
    t = latest(st)
    if not t:
        sys.exit("no tests logged: run log --fc .. --ph ..")
    vol = st["pool"]["liters"]
    tg = _targets(st)
    print(f"POOL {vol:,} L | {st['pool']['surface']} | {st['pool']['sanitizer']} | last test {t.get('date', '?')}\n")
    for p in ("fc", "cc", "ph", "ta", "ch", "cya", "salt", "borates"):
        if p not in t:
            continue
        v = t[p]
        lo, hi = tg[p]
        if v < lo:
            verdict = f"LOW (target {lo}-{hi})"
        elif v > hi:
            verdict = f"HIGH (target {lo}-{hi})"
        else:
            verdict = f"OK ({lo}-{hi})"
        print(f"  {p.upper():>8}: {v:>7}  {verdict}")
    # FC/CYA ratio
    fc, cya = t.get("fc"), t.get("cya")
    if fc is not None and cya is not None and cya > 0:
        ratio = fc / cya * 100
        min_fc = max(cya * 0.075, 3.0)
        print(f"\n  FC/CYA = {ratio:.1f}% (maintain >= 7.5% of CYA -> FC >= {min_fc:.1f})")
        if fc < min_fc:
            print("  !! FC BELOW MAINTENANCE for your CYA — algae risk; raise FC or dilute CYA")
        if cya > 80:
            print(f"  !! CYA {cya}: slam would need FC {slam_fc(cya):.0f} — consider partial drain (see plan --cya-target)")
    c = csi(t.get("ph"), t.get("temp") or 27, t.get("ch"), t.get("ta"), t.get("cya"))
    if c is not None:
        flag = "OK" if -0.3 <= c <= 0.3 else ("SCALING" if c > 0.3 else "CORROSIVE")
        print(f"  CSI = {c:+.2f} ({flag}; keep -0.3..+0.3)")
    if t.get("cc", 0) > 0.5:
        print("  !! CC elevated — organics winning; slam (see slam command)")


def cmd_plan(a, st, state):
    if not st["pool"]:
        sys.exit("run setup first")
    t = latest(st)
    if not t:
        sys.exit("no tests logged")
    vol = st["pool"]["liters"]
    v10k = vol / 10000.0
    swg = st["pool"].get("sanitizer") == "swg"
    steps = []

    # 1. pH first
    ph = t.get("ph")
    if ph is not None and ph > (a.ph_target or 7.6):
        ta = t.get("ta") or 80
        delta = ph - (a.ph_target or 7.6)
        ml = acid_ml_per_ph02(vol, ta) * (delta / 0.2)
        steps.append((f"LOWER pH {ph} -> {a.ph_target or 7.6}",
                      f"muriatic acid 31.45%: {fmt(ml, 'mL')} (dose 80% = {fmt(ml*0.8,'mL')}, circulate 30-60 min, re-test)",
                      "pH out of range makes chlorine less effective and irritates eyes — always first"))
    # 2. FC
    fc, cya = t.get("fc"), t.get("cya")
    if fc is not None:
        min_fc = max((cya or 30) * 0.075, 3.0)
        if fc < min_fc:
            need = min_fc - fc + 1.5
            if swg:
                steps.append((f"RAISE FC {fc} -> {min_fc:.1f}+ (manual boost)",
                              f"liquid chlorine 12%: {fmt(DOSE['fc_liquid12']*need*v10k, 'mL')} — SWG alone can't catch up; boost then let cell maintain",
                              "min FC = 7.5% of CYA"))
            else:
                steps.append((f"RAISE FC {fc} -> {min_fc:.1f}+",
                              f"liquid chlorine 12%: {fmt(DOSE['fc_liquid12']*need*v10k, 'mL')} (or dichlor {fmt(DOSE['fc_dichlor']*need*v10k,'g')} — adds CYA {0.9*need:.0f} ppm)",
                              "min FC = 7.5% of CYA"))
    # 3. CYA
    if cya is not None and a.cya_target and cya > a.cya_target:
        pct = (cya - a.cya_target) / cya * 100
        steps.append((f"LOWER CYA {cya} -> {a.cya_target} (dilution)",
                      f"replace {pct:.0f}% of pool water ({vol*pct/100/1000:.1f} m3 / {vol*pct/100/3.78541:.0f} gal), no chemical removes CYA",
                      "each drain/refill mixes ~50% if you refill while draining — iterate"))
    if cya is not None and cya < 30 and not swg:
        need = 35 - cya
        steps.append((f"RAISE CYA {cya} -> 35",
                      f"stabilizer (cyanuric acid): {fmt(DOSE['cya_stabilizer']*need*v10k, 'g')} in a sock in the skimmer, pump 24/7; re-test in 3-5 days (dissolves slowly)",
                      "CYA < 20 in a sunlit pool = chlorine burns off daily"))
    # 4. TA
    ta = t.get("ta")
    if ta is not None and ta < 60:
        need = 70 - ta
        steps.append((f"RAISE TA {ta} -> 70",
                      f"baking soda: {fmt(DOSE['ta_baking_soda']*need*v10k, 'g')}",
                      "low TA = pH bounces; baking soda is sodium bicarbonate, same thing as 'alkalinity increaser' at 1/3 the price"))
    # 5. CH
    ch = t.get("ch")
    if ch is not None and st["pool"]["surface"] == "plaster" and ch < 250:
        need = 300 - ch
        steps.append((f"RAISE CH {ch} -> 300 (plaster)",
                      f"calcium chloride 77%: {fmt(DOSE['ch_calcium_chloride']*need*v10k, 'g')} — pre-dissolve in a bucket, add to water NOT water to product",
                      "low CH on plaster = water pulls calcium from the surface (etching)"))
    # 6. salt for SWG
    salt = t.get("salt")
    if swg and salt is not None and salt < 3000:
        need = 3200 - salt
        steps.append((f"RAISE SALT {salt} -> 3200",
                      f"pool salt (NaCl): {fmt(DOSE['salt_nacl']*need*v10k, 'g')} — add in batches, brush to dissolve, verify with drop test not just cell display",
                      "cell reads salt indirectly and drifts"))
    if not steps:
        print("WATER BALANCED — nothing to add. Keep testing same hour daily.")
        return
    print(f"TREATMENT PLAN ({vol:,} L) — add in this order, pump running, 30-60 min between steps:\n")
    for n, (title, dose, why) in enumerate(steps, 1):
        print(f"{n}. {title}")
        print(f"   {dose}")
        print(f"   why: {why}\n")
    print("Never mix concentrated chemicals; add acid to water; chlorine and acid >=30 min apart.")
    print("Doses are estimates from standard tables — re-test after each step, adjust.")


def cmd_slam(a, st, state):
    t = latest(st)
    cya = t.get("cya")
    if cya is None:
        sys.exit("log --cya first: slam level depends on CYA")
    vol = st["pool"]["liters"]
    v10k = vol / 10000.0
    target = slam_fc(cya)
    fc = t.get("fc") or 0
    need = target - fc
    ml = DOSE["fc_liquid12"] * need * v10k
    print(f"SLAM PROTOCOL | CYA {cya} -> slam FC {target:.0f} ppm | pool {vol:,} L")
    if cya >= 100:
        print("!! CYA >= 100: slam level unmanageable — drain 50-60% and refill first, then slam at the new CYA")
    print(f"current FC {fc} -> add liquid chlorine 12%: {fmt(ml, 'mL')} to reach {target:.0f}\n")
    print("Daily loop until done:")
    print("  1. test FC morning & evening (FAS-DPD), re-dose back to slam level")
    print("  2. brush entire pool twice a day")
    print("  3. pump + filter 24/7; clean filter when pressure +25%")
    print("  4. keep pH 7.2-7.3 while slamming (acid before starting if >7.8; acid demand drops while slamming)")
    print("DONE when: FC holds overnight (loss <1 ppm dusk->dawn) + CC <0.5 + water crystal clear.")
    print("Then let FC drift down to maintenance (7.5% of CYA). Do NOT swim until FC < ~10 and water clear.")


def cmd_history(a, st, state):
    if not st["tests"]:
        sys.exit("no tests logged")
    keys = ["fc", "cc", "ph", "ta", "ch", "cya", "salt"]
    print(f"{'date':>10} " + " ".join(f"{k:>6}" for k in keys))
    for t in st["tests"][-14:]:
        row = " ".join(f"{t.get(k, '-'):>6}" if isinstance(t.get(k), str) or t.get(k) is None else f"{t[k]:>6.1f}" for k in keys)
        print(f"{t['date']:>10} {row}")
    n = len(st["tests"])
    print(f"\n({n} tests; most 'sudden' problems are visible as 3-week trends in hindsight)")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state", default=str(DEFAULT_STATE))
    sub = p.add_subparsers(dest="cmd", required=True)
    su = sub.add_parser("setup")
    su.add_argument("--liters", type=float)
    su.add_argument("--gallons", type=float)
    su.add_argument("--shape", choices=["rect", "round"])
    su.add_argument("--length", type=float)
    su.add_argument("--width", type=float)
    su.add_argument("--diameter", type=float)
    su.add_argument("--avg-depth", type=float, required=False)
    su.add_argument("--unit", choices=["metric", "us"], default="metric")
    su.add_argument("--surface", choices=["plaster", "vinyl", "fiberglass"], default="plaster")
    su.add_argument("--sanitizer", choices=["liquid", "trichlor", "dichlor", "swg", "bromine"], default="liquid")
    lg = sub.add_parser("log")
    for k in ("fc", "cc", "ph", "ta", "ch", "cya", "salt", "borates", "temp"):
        lg.add_argument(f"--{k}", type=float)
    lg.add_argument("--date", help="YYYY-MM-DD for backfill")
    sub.add_parser("status")
    pl = sub.add_parser("plan")
    pl.add_argument("--ph-target", type=float, default=7.6)
    pl.add_argument("--cya-target", type=int)
    sub.add_parser("slam")
    sub.add_parser("history")
    a = p.parse_args()
    st = load(a.state)
    {"setup": cmd_setup, "log": cmd_log, "status": cmd_status,
     "plan": cmd_plan, "slam": cmd_slam, "history": cmd_history}[a.cmd](a, st, a.state)


if __name__ == "__main__":
    main()
