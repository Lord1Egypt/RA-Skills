#!/usr/bin/env python3
"""bt-pan — Use a paired phone as an internet uplink via Bluetooth PAN.

When the phone advertises NAP (0x1116 = Network Access Point), we can
connect to it as a PANU (User) and the kernel creates a bnep0 network
interface that we can DHCP on.

Usage:
  bt-pan up MAC                   # connect, bring up bnep0, run DHCP
  bt-pan down MAC                 # disconnect PAN, deconfigure interface
  bt-pan status                   # show current state

Phone-side prerequisite (one-time):
  - Phone must have BT-tethering enabled
  - Settings → Connections → Mobile Hotspot and Tethering → Bluetooth tethering ON
"""
from __future__ import annotations
import argparse, os, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import dbus
from bt_lib import (BLUEZ_SERVICE, get_bus, adapter_path, _mac_to_device_path,
                    DEVICE_IFACE)

NETWORK_IFACE = "org.bluez.Network1"


def _sudo(*args: str) -> tuple[int, str]:
    """Run a command via sudo.

    Reads password from SUDO_PASS env if set; otherwise relies on sudo's
    own prompt or a passwordless-sudo rule. NEVER hardcodes a password.

    Recommended: configure passwordless sudo for ip + dhclient, e.g.:
      <youruser> ALL=(root) NOPASSWD: /usr/sbin/ip, /usr/sbin/dhclient
    """
    pw = os.environ.get("SUDO_PASS")
    cmd = ["sudo", "-S" if pw else "-n", *args]
    stdin_input = (pw + "\n") if pw else None
    p = subprocess.run(cmd, input=stdin_input, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def pan_up(mac: str, adapter: str = "hci0") -> dict:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise RuntimeError(f"adapter {adapter!r} not found")
    dpath = _mac_to_device_path(apath, mac)
    dobj = bus.get_object(BLUEZ_SERVICE, dpath)
    net = dbus.Interface(dobj, NETWORK_IFACE)
    iface = str(net.Connect("nap"))   # "nap" = Network Access Point profile
    return {"interface": iface}


def pan_down(mac: str, adapter: str = "hci0") -> None:
    bus = get_bus()
    apath = adapter_path(adapter)
    dpath = _mac_to_device_path(apath, mac)
    dobj = bus.get_object(BLUEZ_SERVICE, dpath)
    net = dbus.Interface(dobj, NETWORK_IFACE)
    net.Disconnect()


def main() -> int:
    ap = argparse.ArgumentParser(description="BT PAN — phone-as-internet-uplink")
    ap.add_argument("op", choices=["up", "down", "status"])
    ap.add_argument("mac", nargs="?")
    ap.add_argument("--adapter", default="hci0")
    args = ap.parse_args()

    if args.op == "status":
        rc, out = _sudo("ip", "link", "show", "type", "bridge_slave")
        # bnep is not a bridge; try direct
        rc, out = _sudo("ip", "-br", "link", "show")
        for line in out.splitlines():
            if line.startswith("bnep"):
                print(line)
        # Also show route table
        rc, out = _sudo("ip", "-br", "route")
        print("\n--- Routes ---")
        for line in out.splitlines():
            if "bnep" in line or "default" in line:
                print(line)
        return 0

    if not args.mac:
        sys.stderr.write("MAC required for up/down\n")
        return 2

    if args.op == "up":
        try:
            r = pan_up(args.mac, args.adapter)
        except Exception as e:
            sys.stderr.write(f"PAN connect failed: {e}\n"
                             f"  Hint: ensure 'Bluetooth tethering' is ON on the phone.\n")
            return 1
        iface = r["interface"]
        print(f"connected, interface = {iface}")

        # Bring up + DHCP
        time.sleep(1)
        _sudo("ip", "link", "set", iface, "up")
        rc, out = _sudo("dhclient", "-v", iface)
        print(out[-500:] if len(out) > 500 else out)

        # Show resulting IP
        rc, out = _sudo("ip", "-br", "addr", "show", iface)
        print(out)
        return 0

    if args.op == "down":
        # Release DHCP
        _sudo("dhclient", "-r", "bnep0")
        try:
            pan_down(args.mac, args.adapter)
        except Exception as e:
            sys.stderr.write(f"PAN disconnect failed: {e}\n")
            return 1
        print("disconnected")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
