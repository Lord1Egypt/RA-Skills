#!/usr/bin/env python3
"""rx_decode.py — eyeglass prescription decoder, differ, and PD helper.

Subcommands:
  decode   parse an Rx (SPH/CYL/AXIS/ADD/PD) and explain it in plain language
  diff     compare old vs new prescriptions per field, verdict felt-vs-noise
  pd       pupillary-distance self-measurement assistant + record
  computer derive intermediate/computer-glasses powers from distance Rx + ADD

Convention: internally normalized to MINUS cylinder. Accepts plus-cylinder
input (auto-transposes, tells you). All values in diopters / degrees / mm.
"""
import argparse
import json
import re
import sys

# ---------------------------------------------------------------- parsing --

def parse_eye(s):
    """Parse one eye string like '-2.75 -1.25 x175', '-3.00', '+1.50 +0.75 x90'."""
    if not s or s.strip() in {"---", "-", "SPH", "plano", "PLANO", ""}:
        return dict(sph=0.0, cyl=0.0, axis=None, plus_conv=False)
    s = s.strip()
    plus_conv = False
    # detect explicit plus-cylinder style: two signed numbers where 2nd is '+'
    nums = re.findall(r"([+-]?\d+\.?\d*)\s*(?:x|×|@)?\s*(\d*)", s)
    toks = re.findall(r"[+-]?\d+\.?\d*|\d+", s.replace("x", " ").replace("×", " "))
    vals = [float(t) for t in toks]
    if not vals:
        raise SystemExit(f"cannot parse eye '{s}'")
    sph = vals[0]
    cyl = 0.0
    axis = None
    if len(vals) >= 2 and abs(vals[1]) > 0:
        cyl = vals[1]
        if len(vals) >= 3:
            axis = int(vals[2]) % 180
    if cyl > 0:
        plus_conv = True
        sph, cyl, axis = transpose(sph, cyl, axis or 90)
        axis = axis % 180
    return dict(sph=sph, cyl=cyl, axis=axis, plus_conv=plus_conv)

def transpose(sph, cyl, axis):
    """Plus-cylinder -> minus-cylinder."""
    return round(sph + cyl, 2), -cyl, (axis + 90) % 180 if axis <= 90 else (axis - 90) % 180

def fmt_eye(e):
    s = f"{e['sph']:+.2f}"
    if e["cyl"]:
        s += f" {e['cyl']:+.2f} x{e['axis']:03d}"
    return s

# ------------------------------------------------------------- interpreting -

def sph_band(v):
    a = abs(v)
    if v < 0:
        if a < 1: return "mild myopia (nearsighted) — distance blur, fine up close"
        if a < 3: return "low-moderate myopia — daily-wear zone"
        if a < 6: return "moderate-high myopia — constant wear; uncorrected clear only ~arm's length"
        return "high myopia — 1.74 index + small frame; annual retinal check"
    else:
        if a < 0.25: return "plano (no sphere)"
        if a < 2: return "low hyperopia (farsighted) — often fine young, strain at screens"
        if a < 3.5: return "moderate hyperopia — constant effort to focus; kids: follow up"
        return "high hyperopia — children need prompt follow-up (amblyopia risk)"

def cyl_band(v):
    a = abs(v)
    if a == 0: return "no astigmatism"
    if a <= 0.75: return "trace/mild astigmatism — often left uncorrected"
    if a <= 2.0: return "moderate astigmatism — night starbursts, tilted edges"
    return "high astigmatism — axis accuracy critical; allow adaptation time"

def add_band(v):
    if v == 0: return "no ADD — single vision"
    if v <= 1.25: return "early presbyopia — phone drifting farther, more light"
    if v <= 2.0: return "established presbyopia — progressive or dedicated readers"
    return "mature presbyopia — reading zone ~35–40 cm fixed"

def axis_desc(axis):
    if axis is None: return ""
    if 170 <= axis or axis <= 10: return "near-horizontal (with-the-rule-ish)"
    if 80 <= axis <= 100: return "near-vertical (against-the-rule)"
    return "oblique"

def decode(rx, label=""):
    print(f"--- {label or 'prescription'} (normalized to minus cylinder) ---")
    for eye in ("od", "os"):
        e = rx[eye]
        name = "OD (right)" if eye == "od" else "OS (left)"
        if e.get("plus_conv"):
            print(f"  {name}: input was PLUS cylinder — transposed to {fmt_eye(e)}")
        print(f"  {name}: {fmt_eye(e)}")
        print(f"     sphere: {sph_band(e['sph'])}")
        if e["cyl"]:
            print(f"     cyl:    {cyl_band(e['cyl'])} at axis {e['axis']}° ({axis_desc(e['axis'])})")
        else:
            print(f"     cyl:    none")
    if rx.get("add"):
        print(f"  ADD {rx['add']:+.2f}: {add_band(rx['add'])}")
        print(f"     full-reader SPH = distance SPH + ADD → OD {rx['od']['sph']+rx['add']:+.2f} / "
              f"OS {rx['os']['sph']+rx['add']:+.2f}")
    if rx.get("pd"):
        print(f"  PD {rx['pd']} mm {'(binocular)' if rx['pd'] > 40 else '(monocular each eye?)'}")
    # anisometropia
    d = abs(rx["od"]["sph"] - rx["os"]["sph"])
    dm = d + max(abs(rx["od"]["cyl"]), abs(rx["os"]["cyl"])) * 0
    if d > 1.0:
        print(f"  ! inter-eye sphere difference {d:.2f} D > 1.00 D (anisometropia): "
              "adaptation harder; contacts may beat glasses (unequal image size)")
    # add mismatch
    if rx.get("add_od") and rx.get("add_os") and rx["add_od"] != rx["add_os"]:
        print("  ! ADD differs between eyes — query this; almost always an entry error")

def cmd_decode(a):
    rx = dict(od=parse_eye(a.od), os=parse_eye(a.os or a.od),
              add=a.add or 0.0, pd=a.pd)
    decode(rx, "input prescription")
    # lens type verdict
    print("\nLens-type verdict:")
    maxp = max(abs(rx["od"]["sph"]) + abs(rx["od"]["cyl"]),
               abs(rx["os"]["sph"]) + abs(rx["os"]["cyl"]))
    if rx["add"]:
        print("  ADD present → progressive PAL / bifocal / or TWO pairs (distance + readers)")
        print("  two online pairs usually beat one progressive in field-of-view per dollar")
    else:
        print("  no ADD → single vision (cheapest tier is fine)")
    if maxp > 6:
        print(f"  combined power {maxp:.2f} D > 6 → 1.74 index + small eye-size frame")
    elif maxp > 4:
        print(f"  combined power {maxp:.2f} D → 1.67 index recommended")
    print(f"  anti-reflective coating: best comfort-per-dollar if screen user")
    return 0

def cmd_diff(a):
    old_od, old_os = [parse_eye(x) for x in a.old.split("|")]
    new_od, new_os = [parse_eye(x) for x in a.new.split("|")]
    print(f"{'eye':5} {'field':6} {'old':>10} {'new':>10} {'delta':>7}  verdict")
    for name, o, n in (("OD", old_od, new_od), ("OS", old_os, new_os)):
        for f, label in (("sph", "SPH"), ("cyl", "CYL"), ("axis", "AXIS")):
            ov, nv = o[f], n[f]
            if f == "axis":
                if ov is None and nv is None: continue
                ov = ov if ov is not None else 0
                nv = nv if nv is not None else 0
                d = min(abs(nv - ov), 180 - abs(nv - ov))
                if o["cyl"] == 0 and n["cyl"] == 0: continue
                verdict = "will feel it" if (d >= 10 and abs(n["cyl"]) >= 0.75) else "noise"
                ov = 180 if ov == 0 else ov
                nv = 180 if nv == 0 else nv
            else:
                if f == "cyl" and o["cyl"] == 0 and n["cyl"] == 0: continue
                d = nv - ov
                verdict = "WILL FEEL IT" if abs(d) >= 0.50 else ("borderline" if abs(d) >= 0.25 else "noise")
                d = round(d, 2)
            print(f"{name:5} {label:6} {ov:>10} {nv:>10} {d:>7.2f}  {verdict}")
    # OD/OS swap detection
    if (new_od["sph"] - new_os["sph"]) * (old_od["sph"] - old_os["sph"]) < 0 \
       and abs(new_od["sph"] - old_os["sph"]) > 0.5:
        print("\n!! inter-eye difference sign FLIPPED — possible OD/OS swap in data entry")
    return 0

def cmd_pd(a):
    if a.method == "mirror":
        print("Mirror method (5 min, ±1 mm):")
        print(" 1. Stand ~50 cm from bathroom mirror. Wear current glasses.")
        print(" 2. With fine marker, dot lens directly over CENTER of each pupil")
        print("    (look at your reflection's LEFT eye while dotting BOTH? no —")
        print("     look at the bridge of your own nose reflection, dot both).")
        print(" 3. Repeat 3×, measure dot-to-dot in mm each time, average.")
        print(" 4. That's DISTANCE PD. For readers: subtract 3–4 mm.")
        print(" Record with: python3 rx_decode.py pd --record <value>")
    elif a.method == "photo":
        print("Photo method: arm's-length selfie with flash (red-eye dots = pupil centers),")
        print("credit-card-sized card held flat at cheekbone for scale. Any free PD app")
        print("does the ratio; sanity-check against 54–74 mm adult range.")
    elif a.method == "glasses":
        print("Old-glasses method: have someone hold a small light ~40 cm in front of you;")
        print("they mark the reflection on EACH lens with marker; measure between marks.")
    if a.record:
        with open("pd_record.json", "w") as f:
            json.dump(dict(pd_mm=a.record, method=a.method,
                           note="binocular distance PD unless noted"), f, indent=1)
        print(f"saved pd_record.json: PD {a.record} mm ({a.method} method)")
    return 0

def cmd_computer(a):
    rx_od, rx_os = [parse_eye(x) for x in a.rx.split("|")]
    add = a.add if a.add else 0.0
    wd = a.distance_cm
    frac = (1 / 0.40 - 1 / (wd / 100.0)) / (1 / 0.40)  # portion of ADD for this distance
    frac = min(max(frac, 0.0), 1.0)
    print(f"Working distance {wd} cm → use {frac * 100:.0f}% of ADD ({add * frac:+.2f} D)")
    for name, e in (("OD", rx_od), ("OS", rx_os)):
        comp = e["sph"] + add * frac
        print(f"  {name}: {comp:+.2f} {('' if not e['cyl'] else f'{e[chr(99)+chr(121)+chr(108)]:+.2f} x' + str(e['axis']).zfill(3))}")
    print("  (order as SINGLE VISION 'computer/office' glasses; CYL/AXIS unchanged)")
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("decode"); d.add_argument("--od", required=True)
    d.add_argument("--os"); d.add_argument("--add", type=float, default=0.0)
    d.add_argument("--pd", type=float); d.set_defaults(fn=cmd_decode)
    f = sub.add_parser("diff")
    f.add_argument("--old", required=True, help="'od | os' e.g. '-2.50 -1.00 x180 | -2.75'")
    f.add_argument("--new", required=True); f.set_defaults(fn=cmd_diff)
    p = sub.add_parser("pd")
    p.add_argument("--method", choices=["mirror", "photo", "glasses"], default="mirror")
    p.add_argument("--record", type=float); p.set_defaults(fn=cmd_pd)
    c = sub.add_parser("computer")
    c.add_argument("--rx", required=True, help="'od | os' distance prescription")
    c.add_argument("--add", type=float, default=2.0)
    c.add_argument("--distance-cm", type=float, default=65); c.set_defaults(fn=cmd_computer)
    a = ap.parse_args(); sys.exit(a.fn(a))

if __name__ == "__main__":
    main()
