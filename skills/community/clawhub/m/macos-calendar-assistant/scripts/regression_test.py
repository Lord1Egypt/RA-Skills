#!/usr/bin/env python3
import datetime as dt
import json
import subprocess
import tempfile
import uuid
from pathlib import Path

from config_utils import get_zoneinfo

SCRIPT_DIR = Path(__file__).resolve().parent
TZ = get_zoneinfo()


def run(cmd, check=True):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return p


def iso(d):
    return d.astimezone(TZ).isoformat(timespec="seconds")


def parse_candidates(clean_output: str):
    data = json.loads(clean_output)
    return int(data.get("delete_candidates", 0))


def main():
    now = dt.datetime.now(TZ).replace(minute=0, second=0, microsecond=0) + dt.timedelta(days=3)
    start = now
    end = now + dt.timedelta(minutes=30)
    title = f"[回归测试]{uuid.uuid4().hex[:8]}"
    cal = "产品"

    # 1) create
    p1 = run([
        "python3", str(SCRIPT_DIR / "upsert_event.py"),
        "--title", title,
        "--start", iso(start),
        "--end", iso(end),
        "--calendar", cal,
        "--notes", "regression-create",
        "--alarm-minutes", "5",
    ])
    if not any(x in p1.stdout for x in ["CREATED", "UPDATED", "SKIPPED"]):
        raise RuntimeError("unexpected upsert create output")

    # 2) idempotent
    p2 = run([
        "python3", str(SCRIPT_DIR / "upsert_event.py"),
        "--title", title,
        "--start", iso(start),
        "--end", iso(end),
        "--calendar", cal,
        "--notes", "regression-create",
        "--alarm-minutes", "5",
    ])
    if not any(x in p2.stdout for x in ["SKIPPED", "UPDATED"]):
        raise RuntimeError("expected SKIPPED/UPDATED in idempotent run")

    # 3) update
    p3 = run([
        "python3", str(SCRIPT_DIR / "upsert_event.py"),
        "--title", title,
        "--start", iso(start),
        "--end", iso(end + dt.timedelta(minutes=15)),
        "--calendar", cal,
        "--notes", "regression-updated",
        "--alarm-minutes", "10",
    ])
    if not any(x in p3.stdout for x in ["UPDATED", "SKIPPED"]):
        raise RuntimeError("expected UPDATED/SKIPPED in update run")

    # 4) create a deliberate duplicate via legacy add_event
    run([
        "python3", str(SCRIPT_DIR / "add_event.py"),
        "--title", title,
        "--start", iso(start),
        "--end", iso(end + dt.timedelta(minutes=15)),
        "--calendar", cal,
        "--notes", "regression-duplicate",
    ])

    range_start = iso(start - dt.timedelta(hours=1))
    range_end = iso(end + dt.timedelta(hours=2))
    snapshot_path = Path(tempfile.gettempdir()) / f"mca-regression-delete-plan-{uuid.uuid4().hex[:6]}.json"

    # 5) clean dry-run should find duplicate
    c1 = run([
        "python3", str(SCRIPT_DIR / "calendar_clean.py"),
        "--start", range_start,
        "--end", range_end,
        "--snapshot-out", str(snapshot_path),
    ])
    cand1 = parse_candidates(c1.stdout)
    if cand1 < 1:
        raise RuntimeError("expected duplicate candidates >= 1")

    # 6) apply with confirm
    run([
        "python3", str(SCRIPT_DIR / "calendar_clean.py"),
        "--start", range_start,
        "--end", range_end,
        "--apply", "--confirm", "yes",
    ])

    # 7) verify candidates reduced to 0 for this narrow window
    c2 = run([
        "python3", str(SCRIPT_DIR / "calendar_clean.py"),
        "--start", range_start,
        "--end", range_end,
    ])
    cand2 = parse_candidates(c2.stdout)
    if cand2 != 0:
        raise RuntimeError(f"expected duplicate candidates 0 after cleanup, got {cand2}")

    # 8) cleanup remaining test event
    cleanup = run([
        "python3", str(SCRIPT_DIR / "calendar_clean.py"),
        "--start", range_start,
        "--end", range_end,
        "--snapshot-out", str(snapshot_path),
    ])
    # If no candidates, remove exact by title/start as a fallback.
    if parse_candidates(cleanup.stdout) == 0:
        swift_code = f'''import EventKit\nimport Foundation\nlet store = EKEventStore()\nlet fmt = ISO8601DateFormatter()\nlet sem = DispatchSemaphore(value: 0)\nstore.requestAccess(to: .event) {{ granted, _ in\n  guard granted else {{ sem.signal(); return }}\n  guard let start = fmt.date(from: "{iso(start)}") else {{ sem.signal(); return }}\n  guard let cal = store.calendars(for: .event).first(where: {{$0.title == "{cal}"}}) else {{ sem.signal(); return }}\n  let pred = store.predicateForEvents(withStart: start, end: start.addingTimeInterval(60), calendars: [cal])\n  let events = store.events(matching: pred).filter {{$0.title == "{title}"}}\n  for e in events {{ try? store.remove(e, span: .thisEvent) }}\n  sem.signal()\n}}\nsem.wait()\n'''
        subprocess.run(["swift", "-"], input=swift_code, capture_output=True, text=True)

    print(json.dumps({
        "ok": True,
        "title": title,
        "range": {"start": range_start, "end": range_end},
        "snapshot": str(snapshot_path),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
