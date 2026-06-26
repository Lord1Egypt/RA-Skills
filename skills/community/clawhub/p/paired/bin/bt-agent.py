#!/usr/bin/env python3
"""
bt-agent — BlueZ pairing agent daemon for the OpenClaw `bluetooth` skill.

Runs as a user systemd service. Registers a D-Bus agent so that pair
requests from peer devices (phones, headphones, beacons) are handled
without a human at the keyboard.

Modes:
  --mode pin    (default) KeyboardDisplay agent.
                Surfaces passkey/PIN prompts via:
                  * a JSON file at ~/.cache/bluetooth/pending-passkey.json
                  * stderr (so journalctl shows it)
                Confirms when ~/.cache/bluetooth/confirm exists, denies when
                ~/.cache/bluetooth/deny exists. Times out after 60s -> deny.
  --mode auto   NoInputNoOutput agent. Auto-confirms pairing.
                Works for: BLE peripherals, headphones, speakers, most
                beacons, and Just Works pairings.
                IMPORTANT: --mode auto without --device-filter will accept
                ANY incoming pairing request. Always pair --mode auto with
                --device-filter unless you genuinely want a wide-open agent
                for a brief, supervised pairing window. Pass --i-mean-it to
                acknowledge that risk and use --mode auto without a filter.

Both modes accept any service authorisation (so an A2DP/HFP profile just works
once paired+trusted).

Useful CLI flags:
  --device-filter=AA:BB:CC:DD:EE:FF
        Only auto-confirm pair requests from this MAC; everything else is
        denied. Useful when you want a one-shot "let me pair THIS phone".
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path

# Ensure we can import from the same dir
sys.path.insert(0, str(Path(__file__).resolve().parent))

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

from bt_lib import (
    BLUEZ_SERVICE, AGENT_MANAGER_IFACE, AGENT_IFACE, _device_path_to_mac,
)

AGENT_PATH = "/openclaw/bluetooth/agent"
DEFAULT_CACHE = Path(os.path.expanduser("~/.cache/bluetooth"))
PENDING_FILE = DEFAULT_CACHE / "pending-passkey.json"
CONFIRM_FILE = DEFAULT_CACHE / "confirm"
DENY_FILE = DEFAULT_CACHE / "deny"


def _log(msg: str) -> None:
    sys.stderr.write(f"[bt-agent] {msg}\n")
    sys.stderr.flush()


class BluezAgent(dbus.service.Object):
    def __init__(self, bus, path, mode: str = "auto",
                 device_filter: str | None = None):
        super().__init__(bus, path)
        self.mode = mode
        self.device_filter = device_filter.upper() if device_filter else None
        DEFAULT_CACHE.mkdir(parents=True, exist_ok=True)
        # Wipe any stale confirm/deny markers from a previous invocation
        for f in (PENDING_FILE, CONFIRM_FILE, DENY_FILE):
            f.unlink(missing_ok=True)

    # --- Helpers --------------------------------------------------------
    def _allowed(self, dev_path: str) -> bool:
        """Return True if the device is allowed to pair under our policy."""
        if self.device_filter is None:
            return True
        mac = (_device_path_to_mac(dev_path) or "").upper()
        if mac == self.device_filter:
            return True
        _log(f"deny: {mac} not in filter {self.device_filter!r}")
        return False

    def _wait_for_decision(self, timeout: float = 60.0) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            if CONFIRM_FILE.exists():
                CONFIRM_FILE.unlink(missing_ok=True)
                return True
            if DENY_FILE.exists():
                DENY_FILE.unlink(missing_ok=True)
                return False
            time.sleep(0.25)
        _log("decision timeout — denying")
        return False

    def _publish_pending(self, payload: dict) -> None:
        with open(PENDING_FILE, "w") as f:
            json.dump(payload, f, indent=2)
        _log(f"pending decision: {payload}")
        _log(f"to confirm: touch {CONFIRM_FILE}")
        _log(f"to deny:    touch {DENY_FILE}")

    # --- D-Bus methods (BlueZ Agent1 interface) -------------------------
    @dbus.service.method(AGENT_IFACE, in_signature="", out_signature="")
    def Release(self):
        _log("Release")

    @dbus.service.method(AGENT_IFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        _log(f"AuthorizeService {device} uuid={uuid} -> ALLOW")
        # Trusting = auto-authorising future profile use
        if not self._allowed(device):
            raise dbus.DBusException(
                "org.bluez.Error.Rejected", "device filter blocked"
            )

    @dbus.service.method(AGENT_IFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        if self.mode == "auto":
            _log(f"RequestPinCode {device} -> 0000 (auto)")
            return "0000"
        mac = _device_path_to_mac(device) or device
        self._publish_pending({"event": "RequestPinCode", "mac": mac})
        _log(f"RequestPinCode {mac} -> waiting decision")
        ok = self._wait_for_decision()
        if not ok:
            raise dbus.DBusException("org.bluez.Error.Rejected", "user denied")
        return "0000"

    @dbus.service.method(AGENT_IFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        if self.mode == "auto":
            _log(f"RequestPasskey {device} -> 0 (auto)")
            return dbus.UInt32(0)
        mac = _device_path_to_mac(device) or device
        self._publish_pending({"event": "RequestPasskey", "mac": mac})
        ok = self._wait_for_decision()
        if not ok:
            raise dbus.DBusException("org.bluez.Error.Rejected", "user denied")
        return dbus.UInt32(0)

    @dbus.service.method(AGENT_IFACE, in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device, passkey, entered):
        mac = _device_path_to_mac(device) or device
        _log(f"DisplayPasskey {mac} passkey={passkey:06d} entered={entered}")
        self._publish_pending({
            "event": "DisplayPasskey",
            "mac": mac,
            "passkey": int(passkey),
            "entered": int(entered),
        })

    @dbus.service.method(AGENT_IFACE, in_signature="os", out_signature="")
    def DisplayPinCode(self, device, pincode):
        mac = _device_path_to_mac(device) or device
        _log(f"DisplayPinCode {mac} pin={pincode}")
        self._publish_pending({
            "event": "DisplayPinCode",
            "mac": mac,
            "pincode": str(pincode),
        })

    @dbus.service.method(AGENT_IFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        mac = _device_path_to_mac(device) or device
        if not self._allowed(device):
            raise dbus.DBusException(
                "org.bluez.Error.Rejected", "device filter blocked"
            )
        if self.mode == "auto":
            _log(f"RequestConfirmation {mac} passkey={passkey:06d} -> AUTO-CONFIRM")
            return
        self._publish_pending({
            "event": "RequestConfirmation",
            "mac": mac,
            "passkey": int(passkey),
        })
        ok = self._wait_for_decision()
        if not ok:
            raise dbus.DBusException("org.bluez.Error.Rejected", "user denied")
        _log(f"RequestConfirmation {mac} -> CONFIRMED")

    @dbus.service.method(AGENT_IFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        mac = _device_path_to_mac(device) or device
        if not self._allowed(device):
            raise dbus.DBusException(
                "org.bluez.Error.Rejected", "device filter blocked"
            )
        if self.mode == "auto":
            _log(f"RequestAuthorization {mac} -> AUTO-ALLOW")
            return
        self._publish_pending({"event": "RequestAuthorization", "mac": mac})
        ok = self._wait_for_decision()
        if not ok:
            raise dbus.DBusException("org.bluez.Error.Rejected", "user denied")

    @dbus.service.method(AGENT_IFACE, in_signature="", out_signature="")
    def Cancel(self):
        _log("Cancel")
        for f in (PENDING_FILE,):
            f.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="BlueZ pairing agent for the bluetooth skill")
    # Default is now `pin` (interactive) for safety. `auto` requires explicit opt-in.
    ap.add_argument("--mode", default="pin", choices=["auto", "pin"])
    ap.add_argument("--device-filter", default=None,
                    help="Only auto-confirm pairings from this MAC")
    ap.add_argument("--i-mean-it", action="store_true",
                    help="Required to use --mode auto without --device-filter")
    ap.add_argument("--make-pairable", action="store_true",
                    help="Set Pairable=on, PairableTimeout=180 on hci0 then exit")
    args = ap.parse_args()

    # Safety check: refuse wide-open auto-pairing unless user explicitly opted in.
    if args.mode == "auto" and not args.device_filter and not args.i_mean_it:
        _log("REFUSING: --mode auto without --device-filter is wide-open pairing.")
        _log("Either: (a) supply --device-filter MAC, or (b) pass --i-mean-it to")
        _log("acknowledge the risk and proceed (e.g. for a brief supervised pair).")
        return 2

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    if args.make_pairable:
        from bt_lib import adapter_path, ADAPTER_IFACE, PROPS_IFACE
        ap_p = adapter_path("hci0")
        aobj = bus.get_object(BLUEZ_SERVICE, ap_p)
        props = dbus.Interface(aobj, PROPS_IFACE)
        props.Set(ADAPTER_IFACE, "Pairable", dbus.Boolean(True))
        props.Set(ADAPTER_IFACE, "PairableTimeout", dbus.UInt32(180))
        props.Set(ADAPTER_IFACE, "Discoverable", dbus.Boolean(True))
        props.Set(ADAPTER_IFACE, "DiscoverableTimeout", dbus.UInt32(180))
        _log("hci0: Pairable=on Discoverable=on (180s)")
        return 0

    agent = BluezAgent(bus, AGENT_PATH, mode=args.mode,
                       device_filter=args.device_filter)
    capability = "NoInputNoOutput" if args.mode == "auto" else "KeyboardDisplay"
    manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/org/bluez"),
                             AGENT_MANAGER_IFACE)
    try:
        manager.RegisterAgent(AGENT_PATH, capability)
    except dbus.DBusException as e:
        if "AlreadyExists" in str(e):
            _log("agent already registered (probably another instance) — exiting")
            return 1
        raise
    manager.RequestDefaultAgent(AGENT_PATH)
    _log(f"registered as default agent (capability={capability}, mode={args.mode}"
         + (f", filter={args.device_filter}" if args.device_filter else "")
         + ")")

    loop = GLib.MainLoop()

    def _shutdown(*_a):
        _log("shutting down")
        try:
            manager.UnregisterAgent(AGENT_PATH)
        except dbus.DBusException:
            pass
        loop.quit()

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    try:
        loop.run()
    finally:
        try:
            manager.UnregisterAgent(AGENT_PATH)
        except dbus.DBusException:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
