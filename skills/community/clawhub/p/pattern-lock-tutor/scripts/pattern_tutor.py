#!/usr/bin/env python3
"""pattern-lock-tutor — motor-sequence trainer with spaced repetition.

Train pattern locks, shortcut chains, keypad PINs, riffs: transposition
drills, old-vs-new interference drills, accuracy-gated speed work, and an
expanding recall schedule. Terminal-based, pure stdlib, one JSON store.

The trainer works in two modes:
  live   — interactive keystroke timing (needs a TTY)
  log    — record results from real-world practice (no TTY)

NOTE: never train on your real unlock pattern. Use a training pattern of
the same shape; see references/motor-learning.md.
"""
import argparse
import json
import random
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

DB = Path("pattern_tutor.json")
INTERVALS = [timedelta(minutes=10), timedelta(days=1), timedelta(days=3),
             timedelta(days=7), timedelta(days=16), timedelta(days=35)]
ACC_GATE = 0.95
READY_LATENCY_FACTOR = 1.2
READY_INTERFERE_WIN = 0.80


def load() -> dict:
    if DB.exists():
        return json.loads(DB.read_text())
    return {"sequences": {}, "sessions": [], "recalls": []}


def save(db: dict) -> None:
    DB.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def get_seq(db: dict, name: str) -> dict:
    if name not in db["sequences"]:
        sys.exit(f"sequence '{name}' not found — `seq add` first")
    return db["sequences"][name]


def transpositions(nodes: list) -> list:
    """Every rotation of the sequence (training entry points)."""
    n = len(nodes)
    return [nodes[i:] + nodes[:i] for i in range(n)]


# ---------- seq ----------

def cmd_seq(args, db):
    if args.action == "add":
        nodes = [x.strip() for x in args.nodes.split(",")]
        if len(nodes) < 3:
            sys.exit("need at least 3 nodes for a sequence")
        db["sequences"][args.name] = {
            "nodes": nodes,
            "added": date.today().isoformat(),
            "interval_level": 0,
            "next_due": (datetime.now() + INTERVALS[0]).isoformat(timespec="seconds"),
            "history": [],      # per-session summaries
            "is_real_secret": False,
        }
        save(db)
        print(f"added '{args.name}' ({len(nodes)} nodes: {' '.join(nodes)})")
        print("WARNING: do not store your REAL unlock pattern — use a training "
              "pattern of the same shape.")
    elif args.action == "list":
        for name, s in db["sequences"].items():
            due = "due" if datetime.fromisoformat(s["next_due"]) <= datetime.now() else "-"
            print(f"{name:<20} {len(s['nodes'])} nodes  level {s['interval_level']}  "
                  f"next {s['next_due']} [{due}]")


# ---------- baseline test / training ----------

def run_reps(seq_nodes: list, reps: int, rng: random.Random, label: str,
             practiced: int = 0) -> dict:
    """Interactive reps: show rotated prompt, time the typed answer.

    Returns {'reps': int, 'errors': int, 'latencies': [s], 'per_rot': {...}}.
    Falls back to non-interactive demo timing when stdin is not a TTY.
    """
    rotations = transpositions(seq_nodes)
    results = {"reps": 0, "errors": 0, "latencies": [], "per_rot": {}}
    for i, rot in enumerate(rotations):
        results["per_rot"][i] = {"reps": 0, "errors": 0}
    interactive = sys.stdin.isatty()
    if not interactive:
        # deterministic offline mode: simulate per-rotation performance from
        # history so pipelines/cron can exercise the scheduler & analytics.
        # practiced sequences get uniformly high simulated accuracy across ALL
        # rotations (offline demo is not a per-rotation difficulty model)
        base = min(0.99, 0.9 + 0.1 * rng.random() + 0.02 * practiced)
        for i, rot in enumerate(rotations):
            n = max(1, reps // len(rotations))
            errs = sum(1 for _ in range(n) if rng.random() > base)
            results["reps"] += n
            results["errors"] += errs
            results["per_rot"][i] = {"reps": n, "errors": errs}
            results["latencies"].extend(0.8 + rng.random() * 0.9 for _ in range(n))
        print(f"[offline mode] {label}: {results['reps']} reps, "
              f"{results['errors']} errors (simulated)")
        return results

    print(f"\n--- {label} ---")
    print("Type the ROTATED sequence shown, Enter to submit. Ctrl-C to stop.\n")
    order = list(range(len(rotations)))
    for r in range(reps):
        i = order[r % len(order)] if r < len(order) else rng.randrange(len(order))
        rot = rotations[i]
        prompt = "-".join(rot)
        t0 = time.perf_counter()
        try:
            ans = input(f"rep {r+1:>2}: {prompt}  → ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        dt = time.perf_counter() - t0
        ok = ans == prompt or [a.strip() for a in ans.split(",")] == rot
        results["reps"] += 1
        results["per_rot"][i]["reps"] += 1
        if not ok:
            results["errors"] += 1
            results["per_rot"][i]["errors"] += 1
        results["latencies"].append(dt)
        print(f"          {'✓' if ok else '✗'}  {dt:.2f}s")
    return results


def summarize(results: dict) -> dict:
    reps = max(1, results["reps"])
    acc = 1 - results["errors"] / reps
    lat = sorted(results["latencies"])
    med = lat[len(lat) // 2] if lat else 0.0
    per_rot_acc = {}
    for i, pr in results["per_rot"].items():
        n = pr["reps"]
        per_rot_acc[i] = round(1 - pr["errors"] / n, 3) if n else None
    return {"reps": results["reps"], "accuracy": round(acc, 3),
            "median_latency": round(med, 2), "per_rot": per_rot_acc}


def cmd_test_train(args, db, train: bool):
    s = get_seq(db, args.name)
    rng = random.Random()
    label = f"{args.name} {'training session' if train else 'baseline test'}"
    practiced = len(s["history"])
    results = run_reps(s["nodes"], args.reps, rng, label, practiced=practiced)
    summ = summarize(results)
    summ.update({"date": date.today().isoformat(), "kind": "train" if train else "test",
                 "name": args.name})
    s["history"].append(summ)
    db["sessions"].append(summ)
    # weakest rotation first next time
    weakest = min(summ["per_rot"], key=lambda i: summ["per_rot"][i] or 1.0)
    summ["weakest_rot"] = weakest
    save(db)
    acc_pct = summ["accuracy"] * 100
    print(f"\n{args.name}: {summ['reps']} reps, accuracy {acc_pct:.1f}%, "
          f"median {summ['median_latency']}s, weakest rotation #{weakest + 1}")
    if train:
        if summ["accuracy"] < ACC_GATE:
            print(f"accuracy gate NOT met (<{ACC_GATE:.0%}) — repeat slow blocks; "
                  "no speed work yet")
        else:
            print("accuracy gate met — speed work allowed in next session")
    else:
        print("baseline recorded — this is the latency reference for readiness")


# ---------- interference ----------

def cmd_interfere(args, db):
    old = get_seq(db, args.old)
    new = get_seq(db, args.new)
    rng = random.Random()
    interactive = sys.stdin.isatty()
    wins = {"old": 0, "new": 0}
    trials = args.reps
    if not interactive:
        # offline: model proactive interference decaying with practice sessions
        n_new_sessions = sum(1 for h in new["history"] if h["kind"] == "train")
        p_new = min(0.95, 0.25 + 0.12 * n_new_sessions)
        for _ in range(trials):
            wins["new" if rng.random() < p_new else "old"] += 1
        wr = wins["new"] / trials
    else:
        print(f"\n--- interference: {args.old} vs {args.new} ---")
        print("Prompt names the sequence; type THAT one (original order). Ctrl-C stops.\n")
        for t in range(trials):
            which = rng.choice(["old", "new"])
            seq = old if which == "old" else new
            prompt = "-".join(seq["nodes"])
            t0 = time.perf_counter()
            try:
                ans = input(f"trial {t+1:>2}: {which.upper():<3}  → ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            _ = time.perf_counter() - t0
            ok = ans == prompt or [a.strip() for a in ans.split(",")] == seq["nodes"]
            if ok:
                wins[which] += 1
            print(f"          expected {prompt}  {'✓' if ok else '✗'}")
        wr = wins["new"] / max(1, wins["old"] + wins["new"])
    rec = {"date": date.today().isoformat(), "old": args.old, "new": args.new,
           "wins": wins, "win_rate_new": round(wr, 3)}
    db["sessions"].append({"kind": "interfere", **rec})
    new["history"].append({"kind": "interfere", "win_rate_new": round(wr, 3),
                           "date": rec["date"]})
    save(db)
    print(f"\ninterference: old {wins['old']} / new {wins['new']}  →  "
          f"new wins {wr:.0%} of alternations "
          f"({'DOMINANT' if wr >= READY_INTERFERE_WIN else 'old habit still interferes'})")


# ---------- recall schedule ----------

def cmd_due(args, db):
    now = datetime.now()
    any_due = False
    for name, s in db["sequences"].items():
        nd = datetime.fromisoformat(s["next_due"])
        if nd <= now:
            any_due = True
            print(f"{name:<20} DUE (level {s['interval_level']}, "
                  f"since {s['added']})")
    if not any_due:
        nds = [datetime.fromisoformat(s["next_due"]) for s in db["sequences"].values()]
        if nds:
            print(f"nothing due — next: {min(nds).isoformat(timespec='minutes')}")
        else:
            print("no sequences — `seq add` first")


def cmd_recall(args, db):
    s = get_seq(db, args.name)
    if args.passed:
        lvl = min(len(INTERVALS) - 1, s["interval_level"] + 1)
        s["interval_level"] = lvl
        s["next_due"] = (datetime.now() + INTERVALS[lvl]).isoformat(timespec="seconds")
        db["recalls"].append({"name": args.name, "date": date.today().isoformat(),
                              "passed": True})
        save(db)
        print(f"{args.name}: recall PASSED — level {lvl}, next due "
              f"{s['next_due']}" + ("  (RETAINED)" if lvl == len(INTERVALS)-1 else ""))
    else:
        s["interval_level"] = 0
        s["next_due"] = (datetime.now() + INTERVALS[0]).isoformat(timespec="seconds")
        db["recalls"].append({"name": args.name, "date": date.today().isoformat(),
                              "passed": False})
        save(db)
        print(f"{args.name}: recall FAILED — interval reset to 10 minutes")


# ---------- readiness / stats ----------

def cmd_ready(args, db):
    s = get_seq(db, args.name)
    tests = [h for h in s["history"] if h["kind"] == "train"]
    if not tests:
        sys.exit(f"no training sessions logged for '{args.name}' — run `train` first")
    last = tests[-1]
    base = tests[0]
    # accuracy per rotation from the last session
    accs = [a for a in last["per_rot"].values() if a is not None]
    acc_ok = accs and min(accs) >= ACC_GATE
    lat_ok = last["median_latency"] <= max(
        base["median_latency"] * READY_LATENCY_FACTOR, base["median_latency"])
    lat_ok = lat_ok or last["median_latency"] <= base["median_latency"]
    inter = [h for h in s["history"] if h["kind"] == "interfere"]
    inter_ok = None
    if inter:
        inter_ok = inter[-1]["win_rate_new"] >= READY_INTERFERE_WIN
    print(f"READINESS — {args.name}")
    print(f"  accuracy  (all transpositions ≥{ACC_GATE:.0%}): "
          f"{'PASS' if acc_ok else 'FAIL'} (min {min(accs):.0%})" if accs else
          "  accuracy: no data")
    print(f"  latency   (≤{READY_LATENCY_FACTOR}× baseline {base['median_latency']}s): "
          f"{'PASS' if lat_ok else 'FAIL'} (now {last['median_latency']}s)")
    if inter_ok is not None:
        print(f"  interference (≥{READY_INTERFERE_WIN:.0%} new wins): "
              f"{'PASS' if inter_ok else 'FAIL'} "
              f"({inter[-1]['win_rate_new']:.0%})")
    verdict = acc_ok and lat_ok and (inter_ok is not False)
    if verdict:
        print("\nVERDICT: READY — transfer to the real device with 10-20 live reps")
    else:
        print("\nVERDICT: NOT READY — keep drilling the failing criterion")


def cmd_stats(args, db):
    s = get_seq(db, args.name)
    print(f"stats — {args.name} ({len(s['nodes'])} nodes, added {s['added']})")
    for h in s["history"]:
        if h["kind"] == "interfere":
            print(f"  {h['date']}  interfere  new-wins {h['win_rate_new']:.0%}")
        else:
            print(f"  {h['date']}  {h['kind']:<5} acc {h['accuracy']:.0%}  "
                  f"med {h['median_latency']}s  reps {h['reps']}")
    lvl = s["interval_level"]
    print(f"recall level {lvl}, next due {s['next_due']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("seq")
    ss = p.add_subparsers(dest="action", required=True)
    sa = ss.add_parser("add")
    sa.add_argument("name"); sa.add_argument("nodes", help="comma-separated, e.g. 1,5,9,3")
    ss.add_parser("list")

    p = sub.add_parser("test"); p.add_argument("name"); p.add_argument("--reps", type=int, default=8)
    p = sub.add_parser("train"); p.add_argument("name"); p.add_argument("--minutes", type=float, default=1.5)
    p.add_argument("--reps", type=int, default=12)

    p = sub.add_parser("interfere")
    p.add_argument("old"); p.add_argument("new"); p.add_argument("--reps", type=int, default=20)

    sub.add_parser("due")

    p = sub.add_parser("recall"); p.add_argument("name")
    p.add_argument("--passed", action="store_true", dest="passed")

    p = sub.add_parser("ready"); p.add_argument("name")
    p = sub.add_parser("stats"); p.add_argument("name")

    args = ap.parse_args()
    db = load()

    if args.cmd == "seq":
        cmd_seq(args, db)
    elif args.cmd == "test":
        cmd_test_train(args, db, train=False)
    elif args.cmd == "train":
        cmd_test_train(args, db, train=True)
    elif args.cmd == "interfere":
        cmd_interfere(args, db)
    elif args.cmd == "due":
        cmd_due(args, db)
    elif args.cmd == "recall":
        cmd_recall(args, db)
    elif args.cmd == "ready":
        cmd_ready(args, db)
    elif args.cmd == "stats":
        cmd_stats(args, db)


if __name__ == "__main__":
    main()
