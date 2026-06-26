#!/usr/bin/env python3
"""bt-volume — Get / set volume on a sink (BT or local).

Examples:
  bt-volume                                  # show default sink volume
  bt-volume --sink AA:BB:CC:DD:EE:FF         # show specific BT sink
  bt-volume --sink AA:BB:CC:DD:EE:FF 50      # set to 50%
  bt-volume --id 55 75                       # set sink id 55 to 75%
  bt-volume --mute --id 55                   # mute
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_audio


def _resolve_target(args) -> int:
    """Return the wpctl object id to control."""
    if args.id is not None:
        return args.id
    if args.sink:
        s = bt_audio.find_bluez_sink(args.sink)
        if s is None:
            sys.stderr.write(f"error: no sink for {args.sink}\n")
            sys.exit(1)
        return s["id"]
    # Default: find the default sink
    sinks = bt_audio.list_sinks()
    default = next((s for s in sinks if s["default"]), None)
    if default is None:
        sys.stderr.write("error: no default sink and no --sink/--id given\n")
        sys.exit(1)
    return default["id"]


def main() -> int:
    ap = argparse.ArgumentParser(description="Get/set audio volume")
    ap.add_argument("level", nargs="?", type=int, help="0-150 percent (omit to read)")
    ap.add_argument("--sink", help="BT MAC of target sink")
    ap.add_argument("--id", type=int, help="numeric wpctl object id")
    ap.add_argument("--mute", action="store_true", help="mute (instead of setting level)")
    ap.add_argument("--unmute", action="store_true")
    args = ap.parse_args()

    target = _resolve_target(args)

    if args.mute:
        bt_audio.set_muted(target, True)
        print(f"id {target}: muted")
        return 0
    if args.unmute:
        bt_audio.set_muted(target, False)
        print(f"id {target}: unmuted")
        return 0

    if args.level is None:
        vol, muted = bt_audio.get_volume(target)
        print(f"id {target}: {vol*100:.0f}%{'  [MUTED]' if muted else ''}")
        return 0

    if not 0 <= args.level <= 150:
        sys.stderr.write("error: level must be 0-150\n")
        return 2
    bt_audio.set_volume_pct(target, args.level)
    print(f"id {target}: {args.level}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
