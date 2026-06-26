#!/usr/bin/env python3
"""Stateless MTA commuter rail track check.

Checks the MTA arrivals API for a track assignment on a specific train.
Prints a notification message if a track is assigned; exits silently if not.

Designed to be run via `openclaw cron` on a schedule:
    openclaw cron add --every 1m \
      --command "python3 scripts/check_track.py --train 1582 --station NYK" \
      --channel telegram --delete-after-run \
      --name "Track watch: 5:22 PM to Huntington"

    # Metro-North:
    openclaw cron add --every 1m \
      --command "python3 scripts/check_track.py --system mnr --train 873 --station GCT" \
      --channel telegram --delete-after-run \
      --name "Track watch: 5:43 PM to White Plains"
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request

SYSTEMS = {
    "lirr": {
        "api_base": "https://backend-unified.mylirr.org/arrivals",
        "api_headers": {
            "Accept": "application/json",
            "accept-version": "3.0",
            "Origin": "https://traintime.mta.info",
        },
    },
    "mnr": {
        "api_base": "https://backend-unified.mymnr.org/arrivals",
        "api_headers": {
            "Accept": "application/json",
            "accept-version": "3.0",
            "Origin": "https://traintime.mta.info",
        },
    },
}

STATION_NAMES = {
    "NYK": "Penn Station",
    "ATL": "Atlantic Terminal",
    "GCT": "Grand Central",
    "HM": "Harlem-125 St",
}


def fetch_arrivals(station, system="lirr"):
    """Fetch arrivals from the MTA API."""
    cfg = SYSTEMS[system]
    url = f"{cfg['api_base']}/{station}"
    req = Request(url, headers=cfg["api_headers"])
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def find_train(arrivals, train_num):
    """Find a specific train in the arrivals list."""
    target = str(train_num)
    for a in arrivals.get("arrivals", []):
        if str(a.get("train_num", "")) == target:
            return a
    return None


def main():
    parser = argparse.ArgumentParser(description="Check track assignment for an MTA commuter rail train.")
    parser.add_argument("--train", required=True, help="Train number")
    parser.add_argument("--station", default="NYK", help="Station code (default: NYK)")
    parser.add_argument("--system", "-s", choices=["lirr", "mnr"], default="lirr",
                        help="System: lirr or mnr (default: lirr)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        data = fetch_arrivals(args.station, args.system)
    except Exception as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)

    train = find_train(data, args.train)
    if not train:
        # Train not in arrivals yet — exit non-zero so cron keeps the job
        sys.exit(1)

    track = train.get("track")
    if not track:
        # No track assigned yet — exit non-zero so cron keeps the job
        sys.exit(1)

    canceled = train.get("status", {}).get("canceled", False)
    delay_sec = train.get("status", {}).get("otp", 0)
    sched_track = train.get("sched_track", "")
    station_name = STATION_NAMES.get(args.station, args.station)

    if args.json:
        print(json.dumps({
            "train": args.train,
            "station": args.station,
            "system": args.system,
            "track": track,
            "sched_track": sched_track,
            "canceled": canceled,
            "delay_sec": delay_sec,
        }))
        sys.exit(0)

    if canceled:
        print(f"Train {args.train} has been canceled")
    else:
        delay_info = ""
        if delay_sec and abs(delay_sec) >= 60:
            delay_min = abs(delay_sec) // 60
            if delay_sec > 0:
                delay_info = f" (running {delay_min} min late)"
            else:
                delay_info = f" (running {delay_min} min early)"

        print(f"Track {track} at {station_name} for train {args.train}{delay_info}")


if __name__ == "__main__":
    main()
