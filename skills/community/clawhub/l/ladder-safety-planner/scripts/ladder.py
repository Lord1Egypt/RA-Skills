#!/usr/bin/env python3
"""Ladder setup planner: size, 4:1 angle, duty rating, power lines, checklist."""
import argparse
import math
import sys

# Nominal -> max usable extension length (section overlap accounted, industry std)
EXT_USABLE = {16: 13, 20: 17, 24: 21, 28: 25, 32: 29, 36: 33, 40: 37}

# Stepladder size -> max standing platform height (top 2 steps off-limits)
STEP_PLATFORM = {4: 2.0, 6: 3.5, 8: 5.0, 10: 6.5, 12: 8.0, 14: 9.5, 16: 11.0, 20: 14.0}

DUTY = [
    (200, "III", "Light duty household"),
    (225, "II", "Medium duty (doorman/warehouse light)"),
    (250, "I", "Heavy duty industrial"),
    (300, "IA", "Extra heavy duty (pro painter/roofer)"),
    (350, "IAA", "Special duty (max capacity)"),
]


def cmd_setup(a):
    """Pick ladder size from desired touch-reach height (ft)."""
    reach = a.reach
    print(f"Target: comfortably TOUCH a point {reach} ft above ground")
    print("(max reach assumes ~5'9\" person, 12\" vertical arm reach)")
    print()
    if a.type == "step":
        ok = [s for s, p in sorted(STEP_PLATFORM.items()) if p + 4 >= reach]
        if not ok:
            size = None
        else:
            size = ok[0]
        print("STEPLADDER plan:")
        if size is None:
            print(f"  ✗ No safe stepladder reaches {reach} ft. Use an extension ladder")
            print("    (or platform ladder over 20 ft does not exist).")
            return
        plat = STEP_PLATFORM[size]
        print(f"  → {size}-ft stepladder (platform {plat} ft, reach ~{plat+4:.0f} ft)")
        print(f"  - Stand no higher than {plat} ft (top 2 steps stay empty)")
        print(f"  - Never lean it closed against a wall")
        print(f"  - Lock the spreaders fully open before climbing")
    else:
        # Height the ladder must physically span: support wall height.
        # For roof access: reach == roof edge height; need edge+3 above.
        span = reach + (3 if a.purpose == "roof" else 0)
        ok = [n for n, u in sorted(EXT_USABLE.items()) if u >= span]
        print("EXTENSION LADDER plan:")
        if not ok:
            print(f"  ✗ Required span {span} ft exceeds common 40-ft ratings.")
            print("    Rent a lift / hire a pro. Do not improvise.")
            return
        size = ok[0]
        usable = EXT_USABLE[size]
        base = span / 4.0
        ang = math.degrees(math.atan(span / base))
        print(f"  Ladder must span {span} ft"
              f"{' (roof edge + 3 ft rail above)' if a.purpose == 'roof' else ' (wall support height)'}")
        print(f"  → {size}-ft extension ladder (usable {usable} ft ≥ {span} ft)")
        print(f"  - Base set {base:.1f} ft out from the wall (4:1 rule, {ang:.0f}°)")
        print(f"  - Overlap: fly section must fully engage; never two sections apart")
        if a.purpose == "roof":
            print("  - 3 ft of rail above roof edge = handhold for step-off/return")
            print("  - Helper foots the base or tie top to an anchor")
    print()
    print("Buy/borrow the next size up if surface is uneven or you wear boots+gear.")


def cmd_angle(a):
    h = a.height
    base = h / 4.0
    print(f"Extension ladder against {h} ft support height:")
    print(f"  Base distance from wall: {base:.1f} ft ({base*12:.0f} in)")
    print(f"  Angle from ground: {math.degrees(math.atan(h/base)):.1f}° (target 75°)")
    print()
    print("Field check (no tape measure):")
    print("  toes against rails, arms straight out ahead — palm just touches rungs.")
    print("  Can't touch = too shallow (slides out); wrist deep = too steep (tips).")


def cmd_duty(a):
    total = a.weight + a.gear
    print(f"Load: {a.weight} lb body + {a.gear} lb gear/materials = {total} lb")
    for cap, t, desc in DUTY:
        mark = "→ MINIMUM" if cap >= total else None
        if mark:
            print(f"  {mark}: Type {t} ({cap} lb) — {desc}")
            nxt = [c for c, _, _ in DUTY if c > cap]
            if nxt:
                print(f"  Headroom option: Type {[t2 for c2,t2,_ in DUTY if c2==nxt[0]][0]}"
                      f" ({nxt[0]} lb) if you'll carry more later")
            break
    else:
        print("  ✗ Over 350 lb total: no common ladder rated. Use a work platform")
        print("    rated for the load or re-plan materials hoisting separately.")


def cmd_powerline(a):
    kv = a.kv
    if kv <= 50:
        clear, note = 10.0, "≤50 kV (incl. residential service drop)"
    elif kv <= 200:
        clear = 10.0 + (kv - 50) * 0.4 / 1.0 * 10  # +4in per kV over 50, in ft
        note = f"{kv} kV"
    else:
        clear = 10.0 + (kv - 50) * 0.4 * 10 / 12  # +0.4in/kV over 50kV
        note = f"{kv} kV"
    print(f"Overhead line: {note}")
    print(f"  Minimum clearance: {clear:.0f} ft (ladder AND you, in any position)")
    print()
    print("Rules:")
    print("  - Aluminum ladder + ANY overhead line = never inside clearance")
    print("  - Service drop (house line) is usually 120/240V — still lethal,")
    print("    still keep 10 ft; wet wood/fiberglass-dirty conducts")
    print("  - Carrying a ladder upright near lines kills people — carry low")
    print("  - If the job puts you within clearance: utility must move/shield")
    print("    the line or the job waits. No exceptions for 'quick' jobs.")


def cmd_checklist(_):
    print("60-SECOND PRE-CLIMB CHECKLIST")
    print("=" * 29)
    items = [
        "Ladder inspected: no cracks, dents, bent rungs, slick rungs",
        "Correct size for the touch-reach (not 'make it work')",
        "Duty rating ≥ body + clothes + tools + materials",
        "Extension: base at height/4, fly locked, rope+runlock engaged",
        "Stepladder: spreaders locked open, both rails on firm level base",
        "Overhead lines scanned in ALL ladder positions incl. carry",
        "Weather: no wind gusts, dry rungs, no storm within 10 mi",
        "Helper informed / ladder tied / base footed for roof step-off",
        "3-points-of-contact plan; tools in belt or hoisted, not hands",
        "Phone on body; someone knows you're up there",
    ]
    for i, it in enumerate(items, 1):
        print(f"[{' '}] {i}. {it}")
    print()
    print("Abort triggers: wet roof, steep pitch, gusting wind, feel of slip,")
    print("any 'just one more step' reasoning. Down is always available.")


def main():
    p = argparse.ArgumentParser(description="Ladder setup planner (sizes, angle, duty, power).")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup", help="pick ladder size from reach height")
    s.add_argument("--reach", type=float, required=True, help="ft: highest point you TOUCH")
    s.add_argument("--type", choices=["step", "extension"], required=True)
    s.add_argument("--purpose", choices=["wall", "roof"], default="wall")
    s.set_defaults(f=cmd_setup)
    s = sub.add_parser("angle", help="4:1 base distance for support height")
    s.add_argument("--height", type=float, required=True, help="ft of wall/support height")
    s.set_defaults(f=cmd_angle)
    s = sub.add_parser("duty", help="minimum duty rating from load")
    s.add_argument("--weight", type=float, required=True)
    s.add_argument("--gear", type=float, default=15.0, help="tools+materials lb (default 15)")
    s.set_defaults(f=cmd_duty)
    s = sub.add_parser("powerline", help="clearance for overhead line")
    s.add_argument("--kv", type=float, required=True)
    s.set_defaults(f=cmd_powerline)
    s = sub.add_parser("checklist", help="print pre-climb checklist")
    s.set_defaults(f=cmd_checklist)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
