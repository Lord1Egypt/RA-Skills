"""memory-doctor CLI.

  memory-doctor report  --dir PATH        read-only health card
  memory-doctor lint    --dir PATH        show the index-reconciliation plan (no write)
  memory-doctor lint    --dir PATH --fix  apply it (snapshots first, reversible)
  memory-doctor undo    --dir PATH        restore the last snapshot
"""

from __future__ import annotations

import argparse
import os
import sys

from . import __version__, lint as lint_mod, report as report_mod, snapshot as snap
from .adapters import detect_format, get_adapter


def _load(args):
    root = os.path.abspath(os.path.expanduser(args.dir))
    if not os.path.isdir(root):
        sys.exit(f"error: not a directory: {root}")
    fmt = args.format or detect_format(root)
    store = get_adapter(fmt).load(root)
    return root, store


def cmd_report(args):
    _, store = _load(args)
    print(report_mod.render_card(report_mod.analyze(store)))


def cmd_lint(args):
    root, store = _load(args)
    if not store.has_index:
        print(f"lint: '{store.fmt}' has a derived spine (no persisted index to reconcile) — "
              "nothing to fix. Use `report` for health, or mneme's own tool for spine/lint.")
        return
    plan = lint_mod.plan_index(store)
    if not plan.changed:
        print("✓ index is in sync — nothing to fix.")
        return
    print("Index reconciliation plan:")
    for e in plan.add:
        print(f"  + add     [{e.id}] -> {e.target}")
    for e in plan.remove:
        print(f"  - remove  [{e.id}] -> {e.target} (dangling)")
    if not args.fix:
        print("\n(dry-run) re-run with --fix to apply.")
        return
    snap_path = snap.snapshot(root)
    lint_mod.apply_index(store, plan)
    snap.log_change(root, f"lint --fix: +{len(plan.add)} / -{len(plan.remove)} index entries")
    print(f"\n✓ applied. snapshot: {os.path.relpath(snap_path, root)} (use `undo` to revert)")


def cmd_undo(args):
    root, _ = _load(args)
    snap_path = snap.latest_snapshot(root)
    if not snap_path:
        print("nothing to undo — no snapshots found.")
        return
    n = snap.restore(root, snap_path)
    snap.log_change(root, f"undo: restored {n} files from {os.path.basename(snap_path)}")
    print(f"✓ restored {n} files from {os.path.basename(snap_path)}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="memory-doctor",
                                description="Keep LLM-agent long-term memory healthy.")
    p.add_argument("--version", action="version", version=f"memory-doctor {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp):
        sp.add_argument("--dir", required=True, help="memory directory")
        sp.add_argument("--format", choices=["auto-memory", "mneme"], default=None)

    sp = sub.add_parser("report", help="read-only health card"); add_common(sp)
    sp.set_defaults(func=cmd_report)
    sp = sub.add_parser("lint", help="index reconciliation"); add_common(sp)
    sp.add_argument("--fix", action="store_true", help="apply (snapshots first)")
    sp.set_defaults(func=cmd_lint)
    sp = sub.add_parser("undo", help="restore last snapshot"); add_common(sp)
    sp.set_defaults(func=cmd_undo)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
