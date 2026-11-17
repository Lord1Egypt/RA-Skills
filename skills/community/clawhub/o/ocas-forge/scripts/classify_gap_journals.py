#!/usr/bin/env python3
"""classify_gap_journals.py — classify dispatch-closure genuine gaps as
noop self-reference heartbeats vs genuine work, BEFORE bridging.

Companion to verify_genuine_gap_profile.py (which finds gaps) and
bridge_eval_inline.py (which bridges them). This script walks the same
bounded per-skill/date tree, finds journals missing from either eval
store, loads each, and prints the noop-self-reference discriminator
fields + a VERDICT. It does NOT bridge — bridging is an explicit
separate step so the agent can eyeball the fields first.

Why this exists: in a Mode-C no-op re-detection closure, the
dispatcher's `new_files` list is NOT the complete gap set. The
genuine-gap SCAN is authoritative — it frequently finds MORE gaps
than the dispatcher named (e.g. 2026-07-23: dispatcher named 1
mentor-light journal, the scan found 6 post-dispatch heartbeats
all missing from eval stores). Bridge per the SCAN, not the named list.

Usage:
  python3 scripts/classify_gap_journals.py --date 2026-07-23
"""
import os, sys, json, argparse

PROFILE = os.path.expanduser("~/.hermes/profiles/indigo")
JDIR = os.path.join(PROFILE, "commons", "journals")
PRAXIS_EV = os.path.join(PROFILE, "commons", "data", "ocas-praxis", "journals_evaluated.jsonl")
DISPATCH_EV = os.path.join(PROFILE, "commons", "data", "ocas-dispatch", "journals_evaluated.jsonl")

def in_store(fpath, rel):
    if not os.path.exists(fpath):
        return False
    with open(fpath) as f:
        for line in f:
            if rel in line:
                return True
    return False

def classify(d):
    """Return (VERDICT, reasons). VERDICT in {NOOP_SELF_REF, GENUINE}."""
    run_id = d.get("run_id", "") or ""
    hb = d.get("heartbeat_type")
    ent = d.get("entities_observed") or []
    m = d.get("metrics") or {}
    gap = m.get("gap_detected")
    out = d.get("outcome")
    is_mentor = run_id.startswith("mentor-light-")
    mentor_dom = "ocas-mentor" in ent
    gap_false = gap in (False, None)
    out_ok = out in (None, "success")
    ev = d.get("events") or m.get("events") or 0
    props = d.get("proposals") or m.get("proposals") or 0
    decs = d.get("decisions") or m.get("decisions") or 0
    no_signals = (ev == 0 and props == 0 and decs == 0)
    if is_mentor and mentor_dom and gap_false and out_ok and no_signals:
        return ("NOOP_SELF_REF",
                ["run_id=%s" % run_id, "hb=%s" % hb, "ent=%s" % ent,
                 "gap_detected=%s" % gap, "outcome=%s" % out,
                 "events/props/decs=%s/%s/%s" % (ev, props, decs)])
    return ("GENUINE",
            ["run_id=%s" % run_id, "hb=%s" % hb, "ent=%s" % ent,
             "gap_detected=%s" % gap, "outcome=%s" % out,
             "events/props/decs=%s/%s/%s" % (ev, props, decs),
             "fails noop-self-ref discriminator"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD journal dir date")
    args = ap.parse_args()
    date = args.date
    if not os.path.isdir(JDIR):
        print("JDIR missing:", JDIR)
        sys.exit(2)
    gaps = []
    for skill in os.listdir(JDIR):
        if skill == "ocas-custodian":
            continue
        d = os.path.join(JDIR, skill, date)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.startswith("dispatch-wave-"):
                continue
            fp = os.path.join(d, fn)
            if not fp.endswith(".json"):
                continue
            rel = "%s/%s/%s" % (skill, date, fn)
            in_p = in_store(PRAXIS_EV, rel)
            in_d = in_store(DISPATCH_EV, rel)
            if in_p and in_d:
                continue
            gaps.append((rel, fp))
    if not gaps:
        print("NO GAPS — nothing to classify. Closure gates already satisfied.")
        sys.exit(0)
    print("GENUINE GAPS (missing from >=1 eval store): %d\n" % len(gaps))
    n_noop = 0
    n_genuine = 0
    for rel, fp in sorted(gaps):
        try:
            d = json.load(open(fp))
        except Exception as e:
            print("  %s: UNREADABLE (%s) -> GENUINE (treat as gap)" % (rel, e))
            n_genuine += 1
            continue
        verdict, reasons = classify(d)
        if verdict == "NOOP_SELF_REF":
            n_noop += 1
        else:
            n_genuine += 1
        print("  %s" % rel)
        for r in reasons:
            print("      %s" % r)
        print("      >>> VERDICT: %s\n" % verdict)
    print("SUMMARY: %d NOOP_SELF_REF (bridge cross_skill_noop_mentor_self_reference) | %d GENUINE (run full pipeline)" % (n_noop, n_genuine))
    if n_genuine == 0 and n_noop > 0:
        print("ALL GAPS ARE NOOP SELF-REFERENCES — safe to bridge all + advance state (Mode C closure).")
    elif n_genuine > 0:
        print("GENUINE GAPS PRESENT — do NOT no-op-close; run full Forge/Mentor/Praxis pipeline for those.")

if __name__ == "__main__":
    main()
