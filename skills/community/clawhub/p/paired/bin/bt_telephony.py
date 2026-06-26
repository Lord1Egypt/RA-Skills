"""
bt_telephony.py — ofono telephony for the OpenClaw `bluetooth` skill.

ofono provides a D-Bus API on the SYSTEM bus (org.ofono) that exposes
HFP modems, voice calls, and message manager. When a paired phone
connects with the Hands-Free profile, ofono auto-creates a modem object
for it whose path embeds the phone's BD address.

This module wraps:
  * list_modems()                 — enumerate ofono modems (1 per HFP phone)
  * modem_for_mac(mac)            — find the modem whose BD matches
  * dial(modem, number)           — start an outgoing call
  * answer(modem) / hangup(modem) — control current call
  * list_calls(modem)             — list current voice calls
  * sms_send(modem, num, text)    — outgoing SMS via MessageManager
  * sms_list(modem)               — list inbound SMS (recent only — ofono
                                    doesn't keep history; use MAP via OBEX
                                    for historical SMS — see bt_obex_msg.py)

Requires: dbus-1 policy at /etc/dbus-1/system.d/ofono-${USER}.conf
allowing user `${USER}` to send to `org.ofono`.
"""
from __future__ import annotations

import sys
from typing import Optional

import dbus
import dbus.mainloop.glib


OFONO_BUS = "org.ofono"
MANAGER_IFACE = "org.ofono.Manager"
MODEM_IFACE = "org.ofono.Modem"
VOICE_CALL_MGR_IFACE = "org.ofono.VoiceCallManager"
VOICE_CALL_IFACE = "org.ofono.VoiceCall"
MESSAGE_MGR_IFACE = "org.ofono.MessageManager"
HANDSFREE_IFACE = "org.ofono.Handsfree"
NETWORK_REG_IFACE = "org.ofono.NetworkRegistration"


def _bus():
    if not getattr(_bus, "_set_default", False):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        _bus._set_default = True
    return dbus.SystemBus()


def list_modems() -> list[dict]:
    bus = _bus()
    mgr = dbus.Interface(bus.get_object(OFONO_BUS, "/"), MANAGER_IFACE)
    out = []
    for path, props in mgr.GetModems():
        d = {"path": str(path)}
        for k, v in props.items():
            d[str(k)] = _dbus_to_py(v)
        out.append(d)
    return out


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


def modem_for_mac(mac: str) -> Optional[dict]:
    """Find the ofono modem whose path contains the BD address of the given MAC.

    ofono path format for HFP modems: /hfp/<adapter_bd>/dev_<peer_bd>
    e.g. /hfp/441CA8A51398/dev_AABBCCDDEEFF
    """
    target = mac.upper().replace(":", "")
    for m in list_modems():
        if target in m["path"].upper().replace("_", ""):
            return m
    return None


def power_modem(modem_path: str, on: bool = True) -> None:
    bus = _bus()
    mobj = bus.get_object(OFONO_BUS, modem_path)
    miface = dbus.Interface(mobj, MODEM_IFACE)
    miface.SetProperty("Powered", dbus.Boolean(on))


def online_modem(modem_path: str, on: bool = True) -> None:
    bus = _bus()
    mobj = bus.get_object(OFONO_BUS, modem_path)
    miface = dbus.Interface(mobj, MODEM_IFACE)
    miface.SetProperty("Online", dbus.Boolean(on))


# ---------------------------------------------------------------------------
# Voice calls
# ---------------------------------------------------------------------------
def list_calls(modem_path: str) -> list[dict]:
    bus = _bus()
    mgr = dbus.Interface(bus.get_object(OFONO_BUS, modem_path),
                          VOICE_CALL_MGR_IFACE)
    out = []
    for path, props in mgr.GetCalls():
        d = {"path": str(path)}
        for k, v in props.items():
            d[str(k)] = _dbus_to_py(v)
        out.append(d)
    return out


def dial(modem_path: str, number: str, hide_caller_id: bool = False) -> str:
    """Start an outgoing call. Returns the call's D-Bus path."""
    bus = _bus()
    mgr = dbus.Interface(bus.get_object(OFONO_BUS, modem_path),
                          VOICE_CALL_MGR_IFACE)
    hide = "enabled" if hide_caller_id else "default"
    call_path = mgr.Dial(number, hide)
    return str(call_path)


def answer_first(modem_path: str) -> Optional[str]:
    """Answer the first incoming call. Returns its path, or None if none ringing."""
    bus = _bus()
    for c in list_calls(modem_path):
        if c.get("State") in ("incoming", "waiting"):
            cobj = bus.get_object(OFONO_BUS, c["path"])
            iface = dbus.Interface(cobj, VOICE_CALL_IFACE)
            iface.Answer()
            return c["path"]
    return None


def hangup_all(modem_path: str) -> int:
    """Terminate every active/incoming/dialing call. Returns count terminated."""
    bus = _bus()
    mgr = dbus.Interface(bus.get_object(OFONO_BUS, modem_path),
                          VOICE_CALL_MGR_IFACE)
    calls = list_calls(modem_path)
    if not calls:
        return 0
    mgr.HangupAll()
    return len(calls)


# ---------------------------------------------------------------------------
# SMS via ofono Message Manager (live, not historical)
# ---------------------------------------------------------------------------
def sms_send(modem_path: str, number: str, text: str) -> str:
    bus = _bus()
    msg = dbus.Interface(bus.get_object(OFONO_BUS, modem_path),
                          MESSAGE_MGR_IFACE)
    return str(msg.SendMessage(number, text))


def sms_list_outgoing(modem_path: str) -> list[dict]:
    """Pending outgoing messages still being delivered."""
    bus = _bus()
    msg = dbus.Interface(bus.get_object(OFONO_BUS, modem_path),
                          MESSAGE_MGR_IFACE)
    out = []
    for path, props in msg.GetMessages():
        d = {"path": str(path)}
        for k, v in props.items():
            d[str(k)] = _dbus_to_py(v)
        out.append(d)
    return out


# ---------------------------------------------------------------------------
# Network / signal
# ---------------------------------------------------------------------------
def network_state(modem_path: str) -> dict:
    bus = _bus()
    mobj = bus.get_object(OFONO_BUS, modem_path)
    try:
        netreg = dbus.Interface(mobj, NETWORK_REG_IFACE)
        props = netreg.GetProperties()
        return {str(k): _dbus_to_py(v) for k, v in props.items()}
    except dbus.DBusException:
        return {}


# ---------------------------------------------------------------------------
# Convenience: get full state of a modem (one dict)
# ---------------------------------------------------------------------------
def modem_state(modem_path: str) -> dict:
    bus = _bus()
    mobj = bus.get_object(OFONO_BUS, modem_path)
    miface = dbus.Interface(mobj, MODEM_IFACE)
    try:
        props = miface.GetProperties()
    except dbus.DBusException as e:
        return {"path": modem_path, "error": str(e)}
    state = {"path": modem_path,
             **{str(k): _dbus_to_py(v) for k, v in props.items()}}
    state["calls"] = list_calls(modem_path) if "VoiceCallManager" in (state.get("Interfaces") or []) else []
    state["network"] = network_state(modem_path)
    return state
