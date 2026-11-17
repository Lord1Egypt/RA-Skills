#!/usr/bin/env python3
"""trigger_analysis.py — lift analysis over a trigger journal.

Reads JSONL entries from trigger_log.py (or same schema), computes per-factor
lift vs baseline, time-of-day hotspots, preceding-action chains, assembles a
habit-loop narrative, and prints reengineered if-then plans.

Usage: trigger_analysis.py journal.jsonl [--replacement "10 squats"]
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict

TIME_BINS = [
    ("morning (06-12)", lambda h: 6 <= h < 12),
    ("afternoon (12-18)", lambda h: 12 <= h < 18),
    ("evening (18-23)", lambda h: 18 <= h < 23),
    ("night (23-06)", lambda h: h >= 23 or h < 6),
]

URGE_MARKERS = {"bored": "boredom", "tv": "boredom", "wait": "boredom",
                "scroll": "boredom", "nothing": "boredom",
                "deadline": "stress", "stress": "stress", "work": "stress",
                "call": "stress", "meeting": "stress", "conflict": "stress",
                "tired": "fatigue", "sleep": "fatigue"}

MIN_EVENTS = 8
MIN_BASELINES = 5
LOW_CONF_EVENT_CELLS = 3
LOW_CONF_BASE_CELLS = 2


def load(path):
    events, baselines = [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("type") == "baseline":
                baselines.append(row)
            else:
                events.append(row)
    return events, baselines


def hour_of(row):
    try:
        return int(row["ts"][11:13])
    except (KeyError, ValueError, IndexError):
        return None


def bin_of(h):
    for name, test in TIME_BINS:
        if h is not None and test(h):
            return name
    return None


def norm_action(text):
    t = (text or "").lower()
    for key in URGE_MARKERS:
        if key in t:
            return key
    return t.strip() or "unknown"


def lift_table(events, baselines, key):
    """Case-control lift per value of journal field `key`.

    Baseline entries are sampled non-event moments, so:
      P(behavior|factor)     = k_ev / (k_ev + k_base)
      P(behavior|no factor)  = (n_ev-k_ev) / (n_ev-k_ev + n_base-k_base)
      lift = ratio of the two.
    """
    ev_vals = Counter(r.get(key, "?") for r in events)
    base_vals = Counter(r.get(key, "?") for r in baselines)
    n_ev, n_base = len(events), len(baselines)
    if n_ev == 0 or n_base == 0:
        return []
    out = []
    all_vals = set(ev_vals) | set(base_vals)
    for v in all_vals:
        k_ev, k_base = ev_vals.get(v, 0), base_vals.get(v, 0)
        if k_ev == 0:
            continue
        with_v = k_ev + k_base
        p_pos = k_ev / with_v
        ev_wo, base_wo = n_ev - k_ev, n_base - k_base
        wo = ev_wo + base_wo
        p_neg = (ev_wo / wo) if wo > 0 else 1.0
        lift = p_pos / max(p_neg, 1e-9)
        low_conf = k_ev < LOW_CONF_EVENT_CELLS or k_base < LOW_CONF_BASE_CELLS
        out.append({"value": v, "events": k_ev, "baselines": k_base,
                    "lift": min(lift, 99.0), "low_conf": low_conf,
                    "factor": key})
    return sorted(out, key=lambda r: -r["lift"])


def time_hotspots(events, baselines):
    """Same case-control lift, with time bin as the factor."""
    ev_bins = Counter(b for b in (bin_of(hour_of(r)) for r in events) if b)
    base_bins = Counter(b for b in (bin_of(hour_of(r)) for r in baselines) if b)
    n_ev, n_base = len(events), len(baselines)
    out = []
    for name, _ in TIME_BINS:
        k_ev, k_base = ev_bins.get(name, 0), base_bins.get(name, 0)
        if k_ev == 0:
            continue
        with_v = k_ev + k_base
        p_pos = k_ev / with_v
        ev_wo, base_wo = n_ev - k_ev, n_base - k_base
        wo = ev_wo + base_wo
        p_neg = (ev_wo / wo) if wo > 0 else 1.0
        out.append({"bin": name, "events": k_ev, "baselines": k_base,
                    "lift": min(p_pos / max(p_neg, 1e-9), 99.0)})
    return sorted(out, key=lambda r: -r["lift"])


def action_chains(events):
    acts = Counter(norm_action(r.get("prev_action", "")) for r in events)
    total = len(events)
    return [(a, c, c / total) for a, c in acts.most_common() if c >= 2]


def habit_loop(narrative_triggers, top_action, mean_urge, mean_mood,
               social_events, n_events):
    cues = " + ".join(t["value"] for t in narrative_triggers[:3])
    routine = "the tracked behavior"
    if social_events / max(n_events, 1) >= 0.6:
        reward = "connection/social reward"
    elif mean_mood <= 2.5 and mean_urge >= 3.5:
        reward = "mood repair (escape/relief)"
    elif top_action in ("bored", "tv", "scroll", "wait", "nothing"):
        reward = "stimulation (relief from boredom)"
    elif top_action in ("deadline", "stress", "work", "call", "meeting"):
        reward = "tension release"
    else:
        reward = "transition ritual (marking a switch between modes)"
    return f"CUE: {cues}\nROUTINE: {routine}\nREWARD (hypothesis): {reward}"


def fmt_lift(x):
    return f">{x:.0f}" if x >= 10 else f"{x:.2f}"


CUE_PHRASE = {
    "location": lambda v: f"in location '{v}'",
    "company": lambda v: f"{v}" if v == "alone" else f"with {v}",
    "device": lambda v: f"{v} in hand" if v != "none" else "device-free",
    "emotional_state": lambda v: f"mood at {v}/5",
}

DISRUPT = {
    "location": "redesign that spot: remove the routine's tools from arm's reach there",
    "company": "change the social setup for that moment (join someone, call, or go public)",
    "device": f"put physical distance between you and the device in that window",
    "emotional_state": "build a mood-repair menu that isn't the routine (walk, music, call)",
}


def if_then_plans(triggers, hotspot, replacement):
    repl = replacement or "a 2-minute substitute you choose NOW (write it down)"
    plans = []
    for t in triggers[:2]:
        cue = CUE_PHRASE.get(t.get("factor", ""), lambda v: str(v))(t["value"])
        plans.append(
            f"IF urge hits {cue} (lift {fmt_lift(t['lift'])}), "
            f"THEN do: {repl}")
    if hotspot:
        plans.append(
            f"IF it is {hotspot['bin']} (lift {fmt_lift(hotspot['lift'])}), "
            f"THEN pre-empt: place the substitute in reach BEFORE this window")
    return plans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("journal")
    ap.add_argument("--replacement", default=None,
                    help="substitute routine for if-then plans")
    ap.add_argument("--all", action="store_true",
                    help="show low-confidence rows too")
    args = ap.parse_args()

    events, baselines = load(args.journal)
    print("=" * 66)
    print(f"TRIGGER ANALYSIS — {len(events)} events, {len(baselines)} baselines")
    print("=" * 66)
    if len(events) < MIN_EVENTS:
        print(f"[!] need >= {MIN_EVENTS} events (have {len(events)}). "
              f"Keep journaling.")
        return 1
    if len(baselines) < MIN_BASELINES:
        print(f"[!] need >= {MIN_BASELINES} baseline entries (have "
              f"{len(baselines)}). Without them lift is meaningless.")
        return 1

    tables = {}
    for key, label in (("location", "LOCATION"), ("company", "COMPANY"),
                       ("device", "DEVICE"),
                       ("emotional_state", "EMOTIONAL STATE (1-5)")):
        rows = lift_table(events, baselines, key)
        tables[key] = rows
        print(f"\n--- {label} ---")
        for r in rows[:6]:
            flag = " LOW-CONF" if r["low_conf"] else ""
            print(f"  lift {r['lift']:>5.2f}  {str(r['value']):<12} "
                  f"events {r['events']:>2}  baselines {r['baselines']:>2}{flag}")
        if not args.all and len(rows) > 6:
            print(f"  (+{len(rows)-6} more, use --all)")

    hotspots = time_hotspots(events, baselines)
    print("\n--- TIME OF DAY ---")
    for h in hotspots:
        print(f"  lift {h['lift']:>5.2f}  {h['bin']:<18} events {h['events']:>2}"
              f"  baselines {h['baselines']:>2}")

    chains = action_chains(events)
    print("\n--- PRECEDING ACTION (last 30 min) ---")
    for a, c, p in chains[:6]:
        print(f"  {p*100:>4.0f}%  {a}")

    # confound check: values that co-occur in every event
    confounds = []
    for key in ("location", "company", "device"):
        for r in tables[key]:
            if r["events"] == len(events) and r["baselines"] == 0:
                confounds.append(f"{key}={r['value']}")
    if len(confounds) >= 2:
        print("\n[!] CONFOUNDED: " + " and ".join(confounds) +
              " always appear together — can't separate with this data. "
              "Next week: vary one deliberately.")

    ranked = [r for t in tables.values() for r in t if not r["low_conf"]]
    ranked.sort(key=lambda r: -r["lift"])
    top = [r for r in ranked if r["lift"] >= 1.5][:3]
    mean_urge = sum(e.get("urge", 3) for e in events) / len(events)
    mean_mood = sum(e.get("emotional_state", 3) for e in events) / len(events)
    social = sum(1 for e in events if e.get("company") not in
                 ("alone", "?", "other"))
    top_action = chains[0][0] if chains else "unknown"

    print("\n" + "=" * 66)
    print("HABIT LOOP (hypothesis)")
    print("=" * 66)
    print(habit_loop(top, top_action, mean_urge, mean_mood, social,
                     len(events)))

    print("\n" + "=" * 66)
    print("REENGINEERED IF-THEN PLANS (pick 1-2, not all)")
    print("=" * 66)
    for p in if_then_plans(top, hotspots[0] if hotspots else None,
                           args.replacement):
        print(" * " + p)
    print("\nCue-disruption moves for each top trigger:")
    for t in top[:2]:
        move = DISRUPT.get(t.get("factor", ""),
                           "make it 20s harder to reach from the usual spot")
        print(f"  - {t['value']}: {move}")
    print("\nWeek 2: journal again, re-run, compare lift — target: top cue "
          "lift toward 1.0 (decoupled).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
