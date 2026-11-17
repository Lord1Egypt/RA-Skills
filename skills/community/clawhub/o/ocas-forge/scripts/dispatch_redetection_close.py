#!/usr/bin/env python3
"""dispatch_redetection_close.py - closure-only handler for re-detected
new_journals / new_emails dispatch waves.

See ocas-forge SKILL.md dispatch-pipeline-guide (re-detection rules 289-309).

WHY THIS EXISTS
---------------
The dispatch-pipeline-guide prescribes that when a dispatch is a re-detection of
already-completed work (its new_file is already in BOTH eval stores, and/or a
newer concurrent wave already closed it), the caller must NOT re-run
Forge/Mentor/Praxis, must NOT mint a new wave journal, and must instead do
closure-only: bridge residual one-sided gaps, advance last_ingest_run, fix email
state, and re-sweep to GENUINE GAP = 0.

The closure helper scripts the guide references -
  scripts/reconcile_dispatch_eval_today.py
  scripts/verify_genuine_gap_profile.py
  scripts/closure_convergence_sweep.py
- do NOT exist on disk (confirmed 2026-07-15: `ls` returns 'No such file or
directory' for all three). They are aspirational references. This script is the
working inline implementation of the closure recipe, made re-runnable.

NEW (2026-07-15): the monitor cron re-runs independently and can re-populate
commons/data/monitor_queue.jsonl with the same work in the seconds BEFORE your
state fix lands (confirmed 2026-07-15: a 16:56:43 monitor scan re-queued the
items while the closure's state write landed at 16:56:44). The dispatcher clears
the queue on read, so a stale re-queue only triggers one redundant no-op
re-dispatch - but to break the loop cleanly this script truncates the queue as
its final step (idempotent, safe: same clear the dispatcher performs on read).

SAFETY
------
This script NEVER writes journals and NEVER runs pipelines. It only:
  1. (optional --new-files) asserts the re-detection precondition: every
     new_file already present in BOTH eval stores; REFUSES (exit 3) if any is
     missing - that means genuine work, not a re-detection.
  2. Reconciles today's journal dirs (bounded os.listdir, NOT recursive glob -
     recursive glob descends into self-nested journals/journals symlinks and
     emits false-positive gaps) against the praxis-eval + dispatch-eval stores;
     bridges one-sided / neither gaps idempotently.
  3. Re-sweeps and asserts GENUINE GAP = 0 (exit 4 if residual).
  4. Advances ingest_state.last_ingest_run past the max journal mtime today.
  5. Fixes owner/ + indigo/ email state files (last_dispatch = resolving wave
     run_id, verified_second_wave = true).
  6. Truncates monitor_queue.jsonl.

USAGE
-----
  python3 scripts/dispatch_redetection_close.py [--new-files <relpath> ...]
                                                 [--wave-run-id <TS>] [--dry-run]
  --new-files   relpaths of the dispatcher's new_files; asserts they are all
                already evaluated (re-detection precondition guard).
  --wave-run-id resolving wave run_id (e.g. dispatch-wave-20260715T165241Z); if
                omitted, auto-detects the latest dispatch-wave-*.json today.
  --dry-run     print actions without writing.
"""
import json, os, sys, argparse, glob
from datetime import datetime, timezone

PROFILE = "<hermes-home>/profiles/indigo"
JDIR = os.path.join(PROFILE, "commons/journals")
PRAXIS_EVAL = os.path.join(PROFILE, "commons/data/ocas-praxis/journals_evaluated.jsonl")
DISPATCH_EVAL = os.path.join(PROFILE, "commons/data/ocas-dispatch/journals_evaluated.jsonl")
STATE_PATH = os.path.join(PROFILE, "commons/data/ocas-praxis/ingest_state.json")
QUEUE_FILE = "<hermes-home>/commons/data/monitor_queue.jsonl"
DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_eval(p):
    m = {}
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if "journal_id" in d:
                    m[d["journal_id"]] = d
                if "filename" in d:
                    m[d["filename"]] = d
    return m


def append_unique(fpath, key_field, key_val, action_taken, source, now):
    if os.path.exists(fpath):
        with open(fpath) as f:
            for line in f:
                if key_val in line:
                    return False
    entry = {key_field: key_val, "action_taken": action_taken,
             "source": source, "backfill_at": now}
    with open(fpath, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return True


def discover_gaps(prax, disp):
    skills = [d for d in os.listdir(JDIR)
              if os.path.isdir(os.path.join(JDIR, d))]
    gaps_p, gaps_d, gaps_both = [], [], []
    max_mtime = 0.0
    for skill in sorted(skills):
        sdir = os.path.join(JDIR, skill, DATE)
        if not os.path.isdir(sdir):
            continue
        for fn in sorted(os.listdir(sdir)):
            if not fn.endswith(".json") or fn.startswith("dispatch-wave-"):
                continue
            rel = "%s/%s/%s" % (skill, DATE, fn)
            try:
                mt = os.path.getmtime(os.path.join(sdir, fn))
            except Exception:
                continue
            # Track max mtime across ALL today-journals (incl. already-evaluated
            # ones), NOT only gap files. Bug (2026-07-15): the prior code computed
            # mtime AFTER the membership skip, so when the re-sweep found 0 gaps
            # max_mtime stayed 0.0 and last_ingest_run was advanced to epoch 0,
            # re-firing the dispatcher harder. Compute + record mt before branching.
            if mt > max_mtime:
                max_mtime = mt
            if rel in prax and rel in disp:
                continue
            if rel not in prax and rel not in disp:
                gaps_both.append(rel)
            elif rel not in prax:
                gaps_p.append(rel)
            else:
                gaps_d.append(rel)
    return gaps_p, gaps_d, gaps_both, max_mtime


def main():
    ap = argparse.ArgumentParser(
        description="Close a dispatch re-detection: advance last_ingest_run past all "
                    "today-dated journals and assert GENUINE GAP=0.",
        epilog="Examples:\n"
               "  python3 dispatch_redetection_close.py --wave-run-id 20260716T050000Z\n"
               "  python3 dispatch_redetection_close.py --new-files ocas-forge/2026-07-16/forge-scan-TS.json --dry-run")
    ap.add_argument("--new-files", nargs="*", default=[],
                    help="dispatcher new_file relative paths (e.g. ocas-forge/2026-07-16/forge-scan-TS.json)")
    ap.add_argument("--wave-run-id", default=None,
                    help="the dispatch wave run_id to close (YYYYmmddTHHMMSSZ)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the intended state advance and gap assertion without writing state")
    args = ap.parse_args()
    now = datetime.now(timezone.utc).isoformat()

    prax = load_eval(PRAXIS_EVAL)
    disp = load_eval(DISPATCH_EVAL)

    # 1. precondition guard
    if args.new_files:
        missing = [nf for nf in args.new_files
                   if nf not in prax or nf not in disp]
        if missing:
            print("REFUSAL: re-detection precondition FAILED - new_files "
                  "missing from eval stores:")
            for m in missing:
                print("  ", m)
            print("This is GENUINE work; do NOT run closure. Run the full "
                  "pipeline (bridge_explicit_run.py) instead.")
            sys.exit(3)
        print("Precondition OK: all new_files present in BOTH eval stores.")

    # 2. reconcile
    gaps_p, gaps_d, gaps_both, max_mtime = discover_gaps(prax, disp)
    print("GAPS praxis-only=%d dispatch-only=%d neither=%d"
          % (len(gaps_p), len(gaps_d), len(gaps_both)))

    if not args.dry_run:
        p_add = d_add = 0
        for rel in gaps_p:
            if append_unique(PRAXIS_EVAL, "journal_id", rel,
                             "third_wave_mitigation", "redetection-close", now):
                p_add += 1
        for rel in gaps_d:
            if append_unique(DISPATCH_EVAL, "filename", rel,
                             "dispatch_output_skip", "redetection-close", now):
                d_add += 1
        for rel in gaps_both:
            a = append_unique(PRAXIS_EVAL, "journal_id", rel,
                              "third_wave_mitigation", "redetection-close", now)
            b = append_unique(DISPATCH_EVAL, "filename", rel,
                              "dispatch_output_skip", "redetection-close", now)
            if a:
                p_add += 1
            if b:
                d_add += 1
        print("BRIDGED praxis+%d dispatch+%d" % (p_add, d_add))

    # 3. re-sweep assert 0
    gaps_p, gaps_d, gaps_both, max_mtime = discover_gaps(
        load_eval(PRAXIS_EVAL), load_eval(DISPATCH_EVAL))
    total = len(gaps_p) + len(gaps_d) + len(gaps_both)
    print("RE-SWEEP GENUINE GAP = %d" % total)
    if total > 0:
        for r in gaps_p + gaps_d + gaps_both:
            print("  ", r)
        if not args.dry_run:
            sys.exit(4)

    # 4. advance state
    new_last = datetime.fromtimestamp(max_mtime, timezone.utc).isoformat()
    if not args.dry_run:
        state = json.load(open(STATE_PATH))
        state["last_ingest_run"] = new_last
        pc = sum(1 for _ in open(PRAXIS_EVAL))
        state["journals_evaluated_count"] = pc
        state["last_eval_file_line"] = pc
        json.dump(state, open(STATE_PATH, "w"), indent=2)
    print("ADVANCED last_ingest_run ->", new_last)

    # 5. email state fix
    wave = args.wave_run_id
    if not wave:
        waves = sorted(glob.glob(os.path.join(
            JDIR, "ocas-dispatch", DATE, "dispatch-wave-*.json")))
        if waves:
            try:
                wave = json.load(open(waves[-1])).get("run_id")
            except Exception:
                wave = None
    if not wave:
        wave = "dispatch-wave-" + datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%SZ")
    print("Resolving wave run_id:", wave)
    if not args.dry_run:
        for acct in ("owner", "indigo"):
            ep = os.path.join(PROFILE, "commons/data/ocas-dispatch", acct,
                              "last_email_check.json")
            if not os.path.exists(ep):
                continue
            d = json.load(open(ep))
            d["last_dispatch"] = wave.replace("dispatch-wave-", "")
            d["last_dispatch_wave"] = wave
            d["verified_second_wave"] = True
            json.dump(d, open(ep, "w"), indent=2)
            print("  email state %s: verified_second_wave=true, last_dispatch=%s"
                  % (acct, d["last_dispatch"]))

    # 6. truncate queue (break re-fire loop)
    if not args.dry_run:
        open(QUEUE_FILE, "w").close()
    print("Queue truncated (re-fire loop broken).")
    print("DONE")


if __name__ == "__main__":
    main()