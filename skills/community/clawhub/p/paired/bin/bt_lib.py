"""
bt_lib.py — Shared core for the OpenClaw `bluetooth` skill on .86.

Talks to BlueZ over D-Bus. Designed to scale: every public function takes an
explicit `adapter` arg so adding a second BT dongle is purely additive.
"""
from __future__ import annotations

import sys
import time
from typing import Iterable, Optional

try:
    import dbus
    import dbus.mainloop.glib
    from gi.repository import GLib
except ImportError as e:
    sys.stderr.write(f"bt_lib: missing system package: {e}\n")
    sys.stderr.write("Run: sudo apt install -y python3-dbus python3-gi\n")
    sys.exit(2)

BLUEZ_SERVICE = "org.bluez"
ADAPTER_IFACE = "org.bluez.Adapter1"
DEVICE_IFACE = "org.bluez.Device1"
GATT_SERVICE_IFACE = "org.bluez.GattService1"
GATT_CHAR_IFACE = "org.bluez.GattCharacteristic1"
GATT_DESC_IFACE = "org.bluez.GattDescriptor1"
AGENT_MANAGER_IFACE = "org.bluez.AgentManager1"
AGENT_IFACE = "org.bluez.Agent1"
PROPS_IFACE = "org.freedesktop.DBus.Properties"
OM_IFACE = "org.freedesktop.DBus.ObjectManager"

MANUFACTURERS = {
    6: "Microsoft", 13: "Texas Instruments", 15: "Broadcom", 76: "Apple",
    89: "Nordic Semiconductor", 117: "Samsung", 196: "LG Electronics",
    224: "Google", 301: "Logitech", 343: "Xiaomi", 637: "Polar Electro",
    647: "Withings", 742: "Fitbit", 1281: "Nordic Semiconductor",
    13825: "Bose", 11033: "Generic Beacon", 59761: "Sony", 65535: "Reserved",
}
REF_POWER_DBM = -55.0
ATTENUATION = 3.0


def manuf_name(mid):
    if mid is None:
        return None
    return MANUFACTURERS.get(mid, f"ID {mid}")


def addr_type(mac: str) -> str:
    try:
        first = int(mac.split(":")[0], 16)
    except (ValueError, IndexError):
        return "?"
    bits = first & 0xC0
    return {0x00: "PUB", 0x40: "RND-RESOLVABLE",
            0x80: "RND-NON-RESOLVABLE", 0xC0: "RND-STATIC"}.get(bits, "?")


def estimate_distance(rssi):
    if rssi is None or rssi == -127:
        return None
    try:
        return round(10 ** ((REF_POWER_DBM - rssi) / (10.0 * ATTENUATION)), 2)
    except (ValueError, OverflowError):
        return None


def _device_path_to_mac(path: str) -> Optional[str]:
    leaf = path.rsplit("/", 1)[-1]
    if not leaf.startswith("dev_"):
        return None
    return leaf[4:].replace("_", ":")


def _mac_to_device_path(adapter_path_str: str, mac: str) -> str:
    return f"{adapter_path_str}/dev_{mac.upper().replace(':', '_')}"


def get_bus():
    if not getattr(get_bus, "_set_default", False):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        get_bus._set_default = True
    return dbus.SystemBus()


def list_adapters() -> list[dict]:
    bus = get_bus()
    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/"), OM_IFACE)
    out = []
    for path, ifaces in om.GetManagedObjects().items():
        if ADAPTER_IFACE not in ifaces:
            continue
        p = ifaces[ADAPTER_IFACE]
        out.append({
            "name": path.rsplit("/", 1)[-1],
            "path": str(path),
            "address": str(p.get("Address", "")),
            "alias": str(p.get("Alias", "")),
            "powered": bool(p.get("Powered", False)),
            "discoverable": bool(p.get("Discoverable", False)),
            "discovering": bool(p.get("Discovering", False)),
            "pairable": bool(p.get("Pairable", False)),
            "uuids": [str(u) for u in (p.get("UUIDs") or [])],
        })
    return out


def adapter_path(adapter: str = "hci0") -> Optional[str]:
    for a in list_adapters():
        if a["name"] == adapter:
            return a["path"]
    return None


class AdapterDownError(RuntimeError):
    pass


def adapter_health(adapter: str = "hci0") -> dict:
    info = {"adapter": adapter, "ok": False, "reason": None}
    found = next((a for a in list_adapters() if a["name"] == adapter), None)
    if not found:
        info["reason"] = f"adapter {adapter} not present in BlueZ"
        return info
    info.update(found)
    if found["address"] == "00:00:00:00:00:00":
        info["reason"] = "BD address all-zero — adapter firmware not loaded; USB reset needed"
        return info
    if not found["powered"]:
        info["reason"] = "adapter is powered down — bring up with `hciconfig hci0 up`"
        return info
    info["ok"] = True
    return info


def ensure_adapter_powered(adapter: str = "hci0") -> None:
    apath = adapter_path(adapter)
    if apath is None:
        raise AdapterDownError(f"adapter {adapter!r} not present")
    bus = get_bus()
    aobj = bus.get_object(BLUEZ_SERVICE, apath)
    props = dbus.Interface(aobj, PROPS_IFACE)
    addr = str(props.Get(ADAPTER_IFACE, "Address"))
    if addr == "00:00:00:00:00:00":
        raise AdapterDownError(
            f"adapter {adapter!r} has BD 00:00:00:00:00:00 — needs USB reset (run `bt-recover`)"
        )
    if not bool(props.Get(ADAPTER_IFACE, "Powered")):
        props.Set(ADAPTER_IFACE, "Powered", dbus.Boolean(True))


def _props_to_partial(props: dict) -> dict:
    out: dict = {}
    if "Address" in props:
        out["mac"] = str(props["Address"]).upper()
    if "Name" in props or "Alias" in props:
        n = props.get("Name") or props.get("Alias") or ""
        out["name_raw"] = str(n)
    if "RSSI" in props:
        try:
            out["rssi"] = int(props["RSSI"])
        except (TypeError, ValueError):
            out["rssi"] = None
    if "ManufacturerData" in props:
        md = props["ManufacturerData"] or {}
        try:
            out["manuf_id"] = int(next(iter(md.keys())))
        except (StopIteration, ValueError, TypeError):
            out["manuf_id"] = None
    if "UUIDs" in props:
        out["service_uuids"] = [str(u) for u in (props["UUIDs"] or [])]
    if "TxPower" in props:
        try:
            out["tx_power"] = int(props["TxPower"])
        except (TypeError, ValueError):
            out["tx_power"] = None
    if "Paired" in props:
        out["paired"] = bool(props["Paired"])
    if "Trusted" in props:
        out["trusted"] = bool(props["Trusted"])
    if "Connected" in props:
        out["connected"] = bool(props["Connected"])
    if "Class" in props:
        try:
            out["class"] = int(props["Class"])
        except (TypeError, ValueError):
            pass
    if "Icon" in props:
        out["icon"] = str(props["Icon"])
    return out


def _finalise(mac: str, partial: dict) -> dict:
    name = partial.get("name_raw", "") or ""
    if name.replace("-", ":").upper() == mac:
        name = ""
    rssi = partial.get("rssi")
    manuf_id = partial.get("manuf_id")
    return {
        "mac": mac, "name": name, "rssi": rssi,
        "manuf_id": manuf_id, "manuf_name": manuf_name(manuf_id),
        "addr_type": addr_type(mac),
        "distance_m": estimate_distance(rssi),
        "service_uuids": partial.get("service_uuids", []),
        "tx_power": partial.get("tx_power"),
        "paired": partial.get("paired", False),
        "trusted": partial.get("trusted", False),
        "connected": partial.get("connected", False),
        "icon": partial.get("icon"),
        "last_seen_unix": partial.get("last_seen_unix", time.time()),
    }


def scan(duration: float = 10.0, adapter: str = "hci0", transport: str = "le") -> list[dict]:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise AdapterDownError(f"BlueZ adapter {adapter!r} not found")
    ensure_adapter_powered(adapter)

    aobj = bus.get_object(BLUEZ_SERVICE, apath)
    aiface = dbus.Interface(aobj, ADAPTER_IFACE)
    try:
        aiface.SetDiscoveryFilter({"Transport": transport, "DuplicateData": False})
    except dbus.DBusException:
        pass

    accum: dict[str, dict] = {}

    def _ingest(mac: str, partial: dict) -> None:
        if not mac:
            return
        cur = accum.setdefault(mac, {"mac": mac, "last_seen_unix": time.time()})
        cur.update(partial)
        cur["last_seen_unix"] = time.time()

    def _on_iface_added(path, ifaces):
        if DEVICE_IFACE not in ifaces:
            return
        partial = _props_to_partial(ifaces[DEVICE_IFACE])
        mac = partial.get("mac") or _device_path_to_mac(path)
        if mac:
            _ingest(mac, partial)

    def _on_props_changed(iface, changed, invalidated, path=None):
        if iface != DEVICE_IFACE:
            return
        partial = _props_to_partial(changed)
        mac = partial.get("mac") or _device_path_to_mac(path or "")
        if mac:
            _ingest(mac, partial)

    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/"), OM_IFACE)
    sig1 = om.connect_to_signal("InterfacesAdded", _on_iface_added)
    sig2 = bus.add_signal_receiver(_on_props_changed,
                                    signal_name="PropertiesChanged",
                                    dbus_interface=PROPS_IFACE,
                                    path_keyword="path")

    for path, ifaces in om.GetManagedObjects().items():
        if not path.startswith(apath + "/") or DEVICE_IFACE not in ifaces:
            continue
        partial = _props_to_partial(ifaces[DEVICE_IFACE])
        mac = partial.get("mac") or _device_path_to_mac(path)
        if mac:
            _ingest(mac, partial)

    aiface.StartDiscovery()
    try:
        loop = GLib.MainLoop()
        GLib.timeout_add_seconds(int(duration), loop.quit)
        loop.run()
    finally:
        try:
            aiface.StopDiscovery()
        except dbus.DBusException:
            pass
        sig1.remove()
        try:
            sig2.remove()
        except Exception:
            pass

    return [_finalise(mac, p) for mac, p in accum.items()]


def filter_devices(devs: Iterable[dict], *, named_only=False, min_rssi=None,
                   manuf=None, addr_type_filter=None,
                   paired_only=False, connected_only=False) -> list[dict]:
    out = list(devs)
    if named_only:
        out = [d for d in out if d.get("name")]
    if min_rssi is not None:
        out = [d for d in out if (d.get("rssi") or -127) >= min_rssi]
    if manuf:
        ml = manuf.lower()
        out = [d for d in out if (d.get("manuf_name") or "").lower() == ml]
    if addr_type_filter:
        out = [d for d in out if d.get("addr_type") == addr_type_filter]
    if paired_only:
        out = [d for d in out if d.get("paired")]
    if connected_only:
        out = [d for d in out if d.get("connected")]
    out.sort(key=lambda d: -(d.get("rssi") or -127))
    return out


def get_device(mac: str, adapter: str = "hci0") -> dict:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise AdapterDownError(f"adapter {adapter!r} not found")
    dpath = _mac_to_device_path(apath, mac)
    try:
        dobj = bus.get_object(BLUEZ_SERVICE, dpath)
        props = dbus.Interface(dobj, PROPS_IFACE)
        all_props = props.GetAll(DEVICE_IFACE)
    except dbus.DBusException as e:
        raise RuntimeError(
            f"BlueZ does not know device {mac!r} on {adapter!r}. "
            f"Run a scan first or check the address. ({e.get_dbus_name()})"
        ) from e
    return _finalise(mac.upper(), _props_to_partial(all_props))


def device_op(mac: str, op: str, adapter: str = "hci0", timeout: float = 30.0) -> None:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise AdapterDownError(f"adapter {adapter!r} not found")
    dpath = _mac_to_device_path(apath, mac)
    dobj = bus.get_object(BLUEZ_SERVICE, dpath)
    diface = dbus.Interface(dobj, DEVICE_IFACE)
    method = getattr(diface, op)
    try:
        method(timeout=int(timeout * 1000))
    except dbus.DBusException as e:
        raise RuntimeError(
            f"{op} {mac} on {adapter} failed: {e.get_dbus_message()}"
        ) from e


def set_trusted(mac: str, trusted: bool, adapter: str = "hci0") -> None:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise AdapterDownError(f"adapter {adapter!r} not found")
    dpath = _mac_to_device_path(apath, mac)
    dobj = bus.get_object(BLUEZ_SERVICE, dpath)
    props = dbus.Interface(dobj, PROPS_IFACE)
    props.Set(DEVICE_IFACE, "Trusted", dbus.Boolean(trusted))


def remove_device(mac: str, adapter: str = "hci0") -> None:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise AdapterDownError(f"adapter {adapter!r} not found")
    aobj = bus.get_object(BLUEZ_SERVICE, apath)
    aiface = dbus.Interface(aobj, ADAPTER_IFACE)
    dpath = _mac_to_device_path(apath, mac)
    try:
        aiface.RemoveDevice(dpath)
    except dbus.DBusException as e:
        raise RuntimeError(
            f"Remove {mac} on {adapter} failed: {e.get_dbus_message()}"
        ) from e


def list_gatt_tree(mac: str, adapter: str = "hci0") -> dict:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise AdapterDownError(f"adapter {adapter!r} not found")
    dpath = _mac_to_device_path(apath, mac)
    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/"), OM_IFACE)
    objs = om.GetManagedObjects()
    services: dict[str, dict] = {}
    svc_path_to_uuid: dict[str, str] = {}
    for path, ifaces in objs.items():
        if not path.startswith(dpath + "/"):
            continue
        if GATT_SERVICE_IFACE in ifaces:
            uuid = str(ifaces[GATT_SERVICE_IFACE].get("UUID", ""))
            svc_path_to_uuid[path] = uuid
            services[uuid] = {"path": path, "characteristics": {}}
    for path, ifaces in objs.items():
        if not path.startswith(dpath + "/"):
            continue
        if GATT_CHAR_IFACE in ifaces:
            cp = ifaces[GATT_CHAR_IFACE]
            svc_path = str(cp.get("Service", ""))
            svc_uuid = svc_path_to_uuid.get(svc_path)
            if svc_uuid is None:
                continue
            uuid = str(cp.get("UUID", ""))
            services[svc_uuid]["characteristics"][uuid] = {
                "path": path,
                "flags": [str(f) for f in (cp.get("Flags") or [])],
                "descriptors": {},
            }
    for path, ifaces in objs.items():
        if not path.startswith(dpath + "/"):
            continue
        if GATT_DESC_IFACE in ifaces:
            d_props = ifaces[GATT_DESC_IFACE]
            char_path = str(d_props.get("Characteristic", ""))
            uuid = str(d_props.get("UUID", ""))
            for sv in services.values():
                for ch in sv["characteristics"].values():
                    if ch["path"] == char_path:
                        ch["descriptors"][uuid] = {"path": path}
                        break
    return services


def gatt_read(mac: str, char_uuid: str, adapter: str = "hci0") -> bytes:
    tree = list_gatt_tree(mac, adapter)
    char_path = None
    for sv in tree.values():
        if char_uuid in sv["characteristics"]:
            char_path = sv["characteristics"][char_uuid]["path"]
            break
    if char_path is None:
        raise RuntimeError(f"characteristic {char_uuid} not found on {mac}")
    bus = get_bus()
    cobj = bus.get_object(BLUEZ_SERVICE, char_path)
    ciface = dbus.Interface(cobj, GATT_CHAR_IFACE)
    return bytes(ciface.ReadValue({}))


def gatt_write(mac: str, char_uuid: str, payload: bytes,
               adapter: str = "hci0", with_response: bool = True) -> None:
    tree = list_gatt_tree(mac, adapter)
    char_path = None
    for sv in tree.values():
        if char_uuid in sv["characteristics"]:
            char_path = sv["characteristics"][char_uuid]["path"]
            break
    if char_path is None:
        raise RuntimeError(f"characteristic {char_uuid} not found on {mac}")
    bus = get_bus()
    cobj = bus.get_object(BLUEZ_SERVICE, char_path)
    ciface = dbus.Interface(cobj, GATT_CHAR_IFACE)
    opts = {"type": dbus.String("request" if with_response else "command")}
    ciface.WriteValue([dbus.Byte(b) for b in payload], opts)


PROFILE_UUIDS = {
    "0000110a": "A2DP Source", "0000110b": "A2DP Sink",
    "0000110c": "AVRCP Target", "0000110e": "AVRCP Controller",
    "0000111e": "Handsfree", "0000111f": "Handsfree AG",
    "00001108": "Headset", "00001112": "Headset AG",
    "00001105": "OBEX Object Push", "00001106": "OBEX File Transfer",
    "00001130": "Phonebook Access (PBAP) PSE",
    "0000112e": "Phonebook Access (PBAP) PCE",
    "00001132": "Message Access (MAP) MSE",
    "00001134": "Message Access (MAP) MCE",
    "00001124": "HID", "00001200": "PnP",
    "0000180f": "Battery Service", "0000180a": "Device Information",
    "00001800": "Generic Access", "00001801": "Generic Attribute",
    "0000fe9f": "Google", "0000feaa": "Eddystone",
}


def detect_profiles(uuids: list[str]) -> list[str]:
    found = []
    for u in uuids:
        prefix = u.lower()[:8]
        if prefix in PROFILE_UUIDS:
            found.append(PROFILE_UUIDS[prefix])
    return sorted(set(found))
