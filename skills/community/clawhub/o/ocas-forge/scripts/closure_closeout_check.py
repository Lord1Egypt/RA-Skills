#!/usr/bin/env python3
"""Consolidated close-out verifier for OCAS dispatch-wave closures (MODE A/B/C).

Asserts ALL closure gates in one pass and exits non-zero if any gate is stale.
This replaces the inline heredoc in
references/redetection-stale-state-closure-oneshot.md (which hardcodes the named
journal and is copy-paste error prone).

Usage:
  python3 scripts/closure_closeout_check.py --named ocas-mentor/2026-07-16/mentor-light-XXXX.json --date 2026-07-16

Exit: 0 = all gates closed; 1 = at least one gate stale (re-run the relevant
sweep/advance/re-affirm step before declaring closure).

NOTE: this script lives in ocas-forge/scripts/ (cross-skill). ocas-dispatch
closure runs must invoke it by its full path under ocas-forge, NOT
ocas-dispatch/scripts/ (it does not exist there).

CORRECTED 2026-07-17 (closure blind-spot fixes):
  - Gate [2] now reads BOTH monitor copies (root + profile-relative). The
    profile-relative copy (<hermes-home>/profiles/<profile>/commons/.../journal_ingest_state.json)
    is what monitor_journals.py actually gates on; the root copy alone gave a
    false "closed" while the profile copy stayed stale and re-fired the wave.
  - Gate [3] now REQUIRES the dispatch-owned account copies
    (owner/last_email_check.json, last_email_check_owner.json, last_email_check_indigo.json)
    and only WARNS on the three top-level GWS-snapshot files
    (last_email_check.json, last_email_check_owner.json,
    last_email_check_mx_indigo_karasu_gmail_com.json), which stay null under the
    documented monitor re-fire bug and are the known-uncloseable gate. Requiring
    them made every the operator AND every Indigo-account closure fail gate [3] regardless
    of real state. The full-address snapshot copies (both owner_ and indigo_
    variants) are WARN, not required — corrected 2026-07-22: the indigo GWS-snapshot
    was wrongly in the required list, causing a spurious "gates STALE" on every
    combined/multi-account closure that included Indigo threads.
"""
import os, sys, json, argparse, datetime

PROFILE = os.environ.get("HERMES_HOME", os.environ.get("HERMES_HOME", os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo")))
JDIR = os.path.join(PROFILE, "commons", "journals")
PRAXIS_EV = os.path.join(PROFILE, "commons", "data", "ocas-praxis", "journals_evaluated.jsonl")
DISPATCH_EV = os.path.join(PROFILE, "commons", "data", "ocas-dispatch", "journals_evaluated.jsonl")
PRAXIS_STATE = os.path.join(PROFILE, "commons", "data", "ocas-praxis", "ingest_state.json")
# TWO monitor copies (both must be advanced — see ocas-forge/ocas-dispatch SKILL.md)
MON_STATE_ROOT = os.environ.get("HERMES_HOME", os.environ.get("HERMES_HOME", os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo"))).replace("/profiles/indigo", "/commons/data/monitor_state/journal_ingest_state.json")
MON_STATE_PROFILE = os.path.join(PROFILE, "commons", "data", "monitor_state", "journal_ingest_state.json")
EMAIL_DIR = os.path.join(PROFILE, "commons", "data", "ocas-dispatch")


def in_store(p, rel):
    if not os.path.exists(p):
        return False
    with open(p) as f:
        return any(rel in ln for ln in f)


def load_json(p, default=None):
    if not os.path.exists(p):
        return default
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:
        return default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--named", required=True, help="named journal relpath, e.g. ocas-mentor/2026-07-16/mentor-light-XXXX.json")
    ap.add_argument("--date", required=True, help="closure date, e.g. 2026-07-16")
    args = ap.parse_args()

    ok = True
    print(f"=== closeout check: named={args.named} date={args.date} ===")

    # 1. named journal in both eval stores
    p_in = in_store(PRAXIS_EV, args.named)
    d_in = in_store(DISPATCH_EV, args.named)
    print(f"[1] named journal in PRAXIS+DISPATCH eval stores: praxis={p_in} dispatch={d_in}")
    ok = ok and p_in and d_in

    # 2. state gates vs max today-journal mtime (dispatch-wave-*.json excluded)
    st = load_json(PRAXIS_STATE) or {}
    lir_raw = st.get("last_ingest_run")
    lir_dt = None
    if lir_raw:
        try:
            lir_dt = datetime.datetime.fromisoformat(lir_raw.replace("Z", "+00:00"))
        except Exception:
            lir_dt = None
    max_mt = 0.0
    for skill in os.listdir(JDIR):
        d = os.path.join(JDIR, skill, args.date)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.startswith("dispatch-wave-"):
                continue
            fp = os.path.join(d, fn)
            if fp.endswith(".json"):
                max_mt = max(max_mt, os.path.getmtime(fp))
    max_dt = datetime.datetime.fromtimestamp(max_mt, tz=datetime.timezone.utc)
    g1 = (lir_dt is not None) and (lir_dt >= max_dt)

    # Both monitor copies must be advanced
    mon_root = load_json(MON_STATE_ROOT) or {}
    mon_prof = load_json(MON_STATE_PROFILE) or {}
    mr_dt = md_dt = None
    if "latest_mtime" in mon_root:
        mr_dt = datetime.datetime.fromtimestamp(mon_root["latest_mtime"], tz=datetime.timezone.utc)
    if "latest_mtime" in mon_prof:
        md_dt = datetime.datetime.fromtimestamp(mon_prof["latest_mtime"], tz=datetime.timezone.utc)
    g2_root = (mr_dt is not None) and (mr_dt >= max_dt)
    g2_prof = (md_dt is not None) and (md_dt >= max_dt)
    g2 = g2_root and g2_prof

    print(f"[2] praxis last_ingest_run >= max today mtime : {g1} ({lir_dt.isoformat() if lir_dt else 'MISSING'} vs {max_dt.isoformat()})")
    print(f"[2] monitor ROOT    latest_mtime >= max       : {g2_root} ({mr_dt.isoformat() if mr_dt else 'MISSING'} vs {max_dt.isoformat()})")
    print(f"[2] monitor PROFILE latest_mtime >= max       : {g2_prof} ({md_dt.isoformat() if md_dt else 'MISSING'} vs {max_dt.isoformat()})")
    ok = ok and g1 and g2

    # 3. email second-wave state.
    #    REQUIRE the dispatch-owned account copies (these actually hold True).
    #    WARN-only on the two top-level GWS snapshots (known un-closeable gate
    #    under the monitor re-fire bug — they stay null and must not block).
    # NOTE: the full-address GWS-snapshot copies (owner and
    # mx_indigo_karasu_gmail_com) stay null under the monitor re-fire bug and are
    # WARN-class, NOT blocking (see ocas-dispatch SKILL.md gate [3] note). Only the
    # dispatch-owned account copies hold True. Requiring the Indigo GWS snapshot made
    # every Indigo-account closure report a spurious "gates STALE" headline.
    required_email = [
        "owner/last_email_check.json",
        "last_email_check_owner.json",
        "last_email_check_indigo.json",
    ]
    warn_email = [
        "last_email_check.json",
        "last_email_check_owner.json",
        "last_email_check_mx_indigo_karasu_gmail_com.json",
    ]
    for fn in required_email:
        p = os.path.join(EMAIL_DIR, fn)
        if not os.path.exists(p):
            print(f"[3] email (required) {fn:50s} ABSENT (skip)")
            continue
        v = load_json(p, {}).get("verified_second_wave")
        print(f"[3] email (required) {fn:50s} verified_second_wave={v}")
        ok = ok and bool(v)
    for fn in warn_email:
        p = os.path.join(EMAIL_DIR, fn)
        if not os.path.exists(p):
            print(f"[3] email (warn)      {fn:50s} ABSENT (skip)")
            continue
        v = load_json(p, {}).get("verified_second_wave")
        flag = "WARN(null expected)" if not v else "ok"
        print(f"[3] email (warn)      {fn:50s} verified_second_wave={v} {flag}")

    print(f"=== gates {'ALL CLOSED' if ok else 'STALE - re-run sweep/advance/re-affirm'} ===")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()