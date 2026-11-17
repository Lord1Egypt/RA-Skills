#!/usr/bin/env python3
"""
noise_log.py — log noise incidents, find patterns, score severity, generate complaint letters.

Storage: local JSON (default ~/.noise-log.json). Pure stdlib.
"""
import argparse
import csv
import datetime as dt
import json
import os
import sys

DEFAULT_FILE = os.path.join(os.path.expanduser("~"), ".noise-log.json")

TYPES = ["music", "tv", "talking", "party", "barking", "construction",
         "renovation", "hvac", "traffic", "venue", "footsteps", "other"]

LOUDNESS_BANDS = {"faint": 1, "moderate": 2, "loud": 3, "very loud": 4}

# Common municipal defaults — adjust with --night-start/--night-end after checking local code
DEFAULT_NIGHT_START = 22
DEFAULT_NIGHT_END = 7


def load(path):
    if os.path.exists(path):
        return json.load(open(path))
    return {"incidents": []}


def save(db, path):
    json.dump(db, open(path, "w"), indent=2)


def parse_start(s):
    if not s:
        return dt.datetime.now()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return dt.datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise SystemExit(f"ERROR: --start must be 'YYYY-MM-DD HH:MM', got {s!r}")


def in_night_hours(hour, night_start, night_end):
    if night_start <= night_end:
        return night_start <= hour < night_end
    return hour >= night_start or hour < night_end


# ---------------------------------------------------------------- commands

def cmd_log(a):
    db = load(a.file)
    if a.type not in TYPES:
        sys.exit(f"ERROR: --type must be one of: {', '.join(TYPES)}")
    if a.loudness not in LOUDNESS_BANDS:
        sys.exit(f"ERROR: --loudness must be one of: {', '.join(LOUDNESS_BANDS)}")
    start = parse_start(a.start)
    inc = {
        "start": start.strftime("%Y-%m-%d %H:%M"),
        "weekday": start.strftime("%a"),
        "hour": start.hour,
        "duration_min": a.duration,
        "type": a.type,
        "loudness": a.loudness,
        "impact": a.impact or "",
        "neighbor": a.neighbor or "",
        "note": a.note or "",
    }
    db["incidents"].append(inc)
    db["incidents"].sort(key=lambda x: x["start"])
    save(db, a.file)
    night = "⚠ night-hours" if in_night_hours(start.hour, a.night_start, a.night_end) else ""
    print(f"logged: {inc['start']} {a.type} {a.duration}min {a.loudness} {night}".strip())


def window(db, days):
    if not days:
        return db["incidents"]
    cutoff = (dt.datetime.now() - dt.timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
    return [i for i in db["incidents"] if i["start"] >= cutoff]


def cmd_stats(a):
    incs = window(load(a.file), a.days)
    if not incs:
        print("(no incidents logged in this window)")
        return
    n = len(incs)
    total_min = sum(i["duration_min"] for i in incs)
    night = [i for i in incs if in_night_hours(i["hour"], a.night_start, a.night_end)]
    span_days = a.days or max(1, (dt.datetime.now() -
                        dt.datetime.strptime(incs[0]["start"], "%Y-%m-%d %H:%M")).days + 1)
    label = f"{a.days} days" if a.days else "all time"
    print(f"Noise Log — {label} ending {dt.date.today()}")
    print(f"  incidents: {n}   ({n / span_days * 7:.1f}/week)   total {total_min/60:.1f} hours")
    print(f"  night-hours ({a.night_start:02d}:00–{a.night_end:02d}:00): {len(night)} of {n}"
          f"  ({len(night)/n*100:.0f}%)  ⚠ {len(night)} potential quiet-hours violations"
          if night else
          f"  night-hours ({a.night_start:02d}:00–{a.night_end:02d}:00): 0 of {n}")
    by_type = {}
    for i in incs:
        by_type[i["type"]] = by_type.get(i["type"], 0) + 1
    ranked = sorted(by_type.items(), key=lambda kv: -kv[1])
    print("  by type:   " + " · ".join(f"{t} {c}" for t, c in ranked))
    weekend = [i for i in incs if i["weekday"] in ("Sat", "Sun")]
    print(f"  weekday vs weekend: {n - len(weekend)} weekday · {len(weekend)} weekend")
    # peak 3-hour window
    buckets = {}
    for i in incs:
        b = (i["hour"] // 3) * 3
        buckets[b] = buckets.get(b, 0) + 1
    peak_b, peak_c = max(buckets.items(), key=lambda kv: kv[1])
    print(f"  peak window: {peak_b:02d}:00–{peak_b+3:02d}:00 ({peak_c} incidents)")
    sleep = [i for i in incs if i.get("impact") and
             any(w in i["impact"].lower() for w in ("woke", "wake", "sleep", "baby", "asleep"))]
    print(f"  impact: sleep disruption reported in {len(sleep)} incidents "
          f"({len(sleep)/n*100:.0f}%)" if sleep else "  impact: no sleep-disruption keywords logged")


def cmd_score(a):
    incs = window(load(a.file), a.days)
    if not incs:
        print("(no incidents logged — score undefined)")
        return
    n = len(incs)
    span_days = a.days or max(1, (dt.datetime.now() -
                        dt.datetime.strptime(incs[0]["start"], "%Y-%m-%d %H:%M")).days + 1)
    freq = min(1.0, n / span_days / 1.0)          # 1+/day saturates
    night_share = sum(1 for i in incs if in_night_hours(i["hour"], a.night_start, a.night_end)) / n
    dur = min(1.0, (sum(i["duration_min"] for i in incs) / n) / 90.0)
    sleep = sum(1 for i in incs if any(w in (i.get("impact") or "").lower()
               for w in ("woke", "wake", "sleep", "baby", "asleep"))) / n
    score = round(100 * (0.30 * freq + 0.30 * night_share + 0.20 * dur + 0.20 * sleep))
    band = ("LOW" if score < 25 else "MODERATE" if score < 50 else
            "HIGH" if score < 75 else "SEVERE")
    why = []
    if freq >= 0.5: why.append("frequent")
    if night_share >= 0.5: why.append("mostly night")
    if dur >= 0.5: why.append("long episodes")
    if sleep >= 0.3: why.append("sleep impact")
    print(f"severity score: {score}/100 — {band}"
          + (f" ({', '.join(why)})" if why else ""))
    print(f"  components: frequency {freq:.2f} · night-share {night_share:.2f} · "
          f"duration {dur:.2f} · sleep-impact {sleep:.2f}")


def cmd_histogram(a):
    incs = window(load(a.file), a.days)
    if not incs:
        print("(no incidents logged)")
        return
    print("Time of day (each █ ≈ 1 incident):")
    for h in range(24):
        c = sum(1 for i in incs if i["hour"] == h)
        if c:
            marker = "⚠" if in_night_hours(h, a.night_start, a.night_end) else " "
            print(f"  {h:02d}:00 {marker} {'█' * c} {c}")
    print("\nBy weekday:")
    for wd in ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"):
        c = sum(1 for i in incs if i["weekday"] == wd)
        if c:
            print(f"  {wd} {'█' * c} {c}")


def cmd_list(a):
    incs = load(a.file)["incidents"]
    for i in incs[-a.limit:]:
        note = f"  — {i['note']}" if i.get("note") else ""
        imp = f"  [{i['impact']}]" if i.get("impact") else ""
        print(f"{i['start']} {i['type']:<12} {i['duration_min']:>4}min {i['loudness']}{imp}{note}")
    print(f"({len(incs)} incidents total)")


def cmd_export(a):
    incs = load(a.file)["incidents"]
    if not incs:
        print("(nothing to export)")
        return
    fields = ["start", "weekday", "hour", "duration_min", "type", "loudness",
              "impact", "neighbor", "note"]
    with open(a.csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i in incs:
            w.writerow({k: i.get(k, "") for k in fields})
    print(f"exported {len(incs)} incidents → {a.csv}")


LETTER_TEMPLATES = {
    "landlord": """{date}

{recipient}
RE: Chronic noise disturbance — {address}

Dear {recipient_name},

I'm writing to formally report a recurring noise problem at {address} that is
affecting my living conditions and, I believe, my right to quiet enjoyment of
the unit.

I have kept a detailed log. In the last {days} days I recorded {n} incidents
({per_week}/week, {hours} hours total). {night_line}The most common source is
{top_type} noise{neighbor_line}. The disturbance peaks between {peak}.

This is a documented, ongoing pattern rather than an occasional annoyance, and
it is affecting sleep and daily life.

I ask that you:
  1. Address this with the resident(s) responsible, citing the lease's
     noise/nuisance clause;
  2. Confirm in writing what steps were taken;
  3. Advise what escalation path is available if the pattern continues.

I'd prefer to resolve this informally and neighborly. My log is available on
request. Thank you for your attention.

Sincerely,
{your_name}
{address}
{contact_line}""",
    "hoa": """{date}

{recipient}
RE: Noise complaint — {address}

Dear Board / Management,

I'm writing to report a recurring noise issue at or originating near {address},
documented in the attached log: {n} incidents in {days} days ({per_week}/week),
{night_share}% during quiet hours ({nstart}:00–{nend}:00), most commonly
{top_type}. The pattern peaks around {peak}.

I request that the Board treat this as a nuisance matter under the community
rules and quiet-hours policy, notify the responsible party, and confirm the
outcome to me in writing. My full log (dates, times, durations, notes) is
available on request.

Respectfully,
{your_name}
{address}
{contact_line}""",
    "city": """{date}

Noise Complaint — {address}
Source of noise: {source}

To the Noise Enforcement Office:

I'm writing to report a recurring noise problem affecting my residence at
{address}. Over the last {days} days I documented {n} incidents ({per_week}/week,
{hours} hours total). {night_line}The primary source is {top_type}. The pattern
peaks around {peak}.

I have kept contemporaneous records — dates, start times, durations, character
of the noise, and impact — and can provide the full log. I request an
inspection or enforcement action as appropriate under the municipal noise
ordinance.

Sincerely,
{your_name}
{address}
{contact_line}
""",
}


def cmd_letter(a):
    db = load(a.file)
    incs = window(db, a.days)
    if len(incs) < 3:
        sys.exit("ERROR: letter needs at least 3 logged incidents to show a pattern "
                 f"(currently {len(incs)}). Keep logging.")
    n = len(incs)
    days = a.days or max(1, (dt.datetime.now() -
                 dt.datetime.strptime(incs[0]["start"], "%Y-%m-%d %H:%M")).days)
    per_week = n / days * 7
    hours = sum(i["duration_min"] for i in incs) / 60
    night = sum(1 for i in incs if in_night_hours(i["hour"], a.night_start, a.night_end))
    by_type = {}
    for i in incs:
        by_type[i["type"]] = by_type.get(i["type"], 0) + 1
    top_type, top_count = max(by_type.items(), key=lambda kv: kv[1])
    buckets = {}
    for i in incs:
        b = (i["hour"] // 3) * 3
        buckets[b] = buckets.get(b, 0) + 1
    peak_b, _ = max(buckets.items(), key=lambda kv: kv[1])
    peak = f"{peak_b:02d}:00 and {peak_b+3:02d}:00"
    neighbors = sorted({i["neighbor"] for i in incs if i.get("neighbor")})
    ctx = {
        "date": dt.date.today().strftime("%B %d, %Y"),
        "recipient": a.recipient or "[Recipient / office address]",
        "recipient_name": (a.recipient.split(",")[0] if a.recipient else ""),
        "address": a.address or "[your address]",
        "your_name": a.your_name or "[your name]",
        "contact_line": (f"Phone: {a.phone}" if a.phone else "[phone]"),
        "phone_line": (f"Phone: {a.phone}" if a.phone else "[phone]"),
        "days": days, "n": n, "per_week": f"{per_week:.1f}", "hours": f"{hours:.1f}",
        "night_line": (f"{night} of {n} ({night/n*100:.0f}%) occurred during typical "
                       f"quiet hours ({a.night_start:02d}:00–{a.night_end:02d}:00). "
                       if night else ""),
        "night_share": f"{night/n*100:.0f}",
        "nstart": f"{a.night_start:02d}", "nend": f"{a.night_end:02d}",
        "top_type": top_type,
        "neighbor_line": (f", associated with {', '.join(neighbors)}" if neighbors else ""),
        "peak": peak, "source": a.source or "[describe the source]",
    }
    body = LETTER_TEMPLATES[a.to].format(**ctx)
    print(body)
    out = os.path.join(os.path.dirname(a.file) or ".", f"noise-complaint-{a.to}.txt")
    with open(out, "w") as f:
        f.write(body)
    print(f"\n[saved to {out} — review and edit before sending]", file=sys.stderr)


# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", default=DEFAULT_FILE)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_window_args(sp):
        sp.add_argument("--days", type=int)
        sp.add_argument("--night-start", type=int, default=DEFAULT_NIGHT_START)
        sp.add_argument("--night-end", type=int, default=DEFAULT_NIGHT_END)

    sp = sub.add_parser("log", help="log an incident")
    sp.add_argument("--type", required=True, choices=TYPES)
    sp.add_argument("--duration", type=int, required=True, help="minutes")
    sp.add_argument("--loudness", required=True, choices=list(LOUDNESS_BANDS))
    sp.add_argument("--start", help="YYYY-MM-DD HH:MM (default now)")
    sp.add_argument("--impact")
    sp.add_argument("--neighbor", help="e.g. 'upstairs 4B'")
    sp.add_argument("--note")
    sp.add_argument("--night-start", type=int, default=DEFAULT_NIGHT_START)
    sp.add_argument("--night-end", type=int, default=DEFAULT_NIGHT_END)
    sp.set_defaults(func=cmd_log)

    for name, fn, help_ in (("stats", cmd_stats, "pattern summary"),
                            ("score", cmd_score, "severity score"),
                            ("histogram", cmd_histogram, "time-of-day/weekday charts")):
        sp = sub.add_parser(name, help=help_)
        add_window_args(sp)
        sp.set_defaults(func=fn)

    sp = sub.add_parser("list", help="recent incidents")
    sp.add_argument("--limit", type=int, default=10)
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("export", help="CSV export")
    sp.add_argument("--csv", default="noise-log.csv")
    sp.set_defaults(func=cmd_export)

    sp = sub.add_parser("letter", help="generate complaint letter (landlord|hoa|city)")
    sp.add_argument("--to", required=True, choices=["landlord", "hoa", "city"])
    sp.add_argument("--recipient")
    sp.add_argument("--your-name")
    sp.add_argument("--address")
    sp.add_argument("--phone")
    sp.add_argument("--source", help="for city: where the noise comes from")
    sp.add_argument("--days", type=int, default=30)
    sp.add_argument("--night-start", type=int, default=DEFAULT_NIGHT_START)
    sp.add_argument("--night-end", type=int, default=DEFAULT_NIGHT_END)
    sp.set_defaults(func=cmd_letter)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
