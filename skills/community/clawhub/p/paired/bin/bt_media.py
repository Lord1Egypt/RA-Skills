"""
bt_media.py — AVRCP / MediaPlayer1 control for the bluetooth skill.

When a phone connects with AVRCP-CT (controller) advertised, BlueZ creates a
MediaPlayer1 D-Bus object exposing the phone's currently-active player. We
can:
  - Read current track metadata (Title, Artist, Album, Duration, Position)
  - Read playback status (playing, paused, stopped)
  - Send transport commands (Play, Pause, Stop, Next, Previous)
  - Read playlist state

BlueZ paths look like:
  /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF/player0
"""
from __future__ import annotations
import sys
from typing import Optional

import dbus

from bt_lib import (BLUEZ_SERVICE, OM_IFACE, PROPS_IFACE, get_bus,
                    adapter_path, _mac_to_device_path, _device_path_to_mac)

MEDIA_PLAYER_IFACE = "org.bluez.MediaPlayer1"
MEDIA_TRANSPORT_IFACE = "org.bluez.MediaTransport1"
MEDIA_CONTROL_IFACE = "org.bluez.MediaControl1"  # legacy AVRCP1.3
MEDIA_FOLDER_IFACE = "org.bluez.MediaFolder1"
MEDIA_ITEM_IFACE = "org.bluez.MediaItem1"


def _dbus_to_py(v):
    if isinstance(v, dbus.Dictionary):
        return {str(k): _dbus_to_py(x) for k, x in v.items()}
    if isinstance(v, (dbus.Array, list, tuple)):
        return [_dbus_to_py(x) for x in v]
    if isinstance(v, (dbus.String, dbus.ObjectPath)):
        return str(v)
    if isinstance(v, dbus.Boolean):
        return bool(v)
    if isinstance(v, (dbus.Int16, dbus.Int32, dbus.Int64,
                       dbus.UInt16, dbus.UInt32, dbus.UInt64,
                       dbus.Byte)):
        return int(v)
    if isinstance(v, dbus.Double):
        return float(v)
    return v


def find_player(mac: str, adapter: str = "hci0") -> Optional[dict]:
    """Find the MediaPlayer1 object for a given device MAC.

    Returns dict with path + properties, or None if no player object exists.
    """
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise RuntimeError(f"adapter {adapter!r} not found")
    dpath = _mac_to_device_path(apath, mac)
    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/"), OM_IFACE)
    for path, ifaces in om.GetManagedObjects().items():
        if not path.startswith(dpath + "/"):
            continue
        if MEDIA_PLAYER_IFACE in ifaces:
            return {
                "path": str(path),
                **{str(k): _dbus_to_py(v)
                   for k, v in ifaces[MEDIA_PLAYER_IFACE].items()},
            }
    return None


def find_transport(mac: str, adapter: str = "hci0") -> Optional[dict]:
    """Find the MediaTransport1 (audio stream metadata)."""
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise RuntimeError(f"adapter {adapter!r} not found")
    dpath = _mac_to_device_path(apath, mac)
    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/"), OM_IFACE)
    for path, ifaces in om.GetManagedObjects().items():
        if not path.startswith(dpath + "/"):
            continue
        if MEDIA_TRANSPORT_IFACE in ifaces:
            return {
                "path": str(path),
                **{str(k): _dbus_to_py(v)
                   for k, v in ifaces[MEDIA_TRANSPORT_IFACE].items()},
            }
    return None


def player_action(mac: str, action: str, adapter: str = "hci0") -> None:
    """Send an AVRCP transport command.

    action: Play | Pause | Stop | Next | Previous | FastForward | Rewind
    """
    p = find_player(mac, adapter)
    if p is None:
        raise RuntimeError(
            f"No MediaPlayer1 for {mac}. Phone might not have AVRCP active "
            f"or no media is loaded."
        )
    bus = get_bus()
    pobj = bus.get_object(BLUEZ_SERVICE, p["path"])
    iface = dbus.Interface(pobj, MEDIA_PLAYER_IFACE)
    method = getattr(iface, action)
    method()


def media_status(mac: str, adapter: str = "hci0") -> dict:
    """Get current track + playback status as a flat dict."""
    p = find_player(mac, adapter)
    if p is None:
        return {"connected": False, "reason": "no MediaPlayer1 object"}
    track = p.get("Track", {}) or {}
    return {
        "connected": True,
        "player_path": p["path"],
        "name": p.get("Name", ""),
        "type": p.get("Type", ""),
        "subtype": p.get("Subtype", ""),
        "status": p.get("Status", "unknown"),
        "position_ms": p.get("Position", 0),
        "shuffle": p.get("Shuffle", "off"),
        "repeat": p.get("Repeat", "off"),
        "title": track.get("Title", ""),
        "artist": track.get("Artist", ""),
        "album": track.get("Album", ""),
        "genre": track.get("Genre", ""),
        "duration_ms": track.get("Duration", 0),
        "track_number": track.get("TrackNumber", 0),
        "track_count": track.get("NumberOfTracks", 0),
    }
