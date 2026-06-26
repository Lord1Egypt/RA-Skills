#!/usr/bin/env python3
"""paired-media — High-level media control for Agent.

Auto-picks the connected phone and dispatches to bt-media (BT/AVRCP) or
bt-adb-media (ADB) depending on what's healthier. Designed so Agent can call:

    paired-media status
    paired-media play
    paired-media pause
    paired-media next
    paired-media prev
    paired-media volume 50
    paired-media current

…without needing to know the phone MAC, adapter, or transport.

Returns clean JSON when --json is set so it composes well with Agent's
tool-result chain.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import dbus
from pathlib import Path
_HOME = str(Path.home())

VALID_ACTIONS = {"status", "play", "pause", "play-pause",
                 "next", "prev", "stop", "ff", "rew", "current",
                 "volume", "watch"}


def find_connected_phone() -> tuple[str, str] | tuple[None, None]:
    """Return (mac, adapter) for the first paired+connected device with AVRCP."""
    try:
        bus = dbus.SystemBus()
        manager = dbus.Interface(
            bus.get_object("org.bluez", "/"),
            "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()
        for path, ifaces in objects.items():
            if "org.bluez.Device1" not in ifaces:
                continue
            dev = ifaces["org.bluez.Device1"]
            if not dev.get("Paired", False) or not dev.get("Connected", False):
                continue
            uuids = [str(u).lower() for u in dev.get("UUIDs", [])]
            # AVRCP Target = phone is controllable
            if any(u.startswith("0000110c") for u in uuids):
                # Adapter is the parent of the device path:
                # /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF -> hci0
                adapter = path.split("/")[3] if len(path.split("/")) > 3 else "hci0"
                return str(dev.get("Address", "")), adapter
    except dbus.DBusException:
        pass
    return None, None


def call_bt_media(mac: str, adapter: str, action: str,
                  extra: list[str] | None = None) -> tuple[int, str, str]:
    """Run bt-media and return (exit_code, stdout, stderr)."""
    cmd = [f"{_HOME}/bin/bt-media", mac, "--adapter", adapter]
    if action == "status":
        cmd.append("--json")
    elif action == "current":
        # Same as status but more readable
        pass
    elif action in ("play", "pause", "stop"):
        cmd.append(f"--{action}")
    elif action == "next":
        cmd.append("--next")
    elif action == "prev":
        cmd.append("--prev")
    elif action == "ff":
        cmd.append("--ff")
    elif action == "rew":
        cmd.append("--rew")
    elif action == "watch":
        cmd.append("--watch")
    if extra:
        cmd.extend(extra)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return p.returncode, p.stdout, p.stderr


def call_bt_adb_media(action: str) -> tuple[int, str, str]:
    """Run bt-adb-media (ADB-based control)."""
    cmd = [f"{_HOME}/bin/bt-adb-media"]
    # bt-adb-media takes positional action: status/play/pause/play-pause/next/previous/stop
    if action == "prev":
        cmd.append("previous")
    elif action == "current":
        cmd.append("status")
    elif action in ("play", "pause", "play-pause", "next", "stop", "status"):
        cmd.append(action)
    else:
        return 2, "", f"action '{action}' not supported via ADB"
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return p.returncode, p.stdout, p.stderr


def call_bt_volume(mac: str, level: int | None = None) -> tuple[int, str, str]:
    cmd = [f"{_HOME}/bin/bt-volume"]
    if level is not None:
        cmd.extend([str(level)])
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return p.returncode, p.stdout, p.stderr


def emit(success: bool, action: str, transport: str,
         stdout: str, stderr: str, as_json: bool, extra: dict | None = None):
    if as_json:
        payload = {
            "ok": success,
            "action": action,
            "transport": transport,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }
        if extra:
            payload.update(extra)
        print(json.dumps(payload, indent=2))
    else:
        if stdout.strip():
            print(stdout.rstrip())
        if not success and stderr.strip():
            print(f"warn: {stderr.strip()}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="High-level media control for Agent (auto-pick phone, BT or ADB).")
    ap.add_argument("action", choices=sorted(VALID_ACTIONS),
                    help="What to do: status, play, pause, next, prev, etc.")
    ap.add_argument("level", nargs="?", default=None,
                    help="For 'volume' action: 0-100")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON result")
    ap.add_argument("--prefer", choices=["bt", "adb", "auto"], default="auto",
                    help="Force transport. Default auto: try BT/AVRCP first, fall back to ADB.")
    args = ap.parse_args()

    # Volume is special-cased
    if args.action == "volume":
        if args.level is None:
            ap.error("volume action requires a level (0-100)")
        try:
            level = int(args.level)
        except ValueError:
            ap.error("level must be an integer 0-100")
            return 2
        rc, out, err = call_bt_volume("", level)
        emit(rc == 0, "volume", "bt", out, err, args.json,
             {"level": level})
        return rc

    # All other actions need a phone
    mac, adapter = find_connected_phone()
    if not mac:
        emit(False, args.action, "none", "",
             "No connected paired phone with AVRCP support", args.json)
        return 2

    # Decide transport
    if args.prefer == "adb":
        rc, out, err = call_bt_adb_media(args.action)
        emit(rc == 0, args.action, "adb", out, err, args.json,
             {"phone": mac})
        return rc

    if args.prefer == "bt":
        rc, out, err = call_bt_media(mac, adapter, args.action)
        emit(rc == 0, args.action, "bt", out, err, args.json,
             {"phone": mac, "adapter": adapter})
        return rc

    # auto: try BT/AVRCP first
    rc, out, err = call_bt_media(mac, adapter, args.action)
    if rc == 0:
        # Check if the BT response indicates "no active media player"
        if "no MediaPlayer1" in out or "no active media player" in out.lower():
            # Fall back to ADB
            rc2, out2, err2 = call_bt_adb_media(args.action)
            emit(rc2 == 0, args.action, "adb-fallback", out2, err2, args.json,
                 {"phone": mac, "bt_attempt": "no media player active"})
            return rc2
        emit(True, args.action, "bt", out, err, args.json,
             {"phone": mac, "adapter": adapter})
        return 0

    # BT errored — try ADB
    rc2, out2, err2 = call_bt_adb_media(args.action)
    emit(rc2 == 0, args.action, "adb-fallback", out2, err2, args.json,
         {"phone": mac, "bt_error": err.strip()[:100]})
    return rc2


if __name__ == "__main__":
    sys.exit(main())
