#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def main():
    now = datetime.now().astimezone()
    horizon = now + timedelta(hours=2)
    list_events_swift = str(Path(__file__).resolve().parent / "list_events.swift")

    # Query a wider range to include today+tomorrow context, then filter in Python.
    from_iso = now.isoformat(timespec="seconds")
    to_iso = (now + timedelta(hours=48)).isoformat(timespec="seconds")

    out = subprocess.check_output([
        "swift",
        list_events_swift,
        from_iso,
        to_iso,
    ], text=True)

    events = json.loads(out).get("events", [])
    upcoming = []
    for ev in events:
        if ev.get("isAllDay"):
            continue
        start_ts = int(ev.get("start", 0))
        start = datetime.fromtimestamp(start_ts).astimezone()
        if now < start <= horizon:
            upcoming.append(ev)

    print(json.dumps({
        "now": now.isoformat(),
        "horizon": horizon.isoformat(),
        "count": len(upcoming),
        "events": upcoming,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
