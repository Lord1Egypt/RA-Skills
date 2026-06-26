#!/usr/bin/env python3
"""bt-media — Control music playback on a connected phone via AVRCP.

Examples:
  bt-media MAC                      # show current track + playback status
  bt-media MAC --play
  bt-media MAC --pause
  bt-media MAC --next
  bt-media MAC --prev
  bt-media MAC --json
  bt-media MAC --watch              # follow track changes (Ctrl-C to stop)
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_media


def main() -> int:
    ap = argparse.ArgumentParser(description="AVRCP media control")
    ap.add_argument("mac")
    ap.add_argument("--adapter", default="hci0")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--play", action="store_true")
    g.add_argument("--pause", action="store_true")
    g.add_argument("--stop", action="store_true")
    g.add_argument("--next", dest="next_", action="store_true")
    g.add_argument("--prev", action="store_true")
    g.add_argument("--ff", action="store_true", help="Fast forward")
    g.add_argument("--rew", action="store_true", help="Rewind")
    g.add_argument("--watch", action="store_true",
                    help="Follow track changes (poll every 2s)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    action_map = {
        "play": "Play", "pause": "Pause", "stop": "Stop",
        "next_": "Next", "prev": "Previous",
        "ff": "FastForward", "rew": "Rewind",
    }
    for k, method in action_map.items():
        if getattr(args, k, False):
            try:
                bt_media.player_action(args.mac, method, args.adapter)
            except Exception as e:
                sys.stderr.write(f"{method} failed: {e}\n")
                return 1
            print(f"{method} sent")
            time.sleep(0.5)
            # Show new status
            s = bt_media.media_status(args.mac, args.adapter)
            print(f"  → status={s.get('status')} title={s.get('title')!r}")
            return 0

    if args.watch:
        last = None
        try:
            while True:
                s = bt_media.media_status(args.mac, args.adapter)
                key = (s.get("title"), s.get("artist"), s.get("status"))
                if key != last:
                    last = key
                    ts = time.strftime("%H:%M:%S")
                    print(f"[{ts}] {s.get('status', '?'):<8} | "
                          f"{s.get('artist') or '?':<25.25} | "
                          f"{s.get('title') or '?':<35.35} | "
                          f"{s.get('album') or '?'}", flush=True)
                time.sleep(2)
        except KeyboardInterrupt:
            return 0

    # Default: show current status
    s = bt_media.media_status(args.mac, args.adapter)
    if args.json:
        print(json.dumps(s, indent=2))
        return 0
    if not s.get("connected"):
        print(f"No active media player on {args.mac}.")
        print(f"  Reason: {s.get('reason', '?')}")
        print(f"  Hint: open any music/media app on the phone first")
        return 1
    print(f"Player:    {s['name']} ({s['type']}/{s.get('subtype', '?')})")
    print(f"Status:    {s['status']}")
    if s.get("title"):
        print(f"Track:     {s['title']}")
        print(f"Artist:    {s.get('artist', '?')}")
        print(f"Album:     {s.get('album', '?')}")
        if s.get("duration_ms"):
            cur = s.get("position_ms", 0) // 1000
            tot = s["duration_ms"] // 1000
            print(f"Position:  {cur//60}:{cur%60:02d} / {tot//60}:{tot%60:02d}")
        if s.get("track_number"):
            print(f"Track #:   {s['track_number']}/{s.get('track_count', '?')}")
    print(f"Shuffle:   {s.get('shuffle', '?')}    Repeat: {s.get('repeat', '?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
