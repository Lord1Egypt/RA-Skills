#!/usr/bin/env python3
"""Jet-lag protocol planner: day-by-day circadian shift schedule.

Computes a dated protocol from home/destination timezone offsets and your
habitual wake time: pre-trip sleep shifting, SEEK/AVOID light windows around
your shifting CBTmin, low-dose melatonin timing, caffeine cutoffs, in-flight
rules, and first-days light discipline at destination.

Model summary (see references/circadian-science.md):
  CBTmin ~= habitual wake - 2h
  Light before CBTmin -> phase DELAY (westward tool)
  Light after  CBTmin -> phase ADVANCE (eastward tool)
  Melatonin ~5h before CBTmin -> advance (low dose 0.3-1 mg)
  Alignment speed: ~1.0 h/day advancing, ~1.5 h/day delaying
  Wrap: a raw east difference >12h is planned as a westward delay.

Pure stdlib. All output times are local wall-clock of whichever day is shown.
"""
import argparse
import json
import math

MIN = 60  # minutes per hour


def hhmm(minutes):
    m = int(round(minutes)) % (24 * MIN)
    return f"{m // MIN:02d}:{m % MIN:02d}"


def parse_hhmm(s):
    h, m = s.split(":")
    return int(h) * MIN + int(m)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def plan(home_tz, dest_tz, wake_home, wake_dest, pre_days):
    diff = (dest_tz - home_tz)  # east-positive hours
    if diff > 12:
        diff -= 24
    if diff < -12:
        diff += 24
    east = diff > 0
    required = abs(diff)
    rate = 1.0 if east else 1.5  # h/day at destination with protocol
    pre_cap = 3.0 if east else 2.0
    pre_step_cap = 1.0  # never shift >1h/day while living at home

    cbt0 = wake_home - 2 * MIN  # home-clock CBTmin, minutes
    target = (wake_dest - 2 * MIN) % (24 * MIN)          # wanted local position
    now_dest = (cbt0 + diff * MIN) % (24 * MIN)          # current pos, dest clock

    if required < 1:
        return {
            "needed": False,
            "diff_hours": diff,
            "note": ("Crossing <1 h of time difference: no shift protocol needed. "
                     "Arrive-mode only: daylight on arrival, normal bedtime local, "
                     "caffeine cutoff 8h before that bedtime."),
        }

    # --- pre-trip shifting (home clock) ---
    pre = []
    cum = 0.0
    for d in range(1, pre_days + 1):
        step = min(pre_step_cap, pre_cap - cum, required - cum)
        if step <= 0:
            break
        cum += step
        p = (cbt0 + (cum if not east else -cum) * MIN) % (24 * MIN)
        pre.append(_day_row(f"Day -{pre_days - d + 1}", p, east, clock="home",
                            wake=(wake_home + (-cum if east else cum) * MIN)))

    remaining = required - cum

    # --- destination days (destination clock) ---
    dest_days = max(1, math.ceil(remaining / rate)) if remaining > 0 else 0
    post = []
    shifted = cum
    for k in range(1, dest_days + 1):
        step = min(rate, required - shifted)
        shifted += step
        p_abs = (cbt0 + (-shifted if east else shifted) * MIN) % (24 * MIN)
        p_local = (p_abs + diff * MIN) % (24 * MIN)  # absolute -> local wall
        post.append(_day_row(f"Dest day {k}", p_local, east, clock="destination",
                             wake=wake_dest, progress=shifted, required=required))

    # flight-day row: position = after pre-shift, shown in DESTINATION clock
    p_flight_abs = (cbt0 + (-cum if east else cum) * MIN) % (24 * MIN)
    p_flight_local = (p_flight_abs + diff * MIN) % (24 * MIN)
    flight = _day_row("Flight day", p_flight_local, east, clock="destination",
                      wake=wake_dest, progress=cum, required=required)

    return {
        "needed": True,
        "diff_hours": diff,
        "direction": "advance (eastward)" if east else "delay (westward)",
        "required_shift_h": required,
        "prepaid_h": round(cum, 2),
        "remaining_at_landing_h": round(remaining, 2),
        "destination_days_to_align": dest_days,
        "cbtmin_home": hhmm(cbt0),
        "cbtmin_target_local": hhmm(target),
        "cbtmin_now_local": hhmm(now_dest),
        "pre_trip_days": pre,
        "flight_day": flight,
        "destination_days": post,
        "inflight_rules": _inflight(east, diff, wake_dest),
        "first_days": _first_days(east),
    }


def _day_row(label, cbt_local, east, clock, wake, progress=None, required=None):
    """Build one protocol row from CBTmin position in the day's local clock."""
    if east:
        seek = (cbt_local, cbt_local + 4 * MIN)                 # after CBTmin
        avoid = (cbt_local - 4 * MIN, cbt_local)                # before CBTmin
        melatonin = cbt_local - 5 * MIN                         # advance dose
        mel = f"{hhmm(melatonin)} (0.3–1 mg)"
    else:
        seek = (cbt_local - 4 * MIN, cbt_local)                 # evening light
        avoid = (cbt_local, cbt_local + 4 * MIN)                # morning light
        mel = "none (light-only westward)"
    bed = wake - 8 * MIN
    row = {
        "day": label,
        "clock": clock,
        "wake_target": hhmm(wake),
        "cbtmin": hhmm(cbt_local),
        "seek_light": f"{hhmm(seek[0])}–{hhmm(seek[1])}",
        "avoid_light": f"{hhmm(avoid[0])}–{hhmm(avoid[1])}",
        "melatonin": mel,
        "caffeine_cutoff": hhmm(bed - 6 * MIN),
    }
    if progress is not None:
        row["shift_done"] = f"{progress:.1f}/{required:.0f} h"
    return row


def _inflight(east, diff, wake_dest):
    return [
        "Set watch to destination time at boarding; follow destination cues for meals/sleep.",
        "Sleep on the plane only inside destination night hours that overlap the flight; else stay awake (eye mask ON = artificial night).",
        "Caffeine only in the destination-morning portion of the flight; cutoff 6 h before destination bedtime.",
        "No alcohol (wrecks sleep architecture and the phase marker); hydrate aggressively (cabin 10–20% RH).",
        f"Land-day naps: max 25–30 min, before 15:00 local, alarm set. Target bedtime local: {hhmm(wake_dest - 8 * MIN)}.",
    ]


def _first_days(east):
    if east:
        return [
            "DANGER ZONE = early morning: bright light BEFORE your shifted CBTmin delays you further (wrong way). Sunglasses/dim light until the AVOID window ends.",
            "Seek bright outdoor light from mid-morning onward (the SEEK window), 30+ min.",
            "Melatonin early evening local (per table) — it lands 4–6 h before your drifting CBTmin and advances you.",
            "Expect early-evening sleepiness: it is 22:00 on your body clock at 17:00 local — do not nap through it; short walk + light instead.",
        ]
    return [
        "DANGER ZONE = late evening: you want to STAY UP later (delay), so evening bright light is your tool — keep lights ON until the SEEK window ends.",
        "AVOID bright early-morning light (before/just after shifted CBTmin in the table) — morning light ADVANCES you, the wrong way westward; sunglasses on the morning commute.",
        "No melatonin at destination (daytime dosing = grogginess; westward shifting is done with light).",
        "Early waking (03–04 local) is the westward signature: do not turn on bright lights; rest in dim light until your wake target.",
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--home-tz", type=float, required=True,
                    help="home UTC offset in hours, east positive (e.g. 3, -5)")
    ap.add_argument("--dest-tz", type=float, required=True,
                    help="destination UTC offset in hours")
    ap.add_argument("--wake-home", default="07:00",
                    help="habitual wake time at home, HH:MM (default 07:00)")
    ap.add_argument("--wake-dest", default=None,
                    help="desired wake time at destination, HH:MM (default same as home)")
    ap.add_argument("--pre-days", type=int, default=0,
                    help="days available to pre-shift before flight (0-3)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()

    wake_home = parse_hhmm(a.wake_home)
    wake_dest = parse_hhmm(a.wake_dest) if a.wake_dest else wake_home
    p = plan(a.home_tz, a.dest_tz, wake_home, wake_dest,
             clamp(a.pre_days, 0, 3))

    if a.json:
        print(json.dumps(p, indent=2, ensure_ascii=False))
        return

    if not p["needed"]:
        print(f"Shift needed: {p['diff_hours']:+.1f} h — {p['note']}")
        return

    print(f"=== Jet-lag protocol: {p['direction']}, {p['required_shift_h']:.0f} h total ===")
    print(f"Home CBTmin {p['cbtmin_home']} -> target CBTmin {p['cbtmin_target_local']} (dest clock; now {p['cbtmin_now_local']})")
    print(f"Pre-paid {p['prepaid_h']} h before flight; {p['remaining_at_landing_h']} h left; "
          f"~{p['destination_days_to_align']} destination day(s) to align\n")

    rows = p["pre_trip_days"] + [p["flight_day"]] + p["destination_days"]
    hdr = f"{'Day':<12}{'Clock':<13}{'Wake':<7}{'CBTmin':<8}{'SEEK light':<14}{'AVOID light':<14}{'Melatonin':<22}{'Caff cut':<9}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['day']:<12}{r['clock']:<13}{r['wake_target']:<7}{r['cbtmin']:<8}"
              f"{r['seek_light']:<14}{r['avoid_light']:<14}{r['melatonin']:<22}{r['caffeine_cutoff']:<9}")

    print("\n--- In-flight rules ---")
    for i, r in enumerate(p["inflight_rules"], 1):
        print(f"{i}. {r}")
    print("\n--- First days at destination ---")
    for i, r in enumerate(p["first_days"], 1):
        print(f"{i}. {r}")
    print("\nSafety: melatonin 0.3–1 mg is a timing tool, not a sleeping pill; skip if pregnant,")
    print("on anticoagulants/immunosuppressants, or giving to children — ask a clinician.")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
