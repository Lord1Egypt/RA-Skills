"""
bt_obex_msg.py — PBAP (contacts) + MAP (SMS) over OBEX, for the bluetooth skill.

Builds on bt_obex.py's session abstraction, but adds session targets:
  - "pbap" (Phone Book Access Profile)   — contacts
  - "map"  (Message Access Profile)       — SMS, MMS, email folders on phone

Phones expose these to a paired+trusted host. iOS exposes PBAP. Android
needs the user to enable "Phonebook access" / "Message access" in the
Bluetooth pair settings on a per-host basis.
"""
from __future__ import annotations

from typing import Optional

import dbus

from bt_obex import (_session_bus, _client, _wait_for_transfer,
                     OBEX_BUS, CLIENT_IFACE)

PBAP_IFACE = "org.bluez.obex.PhonebookAccess1"
MAP_IFACE = "org.bluez.obex.MessageAccess1"
MAP_FOLDER_IFACE = "org.bluez.obex.MessageAccess1"  # same iface, ChDir/ListMessages methods


# ---------------------------------------------------------------------------
# PBAP — contacts
# ---------------------------------------------------------------------------
def pbap_list_contacts(mac: str, repo: str = "internal",
                        max_count: int = 0) -> list[dict]:
    """List contacts from the phone's address book.

    repo: one of 'internal' (phone) or 'sim'.
    max_count: 0 = all (subject to phone's limits).
    """
    bus = _session_bus()
    args = dbus.Dictionary({"Target": "pbap"}, signature="sv")
    session_path = str(_client().CreateSession(mac.upper(), args))
    sobj = bus.get_object(OBEX_BUS, session_path)
    pbap = dbus.Interface(sobj, PBAP_IFACE)

    try:
        # Select the phone book.
        pbap.Select(repo, "pb")
        # The List method returns vcard handles; the Pull method gets the actual cards.
        filters = dbus.Dictionary(
            {"MaxCount": dbus.UInt16(max_count)} if max_count else {},
            signature="sv",
        )
        listing = pbap.List(filters)
    finally:
        try:
            _client().RemoveSession(session_path)
        except dbus.DBusException:
            pass

    out = []
    for entry in listing:
        # entry is (handle: str, name: str)
        out.append({"handle": str(entry[0]), "name": str(entry[1])})
    return out


def pbap_pull_all_vcards(mac: str, repo: str = "internal",
                         save_to: str = None,
                         timeout: float = 60.0) -> dict:
    """Pull the entire phonebook as a single .vcf file."""
    import os
    if save_to is None:
        save_to = os.path.expanduser(f"~/Downloads/bluetooth/{mac.replace(':', '')}-{repo}.vcf")
    os.makedirs(os.path.dirname(save_to), exist_ok=True)

    bus = _session_bus()
    args = dbus.Dictionary({"Target": "pbap"}, signature="sv")
    session_path = str(_client().CreateSession(mac.upper(), args))
    sobj = bus.get_object(OBEX_BUS, session_path)
    pbap = dbus.Interface(sobj, PBAP_IFACE)

    try:
        pbap.Select(repo, "pb")
        filters = dbus.Dictionary({"Format": "vcard30"}, signature="sv")
        transfer_path, _props = pbap.PullAll(save_to, filters)
        result = _wait_for_transfer(str(transfer_path), timeout=timeout)
    finally:
        try:
            _client().RemoveSession(session_path)
        except dbus.DBusException:
            pass

    return {
        "mac": mac.upper(),
        "saved_to": save_to,
        "status": result.get("Status", "unknown"),
        "size": result.get("Size"),
    }


# ---------------------------------------------------------------------------
# MAP — SMS / messages
# ---------------------------------------------------------------------------
def map_list_messages(mac: str, folder: str = "telecom/msg/inbox",
                      max_count: int = 25) -> list[dict]:
    """List recent messages from a folder on the phone (SMS/MMS via MAP)."""
    bus = _session_bus()
    args = dbus.Dictionary({"Target": "map"}, signature="sv")
    session_path = str(_client().CreateSession(mac.upper(), args))
    sobj = bus.get_object(OBEX_BUS, session_path)
    map_iface = dbus.Interface(sobj, MAP_IFACE)

    try:
        map_iface.SetFolder(folder)
        filters = dbus.Dictionary(
            {"MaxCount": dbus.UInt16(max_count)} if max_count else {},
            signature="sv",
        )
        listing = map_iface.ListMessages("", filters)
    finally:
        try:
            _client().RemoveSession(session_path)
        except dbus.DBusException:
            pass

    out = []
    # BlueZ MAP returns a dict {ObjectPath: {properties...}}, not a list of tuples
    if hasattr(listing, "items"):
        for path, props in listing.items():
            d = {"path": str(path)}
            if hasattr(props, "items"):
                for k, v in props.items():
                    d[str(k)] = str(v)
            out.append(d)
    else:
        for entry in listing:
            d = {"path": str(entry[0]) if entry else "?"}
            if len(entry) > 1 and hasattr(entry[1], "items"):
                for k, v in entry[1].items():
                    d[str(k)] = str(v)
            out.append(d)
    return out


def map_send_message(mac: str, number: str, text: str,
                     folder: str = "telecom/msg/outbox",
                     timeout: float = 30.0) -> dict:
    """Send an SMS through the paired phone (MAP profile).

    Note: MAP is the read/management API. For sending, oFono's MessageManager
    on a connected HFP modem is usually more reliable on Android. This MAP
    sender is a fallback when ofono refuses (some phones expose MAP-send but
    not HFP-send, or vice versa).
    """
    import os
    import tempfile
    bus = _session_bus()
    args = dbus.Dictionary({"Target": "map"}, signature="sv")
    session_path = str(_client().CreateSession(mac.upper(), args))
    sobj = bus.get_object(OBEX_BUS, session_path)
    map_iface = dbus.Interface(sobj, MAP_IFACE)

    # Probe whether the MAP server actually accepts writes. Many Android
    # devices (notably Samsung) advertise MAP-MSE but only implement the
    # read-side methods. UpdateInbox is the canonical write-probe.
    try:
        map_iface.UpdateInbox()
    except dbus.DBusException as e:
        if "Not Implemented" in str(e):
            try:
                _client().RemoveSession(session_path)
            except dbus.DBusException:
                pass
            return {
                "mac": mac.upper(),
                "to": number,
                "status": "rejected_read_only",
                "reason": "phone has read-only MAP — UpdateInbox not implemented. "
                          "Samsung deliberately disables MAP write methods. "
                          "SMS-send via MAP is not possible on this phone."
            }

    # Build a minimal bMessage envelope
    bmsg = (
        "BEGIN:BMSG\r\n"
        "VERSION:1.0\r\n"
        "STATUS:READ\r\n"
        "TYPE:SMS_GSM\r\n"
        "FOLDER:telecom/msg/outbox\r\n"
        "BEGIN:VCARD\r\nVERSION:2.1\r\n"
        f"TEL:{number}\r\n"
        "END:VCARD\r\n"
        "BEGIN:BENV\r\n"
        "BEGIN:BBODY\r\n"
        "ENCODING:8BIT\r\n"
        "CHARSET:UTF-8\r\n"
        f"LENGTH:{len(text)}\r\n"
        "BEGIN:MSG\r\n"
        f"{text}\r\n"
        "END:MSG\r\n"
        "END:BBODY\r\n"
        "END:BENV\r\n"
        "END:BMSG\r\n"
    )
    fd, path = tempfile.mkstemp(prefix="bmsg-", suffix=".bmsg")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(bmsg)
        try:
            map_iface.SetFolder(folder)
        except dbus.DBusException:
            pass
        transfer_path, _props = map_iface.PushMessage(
            path,
            folder,
            dbus.Dictionary({"Transparent": dbus.Boolean(False)},
                             signature="sv")
        )
        result = _wait_for_transfer(str(transfer_path), timeout=timeout)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
        try:
            _client().RemoveSession(session_path)
        except dbus.DBusException:
            pass

    return {
        "mac": mac.upper(),
        "to": number,
        "status": result.get("Status", "unknown"),
    }
