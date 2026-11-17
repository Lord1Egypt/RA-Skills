#!/usr/bin/env python3
"""Pizza dough scaler: pan math -> ball weights -> baker's
percentages -> gram-precise recipe + dated timing sheet.

Pure stdlib. Styles: neo (neo-neapolitan), ny, detroit,
sicilian. All percentages overridable.

Usage:
  plan --style ny --pans 16x2
  plan --style detroit --pans 8x10x2x2
  plan --style neo --pans 12x4 --hydration 63 --salt-pct 2.9
  plan --style ny --pans 16x2 --bake "2026-10-24 19:00" \
       --ferment 41 --kitchen-c 18
  styles   show the preset table
"""
import argparse
import math
import sys
from datetime import datetime, timedelta

STYLES = {
    # hyd, salt, oil, sugar, tf (g/in2 round), note
    "neo": dict(hyd=0.64, salt=0.029, oil=0.0, sugar=0.0,
                tf=2.5, name="Neo-Neapolitan"),
    "ny": dict(hyd=0.61, salt=0.020, oil=0.025, sugar=0.015,
               tf=2.9, name="NY-style"),
    "detroit": dict(hyd=0.72, salt=0.022, oil=0.09, sugar=0.0,
                    tf=6.6, name="Detroit",
                    depth_rule=True),
    "sicilian": dict(hyd=0.67, salt=0.020, oil=0.04, sugar=0.0,
                     tf=3.6, name="Sicilian"),
}


def parse_pans(spec):
    """'16x2' -> [(16,1,2)]; '8x10x2x2' -> [(8,10,2,2)] (LxWxdepth x count).
    Multiple specs comma-separated."""
    pans = []
    for chunk in spec.split(","):
        dims = [float(x) for x in chunk.split("x")]
        if len(dims) == 2:            # diameter x count
            pans.append((dims[0], None, 2.0, int(dims[1])))
        elif len(dims) == 3:          # L x W x count (depth 2 default)
            pans.append((dims[0], dims[1], 2.0, int(dims[2])))
        elif len(dims) == 4:          # L x W x depth x count
            pans.append((dims[0], dims[1], dims[2], int(dims[3])))
        else:
            raise ValueError(f"bad pan spec: {chunk!r}")
    return pans


def ball_weight(style, pan, tf):
    d, w, depth, _ = pan
    if w is None:                     # round
        return math.pi * (d / 2) ** 2 * tf
    if STYLES[style].get("depth_rule"):
        return d * w * STYLES[style]["tf"] * (depth / 2.0)
    return d * w * tf


def yeast_pct(ferment_h, cold):
    """instant dry yeast % of flour for a target ferment length.
    Returns PERCENT (e.g. 0.09 = 0.09%)."""
    if not cold:
        if ferment_h >= 8:
            return 0.08
        if ferment_h >= 6:
            return 0.15
        if ferment_h >= 4:
            return 0.30
        return 0.60
    if ferment_h >= 72:
        return 0.03
    if ferment_h >= 48:
        return 0.06
    if ferment_h >= 36:
        return 0.09
    if ferment_h >= 24:
        return 0.12
    return 0.20


def temp_factor(kitchen_c):
    """Q10 ~2 per 10C vs 21C reference."""
    return 2 ** ((21.0 - kitchen_c) / 10.0)


def cmd_styles(_a=None):
    print(f"{'STYLE':<10}{'HYD%':>6}{'SALT%':>7}{'OIL%':>6}"
          f"{'SUGAR%':>8}{'TF g/in2':>10}  NOTE")
    print("-" * 72)
    for k, s in STYLES.items():
        note = "depth-aware (Detroit pans)" if s.get("depth_rule") \
            else "round pan factor"
        print(f"{k:<10}{s['hyd']*100:>6.0f}{s['salt']*100:>7.1f}"
              f"{s['oil']*100:>6.1f}{s['sugar']*100:>8.1f}"
              f"{s['tf']:>10.1f}  {note}")


def cmd_plan(a):
    if a.style not in STYLES:
        sys.exit(f"unknown style {a.style!r}; choices: {list(STYLES)}")
    st = dict(STYLES[a.style])
    st["hyd"] = float(st["hyd"])
    st["salt"] = float(st["salt"])
    st["oil"] = float(st["oil"])
    st["sugar"] = float(st["sugar"])
    st["tf"] = float(st["tf"])
    if a.hydration:
        st["hyd"] = a.hydration / 100
    if a.salt_pct:
        st["salt"] = a.salt_pct / 100
    if a.oil_pct:
        st["oil"] = a.oil_pct / 100
    if a.flour_class == "ap":
        st["hyd"] -= 0.05
    elif a.flour_class == "ww10":
        st["hyd"] += 0.04

    pans = []
    for spec in a.pans:
        pans.extend(parse_pans(spec))
    balls = []
    for pan in pans:
        bw = ball_weight(a.style, pan, st["tf"])
        for _ in range(pan[3]):
            balls.append(bw)
    if not balls:
        sys.exit("no pans parsed")
    total = sum(balls)

    cold = a.ferment and a.ferment > 10
    yp = yeast_pct(a.ferment or 6, cold) / 100.0
    if a.kitchen_c:
        yp *= temp_factor(a.kitchen_c)
        yp = min(yp, 0.01)
    if a.yeast_pct:
        yp = a.yeast_pct / 100

    pct_sum = 1 + st["hyd"] + st["salt"] + st["oil"] + st["sugar"] + yp
    flour = total / pct_sum

    name = st["name"]
    print(f"\n=== {name} — {len(balls)} ball(s) ===")
    for pan in pans:
        bw = ball_weight(a.style, pan, st["tf"])
        shape = (f'{pan[0]:g}" round' if pan[1] is None
                 else f'{pan[0]:g}x{pan[1]:g}" ({pan[2]:g}" deep)')
        print(f"  {shape:<24} x{pan[3]}  @ {bw:,.0f} g")
    print(f"\n  TOTAL dough: {total:,.0f} g")
    print(f"\n  flour      {flour:>8,.0f} g   (100%)")
    print(f"  water      {flour*st['hyd']:>8,.0f} g   "
          f"({st['hyd']*100:.0f}%)"
          + ("  [AP adjust -5%]" if a.flour_class == "ap" else ""))
    print(f"  salt       {flour*st['salt']:>8,.0f} g   "
          f"({st['salt']*100:.1f}%)")
    if st["oil"]:
        print(f"  olive oil  {flour*st['oil']:>8,.0f} g   "
              f"({st['oil']*100:.0f}%)"
              + ("  half in dough, half in pan!" if a.style == "detroit"
                 else ""))
    if st["sugar"]:
        print(f"  sugar      {flour*st['sugar']:>8,.0f} g   "
              f"({st['sugar']*100:.1f}%)")
    print(f"  instant yeast {flour*yp:>3.2f} g  ({yp*100:.2f}%)"
          + (f"  [kitchen {a.kitchen_c}C adj]" if a.kitchen_c else ""))

    if a.bake:
        try:
            bake = datetime.strptime(a.bake, "%Y-%m-%d %H:%M")
        except ValueError:
            sys.exit('--bake format: "YYYY-MM-DD HH:MM"')
        ferm_h = a.ferment or 6
        mix = bake - timedelta(hours=ferm_h)
        print(f"\n  TIMING (ferment {ferm_h:g}h, "
              f"{'cold' if cold else 'room temp'}):")
        if cold:
            bulk_end = mix + timedelta(hours=2)
            pull = bake - timedelta(hours=(2.5 if a.style in
                                           ("ny", "neo") else 1.5))
            print(f"  {mix:%a %H:%M}  mix + knead 8-10 min")
            print(f"  {bulk_end:%a %H:%M}  ball -> oiled box -> fridge")
            print(f"  {pull:%a %H:%M}  OUT of fridge "
                  + ("(press during the hour)" if a.style == "detroit"
                     else "(stretch test at +2h)"))
        else:
            print(f"  {mix:%a %H:%M}  mix; bulk till "
                  f"{mix+timedelta(hours=ferm_h*0.6):%H:%M}; ball")
        print(f"  {bake:%a %H:%M}  BAKE")
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.
                                 RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("styles").set_defaults(func=cmd_styles)
    g = sub.add_parser("plan")
    g.add_argument("--style", required=True, choices=sorted(STYLES))
    g.add_argument("--pans", action="append", required=True,
                   help='e.g. 16x2  or  8x10x2x2  (comma-sep for multiple)')
    g.add_argument("--hydration", type=float, default=None)
    g.add_argument("--salt-pct", type=float, default=None)
    g.add_argument("--oil-pct", type=float, default=None)
    g.add_argument("--yeast-pct", type=float, default=None)
    g.add_argument("--flour-class", choices=["bread", "ap", "ww10"],
                   default="bread")
    g.add_argument("--ferment", type=float, default=None,
                   help="total ferment hours before bake")
    g.add_argument("--bake", default=None, help='"YYYY-MM-DD HH:MM"')
    g.add_argument("--kitchen-c", type=float, default=None)
    g.set_defaults(func=cmd_plan)
    a = p.parse_args()
    try:
        a.func(a)
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    main()
