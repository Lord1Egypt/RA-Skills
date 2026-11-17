#!/usr/bin/env python3
"""notify_closed_dryrun — sample the deterministic notifier OUTPUT without sending.

Renders the closure message for every finished (resolve/cancel/fail) bottle in the
ledger, exactly as the real notifier would post it, and prints them to stdout so you
can review the format/result before anything goes to Discord.

Usage:
  python3 notify_closed_dryrun.py                  # all finished bottles
  python3 notify_closed_dryrun.py <cid>            # just one bottle
  python3 notify_closed_dryrun.py --json           # machine-readable list
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTIFIER = HERE / "notify_closed_bottles.py"

spec = importlib.util.spec_from_file_location("notify", NOTIFIER)
nb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nb)

def all_finished():
    seen = set()
    out = []
    for l in nb.load_all_lines():
        try:
            r = json.loads(l)
        except Exception:
            continue
        if r.get("event") in nb.END_EVENTS and r.get("id") not in seen:
            seen.add(r["id"])
            out.append(r["id"])
    return out

def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv[1:]
    ids = argv[:1] or all_finished()
    results = []
    for cid in ids:
        msg, status = nb.render_bottle(cid)
        results.append({"id": cid, "message": msg, "status": status})
    if as_json:
        print(json.dumps({"count": len(results), "bottles": results}, indent=2))
        return
    for r in results:
        print("=" * 60)
        print(f"Bottle: {r['id']}")
        print("=" * 60)
        if r["message"]:
            print(r["message"])
        else:
            print(f"  (no message) {r['status']}")
        print()
    print(f"[dry-run] {len(results)} finished bottle(s) rendered. Nothing sent.")

if __name__ == "__main__":
    main()
