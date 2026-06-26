"""
bt_obex.py — OBEX file transfer (push / pull / browse) for the bluetooth skill.

Talks to bluez-obexd via D-Bus on the SESSION bus (not the system bus —
this is critical: org.bluez.obex is per-user). Implements:

  * push_file(mac, path)             — OBEX Object Push (OPP, profile 0x1105)
  * pull_file(mac, remote_name)      — OBEX FTP (profile 0x1106), receive a file
  * list_folder(mac, remote_path)    — Browse the device's filesystem (FTP)
  * register_receive_agent()         — Sit in the foreground, accept incoming pushes,
                                       save to ~/Downloads/bluetooth/

Wraps `org.bluez.obex.Client1`, `org.bluez.obex.Session1`, `Transfer1`,
`ObjectPush1`, `FileTransfer1`, and the agent registration interface.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Optional

import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GLib

OBEX_BUS = "org.bluez.obex"
OBEX_PATH = "/org/bluez/obex"
CLIENT_IFACE = "org.bluez.obex.Client1"
SESSION_IFACE = "org.bluez.obex.Session1"
TRANSFER_IFACE = "org.bluez.obex.Transfer1"
OBJECT_PUSH_IFACE = "org.bluez.obex.ObjectPush1"
FILE_TRANSFER_IFACE = "org.bluez.obex.FileTransfer1"
AGENT_MANAGER_IFACE = "org.bluez.obex.AgentManager1"
AGENT_IFACE = "org.bluez.obex.Agent1"
PROPS_IFACE = "org.freedesktop.DBus.Properties"

DEFAULT_INCOMING = Path(os.path.expanduser("~/Downloads/bluetooth"))


def _session_bus():
    if not getattr(_session_bus, "_set_default", False):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        _session_bus._set_default = True
    return dbus.SessionBus()


def _client():
    bus = _session_bus()
    return dbus.Interface(bus.get_object(OBEX_BUS, OBEX_PATH), CLIENT_IFACE)


def _create_session(mac: str, target: str) -> str:
    """Create an OBEX session. target ∈ {opp, ftp, pbap, map, sync}."""
    args = dbus.Dictionary({"Target": target}, signature="sv")
    return str(_client().CreateSession(mac.upper(), args))


def _wait_for_transfer(transfer_path: str, timeout: float = 120.0) -> dict:
    """Block until the transfer completes; return the final properties dict."""
    bus = _session_bus()
    tobj = bus.get_object(OBEX_BUS, transfer_path)
    props_iface = dbus.Interface(tobj, PROPS_IFACE)

    loop = GLib.MainLoop()
    final: dict = {}

    def _on_props(iface, changed, invalidated):
        if iface != TRANSFER_IFACE:
            return
        status = changed.get("Status")
        if status:
            final["status"] = str(status)
            if str(status) in ("complete", "error"):
                loop.quit()

    sig = bus.add_signal_receiver(
        _on_props,
        signal_name="PropertiesChanged",
        dbus_interface=PROPS_IFACE,
        path=transfer_path,
    )

    # Timeout
    GLib.timeout_add_seconds(int(timeout), loop.quit)

    # Initial state check (transfer may already have completed)
    try:
        all_props = props_iface.GetAll(TRANSFER_IFACE)
        if str(all_props.get("Status", "")) in ("complete", "error"):
            final.update(dict(all_props))
            sig.remove()
            return {k: str(v) for k, v in all_props.items()}
    except dbus.DBusException:
        pass

    loop.run()
    sig.remove()

    try:
        all_props = props_iface.GetAll(TRANSFER_IFACE)
        return {k: str(v) for k, v in all_props.items()}
    except dbus.DBusException:
        return final


def push_file(mac: str, file_path: str, timeout: float = 120.0) -> dict:
    """OBEX Object Push: send a file to a paired phone/device."""
    file_path = os.path.abspath(os.path.expanduser(file_path))
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    bus = _session_bus()
    session_path = _create_session(mac, "opp")
    sobj = bus.get_object(OBEX_BUS, session_path)
    pusher = dbus.Interface(sobj, OBJECT_PUSH_IFACE)

    transfer_path, _props = pusher.SendFile(file_path)
    result = _wait_for_transfer(str(transfer_path), timeout=timeout)

    # Clean up session
    try:
        _client().RemoveSession(session_path)
    except dbus.DBusException:
        pass

    return {
        "mac": mac.upper(),
        "file": file_path,
        "size": os.path.getsize(file_path),
        "transfer_status": result.get("Status", "unknown"),
        "transferred": result.get("Transferred"),
    }


def pull_file(mac: str, remote_name: str, save_to: Optional[str] = None,
              timeout: float = 120.0) -> dict:
    """OBEX FTP: pull a file by name from the device. (FTP profile, not OPP.)"""
    if save_to is None:
        save_to = str(DEFAULT_INCOMING / os.path.basename(remote_name))
    save_to = os.path.abspath(os.path.expanduser(save_to))
    Path(save_to).parent.mkdir(parents=True, exist_ok=True)

    bus = _session_bus()
    session_path = _create_session(mac, "ftp")
    sobj = bus.get_object(OBEX_BUS, session_path)
    ftp = dbus.Interface(sobj, FILE_TRANSFER_IFACE)

    transfer_path, _props = ftp.GetFile(save_to, remote_name)
    result = _wait_for_transfer(str(transfer_path), timeout=timeout)

    try:
        _client().RemoveSession(session_path)
    except dbus.DBusException:
        pass

    return {
        "mac": mac.upper(),
        "remote": remote_name,
        "saved_to": save_to,
        "status": result.get("Status", "unknown"),
    }


def list_folder(mac: str, folder: str = "/") -> list[dict]:
    """OBEX FTP: list folder contents on the device."""
    bus = _session_bus()
    session_path = _create_session(mac, "ftp")
    sobj = bus.get_object(OBEX_BUS, session_path)
    ftp = dbus.Interface(sobj, FILE_TRANSFER_IFACE)
    try:
        if folder != "/":
            ftp.ChangeFolder(folder)
        listing = ftp.ListFolder()
    finally:
        try:
            _client().RemoveSession(session_path)
        except dbus.DBusException:
            pass
    out = []
    for entry in listing:
        out.append({k: str(v) for k, v in entry.items()})
    return out


# ---------------------------------------------------------------------------
# Receive agent — accepts incoming pushes, saves to ~/Downloads/bluetooth
# ---------------------------------------------------------------------------
class ObexReceiveAgent(dbus.service.Object):
    AGENT_PATH = "/openclaw/obex/agent"

    def __init__(self, bus, save_dir: Path):
        super().__init__(bus, self.AGENT_PATH)
        self.save_dir = save_dir
        save_dir.mkdir(parents=True, exist_ok=True)
        self._pending_paths: dict[str, str] = {}

    def _log(self, msg):
        sys.stderr.write(f"[obex-recv] {msg}\n")
        sys.stderr.flush()

    @dbus.service.method(AGENT_IFACE, in_signature="o", out_signature="s")
    def AuthorizePush(self, transfer_path):
        """Called when a peer wants to push a file. Return target filesystem path."""
        bus = _session_bus()
        tobj = bus.get_object(OBEX_BUS, transfer_path)
        props = dbus.Interface(tobj, PROPS_IFACE)
        try:
            name = str(props.Get(TRANSFER_IFACE, "Name"))
            size = int(props.Get(TRANSFER_IFACE, "Size"))
        except dbus.DBusException:
            name = f"unknown-{int(time.time())}"
            size = 0
        # Make name safe
        safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in name) or f"recv-{int(time.time())}"
        target = self.save_dir / safe
        # If exists, append timestamp
        if target.exists():
            ts = time.strftime("%Y%m%d-%H%M%S")
            target = target.with_name(f"{target.stem}-{ts}{target.suffix}")
        self._pending_paths[str(transfer_path)] = str(target)
        self._log(f"AuthorizePush {name} ({size} bytes) -> {target}")
        return str(target)

    @dbus.service.method(AGENT_IFACE, in_signature="", out_signature="")
    def Cancel(self):
        self._log("Cancel")

    @dbus.service.method(AGENT_IFACE, in_signature="", out_signature="")
    def Release(self):
        self._log("Release")


def run_receive_agent(save_dir: Optional[str] = None) -> int:
    """Foreground: register an OBEX agent and wait for incoming files. Ctrl-C to stop."""
    save_path = Path(save_dir or DEFAULT_INCOMING).expanduser()
    bus = _session_bus()
    agent = ObexReceiveAgent(bus, save_path)
    manager = dbus.Interface(bus.get_object(OBEX_BUS, OBEX_PATH), AGENT_MANAGER_IFACE)
    try:
        manager.RegisterAgent(ObexReceiveAgent.AGENT_PATH)
    except dbus.DBusException as e:
        if "AlreadyExists" in str(e):
            sys.stderr.write("OBEX agent already registered (another receiver running?)\n")
            return 1
        raise
    sys.stderr.write(f"[obex-recv] listening, saving incoming files to {save_path}\n")

    loop = GLib.MainLoop()

    def _shutdown(*_a):
        try:
            manager.UnregisterAgent(ObexReceiveAgent.AGENT_PATH)
        except dbus.DBusException:
            pass
        loop.quit()

    import signal as _signal
    _signal.signal(_signal.SIGTERM, _shutdown)
    _signal.signal(_signal.SIGINT, _shutdown)

    try:
        loop.run()
    finally:
        try:
            manager.UnregisterAgent(ObexReceiveAgent.AGENT_PATH)
        except dbus.DBusException:
            pass
    return 0
