#!/usr/bin/env python3
import os
OPERATOR_EMAIL = os.environ.get("OCAS_OPERATOR_EMAIL", "operator@example.com")
"""Bower light-scan triage — read-only.

Resolves parent folder IDs in light_scan_latest.json to names, groups the
owned arrivals by location, flags disorganization signals (timestamp-named
folder piles, asset scatter, naming inconsistency), and lists shared files.

Read-only: makes no changes. Companion to references/light-scan-triage.md.

Usage:
    python3 scripts/bower_light_triage.py [options]

Options:
    -h, --help        Show this help message and exit.
    --data DIR        ocas-bower data dir (default:
                     $HERMES_HOME/commons/data/ocas-bower).
    --account EMAIL  Google account to authenticate as
                     (default: OPERATOR_EMAIL).
    --json            Emit structured JSON on stdout instead of the
                     human-readable report.

Requires an interpreter with googleapiclient + requests available; if
`import googleapiclient, requests` fails the script explains why (see
references/cron-drive-fallback.md -> "Operational pitfalls").
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_DATA = os.path.expanduser("~/.hermes/profiles/indigo/commons/data/ocas-bower")
DEFAULT_OWNER = "OPERATOR_EMAIL"
SCRIPTS = os.path.expanduser("~/.hermes/profiles/indigo/scripts")

# Timestamp-named export/checkpoint folders are exactly YYYY-MM-DD_HH-MM-SS.
# (Avoid naive [:4].isdigit() — it false-positives on names like
#  "2442 Kuhio Avenue 702".)
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$")


def build_parser():
    p = argparse.ArgumentParser(
        prog="bower_light_triage.py",
        description="Read-only light-scan triage: resolve parent IDs to names, "
                    "group owned arrivals, flag disorganization signals, list shared files.",
    )
    p.add_argument("--data", default=DEFAULT_DATA,
                   help=f"ocas-bower data dir (default: {DEFAULT_DATA})")
    p.add_argument("--account", default=DEFAULT_OWNER,
                   help=f"Google account to authenticate as (default: {DEFAULT_OWNER})")
    p.add_argument("--json", action="store_true",
                   help="Emit structured JSON on stdout instead of the human-readable report")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    data = Path(args.data)

    scan_path = data / "light_scan_latest.json"
    if not scan_path.exists():
        sys.stderr.write(
            f"ERROR: light_scan_latest.json not found at {scan_path}\n"
            f"  Expected a bower.scan.light run to have written this file first.\n"
            f"  Run 'bower.scan.light' (or the light-scan cron job), then retry.\n")
        return 2

    # Lazy import: Drive dependencies (googleapiclient, requests) must not block
    # --help. Importing at module top would force a failed import before argparse
    # can print usage on hosts where those packages are missing.
    sys.path.insert(0, SCRIPTS)
    try:
        try:
            from google_auth_mcp import get_service
        except ImportError:
            from google_auth import get_service
    except ImportError as e:
        sys.stderr.write(
            f"ERROR: could not import google_auth.get_service ({e}).\n"
            f"  Use an interpreter with BOTH googleapiclient and requests available, e.g.\n"
            f"  /usr/bin/python3  (verify: python3 -c 'import googleapiclient, requests').\n"
            f"  See references/cron-drive-fallback.md -> 'Operational pitfalls'.\n")
        return 3

    try:
        svc = get_service("drive", "v3", ["https://www.googleapis.com/auth/drive"],
                          account=args.account)
        scan = json.loads(scan_path.read_text())
    except Exception as e:
        sys.stderr.write(f"ERROR: failed to load scan data or authenticate: {e}\n")
        return 4

    owned = scan.get("owned_files", [])
    shared = scan.get("shared_files", [])

    # resolve distinct parent ids (first parent)
    parents = {}
    for f in owned:
        for p in (f.get("parents") or []):
            parents.setdefault(p, None)
    for pid in list(parents.keys()):
        try:
            r = svc.files().get(fileId=pid, fields="id,name,mimeType").execute()
            parents[pid] = r.get("name", "?")
        except Exception as e:
            parents[pid] = f"<unresolved:{str(e)[:40]}>"

    groups = defaultdict(list)
    for f in owned:
        pid = (f.get("parents") or ["?"])[0]
        groups[parents.get(pid, pid)].append(f)

    ts_folders = [it for it in owned
                  if it["mimeType"] == "application/vnd.google-apps.folder"
                  and TS_RE.match(it["name"])]
    life_assets = [it for it in owned if "life101" in it["name"].lower()]

    if args.json:
        out = {
            "owned_by_location": {
                loc: [{"name": it["name"],
                       "kind": "FOLDER" if it["mimeType"] == "application/vnd.google-apps.folder" else "file"}
                      for it in items]
                for loc, items in sorted(groups.items(), key=lambda kv: -len(kv[1]))
            },
            "disorganization_signals": {
                "timestamp_named_folder_piles": (
                    {"count": len(ts_folders),
                     "location": parents.get((ts_folders[0].get("parents") or ["?"])[0], "?"),
                     "names": [it["name"] for it in ts_folders]}
                    if ts_folders else None),
                "life101_scatter": (
                    {"count": len(life_assets),
                     "location": parents.get((life_assets[0].get("parents") or ["?"])[0], "?")}
                    if life_assets else None),
            },
            "shared": [{"name": s["name"], "owners": s.get("owners")} for s in shared],
            "summary": {
                "owned": len(owned),
                "owned_folders": sum(1 for i in owned
                                     if i["mimeType"] == "application/vnd.google-apps.folder"),
                "shared": len(shared),
            },
        }
        print(json.dumps(out, indent=2))
        return 0

    # ── Human-readable report (default) ──
    print("=== OWNED ARRIVALS BY LOCATION ===")
    for loc, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print(f"\n[{loc}] ({len(items)} items)")
        for it in items:
            kind = "FOLDER" if it["mimeType"] == "application/vnd.google-apps.folder" else "file"
            print(f"   - {it['name']}  ({kind})")

    if ts_folders:
        pid = (ts_folders[0].get("parents") or ["?"])[0]
        print(f"\n=== DISORGANIZATION SIGNALS ===")
        print(f"  * TIMESTAMP-NAMED FOLDER PILE: {len(ts_folders)} folders "
              f"('YYYY-MM-DD_HH-MM-SS') under [{parents.get(pid, pid)}]")
        for it in ts_folders:
            print(f"      {it['name']}")

    if life_assets:
        loc = parents.get((life_assets[0].get("parents") or ["?"])[0], "?")
        print(f"  * SCATTER: {len(life_assets)} 'Life101' assets in [{loc}] "
              f"(a person/personal folder) — check whether a dedicated 'Life 101' exists")

    print(f"\n=== SHARED (non-actionable) ===")
    for s in shared:
        print(f"   - {s['name']}  owner={s.get('owners', 'unknown')}")

    n_folders = sum(1 for i in owned if i["mimeType"] == "application/vnd.google-apps.folder")
    print(f"\nSUMMARY: {len(owned)} owned ({n_folders} folders), {len(shared)} shared.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
