#!/usr/bin/env python3
"""bt-audio — Show audio state, find BT audio sinks/sources, switch profiles.

Examples:
  bt-audio                         # Full audio status (sinks + sources + BT devices)
  bt-audio --sink AA:BB:CC:DD:EE:FF   # Find PipeWire sink for this paired BT MAC
  bt-audio --set-default 55       # Make sink id 55 the system default
  bt-audio --profiles AA:BB:CC:..  # List BT profiles for a device (a2dp / hfp / off)
  bt-audio --json
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_audio


def main() -> int:
    ap = argparse.ArgumentParser(description="BT audio routing diagnostics + control")
    ap.add_argument("--sink", help="Find PipeWire sink for this BT MAC")
    ap.add_argument("--source", help="Find PipeWire source for this BT MAC")
    ap.add_argument("--set-default", type=int, metavar="ID",
                    help="Set wpctl object id as default sink")
    ap.add_argument("--profiles", help="List BT profiles for this MAC")
    ap.add_argument("--set-profile", metavar="MAC,IDX", help="Set BT device to profile index, e.g. 'AA:BB:..,1'")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not bt_audio.have_pipewire():
        sys.stderr.write("error: wpctl/pw-cli not in PATH (PipeWire not installed?)\n")
        return 2

    if args.set_default is not None:
        bt_audio.set_default_sink(args.set_default)
        print(f"default sink set to id {args.set_default}")
        return 0

    if args.set_profile:
        mac, idx = args.set_profile.split(",")
        bt_audio.set_bt_profile(mac.strip(), int(idx))
        print(f"profile set on {mac.strip()} -> index {idx}")
        return 0

    if args.profiles:
        profiles = bt_audio.list_profiles_for_bt(args.profiles)
        if args.json:
            print(json.dumps(profiles, indent=2))
            return 0
        if not profiles:
            print(f"No BT profiles for {args.profiles}. Connected?")
            return 1
        for p in profiles:
            print(p)
        return 0

    if args.sink:
        s = bt_audio.find_bluez_sink(args.sink)
        if args.json:
            print(json.dumps(s, indent=2))
        elif s is None:
            print(f"No PipeWire sink for {args.sink} (device not connected with A2DP profile?)")
            return 1
        else:
            print(f"id={s['id']}  node={s['node_name']}")
            print(f"description: {s['node_description']}")
        return 0

    if args.source:
        s = bt_audio.find_bluez_source(args.source)
        if args.json:
            print(json.dumps(s, indent=2))
        elif s is None:
            print(f"No PipeWire source for {args.source}")
            return 1
        else:
            print(f"id={s['id']}  node={s['node_name']}")
        return 0

    # Default: full status
    sinks = bt_audio.list_sinks()
    sources = bt_audio.list_sources()
    if args.json:
        print(json.dumps({"sinks": sinks, "sources": sources}, indent=2))
        return 0
    print("Audio Sinks:")
    for s in sinks:
        mark = " *" if s["default"] else "  "
        print(f"  {mark} id={s['id']:<4}  {s['name']}")
    print("\nAudio Sources:")
    for s in sources:
        mark = " *" if s["default"] else "  "
        print(f"  {mark} id={s['id']:<4}  {s['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
