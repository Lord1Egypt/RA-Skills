#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from collections import defaultdict

from config_utils import load_config, get_zoneinfo


def parse_iso(s: str) -> dt.datetime:
    d = dt.datetime.fromisoformat(s)
    if d.tzinfo is None:
        raise SystemExit(f"Timezone required: {s}")
    return d


def list_events(start_iso: str, end_iso: str):
    list_events_swift = str(Path(__file__).resolve().parent / "list_events.swift")
    cmd = ["swift", list_events_swift, start_iso, end_iso]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(r.stdout).get("events", [])


def norm_title(t: str) -> str:
    return " ".join((t or "").strip().lower().split())


TZ = get_zoneinfo()
CFG = load_config()


def ts_to_iso(ts: int) -> str:
    return dt.datetime.fromtimestamp(ts, TZ).isoformat()


def _swift_escape(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


def delete_events(targets):
    # targets: list[(calendar,title,start_ts)]
    rows = []
    for c, t, s in targets:
        rows.append(f'.init(title:"{_swift_escape(t)}", calendar:"{_swift_escape(c)}", start:{s})')
    swift_targets = ",\n".join(rows)

    code = f'''import EventKit
import Foundation

struct Target {{ let title:String; let calendar:String; let start:Double }}
let targets:[Target] = [
{swift_targets}
]
let store = EKEventStore()
let sem = DispatchSemaphore(value: 0)
store.requestAccess(to: .event) {{ granted, _ in
  guard granted else {{ print("access_denied"); sem.signal(); return }}
  var removed=0
  for t in targets {{
    guard let cal = store.calendars(for: .event).first(where: {{$0.title == t.calendar}}) else {{ continue }}
    let d = Date(timeIntervalSince1970: t.start)
    let pred = store.predicateForEvents(withStart: d, end: d.addingTimeInterval(60), calendars: [cal])
    let events = store.events(matching: pred).filter{{$0.title == t.title && abs($0.startDate.timeIntervalSince1970 - t.start) < 1}}
    for e in events {{ do {{ try store.remove(e, span: .thisEvent); removed += 1 }} catch {{}} }}
  }}
  print("removed=\\(removed)")
  sem.signal()
}}
sem.wait()
'''
    p = subprocess.run(["swift", "-"], input=code, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr or p.stdout)
    return p.stdout.strip()


def build_findings(events):
    # exact duplicate by same calendar + same start + normalized title
    groups = defaultdict(list)
    for e in events:
        if e.get("isAllDay"):
            continue
        key = (e.get("calendar", ""), int(e.get("start", 0)), norm_title(e.get("title", "")))
        groups[key].append(e)

    to_delete = []
    findings = []

    for (cal, start_ts, _), arr in groups.items():
        if len(arr) <= 1:
            continue
        arr_sorted = sorted(arr, key=lambda x: (len(x.get("notes", "") or ""), len(x.get("title", "") or "")), reverse=True)
        keep = arr_sorted[0]
        drops = arr_sorted[1:]
        findings.append({
            "type": "exact-duplicate",
            "calendar": cal,
            "start": ts_to_iso(start_ts),
            "keep": keep.get("title", ""),
            "drop": [d.get("title", "") for d in drops],
        })
        for d in drops:
            to_delete.append((d.get("calendar", ""), d.get("title", ""), int(d.get("start", 0))))

    # cross-calendar duplicates in same slot + same title
    slot_map = defaultdict(list)
    for e in events:
        if e.get("isAllDay"):
            continue
        slot_map[(int(e.get("start", 0)), int(e.get("end", 0)))].append(e)

    for (s, en), arr in slot_map.items():
        if len(arr) < 2:
            continue
        by_title = defaultdict(list)
        for e in arr:
            by_title[norm_title(e.get("title", ""))].append(e)

        for _, same in by_title.items():
            if len(same) < 2:
                continue
            # Prefer calendars by configurable priority / depriority
            priority = set(CFG.get("dedup", {}).get("prefer_calendars", []))
            depriority = set(CFG.get("dedup", {}).get("deprioritize_calendars", ["交流", "日历"]))

            def sort_key(ev):
                cal = ev.get("calendar", "")
                return (0 if cal in priority else 1, 1 if cal in depriority else 0)

            keep = sorted(same, key=sort_key)[0]
            drops = [x for x in same if x is not keep]
            if not drops:
                continue

            findings.append({
                "type": "cross-calendar-duplicate",
                "start": ts_to_iso(s),
                "end": ts_to_iso(en),
                "title": same[0].get("title", ""),
                "keep_calendar": keep.get("calendar", ""),
                "drop_calendars": [d.get("calendar", "") for d in drops],
            })
            for d in drops:
                k = (d.get("calendar", ""), d.get("title", ""), int(d.get("start", 0)))
                if k not in to_delete:
                    to_delete.append(k)

    return findings, to_delete


def main():
    ap = argparse.ArgumentParser(description="Detect and clean duplicated/overlapped calendar events.")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--apply", action="store_true", help="Actually delete suggested duplicates")
    ap.add_argument("--confirm", default="", help="Required for deletion: set --confirm yes")
    ap.add_argument("--snapshot-out", default="", help="Write delete plan JSON before apply")
    args = ap.parse_args()

    _ = parse_iso(args.start)
    _ = parse_iso(args.end)

    events = list_events(args.start, args.end)
    findings, to_delete = build_findings(events)

    output = {
        "range": {"start": args.start, "end": args.end},
        "total_events": len(events),
        "findings": findings,
        "delete_candidates": len(to_delete),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

    if args.snapshot_out:
        snap = {
            "generated_at": dt.datetime.now(TZ).isoformat(),
            "range": output["range"],
            "delete_targets": [
                {"calendar": c, "title": t, "start": s, "start_iso": ts_to_iso(s)}
                for c, t, s in to_delete
            ],
        }
        Path(args.snapshot_out).write_text(json.dumps(snap, ensure_ascii=False, indent=2))

    if args.apply:
        if args.confirm.lower() != "yes":
            raise SystemExit("Refusing to delete without explicit confirmation. Use: --apply --confirm yes")
        if not to_delete:
            print("removed=0")
            return
        res = delete_events(to_delete)
        print(res)


if __name__ == "__main__":
    main()
