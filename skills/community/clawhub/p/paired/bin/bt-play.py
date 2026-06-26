#!/usr/bin/env python3
"""bt-play — Play an audio file, optionally to a specific BT speaker.

Examples:
  bt-play /usr/share/sounds/alsa/Front_Center.wav            # plays to default sink
  bt-play song.mp3 --sink AA:BB:CC:DD:EE:FF                  # routes to a paired BT speaker
  bt-play song.mp3 --bg                                      # background, returns immediately

If --sink MAC is given, the device must be paired+connected with the A2DP-sink
profile active. We look up its PipeWire node via the MAC fragment and use
pw-play --target.
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_audio


def main() -> int:
    ap = argparse.ArgumentParser(description="Play an audio file")
    ap.add_argument("file")
    ap.add_argument("--sink", help="Route to BT MAC's PipeWire sink")
    ap.add_argument("--sink-id", type=int, help="Route to numeric wpctl object id")
    ap.add_argument("--bg", action="store_true", help="Background; return immediately")
    args = ap.parse_args()

    target_id = args.sink_id
    if args.sink:
        s = bt_audio.find_bluez_sink(args.sink)
        if s is None:
            sys.stderr.write(f"error: no PipeWire sink found for {args.sink}. "
                             f"Run `bt-info {args.sink}` and confirm Connected=True with A2DP profile.\n")
            return 1
        target_id = s["id"]
        sys.stderr.write(f"[bt-play] routing to {s['node_description']} (id={s['id']})\n")

    fp = Path(args.file).expanduser().resolve()
    if not fp.exists():
        sys.stderr.write(f"error: file not found: {fp}\n")
        return 1

    if args.bg:
        proc = bt_audio.play_file(str(fp), target_id=target_id, blocking=False)
        print(f"playing in background, pid={proc.pid}")
        return 0
    rc = bt_audio.play_file(str(fp), target_id=target_id, blocking=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
