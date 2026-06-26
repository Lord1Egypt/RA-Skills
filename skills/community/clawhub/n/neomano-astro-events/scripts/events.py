#!/usr/bin/env python3
"""Astronomy events for a location using Skyfield.

Commands:
  tonight --lat ... --lon ... [--tz America/Guayaquil]
  next    --lat ... --lon ... [--tz America/Guayaquil] --days 7

Outputs a compact text report.
"""

import argparse
import math
from datetime import datetime, timedelta

import pytz
from skyfield.api import load, wgs84
from skyfield import almanac


def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def moon_phase_name(deg: float) -> str:
    # crude labels
    if deg < 22.5:
        return "New Moon"
    if deg < 67.5:
        return "Waxing Crescent"
    if deg < 112.5:
        return "First Quarter"
    if deg < 157.5:
        return "Waxing Gibbous"
    if deg < 202.5:
        return "Full Moon"
    if deg < 247.5:
        return "Waning Gibbous"
    if deg < 292.5:
        return "Last Quarter"
    if deg < 337.5:
        return "Waning Crescent"
    return "New Moon"


def twilight_window(ts, eph, location, tz, date_local: datetime):
    t0 = tz.localize(datetime(date_local.year, date_local.month, date_local.day, 0, 0)).astimezone(pytz.utc)
    t1 = (t0 + timedelta(days=1))
    t0s = ts.from_datetime(t0)
    t1s = ts.from_datetime(t1)

    f = almanac.dark_twilight_day(eph, location)
    times, states = almanac.find_discrete(t0s, t1s, f)

    # State mapping: 0=dark, 1=astro, 2=nautical, 3=civil, 4=day
    # We want astro dusk/dawn transitions: between 1 and 0.
    events = []
    for t, s in zip(times, states):
        events.append((t.utc_datetime().astimezone(tz), int(s)))
    return events


def planet_best_window(ts, eph, location, tz, body_name: str, start_utc: datetime, hours: int = 12):
    body = eph[body_name]
    earth = eph["earth"]

    best = None
    for i in range(hours * 6 + 1):  # every 10 min
        dt_utc = start_utc + timedelta(minutes=10 * i)
        t = ts.from_datetime(dt_utc)
        astrometric = (earth + location).at(t).observe(body)
        alt, az, _ = astrometric.apparent().altaz()
        alt_deg = alt.degrees
        if alt_deg > 0:
            if best is None or alt_deg > best[0]:
                best = (alt_deg, dt_utc)
    if not best:
        return None
    alt_deg, dt_utc = best
    return {
        "best_alt_deg": alt_deg,
        "best_time": dt_utc.astimezone(tz),
    }


def infer_tz(lat: float, lon: float) -> str:
    """Infer timezone with a lightweight heuristic (no extra deps).

    For this first version we keep it simple:
    - If coordinates fall within mainland Ecuador bounds, use America/Guayaquil.
    - Otherwise fall back to UTC.

    (We can add robust tz inference later using a compatible library.)
    """
    if -5.5 <= lat <= 2.5 and -81.5 <= lon <= -75.0:
        return "America/Guayaquil"
    return "UTC"


def load_iss_satellite(ts):
    """Load ISS (ZARYA) TLE from Celestrak."""
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    with load.open(url) as f:
        raw_lines = f.readlines()
    lines = []
    for line in raw_lines:
        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="replace")
        line = str(line).strip()
        if line:
            lines.append(line)
    # Find ISS (ZARYA)
    for i in range(len(lines) - 2):
        if lines[i].upper().startswith("ISS"):
            name = lines[i]
            l1 = lines[i + 1]
            l2 = lines[i + 2]
            from skyfield.api import EarthSatellite

            return EarthSatellite(l1, l2, name, ts)
    return None


def iss_passes(ts, eph, location, tz, start_utc: datetime, hours: int = 12, min_alt_deg: float = 10.0):
    """Compute visible-ish ISS passes in the next window.

    We report rise/culminate/set events where max altitude >= min_alt_deg.
    """
    sat = load_iss_satellite(ts)
    if not sat:
        return []

    t0 = ts.from_datetime(start_utc)
    t1 = ts.from_datetime(start_utc + timedelta(hours=hours))

    # find_events returns (times, events) where event: 0 rise, 1 culminate, 2 set
    times, events = sat.find_events(location, t0, t1, altitude_degrees=min_alt_deg)

    passes = []
    current = {}
    for t, ev in zip(times, events):
        dt_local = t.utc_datetime().astimezone(tz)
        if ev == 0:
            current = {"rise": dt_local}
        elif ev == 1:
            # compute max altitude
            alt, az, _ = (sat - location).at(t).altaz()
            current["max_alt_deg"] = alt.degrees
            current["culminate"] = dt_local
        elif ev == 2:
            current["set"] = dt_local
            if current.get("max_alt_deg", 0) >= min_alt_deg and current.get("rise") and current.get("set"):
                passes.append(current)
            current = {}

    return passes


def report_for_date(lat: float, lon: float, tz_name: str, date_local: datetime):
    tz = pytz.timezone(tz_name)
    ts = load.timescale()
    eph = load("de421.bsp")

    location = wgs84.latlon(lat, lon)

    # Twilight events
    tw = twilight_window(ts, eph, location, tz, date_local)

    # Moon phase
    t_mid = ts.from_datetime(tz.localize(datetime(date_local.year, date_local.month, date_local.day, 21, 0)).astimezone(pytz.utc))
    phase = almanac.moon_phase(eph, t_mid).degrees

    # Planets to check (Skyfield names)
    planets = [
        ("mercury", "Mercury"),
        ("venus", "Venus"),
        ("mars", "Mars"),
        ("jupiter barycenter", "Jupiter"),
        ("saturn barycenter", "Saturn"),
    ]

    start_utc = tz.localize(datetime(date_local.year, date_local.month, date_local.day, 18, 0)).astimezone(pytz.utc)

    lines = []
    lines.append(f"Date: {date_local.date()} ({tz_name})")
    lines.append(f"Moon phase: {phase:.1f}° ({moon_phase_name(phase)})")

    lines.append("Twilight transitions (state 0=dark,1=astro,2=naut,3=civil,4=day):")
    for dt_local, state in tw:
        lines.append(f"  - {fmt(dt_local)} state={state}")

    lines.append("Best planet viewing (next ~12h from 18:00 local):")
    for key, label in planets:
        best = planet_best_window(ts, eph, location, tz, key, start_utc, hours=12)
        if not best:
            lines.append(f"  - {label}: not above horizon in this window")
        else:
            lines.append(f"  - {label}: best ~{fmt(best['best_time'])} at {best['best_alt_deg']:.1f}° alt")

    # ISS passes (next 12h)
    passes = iss_passes(ts, eph, location, tz, start_utc, hours=12, min_alt_deg=10.0)
    lines.append("ISS passes (next ~12h, max altitude ≥10°):")
    if not passes:
        lines.append("  - none found in this window")
    else:
        for p in passes[:10]:
            lines.append(
                f"  - rise {fmt(p['rise'])} · max {p.get('max_alt_deg', 0):.0f}° at {fmt(p['culminate'])} · set {fmt(p['set'])}"
            )

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("tonight")
    t.add_argument("--lat", type=float, required=True)
    t.add_argument("--lon", type=float, required=True)
    t.add_argument("--tz", default="", help="IANA timezone (optional; inferred from lat/lon if omitted)")

    n = sub.add_parser("next")
    n.add_argument("--lat", type=float, required=True)
    n.add_argument("--lon", type=float, required=True)
    n.add_argument("--tz", default="", help="IANA timezone (optional; inferred from lat/lon if omitted)")
    n.add_argument("--days", type=int, default=7)

    args = ap.parse_args()

    tz_name = args.tz.strip() or infer_tz(args.lat, args.lon)
    tz = pytz.timezone(tz_name)
    now_local = datetime.now(tz)

    if args.cmd == "tonight":
        print(report_for_date(args.lat, args.lon, tz_name, now_local))
        return 0

    if args.cmd == "next":
        for i in range(args.days):
            d = now_local + timedelta(days=i)
            print(report_for_date(args.lat, args.lon, tz_name, d))
            print("\n" + "-" * 40 + "\n")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
